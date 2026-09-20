#!/usr/bin/env python
"""mdzip_diff.py - semantic diff between two MagicDraw/Cameo .mdzip files.

The problem: mdzip is XML whose xmi:ids churn (every save reorders members,
delta snapshots duplicate subtrees, TeamworkCloud rewrites every element's
server id).  String/XML diffs are noise.  The fix is to diff the MODEL, not
the bytes:

  1. import both files with mdzip_import (ids normalized away);
  2. flatten each to element records: (metaclass, qualified path, features);
  3. match records across versions:
       a. exact qualified-path match,
       b. same metaclass + name with a moved owner (move detection),
       c. same metaclass, same owner, name-changed (rename detection),
       d. remaining unmatched: one-to-one pairing by feature similarity
          (Jaccard over (feature, value) pairs) above a threshold;
  4. diff matched pairs feature-by-feature (human-readable rows);
  5. report added / removed / renamed / moved / changed / unchanged counts
     plus the per-element feature deltas.

xmi:id never participates in matching.  Designed to survive TeamworkCloud
re-saves (server IDs change wholesale) and Cameo delta-snapshot churn.

Usage:
    python mdzip_diff.py old.mdzip new.mdzip [--json] [--threshold 0.6]
"""
import argparse
import difflib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdzip_import import import_mdzip, MdZipImportError  # noqa: E402

# metaclasses whose instances are worth reporting (model content AND the
# profile layer -- "modelers become addicted to adding new stereos");
# everything else is context
REPORTED = {"Package", "Model", "Class", "DataType", "PrimitiveType",
            "Enumeration", "EnumerationLiteral", "Property", "Port",
            "Association", "AssociationClass", "InstanceSpecification",
            "Interface", "Dependency", "Operation", "Connector",
            "Profile", "Stereotype"}

# features that constitute identity/semantics for diffing
NAMEY = {"name", "visibility", "isAbstract", "isLeaf", "aggregation",
         "isDerived", "isReadOnly", "isOrdered", "isUnique", "default"}
FEATURE_SKIP = {"ownedComment", "ownedRule", "nameExpression",
                "appliedStereotype", "taggedValue", "ownedDefinition"}


def _flat(obj, path):
    """Yield (path, value) leaf pairs for gen.uml25 object features."""
    for feat in sorted(obj._props):
        if feat in FEATURE_SKIP:
            continue
        try:
            v = getattr(obj, feat)
        except Exception:
            continue
        if v is None or v == [] or v == ():
            continue
        if isinstance(v, (str, int, bool)):
            yield path + feat, str(v)
        else:
            yield path + feat, f"<{type(v).__name__}>"


def record_of(obj, imp, parent_path):
    """Element record: (metaclass, qualpath, features dict)."""
    name = getattr(obj, "name", None)
    name = name if isinstance(name, str) and name else None
    mc = type(obj).__name__
    if mc not in REPORTED:
        return None
    label = name or f"<{mc}:{getattr(obj, '_xmi_id', '?')[-8:]}>"
    qp = parent_path + "::" + label
    feats = dict(_flat(obj, ""))
    return {"mc": mc, "name": name, "qualpath": qp, "feats": feats}


def flatten_model(imp):
    """Walk constructed objects into records keyed by qualified path.

    The reader builds composition trees through containment features
    (packagedElement, ownedAttribute, ...); we use the parent maps from
    the constructed objects themselves via _vals walk.
    """
    records = []
    parent_of = {}

    # containment walk over constructed objects: use known composite
    # features (from the reader's tables) to traverse
    COMPOSITES = ("ownedMember", "packagedElement", "nestedClassifier",
                  "ownedAttribute", "ownedEnd", "ownedLiteral",
                  "ownedOperation", "ownedParameter", "ownedConnector",
                  "ownedRule", "slot")
    seen = set()

    def walk(obj, path):
        if id(obj) in seen:
            return
        seen.add(id(obj))
        rec = record_of(obj, imp, path)
        if rec is None:
            return
        records.append(rec)
        for feat in COMPOSITES:
            try:
                kids = getattr(obj, feat)
            except Exception:
                continue
            if not kids:
                continue
            for k in kids:
                walk(k, rec["qualpath"])

    for r in imp.xmi.roots:
        walk(r, "")

    # applications travel with their base element (stereotype names)
    return records


def similarity(a, b):
    """Jaccard over (feature, value) pairs."""
    sa = {(k, v) for k, v in a["feats"].items()}
    sb = {(k, v) for k, v in b["feats"].items()}
    if not sa and not sb:
        return 0.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union if union else 0.0


def diff_records(old_recs, new_recs, threshold=0.6):
    """Match + diff; returns the report dict."""
    old_by_path = {r["qualpath"]: r for r in old_recs}
    new_by_path = {r["qualpath"]: r for r in new_recs}

    matched = {}       # old_path -> new_path
    # pass 1: exact qualified path
    for p in old_by_path.keys() & new_by_path.keys():
        matched[p] = p

    # pass 2: same metaclass + name, moved owner (unique on both sides)
    old_free = [p for p in old_by_path if p not in matched.values()]
    new_free = [p for p in new_by_path if p not in matched]
    old_by_name = {}
    for p in old_free:
        old_by_name.setdefault((old_by_path[p]["mc"], old_by_path[p]["name"]),
                               []).append(p)
    new_by_name = {}
    for p in new_free:
        new_by_name.setdefault((new_by_path[p]["mc"], new_by_path[p]["name"]),
                               []).append(p)
    for key in old_by_name.keys() & new_by_name.keys():
        if len(old_by_name[key]) == 1 and len(new_by_name[key]) == 1:
            matched[old_by_name[key][0]] = new_by_name[key][0]

    # pass 3: same metaclass + same owner tail + similarity >= threshold
    def owner_tail(p):
        return p.rsplit("::", 2)[0] if "::" in p else ""

    old_free = [p for p in old_by_path if p not in matched.values()]
    new_free = [p for p in new_by_path if p not in matched]
    pairs = []
    for op in old_free:
        for np_ in new_free:
            if old_by_path[op]["mc"] != new_by_path[np_]["mc"]:
                continue
            if owner_tail(op) != owner_tail(np_):
                continue
            sim = similarity(old_by_path[op], new_by_path[np_])
            if sim >= threshold:
                pairs.append((sim, op, np_))
    pairs.sort(reverse=True)
    used_o, used_n = set(), set()
    for sim, op, np_ in pairs:
        if op in used_o or np_ in used_n:
            continue
        used_o.add(op)
        used_n.add(np_)
        matched[op] = np_

    # pass 3b: same metaclass + same NAME + high similarity regardless of
    # owner (regeneration moves whole packages: the owner chain changes
    # wholesale while the element itself is semantically identical --
    # openEHR AM->AM14 regeneration pattern)
    old_free = [p for p in old_by_path if p not in matched.values()]
    new_free = [p for p in new_by_path if p not in matched]
    pairs = []
    for op in old_free:
        a = old_by_path[op]
        for np_ in new_free:
            b = new_by_path[np_]
            if a["mc"] != b["mc"] or a["name"] is None or a["name"] != b["name"]:
                continue
            sim = similarity(a, b)
            if sim >= threshold:
                pairs.append((sim, op, np_))
    pairs.sort(reverse=True)
    used_o, used_n = set(), set()
    for sim, op, np_ in pairs:
        if op in used_o or np_ in used_n:
            continue
        used_o.add(op)
        used_n.add(np_)
        matched[op] = np_

    added = sorted(set(new_by_path) - set(matched.values()))
    removed = sorted(set(old_by_path) - set(matched.keys()))
    added_recs = [new_by_path[p] for p in added]
    removed_recs = [old_by_path[p] for p in removed]
    for r in added_recs:
        r["kind"] = "added"
    for r in removed_recs:
        r["kind"] = "removed"

    changed = []
    for op, np_ in sorted(matched.items()):
        a, b = old_by_path[op], new_by_path[np_]
        feats_changed = {k: (a["feats"].get(k), b["feats"].get(k))
                         for k in set(a["feats"]) | set(b["feats"])
                         if a["feats"].get(k) != b["feats"].get(k)}
        kind = "changed" if feats_changed else "unchanged"
        entry = {"old": op, "new": np_, "metaclass": a["mc"], "kind": kind}
        if feats_changed:
            entry["feature_changes"] = feats_changed
        if op != np_:
            entry["moved_or_renamed"] = True
        changed.append(entry)

    return {
        "counts": {
            "old": len(old_recs), "new": len(new_recs),
            "matched": len(matched), "added": len(added),
            "removed": len(removed),
            "changed": sum(1 for c in changed if c["kind"] == "changed"),
            "moved_or_renamed": sum(1 for c in changed
                                    if c.get("moved_or_renamed")),
        },
        "added": added_recs,
        "removed": removed_recs,
        "pairs": changed,
    }


def import_records(path):
    imp = import_mdzip(path)
    return flatten_model(imp), imp


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--threshold", type=float, default=0.6)
    a = ap.parse_args(argv)
    old_recs, old_imp = import_records(a.old)
    new_recs, new_imp = import_records(a.new)
    rep = diff_records(old_recs, new_recs, a.threshold)
    if a.json:
        print(json.dumps(rep, indent=2))
        return 0
    c = rep["counts"]
    print(f"old {c['old']} elements | new {c['new']} | matched {c['matched']} "
          f"| added {c['added']} | removed {c['removed']} | "
          f"changed {c['changed']} | moved/renamed {c['moved_or_renamed']}")
    for p in rep["pairs"]:
        if p["kind"] == "changed" or p.get("moved_or_renamed"):
            tag = "M" if p.get("moved_or_renamed") else "C"
            print(f"[{tag}] {p['metaclass']:22s} {p['old']}")
            if p.get("moved_or_renamed"):
                print(f"     -> {p['new']}")
            for k, (va, vb) in sorted(p.get("feature_changes", {}).items()):
                print(f"     {k}: {va!r} -> {vb!r}")
    for r in rep["added"][:20]:
        print(f"[+] {r['mc']:22s} {r['qualpath']}")
    for r in rep["removed"][:20]:
        print(f"[-] {r['mc']:22s} {r['qualpath']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())