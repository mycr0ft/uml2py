# Exploration: building UML 2.5.1 + SysML v1 profiles into Python from the OMG XMI

**Date:** 2026-09-14 · **Status:** spike + profiles + v1→v2 emitter complete —
45/45 UML, 21/21 profile, 6/6 v1→v2 checks pass

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

# Part 2: profiles (StandardProfile + SysML v1)

`generate_profiles.py` emits **one module per profile** (separate namespaces —
SysML's `Trace`/`Refine`/`Copy` must not shadow StandardProfile's):

| Module | Contents |
|---|---|
| `gen/standard_profile.py` | 33 stereotypes (`Derive(Abstraction)`, `Document(File)`, `Metaclass(Class)`…) |
| `gen/sysml.py` | **56 SysML v1 stereotypes**, 4 profile enums (ControlValueKind, FeatureDirectionKind, FlowDirectionKind, VerdictKind), 143 profile constraints as metadata |

Key design: **stereotype = fold-in**. `Block(U.Class)` — applying the
stereotype is Python instantiation; tagged values are `_Ref` descriptors
(reusing the uml25 wiring machinery); `base_*` extension ends are consumed
into the inheritance structure; required/optional extension data is carried
in `_EXTENSIONS`; `AbstractRequirement(U.NamedElement)` gives every
`Requirement` its `text`/`id` tagged values. Base-metaclass combinations that
are C3-incompatible as Python inheritance (ControlOperator, TestCase:
`Behavior`×`Operation`) fall back to the most-specific compatible subset,
with the full set kept in `_BASE_METACLASSES` metadata.

Serialization quirks handled (the two files differ):
- `sysml.xmi` uses **https** namespaces and omits `xmi:type` on the Profile.
- Generalization targets: attribute `general=` (StandardProfile) vs child
  `<general xmi:idref="SysML.X">` (SysML, with `SysML.`-prefixed ids).
- Constraint OCL: child `<body>` (StandardProfile) vs **`body` XML
  attribute** (SysML); some constraints literally carry
  `-- Cannot be expressed in OCL`.
- Typed enums: `<type href>` vs type implied by `defaultValue` InstanceValue
  (`SysML_dataType.FlowDirectionKind.inout`).

`check_profiles.py`: 21/21 (folding, inheritance, tagged values, enum
typing, abstract guards, constraint metadata, no cross-profile shadowing).

# Part 3: SysML v1 → v2 (first working emitter)

**Wave 2 covers 25+ additional initializer mappings.** The emitted v2 for a
model exercising all of them parses cleanly with sysmlpy:

```
{'package': 1, 'part': 5, 'attribute': 1, 'enumeration': 1, 'port': 1,
 'item': 1, 'state': 1, 'action': 1, 'use_case': 2, 'requirement': 2,
 'connection': 2, 'verification': 1, 'metadata': 1, 'dependency': 3,
 'allocation': 1}
```

New mappings (all anchored to normative statements + the doc's own
expected-textual-syntax examples):

| SysML v1 | → SysML v2 emitted |
|---|---|
| Association / AssociationBlock | `connection def` with member ends |
| Connector | `connection c connect p1 to p2;` |
| BindingConnector | `binding b bind p1 = p2;` |
| InterfaceBlock | `port def` |
| Port typed/untyped | `port p : IB;` / `port p;` |
| Actor | `part def` |
| Signal / InformationItem | `item def` (+ item-typed properties) |
| plain Class | `occurrence def` |
| Property typed by plain Class | `occurrence` / `ref occurrence` |
| Activity / OpaqueBehavior | `action def` with in/out parameters |
| Operation | `perform action` with parameters (return → out, per doc example) |
| StateMachine / Region / State / Pseudostate / FinalState | `state def { state …; transition … }` |
| Transition | `transition t first s1 then s2;` |
| InitialState | elided with comment (normative, SYSML2_-203) |
| TestCase | `verification def` + `return verdict : VerificationCases::VerdictKind` |
| Verify | `objective obj_X { verify Req; }` inside its TestCase |
| DeriveReqt | `connection : DerivationConnections::Derivation connect …` |
| Refine / Trace | `dependency from … to … { @RefineData { isRefine = true; } }` (local metadata stub stands in for SysMLv1Library) |
| Allocate | `allocation def` with `end :>> source/target` + `allocate source.x to target.y;` |
| Dependency / Realization / Abstraction | `dependency [name] from … to …;` |
| UseCase / Include | `use case def` + `include use case : …;` |
| PackageImport / ElementImport | honest elision comment (target grammar reader has no import) |

`calibrate_v2.py` documents which textual forms the authoritative reader
accepts (40+ snippets; e.g. sysmlpy has no `import`, transitions use
`first … then …`, untyped ports count as parts in its summary).

The OMG transition document is on disk
(`2b-SysML_v1_to_v2_Transformation.pdf`, ptc/2025-04-07, Beta 4) with 79
normative `To*_Init` initializer mappings and expected-syntax examples
per mapping; `transition.txt` is the extracted text (kept out of the
repository - reference corpus).
`v1_to_v2.py` implements a clean-room emitter for the core structural core,
each mapping anchored to the normative statement (quoted in the module
docstring):

| SysML v1 | → SysML v2 emitted |
|---|---|
| Block | `part def` |
| Property typed by block (isComposite) | `part` / `ref part` with multiplicity |
| Property untyped | `feature` |
| ValueType | `attribute def` |
| Property typed by DataType | `attribute` |
| Enumeration + literals | `enum def { lits; }` |
| Generalization | `:> Super` |
| Comment / Requirement.text | `doc /* … */` |
| Requirement (+id) | `requirement` (usage; v1 id as comment) |
| Satisfy | `satisfy <n> : <req> by <part>;` |
| ConstraintBlock | `constraint def` |

Anything without a normative implemented mapping raises `UnmappedFeature`
naming the v1 metaclass — the emitter refuses to guess.

**End-to-end validation** (`check_v1_to_v2.py`, run under `~/sysmlpy/.venv`):
a v1 model built with the generated classes (Blocks, parts, ValueType,
Enumeration, Generalization, Requirement with text/id, Satisfy) is emitted as
v2 textual notation and **parsed successfully by sysmlpy** — counts:
`{'part': 3, 'attribute': 1, 'enumeration': 1, 'requirement': 2}` (the
satisfy counts as a requirement usage). Output kept at
`vehicle_example_v2.sysml`.

Remaining for a full transformation: ~30 initializers (mostly
interactions/messages, FullPort/ProxyPort metadata, ItemFlow, Constraint
internals, Slot/instance models).

**Corpus eligibility note:** only OMG-published models are eligible as
instance-reader test corpora (e.g. `DoDAFLibrary.xmi` from the UPDM
example). Third-party book models shipped with commercial texts (e.g.
the Craft-of-MBSE Enterprise Architect / Rational model) are **excluded
on copyright grounds** - not used as inputs, test corpora, or
reference outputs in this work.

# Part 4: XMI 2.1 instance reader (real OMG-published models)

With the metamodel, profiles, and emitter in place, the missing piece
for real models was an instance reader. `xmi21.py` (clean-room, from
the XMI 2.1 spec's published behavior plus the OMG-published example
files themselves as corpus) reads EMF-style XMI 2.1 instance documents
into the generated `gen.uml25` metaclasses, so the whole v1→v2 pipeline
runs on published models unchanged.

## The dialect it handles (distinct from the metamodel XMI)

The UML 2.5.1 metamodel XMI (used by the generator) and EMF instance
XMI (published models) differ in almost every convention:

| Aspect | Metamodel XMI (2.5.1, UML 20160901) | Instance XMI (2.1, UML 20090901) |
|---|---|---|
| xmi:id / xmi:type | XML attributes in XMI namespace | same (plain attributes) |
| scalar features | XML attributes (`name="x"`) | child elements (`<name>x</name>`) |
| references | child elements w/ xmi:idref | same, incl. `href` cross-file |
| namespaces | UML ns on every element | UML ns on the Model root; containment features (packagedElement, ownedAttribute, memberEnd, type, ...) are **unprefixed**; stereotype applications sit top-level in profile namespaces (`updm:Measurement`, `StandardProfileL2:ModelLibrary`) |
| multiplicity | packed into metamodel features | `<lowerValue xmi:type="uml:LiteralUnlimitedNatural"/>` + `<upperValue><value>*</value></upperValue>` literal value-spec elements |
| profile application | `<profileApplication><appliedProfile href/>` | both: appliedProfile href **and** top-level stereotype applications with `base_<Metaclass xmi:idref>` extension ends |

## Semantics settled by evidence (documented in code)

- **Empty `<lowerValue/>` = 0.** EMF serialization omits the `value`
  attribute when it equals the feature default (0 for
  UnlimitedNatural); RSA/EMF writers omit lower/upper elements entirely
  for the `[1..1]` default. Observed split in the corpus: 26 properties
  with empty lower + `*` upper (`[0..*]`), 27 with no literal elements
  (`[1..1]`). A `[1..*]` reading is inconsistent with the corpus
  (those are optional multi-valued properties).
- **Cross-file type hrefs** (`<type href="...UML.xmi#String">`, 52 of
  them in the corpus) resolve to synthetic external markers carrying
  the original href verbatim. They are references to the OMG-published
  PrimitiveTypes, not invented content, and are never emitted as
  definitions - only used as types.
- **Unresolved names** are derived from xmi:id tails and **recorded**
  in `derived_names` (provenance, never silently invented). Bare-integer
  tails (RSA numbering) join with the feature segment:
  `...packagedElement-7` → `packagedElement-7`; the unnamed ownedEnd →
  `ownedEnd`. Non-identifier names are emitted quoted: `<'packagedElement-7'>`, `<'DoDAF Class Library'>`, `<'CTS-B'>`.
- **Stereotype applications are collected, not folded**: 61
  applications in the corpus (53 `updm:Measurement` on properties,
  7 `updm:MeasurementSet` on DataTypes, 1
  `StandardProfileL2:ModelLibrary` on the model). They are attached to
  the base elements as `_applied_stereotypes` and carried into the v2
  output as explicit `/* v1 stereotype applied: ... */` comments, since
  UPDM is not SysML v1 and has no normative v2 mapping.
- **UnmappedFeature honesty** carries over: unknown tags/features are
  recorded (`unmapped`, `unmapped_features`), never guessed. The corpus
  exercises none (163 objects, 0 unmapped).

## End-to-end result (check_dodaf.py, 32 checks)

DoDAFLibrary.xmi (OMG UPDM example; 68,999 bytes) → reader →
`gen.uml25` Model → `emit_v2` → **sysmlpy-parsed v2**:

```
package <'DoDAF Class Library'> {
  /* v1 stereotype applied: StandardProfileL2::ModelLibrary */
  attribute def SecurityAttributes {
    doc /* W3C XML Schema for the Intelligence Community Metadata ... */
    /* v1 stereotype applied: updm::MeasurementSet */
    attribute classification : ClassificationType;
    attribute dateOfExemptedSource : String;
    attribute ownerProducer[*] : String;
    ...
  }
  ...
  enum def ClassificationType { C; CTS; <'CTS-B'>; ... }
  connection def <'packagedElement-7'> {
    end ownedEnd : SecurityAttributes;
    end classification : ClassificationType;
  }
}
```

Verified: 163 objects; 7 DataTypes + 1 Enumeration (17 literals) +
1 Association; 53 classifier-owned properties + 1 association-owned
end; 52 external String hrefs + 2 internal idrefs; 30 comments with
bodies; 26 `[0..*]` + 27 default `[1..1]` multiplicities; memberEnd =
[unnamed ownedEnd, SecurityAttributes-classification] with back-refs
resolved. sysmlpy counts: `{'attribute': 7, 'enumeration': 1,
'connection': 1}` — the external String never becomes a definition.
Output kept at `dodaf_library_v2.sysml`.

## Reproduce

```bash
~/ams-gra-sim/.venv/bin/python generate.py           # UML core (lxml)
~/ams-gra-sim/.venv/bin/python generate_profiles.py  # profiles (lxml + gen.uml25)
python check.py                                      # 45 checks (stdlib only)
python check_profiles.py                             # 21 checks
~/sysmlpy/.venv/bin/python check_v1_to_v2.py         # 16 checks (needs sysmlpy)
~/sysmlpy/.venv/bin/python check_dodaf.py            # 32 checks (needs sysmlpy + /mnt/TBFox/DoDAFLibrary.xmi)
```