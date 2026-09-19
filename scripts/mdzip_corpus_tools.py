#!/usr/bin/env python
"""Reproducible mdzip corpus tooling: scour GitHub, bulk-fetch, sweep.

Subcommands (all take --corpus DIR, default /mnt/TBFox/mdzip_corpus):

    scour   GitHub code search for 'mdzip' -> repo tree walk -> candidates JSON
    fetch   download every candidate file (LFS-aware URL resolution, dedup)
    sweep   run mdzip.py forensics over the corpus -> _sweep.json + image manifests

The corpus itself is third-party sample data and is NOT committed; this
script documents provenance and makes the whole pipeline reproducible.
"""
import argparse, json, os, re, subprocess, sys, time
from collections import Counter
from pathlib import Path


def gh(*a):
    r = subprocess.run(['gh', 'api'] + list(a), capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def cmd_scour(args):
    repos = set()
    for page in (1, 2, 3):
        data = gh('-X', 'GET', 'search/code', '-f', 'q=mdzip',
                  '-f', 'per_page=100', '-f', f'page={page}')
        data = json.loads(data) if data else None
        if not data or 'items' not in data:
            break
        repos.update(it['repository']['full_name'] for it in data['items'])
        if len(data['items']) < 100:
            break
        time.sleep(7)
    found = {}
    for i, repo in enumerate(sorted(repos)):
        t = gh(f'repos/{repo}/git/trees/HEAD?recursive=1')
        t = json.loads(t) if t else None
        if not t or 'tree' not in t:
            continue
        for e in t['tree']:
            p = e.get('path', '')
            if p.lower().endswith('.mdzip') and e.get('type') == 'blob':
                found.setdefault(repo, []).append({'path': p, 'size': e.get('size', 0)})
        time.sleep(0.4)
    out = Path(args.corpus) / '_candidates.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(found, open(out, 'w'), indent=1)
    print(f'{len(found)} repos, {sum(len(v) for v in found.values())} files -> {out}')


def cmd_fetch(args):
    cands = json.load(open(Path(args.corpus) / '_candidates.json'))
    dest = Path(args.corpus)
    dest.mkdir(parents=True, exist_ok=True)
    done, failed = 0, []
    for i, (repo, files) in enumerate(sorted(cands.items())):
        slug = repo.replace('/', '__')
        (dest / slug).mkdir(exist_ok=True)
        for f in files:
            dst = dest / slug / os.path.basename(f['path'])
            if dst.is_file() and dst.stat().st_size > 0:
                done += 1
                continue
            if f.get('size', 0) > 80_000_000:
                continue
            url = gh('-X', 'GET', f"repos/{repo}/contents/{f['path']}",
                     '--jq', '.download_url')
            if not url:
                failed.append((repo, f['path']))
                continue
            r = subprocess.run(['curl', '-fsSL', '-o', str(dst), url],
                               capture_output=True, timeout=600)
            if r.returncode == 0 and dst.stat().st_size > 0:
                done += 1
            else:
                failed.append((repo, f['path']))
            time.sleep(0.15)
        print(f'[{i+1}/{len(cands)}] {repo}: done={done} failed={len(failed)}', flush=True)
    n = sum(1 for p in dest.rglob('*.mdzip'))
    print(f'FINAL: {n} files on disk, failed={len(failed)}')


def cmd_sweep(args):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from mdzip import MdZip, HEX_RUN, sniff_bytes
    corpus = Path(args.corpus)
    rows, errors = [], []
    files = sorted(corpus.rglob('*.mdzip'))
    for i, p in enumerate(files):
        rel = str(p.relative_to(corpus))
        try:
            with MdZip(p) as m:
                inv = m.inventory()
                eras, det = m.version_clues()
                desc, _ = m.project_description()
                hex_hits = 0
                for mem in m.members:
                    if mem.file_size < 1000:
                        continue
                    txt = m.zf.read(mem.filename).decode('utf-8', 'replace')
                    for mt in HEX_RUN.finditer(txt):
                        b = mt.group(0)
                        raw = bytes.fromhex(b[:-1] if len(b) % 2 else b)
                        if sniff_bytes(raw):
                            hex_hits += 1
                rows.append({'file': rel, 'size': p.stat().st_size,
                             'inventory': inv, 'eras': eras[:8],
                             'usages': m.usages(), 'description': desc,
                             'hex_image_blobs': hex_hits})
        except Exception as e:
            errors.append({'file': rel, 'error': f'{type(e).__name__}: {e}'})
        if i % 25 == 0:
            print(f'  [{i}/{len(files)}]', flush=True)
    ec = Counter(e for r in rows for e in r['eras'])
    uc = Counter(len(r['usages']) for r in rows)
    summary = {'files': len(rows), 'errors': len(errors),
               'era_histogram': dict(ec.most_common()),
               'usage_counts': {str(k): v for k, v in sorted(uc.items())},
               'with_hex_images': sum(1 for r in rows if r['hex_image_blobs'])}
    json.dump({'summary': summary, 'rows': rows, 'errors': errors},
              open(corpus / '_sweep.json', 'w'), indent=1)
    print(json.dumps(summary, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--corpus', default='/mnt/TBFox/mdzip_corpus')
    ap.add_argument('command', choices=['scour', 'fetch', 'sweep'])
    a = ap.parse_args()
    {'scour': cmd_scour, 'fetch': cmd_fetch, 'sweep': cmd_sweep}[a.command](a)


if __name__ == '__main__':
    main()