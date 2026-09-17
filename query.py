#!/usr/bin/env python
"""Query helpers over gen.uml25 instance graphs (stdlib only).

- walk(root): deterministic DFS over composite containment (derived
  unions via derived.union, cycle-guarded); yields the root first.
- find(root, ...): filtered search; predicates are AND-combined.
  `metaclass` accepts a generated class or metaclass name string
  (isinstance, so abstract metaclasses and subclasses match);
  `stereotype` accepts a full label ("Profile::Pkg::Name"), a bare
  stereotype name (matched on the label's last segment), or a
  (profile, name) pair; `qualified` compares derived.qualified_name;
  `deep=False` restricts to direct children of root.
- of_type(root, cls): find restricted to a metaclass.
- stereotypes(el): resolved labels for the element's stereotype
  applications (the reader records base._applied_stereotypes as
  (profile, stereo, app_id) triples; labels resolve through the
  generated profile modules' _STEREO strings, case-insensitively on
  the profile segment, with "{profile}::{stereo}" as fallback).
- exists(root, ...), count(root, ...).
"""
from __future__ import annotations

import gen.uml25 as uml
import derived as D


def _cls(spec):
    if isinstance(spec, type):
        return spec
    cls = uml.metaclass(spec)
    if cls is None:
        raise ValueError(f"unknown metaclass {spec!r}")
    return cls


def walk(root):
    """DFS over composite containment: root first, then each owned
    subtree in declaration order; cycle-guarded."""
    out, seen = [], set()

    def visit(el):
        if id(el) in seen:
            return
        seen.add(id(el))
        out.append(el)
        for c in D.union(el, "ownedElement"):
            visit(c)

    visit(root)
    return out


def find(root, metaclass=None, stereotype=None, name=None,
         qualified=None, pred=None, deep=True):
    """Elements under root matching all given predicates."""
    cls = _cls(metaclass) if metaclass is not None else None
    out = []
    for el in walk(root):
        if not deep and (el is root or D.owner(el) is not root):
            continue
        if cls is not None and not isinstance(el, cls):
            continue
        if name is not None and getattr(el, "name", None) != name:
            continue
        if qualified is not None and D.qualified_name(el) != qualified:
            continue
        if pred is not None and not pred(el):
            continue
        if stereotype is not None and not _stereo_match(el, stereotype):
            continue
        out.append(el)
    return out


def of_type(root, cls):
    """Shorthand for find(root, metaclass=cls)."""
    return find(root, metaclass=cls)


def exists(root, **kw):
    """True if any element under root matches the predicates."""
    return bool(find(root, **kw))


def count(root, **kw):
    """Number of elements under root matching the predicates."""
    return len(find(root, **kw))


# ---------------------------------------------------------------------------
# stereotype resolution
# ---------------------------------------------------------------------------

def _stereo_registry(modules=None):
    """(profile, localname) -> full _STEREO label, from the generated
    profile modules (gen.uaf / gen.sysml / gen.standard_profile unless
    overridden)."""
    reg = {}
    if modules is None:
        modules = []
        import importlib
        for name in ("gen.uaf", "gen.sysml", "gen.standard_profile"):
            try:
                modules.append(importlib.import_module(name))
            except ImportError:
                pass
    for mod in modules:
        for name, obj in vars(mod).items():
            if (isinstance(obj, type)
                    and getattr(obj, "_STEREO", None)
                    and obj.__module__ == mod.__name__):
                parts = obj._STEREO.split("::")
                if len(parts) >= 2:
                    reg[(parts[0].lower(), parts[-1])] = obj._STEREO
    return reg


def resolve_stereotype(app, registry=None):
    """Full label for one (profile, stereo, app_id) application triple."""
    profile, stereo = app[0], app[1]
    reg = _cached_registry() if registry is None else registry
    full = reg.get((profile.lower(), stereo))
    return full if full is not None else f"{profile}::{stereo}"


_STEREO_REGISTRY = None


def _cached_registry():
    global _STEREO_REGISTRY
    if _STEREO_REGISTRY is None:
        _STEREO_REGISTRY = _stereo_registry()
    return _STEREO_REGISTRY


def stereotypes(el, registry=None):
    """Resolved labels ("Profile::Pkg::Name") of el's applied
    stereotypes."""
    apps = getattr(el, "_applied_stereotypes", None) or ()
    return [resolve_stereotype(a, registry) for a in apps]


def _stereo_match(el, spec):
    labels = stereotypes(el)
    if isinstance(spec, tuple):
        profile, name = spec
        return any(lbl.split("::")[0].lower() == profile.lower()
                   and lbl.split("::")[-1] == name for lbl in labels)
    if "::" in spec:
        return spec in labels
    return any(lbl.split("::")[-1] == spec for lbl in labels)