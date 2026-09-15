# Exploration: building UML 2.5.1 into Python classes from the OMG XMI

**Date:** 2026-09-14 · **Status:** spike complete — 45/45 semantic checks pass

## Question

Can the OMG-published XMI serialization of the UML 2.5.1 metamodel be turned
into a *useful* Python class tree, rather than hand-scaffolding the (very
complex) UML v2 metamodel by hand?

**Answer: yes — and the XMI carries far more than the class tree.** The
serialization is machine-regular enough to drive not just the inheritance
hierarchy but the property-semantics layer (derived unions, subsets, composite
ownership, association opposites), enumerations, operation signatures, and the
normative OCL/prose text.

## Inputs (all already on disk)

| File | Role |
|---|---|
| `/mnt/TBFox/surfacebackup_512GB/uml_xmi/UML.xmi` (1.9 MB) | OMG UML 2.5.1 metamodel, XMI 2.5 serialization (URI `…/UML/20161101`) |
| `…/uml_xmi/PrimitiveTypes.xmi` | Boolean/Integer/Real/String/UnlimitedNatural |
| `…/uml_xmi/sysml.xmi` | SysML v1 profile (56 stereotypes) — next target, not yet parsed |
| `…/uml_xmi/StandardProfile.xmi` | Standard profile — same |

## What was generated (`gen/uml25.py`, 7,835 lines, stdlib-only)

| Metric | Count |
|---|---|
| Metaclasses (with correct C3 MROs) | 242 |
| — abstract (guarded: cannot instantiate) | 49 |
| — multiple inheritance | 34 |
| — max inheritance depth / mean | 11 / 5.6 |
| Properties emitted as descriptors | 620 |
| Operation stubs (typed signatures + docs) | 205 |
| Enumerations (Python `Enum`) | 13 |
| Normative OCL constraints carried | 449 |
| Derived-union attributes (computed live) | 22 |
| Derived attributes | 73 |
| Composite (ownership-wired) properties | 213 |
| Subset references in closure graph | 393 (+212 on hidden ends) |
| Redefinition references (metadata) | 40 |
| Association opposite pairs wired | 180 |
| Associations parsed (memberEnd pairs) | 418 |
| Association-owned hidden ends folded into graph | 328 |
| Generated lines | 7,835 |

Structural shape: 14 subpackages (Actions 62, Activities 24, CommonStructure
23, Interactions 22, Values 22 …); `Element` has 15 direct subclasses; a
`Class` instance sees **13 derived unions**, e.g. `ownedElement` fed by 21
distinct subsetting properties, `member` by 12.

## How it works

- `generate.py` (one file, lxml) parses packages → classes → attributes →
  operations → associations, then emits one module.
- Every property becomes a `_Ref` descriptor carrying its metamodel flags
  (`derived`, `union`, `composite`, `readonly`, `subsets`, `redefines`,
  `assoc`). Multi-valued properties are `_RefList`s; every mutation fires
  wiring hooks.
- **Derived unions** are computed at read time: the generator closes the
  subset lattice (including through association-owned hidden ends) and emits
  per-class contributor tables; `_union()` walks the MRO and dedups by
  identity. Adding a `Property` to `Class.ownedAttribute` makes it appear in
  `ownedElement`, `ownedMember`, `member`, `feature`, `attribute`.
- **Composite ownership** sets `owner`/`namespace` on containment (both are
  derived in the spec, computed here as the inverse of composite wiring).
- **Association opposites** (from `memberEnd` pairs) wire both directions:
  `class.ownedOperation.add(op)` sets `op.class_`, and `op.class_ = cls`
  appends into `ownedOperation` and sets ownership.
- **Abstract guards**: 49 abstract metaclasses raise `TypeError` on direct
  instantiation; writing derived/read-only properties raises
  `AttributeError`.
- **Normative text** is carried: class/property/operation docstrings come
  from the spec's `ownedComment` bodies; `CONSTRAINTS` tuples carry 449 OCL
  constraint texts verbatim.
- Keywords renamed per Python rules (`class` → `class_`,
  `VisibilityKind.public` fine, `ParameterDirectionKind.return_`).

## What is *not* built (honest gaps)

1. **OCL evaluation** — 449 constraints are metadata, not checked. (Prior
   art exists in-house: the FACE CTS OCL-extraction discipline.)
2. **Operation bodies** — 205 stubs raise `NotImplementedError`; signatures
   and spec text are introspectable.
3. **Profiles/stereotypes** — `StandardProfile.xmi` and `sysml.xmi` not yet
   parsed; the same generator would emit stereotype classes folded onto their
   base metaclasses (`base_*` extension attributes).
4. **XMI instance reader** — metamodel XMI (2.5) and model XMI (2.1
   EMF-style, e.g. `DoDAFLibrary.xmi`) are different dialects; no reader yet.
5. Simplifications: redefinitions are metadata-only (same-name shadowing
   gives shared storage); `namespace` is set on every composite add (not
   only Namespace-typed containers); derived non-union properties store
   rather than compute.

## Reproduce

```bash
~/ams-gra-sim/.venv/bin/python generate.py   # lxml needed only here
python check.py                              # generated pkg is stdlib-only
```

## Where this goes next (tiers from the discussion)

- **B: property semantics are done** — the remaining B items are the XMI 2.1
  instance reader + profile application (`DoDAFLibrary.xmi` as first corpus).
- **C: SysML v1 profile parse** (56 stereotypes → Python classes) and then
  v1→v2 mapping into sysmlpy — both build directly on this machinery.
- Fun synergy: the generated hierarchy can render itself (inheritance tree /
  union lattice) via the plantuml.py/graphviz tooling.