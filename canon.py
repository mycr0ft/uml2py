#!/usr/bin/env python
"""Canonical structural comparison for XML/XMI documents.

Used by the exporter check suites (E1, E2, E5, E6): parse two files into a
canonical form and report divergences. Normalizations (the "dialect table"):

  - namespace PREFIXES are dropped; namespace URIs matter (elements are
    keyed by (ns-uri, localname), except containment children, which are
    unprefixed in this dialect and keyed by localname);
  - xmi:id and xmi:uuid are ignored (identity noise; the writer reuses
    reader ids, but cross-produce comparisons must not depend on them);
  - xmi:type is normalized to its local metaclass name (prefix dropped);
  - attributes are compared as a sorted set; attribute ORDER is ignored;
  - text is stripped; comments/PIs ignored;
  - an element's children are GROUPED BY FEATURE: child order is compared
    within a single feature (containment lists, memberEnd sequences are
    semantically ordered) but the relative order of DIFFERENT features is
    ignored (serialization order varies by producer and .genmodel format);
  - root-level children are treated as an unordered multiset (application
    elements may be emitted before or after the model by different tools);
  - reference children (xmi:idref) are resolved to the target's canonical
    containment path, so id-renaming is invisible;
  - drop_names_at: an optional set of xmi:ids whose <name> children are
    ignored in BOTH documents (readers may derive names for unnamed
    elements; a re-written file carries them explicitly).

Standard library only.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET

XMI = "http://schema.omg.org/spec/XMI/2.1"


def _split(tag):
    if tag.startswith("{"):
        uri, local = tag[1:].rsplit("}", 1)
        return uri, local
    return "", tag


def _local(tag):
    return _split(tag)[1]


def canonize(path, drop_names_at=frozenset()):
    """Canonical form of an XML document as a nested hashable structure."""
    root = ET.parse(str(path)).getroot()

    # ---- containment paths for idref resolution ---------------------------
    parent = {c: p for p in root.iter() for c in p}
    idmap = {}
    for e in root.iter():
        i = e.get(f"{{{XMI}}}id")
        if i is not None:
            idmap[i] = e

    def path_of(e):
        """Canonical containment path '/feature[i]/...' from a root child."""
        chain = []
        e2 = e
        while e2 is not None and e2 is not root:
            par = parent.get(e2)
            sibs = [c for c in par if _local(c.tag) == _local(e2.tag)]
            chain.append(f"{_local(e2.tag)}[{sibs.index(e2)}]")
            e2 = par
        return "/" + "/".join(reversed(chain))

    paths = {e: path_of(e) for e in idmap.values()}

    def node(e):
        attrs = {}
        for k, v in e.attrib.items():
            uri, local = _split(k)
            if uri == XMI and local in ("id", "uuid"):
                continue
            if uri == XMI and local == "type":
                v = v.split(":")[-1]
            attrs[(uri, local)] = v
        text = (e.text or "").strip() or None

        kids = []
        for c in e:
            f = _local(c.tag)
            if f == "name" and drop_names_at is not None:
                pid = e.get(f"{{{XMI}}}id")
                if pid is not None and pid in drop_names_at:
                    continue
            ref = c.get(f"{{{XMI}}}idref")
            href = c.get("href")
            if ref is not None:
                tgt = idmap.get(ref)
                key = paths.get(tgt, f"@unresolved:{ref}")
                kids.append((f, ("@ref", f, key)))
            elif href is not None:
                kids.append((f, ("@href", f, href)))
            else:
                kids.append((f, node(c)))

        grouped = {}
        for f, k in kids:
            grouped.setdefault(f, []).append(k)
        children = tuple((f, tuple(v)) for f, v in sorted(grouped.items()))
        return (( _split(e.tag)[0], _split(e.tag)[1]),
                tuple(sorted(attrs.items())), text, children)

    top = [(c.tag, node(c)) for c in root]
    top.sort(key=lambda t: repr(t[1]))
    return repr(((_split(root.tag)[0], _split(root.tag)[1]), tuple(top)))


def compare(a_path, b_path, drop_names_at=None):
    """Canonical-compare two XML documents; return a list of divergences."""
    ca = canonize(a_path, drop_names_at)
    cb = canonize(b_path, drop_names_at)
    if ca == cb:
        return []
    # locate the first divergence for a useful message
    n = min(len(ca), len(cb))
    i = 0
    while i < n and ca[i] == cb[i]:
        i += 1
    return [f"canonical forms diverge at char {i}: "
            f"...{ca[max(0, i - 60):i]}|{ca[i:i + 80]} vs "
            f"...{cb[max(0, i - 60):i]}|{cb[i:i + 80]}"]