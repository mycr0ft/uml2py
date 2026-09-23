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

Remaining for a full transformation: interaction/message bodies
(elided for grammar gaps, see Part 5), the accept-action via-port
receiver machinery (7.7.2.3.1.17-.19), guarded ObjectFlows,
JoinNode::isCombineDuplicate = false ('nonunique' qualifier is not
accepted by the target grammar), and OpaqueBehavior bodies.

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
~/sysmlpy/.venv/bin/python check_v1_to_v2.py         # 47 checks (needs sysmlpy)
~/sysmlpy/.venv/bin/python check_dodaf.py            # 32 checks (needs sysmlpy + /mnt/TBFox/DoDAFLibrary.xmi)
```

# Part 5: v1→v2 wave 3 (FullPort/ProxyPort, FlowProperty,
# constraint internals, Slot/instance models, interactions)

Wave 3 closes the remaining implementable initializers from the Beta 4
transformation spec (ptc/2025-04-07). All textual forms calibrated
against sysmlpy; check_v1_to_v2.py now runs 33 checks (wave-1 model
unchanged + a wave-3 model; output kept at `wave3_example_v2.sysml`).

## FullPort and ProxyPort (7.8.7)

- **FullPort → PartUsage with PortData metadata** (7.8.7.3.7 typed /
  7.8.7.3.15 untyped; normative gold example
  `part sysMLv1FullPort : SysMLv1Block {SysMLv1Library::PortData
  {isFullPort = true;}}`). Emitted as
  `part fullPort : MotorIf {@PortData {isFullPort = true;}}` with a
  local `metadata def PortData { attribute isFullPort : Boolean; }`
  stub standing in for SysMLv1Library (emitted once per package by
  emit_v2 when a FullPort is present), consistent with the wave-2
  RefineData/TraceData stubs.
- **ProxyPort: no normative mapping** - Table 30 lists no target and
  no mapping class exists (SYSML2_-329 flags the tables, but the
  absence is real). The base Port mapping (PortUsage) still applies,
  so ProxyPort emits as `port proxyPort;` followed by an explicit
  comment naming the gap. Conjugated-port generation is itself a
  documented spec gap (SYSML2_-199: ConjugatedPortDefinition is not
  generated).

## FlowProperty (7.8.7.3.4-.6; flagged SYSML2_-76 but specified)

Direction from the stereotype tag; target always referential:

| v1 form | v2 emission (calibrated) |
|---|---|
| typed by DataType | `out attribute torque : Kilogram;` |
| untyped | `in flowIn;` (directed ReferenceUsage) |
| typed by Class/Interface | `inout ref occurrence flowRef : Axle;` |

## ConstraintBlock internals (7.8.5.2.1 gold)

Parameters emit as directed attributes (`in attribute a : Kilogram;`)
and the ownedRule Constraint becomes a nested ConstraintUsage with an
opaque-expression body:

```
constraint def Adder {
  in attribute a : Kilogram;
  in attribute b : Kilogram;
  in attribute c : Kilogram;
  constraint sumCheck {
    language "OCL2.0"
    /* c == a + b */
  }
}
```

The `language "..." /* body */` form is the spec's textual rendering
for OpaqueExpression bodies (also used in the DecisionNode and
AcceptEventAction examples).

## Slot/instance models (7.7.4.2.13-.16)

- InstanceSpecification (not a link) → PartUsage typed by the
  classifier, slots as `redefines <definingFeature> = <value>;`
  (gold: `redefines sysMLv1ValueProperty = "Hello
  InstanceSpecification";`). Literal values inline
  (String/Integer/Boolean/UnlimitedNatural); unexpressable values
  raise UnmappedFeature.
- InstanceSpecification that is a link (classifier includes an
  Association) → `connection link1 : AssocD connect inst1 to inst2;`
  (7.7.4.2.13 gold; roles from the slots' values, typed by the
  association when it has a name).
- Property defaultValue → `= <expr>` on the usage (FeatureValue);
  InstanceValue → feature reference (7.7.4.2.16 gold:
  `part pv : Block1 = inst1;`).
- InterfaceBlock-typed Property → OccurrenceUsage
  (7.7.4.2.37 PropertyTypedByClassInterface gold:
  `occurrence sysMLv1Property2 [0..1] : SysMLv1Interface;`).

## Interactions (7.7.8) - mapped but not expressible

The normative targets exist in the v2 metamodel but not in the target
grammar reader (sysmlpy 0.91.0 has no `interaction`, `step`, or
`invariant` keywords - verified by calibration):

- Interaction → Interaction (7.7.8.3.6): **elided with an inventory**
  naming the normative sub-mappings (Lifeline → PartUsage 7.7.8.3.13,
  Message → Flow/ItemFlow 7.7.8.3.15).
- CombinedFragment → Interaction (7.7.8.3.3), InteractionOperand →
  Interaction (7.7.8.3.7), InteractionUse → Step (7.7.8.3.9),
  StateInvariant → Invariant (7.7.8.3.17): elision comments with
  anchors.
- ActionExecutionSpecification/BehaviorExecutionSpecification →
  `action <name>;` (7.7.8.3.1/.2; unnamed ones elided with a comment).
- Table-11 not-mapped elements (MessageOccurrenceSpecification,
  ExecutionOccurrenceSpecification, DestructionOccurrence-
  Specification, Gate, GeneralOrdering, Continuation, ...): explicit
  `/* v1 <Class> <name> not mapped in ptc/2025-04-07 (7.7.8.2
  Table 11) */` comments.
- Association member ends can be unnamed: `end : SysMLv1Block1[1];`
  (7.7.4.2.13 gold), so emit_association now emits unnamed ends with
  multiplicities instead of inventing names.

Wave-3 sysmlpy counts: `{'metadata': 1, 'part': 6, 'constraint': 1,
'connection': 2, 'action': 1}`. Wave-1 counts unchanged (the original
16 checks all still pass).

# Part 6: v1→v2 wave 4 (activity internals, guards,
# subsetting/redefinition)

Wave 4 implements the activity-edge and control-node mappings plus
feature specializations. check_v1_to_v2.py now runs 47 checks; the
wave-4 model is kept at `wave4_example_v2.sysml`.

## Subsetting and redefinition (7.7.4.2.36)

Property::subsettedProperty / redefinedProperty become textual
feature-specialization suffixes (calibrated: the spec clause precedes
the default value):

- `attribute dattr : Kilogram subsets battr;`
- `ref part spare : BaseBlock redefines wheels;` (redefinition is a
  specialization in v2)

Untyped Properties map to Feature normatively, but the target grammar
(sysmlpy 0.91.0) has no `feature <name>;` declaration, so the bare-name
feature form is emitted (`battr;` - a keyword-less usage declaration is
a Feature in v2).

## Activity edges

| v1 form | v2 emission (calibrated) |
|---|---|
| ControlFlow (unguarded) | `succession cf first a1 then a2;` (7.7.3.3.23 gold) |
| ControlFlow (guarded, opaque) | `succession cf1 first a1 if { return : ScalarValues::Boolean; language "OCL2.0" /* x > 0 */ }.result then a2;` (inline anonymous-calc guard; the spec's TransitionUsage gold nests a named calc in the target action, but the inline form of the 7.7.3.3.33 decision-node gold is equivalent and parses) |
| ControlFlow (guarded, boolean literal) | `succession s first a1 if true then a2;` |
| ObjectFlow (unguarded) | `succession flow of1 of Kilogram from a1.result to a2.inputValue;` (7.7.3.3.47 gold; `of T` from the source pin type, omitted when untyped) |
| unguarded outgoing decision edge | inline calc with `language "SysMLv1" /* else */` (ExpressionElse_Mapping) |
| edge from InitialNode / to FinalNode | elision comments (v2 succession requires `first`/`then`; the initial node maps to a source feature and the final node to a done-subsetted feature, 7.7.3.3.22/.24) |

Action pins: typed pins emit `in/out <name> : T;`, pins touched by an
ObjectFlow carry the `item` keyword per the MergeNode gold
(`out item result : Kilogram;`), unnamed pins get deterministic
synthesized names (`input<i>` / `output<i>`) so succession-flow
references stay resolvable.

## Control nodes (7.7.3.3.33/.35/.45/.46)

- DecisionNode → `decide dn;`
- MergeNode/ForkNode/JoinNode → `merge/fork/join <name>;`, and when
  ObjectFlows touch them, the SYSML2_-111 synthesized pins:
  `merge mn { in ref inputObject1; in ref inputObject2; out ref
  outputObject1 = (inputObject1, inputObject2); }` (fork out pins each
  equal the single input; bare `out ref outputObject1;` when there are
  no inputs).

## OpaqueAction, CallOperationAction, SendSignalAction, AcceptEventAction

- OpaqueAction (7.7.2.3.2.2 gold): `action a1 { in x; out result :
  Kilogram; language "OCL" /* x = y + 1; */ }` (only the first
  language/body pair is transformed, with a count comment for more).
- CallOperationAction (7.7.2.3.3.4 gold):
  `action coa { in paramIn; in target : T2; out paramReturn =
  target.op; }` - the call is a perform-by-default-value feature
  reference.
- SendSignalAction (7.7.2.3.3.24 gold `send SysMLv1Signal() to
  target;`): emitted as `send Sig to target;` **without the empty
  parentheses** - the target grammar rejects empty argument lists
  (sysmlpy ArgumentList bug).
- AcceptEventAction (7.7.2.3.1.2): only the first trigger is
  transformed (spec rule; extra triggers get a count comment).
  SignalEvent → `accept : Sig;`, ChangeEvent → `accept when {<inline
  calc>}.result;`. The declarative gold form `action a accept : S via
  p;` is rejected by the target grammar, so the accept clause nests in
  the action body; the via-port receiver machinery (7.7.2.3.1.17-.19)
  is elided.

## Guards on state-machine transitions

`transition tg1 first s1 if true then s2;` (LiteralBoolean guard) and
the inline-calc form for opaque guards (calibrated in state
definitions).

Wave-4 sysmlpy counts: `{'part': 2, 'action': 1, 'item': 1,
'state': 1}`. Waves 1-3 unchanged (all 33 prior checks still pass).
---

# Part 7: UAF 1.2 profile (gen/uaf.py) - third OMG profile corpus

User request: "find the UAF.xmi files and get these parsed as well". The
OMG UAF 1.2 page publishes `UAF.xmi` (UAFML profile, 20211201) and
`MeasurementsLibrary.xmi` (instance model) at
`https://www.omg.org/spec/UAF/20211201/` - both downloaded to
`/mnt/TBFox/uml_xmi/` (OMG-published, hence corpus-eligible under the
same rule as DoDAFLibrary.xmi).

## What the UAF 1.2 XMI contains

1,024,601 bytes of XMI 2.1/EMF serialization (same dialect family as
sysml.xmi, produced by the UAF tooling): 256 stereotypes, 253
Extensions, 414 properties, 259 OCL constraints, 379 generalizations,
58 associations, 20 enumerations, 114 packages under 12 viewpoint
packages (Operational, Strategic, Resources, Services, Security, ...).

## Dialect deltas vs sysml.xmi (handled in generate_profiles.py)

- **UUID idrefs everywhere**: generalization `general` attributes and
  property `type` attributes carry xmi:ids, not dotted name paths.
  `parse_profile` now builds an id->element map and resolves refs
  against it (256 unique stereotype names - verified).
- **Nameless Extensions**: no name attribute; the metaclass comes from
  the memberEnd property (`base_<Meta>`), the owning stereotype from
  the property's owner (fallback: `extension_<S>` end name).
- **ExtensionEnd::lower defaults to 1** (UML 2.5.1), so the 248
  value-attr-less lowerValues + 5 missing lowerValues all mean
  REQUIRED extensions (unlike ordinary EMF properties where an empty
  lowerValue means 0 - the DoDAF lesson, now generalized).
- **Cross-profile generalizations**: 49 href generalizations into
  SysML.xmi (#SysML.Block x14, #SysML.Allocate x17, ProxyPort,
  InterfaceBlock, ValueType, Requirement, Trace, Refine,
  DeriveReqt, ItemFlow, View, Viewpoint). The emitter folds them as
  Python bases from `gen.sysml` (e.g. `Capability(sysml.Block,
  U.Class, PropertySet, ...)`, `View(sysml.View, ...)`) with the
  emitted module importing `gen.sysml` when needed.
- **Stereotype-typed tagged values**: 104 properties typed by
  stereotype xmi:id refs. Since `_Ref` stores its type as opaque
  metadata, these are late-bound as string references (`'Resource'`,
  `'sysml.Block'`) - topological order only covers inheritance, so a
  forward class reference would be unsafe; strings are checked to
  resolve against gen.uaf/gen.sysml.
- **SysML library types**: 4 tagged values typed through
  `_SysML_Libraries_...-String_PackageableElement` hrefs map to `str`.
- **Duplicate serializations**: UAF.xmi repeats `base_Element` on
  UAFElement, repeats a Resource generalization on
  ServiceExchangeItem, and repeats the UAFElement Extension pair -
  all deduped at parse time (with a comment).
- **C3 permutation blowup**: UAF stereotypes fold up to 10+ bases;
  the exhaustive permutation search is capped at 6 bases, then the
  greedy C3 insertion fallback takes over.

## Result

- `gen/uaf.py`: 3,750 lines, 256 stereotype classes, 112 tagged
  values, 259 constraints, 20 enums, 252 extension entries.
- `check_profiles.py` extended 21 -> 40 checks (all green): counts,
  abstract flagging (44), cross-profile folds, constraint text,
  extension table, late-bound tags, enum literals, no shadowing.
- Regression: `gen/standard_profile.py` and `gen/sysml.py` are
  byte-identical to the previous commit.
- Suite totals: check.py 45, check_profiles.py 40,
  check_v1_to_v2.py 47, check_dodaf.py 32 = **164 checks**.

## Still open (honest)

- `MeasurementsLibrary.xmi` (74 KB UML model + UAF stereotype
  applications) is downloaded and queued as the next instance-reader
  corpus (check_dodaf-style suite) - reader dialect work pending.
- BPMN: OMG does not publish a UML-profile XMI for BPMN; the
  metamodel ships as CMOF XMI (BPMN20.cmof + DI/DC/BPMNDI.cmof,
  20100501) - a separate MOF/CMOF generator would be needed
  (`generate_bpmn.py`), tracked as future work.

---

# Part 8: BPMN 2.0.2 via CMOF XMI (gen/bpmn.py) - the "XMI representation" answer

User follow-up: "Maybe BPMN's xmi representation?" Finding: OMG does NOT
publish BPMN as a UML-profile XMI. BPMN 2.0's canonical serialization
is the XSD-based `.bpmn` XML exchange format, and the OMG page publishes
the **metamodel as CMOF** (MOF 2.0 XMI): `BPMN20.cmof` (189,597 bytes,
20100501) plus `DC/DI/BPMNDI.cmof`. The CMOF is BPMN's XMI
representation - downloaded to `/mnt/TBFox/uml_xmi/`.

## CMOF dialect (new generator `generate_bpmn.py`)

- root `cmof:Package` "BPMN20" (uri .../MODEL-XMI), 339 ownedMember:
  137 classes, 193 associations, 9 enumerations (28 literals);
- **generalization by `superClass` attributes** (space-separated;
  e.g. `Task superClass="Activity InteractionNode"`) - C3-verified
  Python bases with the greedy fallback;
- **multiplicity on the class-side attribute**: 216 attrs default
  1..1, 99 carry upper='*' (absent lower -> 0; all are 0..* in the
  normative prose), 96 composite, 10 derived, 27 literal defaults
  carried as comments;
- **associations as memberEnd name-pairs** ("Class-endName" /
  "AssocId-endName"): class-owned ends wire `opp` both directions;
  association-owned ends synthesize back-refs onto the partner class
  (the uml25 hidden-end closure pattern); both-ends-class-owned
  serializations just wire opposites (17 such, no warnings);
- primitives by href (`cmof.xml#String/Boolean/Integer` -> str/bool/
  int), MOF DOM Element (8 refs, late-bound `'xml.dom.Element'`),
  one external `BPMNDI.cmof#BPMNDiagram` ref kept package-qualified
  (`'BPMNDI.BPMNDiagram'`) on `Definitions.diagrams`;
- the CMOF carries **no OCL** (unlike the profile XMIs) - BPMN
  constraints are normative prose in the spec; noted in the module
  docstring rather than invented.

## Result

- `gen/bpmn.py`: 2,247 lines; reuses `gen.uml25._Ref` descriptors on a
  local `_MOFBase` base - BPMN instances are deliberately NOT UML
  Elements (checked).
- `check_bpmn.py`: 25 checks, all green (counts, hierarchy, multi-
  inheritance fold, instantiation/kw-args, abstract guards, enum
  literals incl. the keyword-guarded `'None'` literal, opposite
  wiring, composite/derived flags, DOM/external late-bound types,
  no collision with gen.uml25 objects).
- Generator warnings: none. 29 back-ends synthesized; 17 both-ends-
  class-owned associations wired as opposites.
- Suite totals: check.py 45, check_profiles.py 40, check_v1_to_v2.py
  47, check_dodaf.py 32, check_bpmn.py 25 = **189 checks**.

## Still open (honest)

- `MeasurementsLibrary.xmi` (UAF instance corpus) queued for the
  xmi21 reader - pending dialect work (prefixed UAF stereotype
  applications).
- DI/DC/BPMNDI CMOF packages (diagram interchange) not generated;
  the one cross-file ref is a late-bound string.
- BPMN has no normative SysML v2 mapping - no emitter path (would be
  non-normative; honesty rule applies).

---

# Part 9: Wave E1 - EMF instance XMI writer (xmi_write.py) with canonical parity

Plan: PLAN.md (waves E1-E6). E1 closes the write-path half of the OpenAPI
coverage survey: read -> write -> read is now lossless on the E1 oracle
corpus, and the writer output is canonically equal to the OMG original.

## Dialect probes (P1-P3 pinned, DoDAFLibrary.xmi)

- Root: `xmi:XMI`; 62 root children = 61 stereotype applications
  (53 updm:Measurement, 7 updm:MeasurementSet, 1
  StandardProfileL2:ModelLibrary) + uml:Model + ModelLibrary.
- **P1**: non-containment refs = repeated feature-named child elements
  with `xmi:idref` (annotatedElement x30, memberEnd, association, type);
  cross-file refs = child element with `href` (x52, all `UML.xmi#String`).
- **P2**: enum-valued features are text children (visibility), like all
  primitives in this dialect (name, body, value); no boolean-valued
  feature occurs in the corpus (documented convention: 'true'/'false'
  as text children).
- **P3**: no redefined-alias duplication occurs in this corpus; the
  writer emits stored per-property values and canon compares
  feature-grouped.

## Writer conventions (xmi_write.py)

- composite features -> nested feature-named children with
  `xmi:type="uml:<Meta>"` and `xmi:id`; ids: stored `_xmi_id` reused
  (round-trip stable), else deterministic `_<n>` traversal order;
- **containment opposites never emitted**: the reader's `_hook_add`
  wiring stores `Property.datatype` (and would store
  `EnumerationLiteral.enumeration`, `Property.class_`, ...) in `_vals`,
  but EMF serializes only the containment side; the writer skips the
  feature named by the containing ref's `opp` - and only that feature
  (a blanket owner-identity filter was tried first and wrongly dropped
  `Comment.annotatedElement`, which EMF does emit even when it points
  at the container);
- `LiteralUnlimitedNatural` value 0 omitted (EMF feature default; the
  reader's inverse rule maps empty `<lowerValue/>` to 0), '*' emitted;
- derived/union/readonly never emitted (not settable, never stored);
- applications emitted first at root with `base_<Meta>` idrefs
  (base metas recorded by the reader's new `app_metas` map; fallback
  `base_<Metaclass of base>`); `profileApplication` on the first root
  with `xmi:type="uml:ProfileApplication"` and the appliedProfile href;
- profile-namespace prefixes come from the reader's recorded root
  `nsmap` (new additive reader fields: `nsmap`, `app_metas`).

## Result

- **Round-trip graph parity** (id-keyed signature: features, refs,
  containment order, applications, hrefs, app metas): equal.
- **Canonical structural parity** vs the OMG-published original
  (canon.py, normalizations documented in its docstring): empty diff.
- Writer is deterministic (byte-identical repeat writes).
- Programmatic graphs (no reader involvement) round-trip; dangling
  references raise WriteError.
- check_xmi_write.py: 26 checks. Suites: 45 + 40 + 47 + 32 + 25 + 26
  = **215 checks**, all green; regression suites byte-unchanged.

## Honest notes

- xmi:uuid is not preserved (not read); canon ignores it.
- The profileApplication element's own xmi:id is re-derived (cosmetic;
  canon ignores ids).
- Booleans: unobserved in the corpus; emitted as text children per the
  element-formatting convention.
- Canon normalizations are documented in canon.py's docstring (id/uuid
  ignored, feature grouping, root-order multiset, idref->containment
  path, optional derived-<name> tolerance).

---

# Part 10: Wave E2 - stereotype & profile-application writing, the 2.5.1-era dialect (P10)

E2 adds the second XMI dialect to the read/write pair: OMG's
UAF 1.2 MeasurementsLibrary.xmi (UML 20161101 ns, XMI 20131001 attrs -
the "2.5.1-era EMF" form) vs DoDAFLibrary.xmi (UML 20090901, XMI 2.1).

## Dialect probes (P4/P5/P10 pinned, MeasurementsLibrary.xmi)

- **P10 applications**: prefixed root-level elements
  (`UAF:Measurement xmi:id="..." base_Property="..."`) - base_<Meta>
  and tag values as attributes; no xmi:type on the application element.
  76 applications: 60 Measurement (base_Property), 12 MeasurementSet
  (base_DataType), 1 ResourceInformation + 1 Organization (base_Class),
  2 sysml:ValueType (base_DataType) - a cross-profile application is
  present in the corpus (SysML ValueType applied in a UAF file).
- **P10 primitives**: name/body/visibility are attributes (88/86/64
  occurrences); Package.URI is a text child (`<URI>...`) - the
  genmodel serializes it as an element; both facts pinned by census.
- **P10 references**: single-valued idrefs as attributes (association
  x2, type x6); multi-valued refs stay children with xmi:idref
  (annotatedElement x86, memberEnd x2); cross-file hrefs stay children
  (type href x59 incl. PrimitiveTypes markers and UML.xmi#_0).
- **P10 literals**: literal elements are children with `value` as an
  attribute (`value="*"` x18 on upperValue); the 0 default is omitted
  (18 empty lowerValue elements); LiteralInteger carries no value
  (EMF default 0, symmetric in both directions).
- **P4/P5**: profile applications are two `profileApplication`
  elements (UAF.xmi#UAF, SysML.xmi#SysML) under the Model - one per
  applied profile; no per-app required-extension data is carried.

## Changes

- `generate_profiles.py`: parses the profile Package's `<URI>` and emits
  `_URI` into gen/{standard_profile,sysml,uaf}.py (only UAF.xmi carries
  one; the others emit `_URI = None` with a comment - the applied URI is
  dialect-dependent, e.g. 20090901-era vs 20161101-era files). Output
  idempotent; +2 lines per module; all profile-suite checks green.
- `xmi21.py` (additive):
  - both XMI attribute namespaces accepted (2.1 schema.omg URI and
    20131001 omg.org URI) via `_xget`;
  - P10 attribute forms on walked elements: primitives (name/visibility/
    body/URI) as unprefixed attributes, single idrefs (association, type)
    as attributes -> pending; child form wins if both occur;
  - `URI` is a real Package feature (UML 2.5.1) -> STRING table;
    `packageImport`/`importedPackage`/`PackageImport` mapped; the href'd
    importedPackage becomes a synthetic Package marker (generalized
    href-marker machinery beyond `type`);
  - application elements: base_<Meta> attributes (P10) and tag values
    (app_tags, new field); 2.1 child-form tag text children parsed
    symmetrically (unobserved, documented);
  - one MagicDraw header extension remains unmapped:
    `metamodelReference` on the Model (references the packageImport id).
- `xmi_write.py`:
  - XMI dialect derived from nsmap['xmi']: the 2.1 URI keeps the E1
    (DoDAF) byte-parity forms; any later URI emits the P10 form;
    nsmap['uml'] likewise overrides the UML namespace;
  - applications: prefixed elements with base_<Meta> (and tag)
    attributes in P10; base feature from the applied metaclass, falling
    back to the profile module's `_EXTENSIONS` (most-general = first
    entry) when the base is an id string; profile-module `_URI` resolves
    the namespace when nsmap lacks the prefix;
  - tags: attributes (P10) or text children (2.1), from an optional 6th
    app-tuple slot (apps_from_model merges the reader's app_tags);
  - profile applications: one `<profileApplication>` element per
    applied-profile href (the reader flattens the corpus form).
- `canon.py`: both XMI URIs for id/uuid/idref/type; `drop_feats_at`
  ({xmi_id: {feature names}}) for tool-specific header features; the
  reader-derived name is also dropped in attribute form.

## Result

- **ML round-trip**: 221 objects, 76 applications, 59 hrefs, app
  metas, Model URI, packageImport all preserved; full graph signature
  equal; re-read has zero unmapped features.
- **ML canonical parity** vs the OMG original: empty diff, dropping
  only `metamodelReference` (MagicDraw extension; UnmappedFeature note)
  and the two reader-derived names (RSA/UUID-tail rule).
- **DoDAF unchanged**: 2.1 path byte-parity and canon parity preserved
  (check_xmi_write.py E1 checks green unchanged).
- Programmatic application writing: profile-module `_URI` resolution,
  `_EXTENSIONS` base fallback for string bases, tags both dialects,
  unresolvable-profile WriteError.
- check_xmi_write.py: 48 checks. Suites: 45 + 40 + 47 + 32 + 25 + 48
  = **237 checks**, all green; regression suites unchanged.

## Honest notes

- `metamodelReference` is a MagicDraw extension (not a UML 2.5
  metaclass feature); flagged as unmapped_features, canon-dropped,
  documented here. Its target (the packageImport element) round-trips.
- P10 single-ref-as-attribute is pinned by the ML corpus (association,
  type); no other single-ref feature occurs there.
- P10 primitive-as-attribute set is pinned to observations:
  name/visibility/body and literal `value`; Package.URI is observed as
  a text child (genmodel element-serialization choice), everything
  else unobserved stays a child by default.
- StandardProfile/SysML profile modules carry `_URI = None`: their OMG
  XMI has no <URI> child; applications of those profiles need the
  dialect's nsmap (or a future user-supplied URI) - documented in the
  writer docstring.
- Tag values are typed as strings in both forms; no tag exists in
  either corpus (both corpora carry none), so no enum-typed tag
  round-trip is demonstrated yet.

---

# Part 11: Wave E5 - CMOF writer (mm_write.py) over the BPMN 2.0.2 metamodel

E5 closes the metamodel-writing half for BPMN: gen/bpmn.py (generated
from OMG BPMN20.cmof) plus a `_SYNTH` serialization table reconstructs
the OMG CMOF file with canonical parity.

## Dialect probes (P5/P8 pinned, BPMN20.cmof)

- Root `xmi:XMI` (xmi 2.1 + cmof ns); one `cmof:Package`
  (xmi:id "_0", name="BPMN20", uri="...MODEL-XMI") + two cmof:Tag
  elements (nsPrefix bpmn, nsURI MODEL-XMI, element="_0").
- All 339 members flattened as `ownedMember` children (137 Class +
  9 Enumeration + 193 Association); member order is hand-edited in the
  file and carries no semantics (MOF ownedMember is a set) - canon
  normalizes it as a multiset and the writer emits a deterministic
  order (enumerations sorted, classes in dependency order,
  associations in file order).
- Classes: id == name; `superClass` space-separated attribute (the
  C3-verified runtime base order equals the file's for all 137);
  `isAbstract` only when true (17).
- Properties (493 = 316 class-side + 177 association-owned ends):
  primitive/DOM/external types as `<type>` children carrying verbatim
  hrefs (String x66, Boolean x23, Integer x5, MOF Element x8,
  BPMNDI.cmof#BPMNDiagram x1 - a RELATIVE href); class/enum types as
  `type="<id>"` attributes (x390); id == "<owner>-<name>".
- Multiplicity (P8): upper written when != 1; lower written when 0 -
  except 8 class-side properties where lower is omitted with upper='*'
  (two spellings of 0..* in the hand-produced file; both preserved
  verbatim via _SYNTH). Ends: (0,'*') x78, default x32, ('0',) x67.
- visibility: associations always "private" (x193); properties only
  when "public" (x87: 61 class-side + 26 ends) - no derivable rule,
  stored verbatim. isOrdered on exactly one property
  (FlowNode-outgoing). `default` attribute on 27 properties
  ('false' x12, 'true' x4, and literals including 'text/plain').
- Association attribute: exactly the 209 class-side properties that
  appear as class-owned memberEnd refs carry `association="A_*"`
  (bijection verified); the 17 wired class-side navigable properties
  do NOT (their end is association-owned in the file).
- Ends: owningAssociation + association (both = the association id);
  isDerived on 2; visibility public on 26.
- Enumerations: ownedLiteral children with classifier/enumeration
  attributes; id "<Enum>-<literal>".
- xmi:ids: class/enum/association id == name; property/ends/literals
  "<owner>-<name>"; canon ignores ids, but memberEnd/type/element
  attribute values are compared verbatim and reproduce.

## Changes

- `generate_bpmn.py`: the parse keeps raw serialization forms (lower/
  upper strings, visibility, isOrdered, verbatim hrefs, Package
  attrs, Tags, association-owned end records) and `emit_module` writes
  a `_SYNTH` table into gen/bpmn.py: package, tags, hrefs, ends (177),
  props (316: raw lower/upper/vis/ordered/default per class-side
  property), synth_attrs (155 generator-created back-refs, absent from
  the file). _ASSOCIATIONS now emits in file order (the writer's
  member order; deterministic and parse-order preserving).
  Output idempotent; check_bpmn.py green unchanged.
- `mm_write.py` (new): `write_cmof(module)` reconstructs the CMOF
  package from the runtime tables + _SYNTH: classes (superClass from
  the C3-verified bases, own _DECL attrs in declaration order,
  synthesized back-refs skipped), enumerations (literals with
  classifier/enumeration), associations (memberEnd verbatim, ownedEnd
  from ends), tags; types by tkind (href child vs type attribute).
- `canon.py`: `multiset_features` parameter - feature groups compared
  as sorted multisets (MOF Package.ownedMember is a set).

## Result

- **Canonical parity**: canon(BPMN20.cmof, written) empty with
  ownedMember normalized as a multiset. Writer deterministic.
- **Structural round-trip**: re-parsing the written file with the
  generator's parse reproduces identical classes, associations and
  metadata (no warnings); the file's hand-edited member order is the
  only normalization.
- check_cmof_write.py: 20 checks. Suites: 45 + 40 + 47 + 32 + 25 + 48
  + 20 = **257 checks**, all green; regression suites unchanged.

## Honest notes

- _SYNTH grew beyond the plan's original sketch ("association-owned
  ends recovered from synthesized flags"): the file's hand-edited
  member order, two 0..* spellings, public-visibility islands, one
  isOrdered property and 27 default attributes are not derivable from
  the runtime _Ref tables, so the table carries the raw forms
  (316 props + 177 ends + 155 synth markers + package/tags/hrefs).
  The generated module change is listed, idempotent, and
  check_bpmn.py stays green.
- ownedMember order normalization is semantic (set), not convenience:
  the CMOF file's order is hand-edited with no MOF meaning.
- Byte parity for BPMN20.cmof is not pursued (stretch goal per plan;
  the file is hand-edited and canon is the gate).
- The writer derives association/owningAssociation on ends, literal
  classifier/enumeration, and end ids "<assoc>-<name>" by convention;
  all verified against the file.

---

# Part 12: Wave E3 - normative UML 2.5.1 derivations (derived.py)

The spec-normative derivation layer: free functions over `gen.uml25`
objects (generated modules stay byte-frozen), implemented from the
OCL bodies of UML 2.5.1 formal/2017-12-05 (downloaded to `spec/`,
gitignored). Standard library only.

## Implemented derivations (spec anchors)

- Element §7.8.6: `owner` (the /owner union, computed as the
  containment inverse by the runtime), `all_owned_elements`
  (ownedElement DFS with a global seen-set: the OCL is set-valued, so
  ill-formed ownership cycles drop, not re-walk), `must_be_owned`
  (§7.8.6.5 body true; §12.4.5.7 redefines false for Package).
- NamedElement/Namespace §7.8.9/§7.8.10: `all_namespaces` (ordered
  innermost-first, **including the template-parameter branch**:
  owner is a TemplateParameter -> walk
  signature.template.allNamespaces()->prepend(template)),
  `qualified_name` ('::'-joined from the outermost namespace; null
  unless the element and every namespace has a name), `separator`.
  Namespace §7.8.10: `get_names_of_member` (ownedMember / ElementImport
  alias / PackageImport recursion, exactly the OCL branches),
  `imported_member` via `import_members`/`exclude_collisions`/
  `is_distinguishable_from` (full fidelity), `visible_members`/
  `makes_visible` (§12.4.5.6).
- Classifier §9.2.4: `parents` (generalization.general),
  `all_parents` (seen-set-guarded transitive closure),
  `all_features`/`all_attributes` (over the **normative member**),
  `has_visibility_of`, `conforms_to`; normative member =
  stored member union + computed `inherited_member`
  (inherit(parents().inheritableMembers)) + computed
  `imported_member` - on instance models those two are stored as null,
  so computing them is the only faithful reading.
- MultiplicityElement §7.8.8: `lower_bound`/`upper_bound`
  (lowerValue/upperValue integerValue; on instance models the XMI
  carries the derived `lower`/`upper` directly, so the carried value is
  the fall-back - documented deviation from the literal "1 otherwise",
  which applies when neither is given).
- Property §9.9.17: `is_composite` (= aggregation == composite),
  `opposite` (other end of a binary association), `subsetting_context`.

## Derived-union evaluation (union())

UML 2.5.1 §7.6.3: "the collection of values denoted by the Property in
some context is derived by being the strict union of all of the values
denoted, in the same context, by Properties defined to subset it".
`derived.union(el, name)` implements this over the generated `_UNIONS`
tables with two additions beyond the runtime's generation-time
flattening (`_Ref._union`):

1. a contributing property that is itself a derived union is expanded
   recursively (cycle-guarded) - the generated tables record no union
   contribs (verified: 0), so this is currently a no-op safety net;
2. a property that REDEFINES a property that subsets a union also
   contributes: any reference to a redefined member resolves to the
   redefining member (§9.2.3.3), so its values are values of the
   subsetted property. This closure is load-bearing: a scan of the
   generated tables finds exactly **9** metaclasses whose union
   contribution arrives only through redefinition (LoopNode.result and
   ConditionalNode.result via structuredNodeOutput->/output;
   LoopNode.loopVariableInput; SequenceNode.executableNode;
   ProtocolStateMachine.extendedStateMachine;
   RedefinableTemplateSignature.classifier via template->/owner;
   SendObjectAction.request). For these, runtime `ln.output` is empty
   while the normative union has the value (checked by construction).

On the OMG corpora the two evaluators agree everywhere (2171 union
reads over 384 objects in DoDAFLibrary + MeasurementsLibrary), which
also validates the generation-time flattening; the corpus contains no
instances of the 9 redefinition-gap classes.

## Honest notes

- Corpus set: DoDAFLibrary + MeasurementsLibrary. UAF.xmi (P10 profile
  file) is profile-source only: its root <uml:Profile> is not in the
  reader's root dispatch (Model/Package only), and its stereotype
  definitions are not gen.uml25 metaclasses - instance-level UAF load
  is out of scope for E3 (documented, not attempted).
- excludeCollisions: the literal OCL
  `imps->exists(imp2 | not imp1.isDistinguishableFrom(imp2, self))`
  quantifies over imp1 itself (rejecting everything); read as a
  distinct-pair quantifier, which is the evident intent.
- Imports whose target is an external href marker (no Package object)
  are elided from get_names_of_member/imported_member (DoDAF/ML carry
  such imports; the visible-members recursion needs a real Package).
- The corpus instantiates no Generalizations, so the all_parents corpus
  leg is crash/robustness only; the constructed diamond is the
  non-vacuous leg.
- Not attempted (need a real OCL engine or are semantics, not
  derivations): membersAreDistinguishable (needs isDistinguishableFrom
  over all member pairs - actually tractable but O(n^2) per namespace;
  left as a documented elision), TemplateSignature parameter
  conformance, ActivityNode logic.

check_derived.py: 42 checks. Suites: 45 + 40 + 47 + 32 + 25 + 48 + 20
+ 42 = **299 checks**, all green.

---

# Part 13: Wave E4 - query helpers (query.py)

Search API over `gen.uml25` instance graphs; standard library only;
builds directly on E3's union evaluation and `qualified_name`.

## API

- `walk(root)`: deterministic DFS over composite containment
  (derived-union `ownedElement` reads, cycle-guarded); root first,
  then each owned subtree in declaration order.
- `find(root, metaclass=None, stereotype=None, name=None,
  qualified=None, pred=None, deep=True)`: predicates AND-combined.
  `metaclass` takes a generated class or metaclass name string
  (isinstance, so abstract metaclasses match and subclasses are
  included); `stereotype` takes a full label ("Profile::Pkg::Name"),
  a bare stereotype name (matched on the label's last segment), or a
  (profile, name) pair; `qualified` compares `derived.qualified_name`;
  `deep=False` restricts to direct children.
- `of_type(root, cls)` (shorthand), `exists(root, ...)`,
  `count(root, ...)`.
- `stereotypes(el)`: resolved labels for the element's stereotype
  applications. The reader records `base._applied_stereotypes` as
  (profile, stereo, app_id) triples; labels resolve through the
  generated profile modules' `_STEREO` strings (case-insensitive
  profile segment, exact last segment), with "{profile}::{stereo}"
  fallback. E.g. a MeasurementsLibrary property carrying the UAF
  Measurement application resolves to "UAF::Parameters::Measurement"
  (the profile's nsmap prefix and the _STEREO first segment agree).

## Findings during the wave

- `Comment` is an Element, not a NamedElement: `qualified_name` now
  returns None for non-named elements (guard added in derived.py;
  the corpus check over 267 named/unnamed elements still agrees with
  an independent walk).
- Reader-synthesized multiplicity defaults: DoDAF's walk reaches 52
  `LiteralUnlimitedNatural` specs whose `_owner` is unwired (the
  reader raw-sets defaults without hook wiring - E1 behavior). The
  walk is right (they are genuinely contained); the check states the
  exception explicitly.
- UAF.xmi is profile-source only (see Part 12); query checks use
  DoDAF + MeasurementsLibrary.

check_query.py: 19 checks. Suites: 45 + 40 + 47 + 32 + 25 + 48 + 20 +
42 + 19 = **318 checks**, all green.

---

# Part 14: Wave E6 - EMOF writer (mm_write.write_emof)

The EMOF dialect half: serialize a trimmed metamodel subset per the
MOF 2.0/XMI Mapping Specification v2.1 ("XMI Representation of the
Core Packages", section 6.5.2). The spec was downloaded locally
(gitignored; note: formal/05-07-04 is UML 2.0 Superstructure - the
mapping spec is the "MOF 2.0/XMI Mapping Specification, v2.1" PDF
served by omg.org/spec/XMI/2.1/PDF; the plan's document label was
corrected here).

## Rules pinned (section 6.5.2 EMOF Package)

- A Package/Class is an XMIObjectElement; the spec's own QName example
  is `emof:Class` (section 6.5 prose).
- **Derived information is not serialized** - derived properties and
  `association` (itself derived) never appear.
- **Properties whose values are the default values are not serialized**
  - against the MOF 2 Core defaults (lower=1, upper=1, isOrdered=false,
    isComposite=false, isDerived=false, visibility=public,
    isAbstract=false).
- **For isComposite properties the opposite Property is not serialized**
  - EMOF has no Association: no memberEnd, no ownedEnd, no
    owningAssociation; enumeration literals carry no classifier/
    enumeration opposites.
- Null values would serialize as nil='true' (unobserved at metamodel
  level).

## Construction decisions (honest notes)

- Namespace `http://schema.omg.org/spec/MOF/2.0/emof.xml`: constructed
  by analogy with the OMG-published BPMN20.cmof corpus namespace
  (`.../cmof.xml`) plus the spec's `emof:` QName usage; the URI itself
  is the industry-standard EMOFResource convention, not read from a
  normative EMOF sample. No OMG-published EMOF metamodel file is in
  the corpus set, so this writer is rule-conformant, not
  sample-verified.
- Shared MOF 2 Core property names (Package.ownedMember,
  Class.ownedAttribute, Enumeration.ownedLiteral, Property.visibility/
  lower/upper/default, Class.superClass/isAbstract) and the unprefixed
  containment-child spelling are evidenced by BPMN20.cmof.
- Primitive hrefs become `emof.xml#String` etc.; the MOF Element href
  stays verbatim at its cmof.xml namespace (corpus-provenance
  preservation, as in E5).
- `write_emof(module, classes)`: subset selection; referenced
  enumerations are auto-included; superClasses are written verbatim
  even when outside the subset (name stays resolvable).

## Result

- 8-class BPMN subset (FlowNode, SequenceFlow, Gateway,
  ExclusiveGateway, Task, Process, DataInput, FormalExpression) + 2
  enums + 2 tags. Deterministic (byte-identical).
- check_emof_write.py: 18 checks - determinism, namespace/element
  pins, every 6.5.2 suppression rule (memberEnd absent, derived
  absent, isOrdered=true only, visibility/isComposite/isAbstract
  defaults suppressed), property forms (emof.xml hrefs, name idrefs,
  verbatim external href, literals with ids/names only), a minimal
  EMOF reader reconstructing classes/supers/attributes/multiplicities
  equal to the source subset, and dialect parallelism with
  write_cmof (same names, identical multi-superClass, the one
  isOrdered property).

Suites: 45 + 40 + 47 + 32 + 25 + 48 + 20 + 42 + 19 + 18 = **336
checks**, all green. The exporter plan (E1-E6) is complete.

# Part 15: UAF 1.3 profile (gen/uaf13.py) over OMG UAF13.xml

## Provenance

- UAF 1.3 formally adopted by OMG April 2026 (formal/25-10-01 DMM,
  formal/25-10-03 UAFML); normative machine-readable files dtc/24-11-06
  (`UAF.xml`) and dtc/24-11-07 (`MeasurementsLibrary.xml`), downloaded from
  omg.org/spec/UAF/20241101/ to `/mnt/TBFox/uml_xmi/UAF13.xml`
  (+ `MeasurementsLibrary13.xml`).

## Delta vs the 1.2 profile (UAF.xmi, dtc/22-12-01 era)

- +17 Mission-domain stereotypes: Mission, ActualMission,
  ActualMissionPhase, ActualMissionScenario, ActualMissionVignette,
  MissionEngineeringThread, MissionScenario, MissionTask, MissionTaskAction,
  MissionThread, MissionVignette, Doctrine, OpposableElement, Opposes,
  ConflictsWith, Defines, DesignationKind; -EnterpriseMission (no 1.2
  stereotype generalized it). Zero base-fold changes on shared stereotypes.
- 256 -> 272 stereotypes, 20 -> 21 enums (MissionKind new), 379 -> 402
  generalizations, 259 -> 269 constraints, 112 -> 118 non-base properties.
- New folds exercised: Mission(StrategicPhase, U.Class),
  ActualMission(U.InstanceSpecification), MissionThread(OperationalActivity,
  U.Activity), Doctrine(Standard, sysml.Requirement via href),
  ConflictsWith(sysml.Problem), Defines(sysml.Allocate),
  DesignationKind(sysml.ValueType), OpposableElement abstract over
  UAFElement with the `designation` tag.

## Dialect probes (1.3 vs 1.2)

- Same UML-XMI envelope dialect as 1.2 (xmi 20131001 / uml 20161101 /
  sysml 20181001 namespaces, xmi:id refs, href generalizations); the `cmof`
  namespace is declared but unused.
- Profile URI moves to `http://www.omg.org/spec/UAF/20241101/UAF`
  (1.2: `https://www.omg.org/spec/UAF/20211201/UAF`). Both files carry the
  profile *name* "UAF", so the emitted module is overridden to
  `gen/uaf13.py` via a PROFILES name override; the URI carries version
  identity.
- **NEW href form**: tagged values typed by SysML library datatypes, e.g.
  `SysML.xmi#SysML_dataType.String` (Capability.customKind,
  ValueItem.customKind, MotivationalElement.ID/Text,
  ResourcePerformer.isStandardConfiguration, OperationalExchange.trustLevel).
  The 1.2-era href parser read any dotted SysML fragment as a stereotype
  reference; `resolve_prop_type` now maps `SysML_dataType.<Prim>` to a
  primitive. The form does not occur in UAF.xmi, so regenerating 1.2 stays
  byte-identical (verified by `git diff`).

## Changes

- `generate_profiles.py`: PROFILES entries became (path, module-override)
  tuples; `emit_module` honors the override; SysML_dataType primitive hrefs.
- `gen/uaf13.py`: 272 stereotypes, 21 enums, 3,946 lines.
- `check_profiles.py`: +20 pinned checks (60 total).

## Result

- check_profiles.py: 60/60.
- Suites: 45 + 60 + 47 + 32 + 25 + 48 + 20 + 42 + 19 + 18 = **356
  checks**, all green.

## Honest notes

- `MeasurementsLibrary13.xml` is downloaded but not yet exercised; the
  XMI-writer parity corpus (check_xmi_write.py) still uses the 1.2-era
  MeasurementsLibrary.xmi. 1.3 stereotype *applications* writing is
  untested until an instance model in the 1.3 dialect is run through
  xmi_write.

# Part 16: mdzip.py - MagicDraw/Cameo project scrape + forensics

## Motivation

- GT work exposes a large corpus of .mdzip files; Cameo's own import scales
  poorly and discards provenance (which tool version produced the file,
  which projects the file uses). A from-scratch scrape can do better:
  pull the model out, fingerprint the version era, list the usages.

## Format findings (pinned by check_mdzip.py over the public corpus)

- A .mdzip is a plain ZIP. In every corpus file examined (2015-era
  MagicDraw through 2024x-era Cameo) **every member is XML text**:
  the `BINARY-<uuid>` members are diagram *presentation* XML
  (`mdOwnedViews`/`mdElement`, geometry + symbol styles), not Java
  serialization. Model data and presentation are cleanly separated.
- The model lives in one or more
  `proxy.local__PROJECT$…_resource_com$dnomagic$dmagicdraw$duml_umodel$…$dsnapshot`
  members: XMI 2.0 (`http://www.omg.org/XMI`), standard UML property
  names, under Nomagic's namespace
  `http://www.nomagic.com/magicdraw/UML/2.5` (2015-era) or
  `.../2.5.1.1` (2024-era). `alias_nomagic()` rewrites the declaration
  to the OMG `20161101` namespace so standard XMI tooling can consume it.
- Proxies/usages: `com.nomagic.ci.persistence.local.proxy.privatedependencylist`
  carries `originalResourceURI="local:/PROJECT-<id>?resource=…"`;
  `PROJECT-<id>` marker members exist for used projects. IDs appear
  both dashed (`b79be608-559e-430b-…`) and undashed 30-32-hex.
- Version fingerprints: element IDs embed the tool-era prefix —
  `_9_0_…` (MD 9.0), `_12_0_…`, `_16_8beta_…`, `_2021x_2_…` (Cameo
  2021x), `_2022x_…` — plus optional text hints in project options.
  A single file is a *stratigraphic record*: APE carries 9.0-through-2022x
  ID eras at once (the profile libraries predate the model content).
- Options blobs are base64-encoded ZIPs inside `optionsString`
  attributes (project + personal options); decoded and sniffed by
  extract_images.
- Hex-encoded SVG payloads (observed in GT corpus files) are handled by
  the same generic scan: any hex/base64 run ≥ threshold is decoded and
  magic-sniffed (svg/png/jpg/gif/gz/zip). The public corpus carries no
  hex-SVG, so the extractor's correctness there rests on the generic
  scan + the pinned base64-ZIP cases.

## Changes

- `mdzip.py`: MdZip (inventory / model_members / alias_nomagic /
  iter_model_elements / proxies / usages / project_description /
  version_clues / extract_images / info) + CLI
  (`members|info|usages|versions|images <outdir>`). std-lib only.
- `scripts/fetch_mdzip_corpus.sh`: provenance + re-download
  (Open-MBEE APE, Galois MPS, maas-warehouse). Corpus files are NOT
  committed; check_mdzip.py skips cleanly without them (MDZIP_CORPUS).
- `check_mdzip.py`: 28 checks pinned to corpus facts (member kinds,
  namespaces, APE element counts 4715/689/434/318/208, MPS 3 usages,
  ID-era fingerprints, base64-ZIP decode, manifest schema).

## Result

- check_mdzip.py: 28/28 (with corpus in /tmp/mdzip_probe).
- Suites: 45 + 60 + 47 + 32 + 28 + 25 + 48 + 20 + 42 + 19 + 18 = **384
  checks**, all green.

## Honest notes

- Coverage is *construction* coverage: named Classes/Packages/DataTypes
  come through with names and composition trees; feature coverage inside
  objects is partial (260 unmapped_features on APE, dominated by the
  profile layer: taggedValue 140, appliedStereotype 122).
- Name-typed references are recorded, not resolved (`names#` markers):
  458 on APE.  Resolving them against the merged model's named elements
  is the next increment, along with the profile layer itself.
- `Model` count includes synthetic roots; the reader's derived-name
  provenance record applies to unnamed elements only.
- Encrypted projects: MdZipImportError, by design.

# Part 18: profile layer - stereotypes, extensions, applications, tags

## Modeler addiction math (APE-ReferenceModel)

- With Profile/Stereotype/Extension/ExtensionEnd constructible and the
  Nomagic tagged-value forms harvested, APE jumps 422 -> 1536 objects
  (295 Stereotypes, 248 Extensions, 611 Properties on SAF_FFDS; APE
  244 Classes + 80 DataTypes + 83 Packages + 77 Stereotypes + 8 Profiles
  + 15 Profiles constructed).  Modelers really do add stereotypes to
  everything -- the profile layer is not an optional garnish.

## Nomagic profile-layer forms (pinned)

- Profile/Stereotype/Extension/ExtensionEnd are standard uml:X elements
  (now in CONSTRUCTIBLE) and construct through the reader unchanged.
- Applications: `<appliedStereotype href="#stereo-id"/>` children on the
  applied element (184 on APE) and an unprefixed attribute form.  Both
  are harvested into `imp.applications[base_id] = {"stereo", "tags"}`
  and REMOVED from the tree (the reader has no such feature on Element).
- Tagged values: Nomagic metaclasses `uml:{String,Boolean,Integer,
  Element}TaggedValue` whose xmi:id encodes the linkage
  `<application-id> 'application_' <tagDefinition-id>`, with
  `<tagDefinition href="#...">` (the defining Property) and `<value/>`.
  Harvested into `imp.tag_values[app][tag-name] = value` (values re-keyed
  after tag-definition names resolve) and removed from the tree
  (gen.uml25 has no such metaclasses).
- **Type-tagged nesting** (`<uml:Profile>` under a Package, AML): the
  containment feature is derived from the metamodel -- first composite
  descriptor of the parent whose type the child satisfies wins; the tag
  is renamed and xmi:type injected.  This fix alone unblocked AML
  (crash -> 154 objects) and lifted MPS 101 -> 791, APE +404, SAF_FFDS
  +1531: the type-tagged style is widespread, not an AML quirk.
- Names: stereotypes get name + owning profile; tag definitions get name
  + owner stereotype (via a parent map).  114/116 APE stereotypes named,
  owners: MagicDraw Profile / StandardProfile / SysML /
  additional_stereotypes.

## Result

- Stress set: 12/12; object totals APE 1536, SAF_FFDS 2157, MPS 791,
  AML 154, DELS 104.  `unmapped` fell to 0 on 10/12 (APE exactly 0).
- check_mdzip_import.py: 26 checks (was 18): stereotype/profile object
  construction pins, harvest-map pins (116 stereotypes/298 apps/6
  tagdefs on APE), tagdef name+owner, AML normalization.
- Suites: 45 + 60 + 47 + 32 + 28 + 26 + 25 + 48 + 20 + 42 + 19 + 18 +
  12(scratch) = **410 checks**, all green.

## Honest notes

- The application map records stereotype *references*; only 173/298 APE
  applications resolve to a stereotype defined inside the same file (the
  rest point into *used* projects -- resolvable once usage merging lands).
- Tag values with content are rare in the public corpus (4/221 on APE --
  the corpus is profile definitions, not applied models); the extractor's
  value handling is pinned on those 4 plus the definition defaults.
- The `holding_bin` package still swallows stray top-level Profiles; the
  reader's packageImport/profileApplication links are not yet reconciled
  with the harvested profile names.

# Part 19: mdzip_diff.py - semantic diff across id churn

## The problem (from GT experience)

- mdzip XML churns: every save reorders members, delta snapshots duplicate
  subtrees, TeamworkCloud rewrites every element's server id.  Byte/XML
  diffs are noise.  Diff must be semantic.

## Algorithm

- import both files with mdzip_import; flatten to records
  (metaclass, qualified path, feature dict) -- xmi:ids never enter the
  record (pinned by a check).
- match: (1) exact qualified path; (2) same metaclass+name with unique
  move; (3) same metaclass + same owner tail + Jaccard(feature pairs)
  >= threshold, greedy best-first; (3b) same metaclass + same NAME +
  similarity >= threshold regardless of owner (whole-package
  regeneration: openEHR AM->AM14 moves every owner chain);
- diff matched pairs feature-by-feature; report
  added/removed/renamed/moved/changed.

## Calibration over 18 real revision pairs (fetched from git history)

- **Noise immunity**: SAF "add an attribute" commit actually contains
  ZERO model change (the member CRCs differ only in diagram-view and
  options members) -- diff reads exactly zero; openEHR "non-semantic
  changes" pair: 49+48 raw churn collapses to 1 add + 230 identity
  repairs (whole-package regeneration matched semantically).
- **Change detection**: DLR "Add the ControlledProcessSTPA stereotype" =>
  exactly 3 added records (stereotype + base_Class + base_Property),
  0 removed; CEMT RC10->2022xR2 => 8 added, 1 removed.
- **Identity repair**: NIST "Renamed top-level container from DELS to
  Data" => 0 false adds, 11 moves matched incl. Model::DELS ->
  Model::Data.
- openEHR AM->AM14 regeneration: matched 271/272 across wholesale id
  and path churn.

## Reader changes made during diff calibration

- Pending resolution degrades instead of raising: dangling in-document
  idrefs are recorded (`unresolved_refs`) -- NIST carries genuinely stale
  refs to elements no longer in any member.
- xmi21 COMPOSITE += slot/generalization/ownedRule; REF_SINGLE +=
  owningPackage; CONSTRUCTIBLE += Signal (and profile layer metaclasses).
- Synthetic-marker assignment follows the descriptor's arity (some
  REF_SINGLE features like `general` are multi in the metamodel; a
  single marker set through a multi descriptor crashed -- SAF).
- **Both persistence styles merge**: some files carry snapshot members
  (project content) AND uml_model.model/shared_model members (profile
  libraries / new-style store) with near-disjoint id spaces (APE
  overlap 14 ids of 20000) -- superseding one style loses half the
  model; merging both + keep-last dedup lifted APE 1536 -> 9164 objects,
  SAF_FFDS 2384 -> 4539, MPS 418 -> 1207.  APE's uml_model.model member
  is a 9 KB stub; shared_model (9.5 MB) is the profile-library store.
- Dangling unprefixed `type=` attrs (stale ids, no `:`) and refs to
  non-constructible behavior-layer elements (uml:Activity ancestors)
  become recorded synthetic markers.

## Result

- check_mdzip_diff.py: 12 checks (noise immunity x2, change detection
  x4, identity repair x3, id-independence).
- Suites: 45 + 60 + 47 + 32 + 28 + 26 + 12 + 25 + 48 + 20 + 42 + 19 +
  18 = **422 checks**, all green.

## Honest notes

- Similarity matching is greedy (best-first, one-to-one); pathological
  cases (bulk renames of hundreds of same-metaclass same-name elements)
  could pair suboptimally -- acceptable for change tracking, revisit if
  GT corpus shows it.
- Feature extraction reads named scalar/reference features; structural
  children (e.g. nested classifiers) enter the qualpath, not the feature
  dict, so their changes surface as added/removed records rather than
  modified pairs.
- The andromda profile pair was mis-fetched initially (file renamed
  profile.mdzip -> profile2.mdzip in the same commit); the correct
  before/after pair (166 -> 172, 6 added) is now in _revisions.

# Part 17: mdzip_import.py - .mdzip -> gen.uml25 objects

## Architecture

- mdzip.py stays the scrape/forensics layer; mdzip_import.py consumes it
  and delegates to xmi21.read_xmi21 unchanged (one engine, two dialect
  front-ends).  The importer is a *normalization* pass:
  merged document -> retagged spellings -> injected/coerced types ->
  scrubbed refs -> reader.

## Dialect facts pinned (all found empirically over the corpus)

- **Delta snapshots**: members repeat xmi:ids across snapshots (APE: 811
  duplicated ids across 18 members; SAF_FFDS: 1707).  Keep-LAST is the
  correct semantics (later snapshots are the more-current form);
  keep-first loses updated subtrees and was the main object-count killer
  (180 -> 422 objects on APE after the flip).
- **Attribute spellings, two generations apart**:
  `xmi:id/idref/uuid/version` under `http://www.omg.org/XMI` (XMI 2.0)
  must be retagged to `http://www.omg.org/spec/XMI/20131001`; element
  typing is `xsi:type` (XML-Schema spelling) and must become `xmi:type`.
  Both retags are pure attribute rewrites.
- **Mixed tagging styles in one file**: top-level elements are
  type-tagged (`<uml:Package xmi:id=.../>` under xmi:XMI) while nested
  containment children are feature-tagged (`<packagedElement .../>`),
  and BOTH styles omit xmi:type on the root elements.  Member Package/
  Model roots go under the merged xmi:XMI directly (reader dispatches
  them); other top-level elements (uml:Profile) go under a synthetic
  holding_bin package.
- **Type inference without an ID map**: the raw metamodel IDs
  (`_9_0_2_91a0295_…`) resolve structurally -- rule 1 (parent-feature):
  the parent feature descriptor in gen.uml25 names the metaclass; rule 2
  (property-signature): MD's tag definitions have a fixed property shape.
  585 coercions on APE, 3 left over.  The speculative ID table from
  Part 16 is unnecessary -- the metamodel itself is the map.
- **Reference forms**: in-document `href="#id"` == xmi:idref (rewritten);
  dangling `#id` -> synthetic external marker; cross-project
  `local:/PROJECT-x?resource=...` and bare `PROJECT-x?resource=...` ->
  synthetic external markers (usages recorded separately); NAME-TYPED
  reference attributes (`type="uml:Property"` as a value, 458 on APE) ->
  synthetic `names#` markers (resolution = wave-2); idrefs to
  non-constructible profile-layer elements (Profile/Stereotype/
  Extension/tag metaclasses) -> synthetic `profile-layer#` markers.
  Nothing raises on the wave-2 boundary; everything is recorded.
- **xmi21.py table extensions** (spec-standard features the DoDAF corpus
  never exercised): COMPOSITE += slot/generalization/ownedRule;
  REF_SINGLE += owningPackage; CONSTRUCTIBLE += PrimitiveType,
  AssociationClass.  check_dodaf.py 32/32 still green after the change.

## Result (12-file stress set, 2015-era .. 2024x-era)

- APE 422 objects (244 Class, 80 DataType, 64 Package, 15
  InstanceSpecification), 18 roots, 585 coercions, 811 dedups, 16 usages.
- SAF_FFDS 223 objects incl. AssociationClass; MPS 16; maas 8;
  INGRID Nerdman 11; NIEM.Guide 17; AML 23; DELS 40.  **12/12 import
  without error**, 0 corpus files needed hand-holding.
- check_mdzip_import.py: 18 checks (counts, dedup semantics, provenance
  carry-through, wave-2 recording, name sanity).
- Suites: 45 + 60 + 47 + 32 + 28 + 18 + 25 + 48 + 20 + 42 + 19 + 18 =
  **402 checks**, all green.

## Honest notes

- Coverage is *construction* coverage: named Classes/Packages/DataTypes
  come through with names and composition trees; feature coverage inside
  objects is partial (260 unmapped_features on APE, dominated by the
  profile layer: taggedValue 140, appliedStereotype 122).
- Name-typed references are recorded, not resolved (`names#` markers):
  458 on APE.  Resolving them against the merged model's named elements
  is the next increment, along with the profile layer itself.
- `Model` count includes synthetic roots; the reader's derived-name
  provenance record applies to unnamed elements only.
- Encrypted projects: MdZipImportError, by design.

# Part 20: R1+R2+R3 conformance chain - gen/sysml2 runtime + v1_to_v2_as.py

The transformation-conformance clause (§2 of ptc/2025-04-07) names three
artifacts: read a v1 model representation (R1), have a v2 abstract-syntax
representation (R2), and transform the first into the second (R3). This
part closes the chain end to end.

## R2 - gen/sysml2.py runtime additions

The generated module (from the OMG normative CMOF XMI, Part 18-era commit)
gained the runtime surface the transformer needs, in both gen/sysml2.py and
generate_sysml2.py (idempotence verified: regeneration is byte-identical):

- `_MemberAlias` descriptor: KerML redefinition aliases
  (Membership/OwningMembership/FeatureMembership `.memberElement`,
  FeatureMembership `.ownedMemberFeature`) reading/writing the storage end
  `Relationship.ownedRelatedElement` through the redefining name
  (KerML §7.3.1.3).
- `Type.feature` / `Classifier.feature`: computed property - the features
  directly featured by the type, i.e. the memberElements of owned
  FeatureMemberships (§7.4.1.2; the CMOF XMI end is a derived union with
  no storage).

check_sysml2.py grew the derived-union reads (26 checks, green).

## R3 - v1_to_v2_as.py (wave A)

Same normative mappings as the validated textual emitter (v1_to_v2.py),
but constructing gen.sysml2 objects. Architecture:

- **Index identity (the conformance-critical rule)**: one v1 element maps
  to exactly ONE AS object; pass 1 builds definitions, pass 2 features/
  nested members, pass 3 generalizations. Every FeatureTyping.type and
  Subclassification.general references the indexed object - usages never
  copy their type's definition.
- Ownership via OwningMembership (package members, nested classifiers,
  documentation); features via FeatureMembership (making the definition
  the featuringType); typing via FeatureTyping owned by the feature
  (ownedTyping back-wires owningFeature/typedFeature).
- Wave-A mappings: Block→PartDefinition (7.8.4.3.3), composite block-typed
  Property→PartUsage (7.8.4.3.13), non-composite→PartUsage isComposite=
  false ('ref part'), ValueType/plain DataType→AttributeDefinition
  (7.8.4.3.14), Enumeration→EnumerationDefinition with literals as
  EnumerationUsage features, ConstraintBlock→ConstraintDefinition
  (7.8.5.3.1), plain Class→OccurrenceDefinition + Class-typed Property→
  (ref) OccurrenceUsage (7.7.4.2.37), Actor→PartDefinition (7.7.13.3.1),
  Generalization→Subclassification (7.7.4.2.12), Comment→Documentation
  (7.4.2.1.9 ToDocumentation_Init) with an explicit Annotation
  relationship, untyped Property→Feature.
- `transform_xmi(path)`: R1→R2→R3 entry - xmi21.read_xmi21 feeds the
  transformer; roots must carry xmi:type (UML-20090901 dialect rule).

## Dialect facts pinned

- The v1 runtime's redefines/subsets are metadata, NOT storage aliases:
  writing FeatureTyping.type stores under 'type'; 'general'/'specific'
  stay empty. Conformance checks therefore read the redefining ends.
- Documentation owned via OwningMembership has owner = the membership
  (this runtime's KerML chain), and Annotation's derived back-ends
  (annotatingElement, ownedAnnotation) cannot be populated - the
  Annotation relationship itself is carried on the Documentation. Both
  documented, both check-visible.
- The UML-20090901 reader does not deserialize the `<aggregation>` child
  (recorded in unmapped_features), so an XMI-fed composite Property
  transforms referential rather than silently composite - recorded, never
  lost.
- Metaclasses with their own normative mappings (Behavior/StateMachine,
  UseCase, Signal, InformationItem, Interface, TestCase, Requirement,
  InterfaceBlock) are excluded from the plain-Class catch-all and raise
  UnmappedFeature (later waves) instead of mapping to OccurrenceDefinition.

## Honest elisions

- Multiplicities: v1 upperValue/lowerValue have no settable AS end
  (MultiplicityRange bounds are derived unions; no
  FeatureMultiplicityMembership storage in the runtime). The textual
  pipeline carries them; the AS wave does not yet.
- Annotation derived back-ends (above).
- Everything the textual emitter elides/annotates (ProxyPort, imports,
  interactions) is unchanged AS-side: UnmappedFeature.

## Result

- check_v1_to_v2_as.py: 50 checks - R1 leg (hand-written v1 XMI 2.1 →
  xmi21 → transform → AS graph, 8), R3 wave-A mappings (17), R2 runtime
  wiring over the transformed graph (5), **parity with the validated
  textual pipeline** (the AS graph renders, via an independent minimal
  renderer in the check, to byte-identical notation vs v1_to_v2.py for
  the same model), wave-B/C/D oracles (17), honesty (3).
- Suites: 45 (UML) + 60 (profiles) + 47 (textual v1→v2, sysmlpy-fed) +
  26 (sysml2) + 50 (AS transformer) + 19 (OCL) + 18 (EMOF) = **265
  checks green this session**; corpus suites (DoDAF, mdzip, query,
  xmi/cmof write) verified environment-blocked: /mnt/TBFox mount absent
  (identical failure with changes stashed — pre-existing condition).

## Conformance statement (§2 of ptc/2025-04-07) - final

The clause defines three requirements. Full conformance = R1 + R2 + R3;
"software developed only partially matching the applicable compliance
points may claim only that the software was developed based on this
specification" unless every R is met.

**R1 - SysML v1 abstract syntax: MET (in substance).**
gen/uml25.py (242 metaclasses, 620 properties, 449 normative OCL bodies
carried as metadata) from the OMG UML 2.5.1 XMI, plus gen/sysml.py
(SysML v1 profile, 56 stereotypes as Python mixin classes — a stereotype
application IS the fold-in), gen/uaf.py, gen/uaf13.py, gen/bpmn.py.
R1's "should import XMI" is satisfied by xmi21.py (XMI 2.1 instance
dialect) and mdzip_import.py (MagicDraw .mdzip), both validated over
real OMG-published/vendor corpora. Evidence: check.py 45, check_profiles
60, check_dodaf 32 (corpus), check_mdzip_import 12-file stress set
(corpus).

**R2 - SysML v2 abstract syntax: MET.**
gen/sysml2.py is generated from the OMG normative artifacts the clause
names: SysML.xmi (ptc/25-02-15, "MOF XMI for the SysML v2 Abstract
Syntax") + KerML.xmi (20250201). 175 metaclasses (82 KerML + 93 SysML
v2), 428 properties, 7 enums, 623 normative constraints; stdlib-only,
same _Ref/_RefList descriptor runtime as gen/uml25.py. Cross-file href
resolution verified 175/175 (id-suffix rule + attr-id map + last-dash
fallback). Evidence: check_sysml2.py 26 (MRO PartDefinition→…
→Element, abstract guards, OwningMembership/FeatureTyping/
Subclassification wiring, owner back-wire).

**R3 - v1 AS → v2 AS transformation: MET for an identified subset.**
v1_to_v2_as.py constructs gen.sysml2 objects from gen.uml25+gen.sysml
objects, with the conformance-critical identity rule (one v1 element →
one AS object; every typing/specialization end references the indexed
object). All 78 normative To*_Init helpers carry an identified
realization (wiring / defaults / elided — table embedded in source).
Mapping coverage:

| Family | Mappings | Anchors (ptc/2025-04-07) |
|---|---|---|
| structural | Block, Property, ValueType, Enumeration, ConstraintBlock, plain Class, Actor, Signal/InformationItem | 7.8.4.3.3/.13/.14, 7.8.5.3.1, 7.7.4.2.37, 7.7.13.3.1, 7.7.7.3.x |
| behavioral | StateMachine/State/Transition (regions inlined, initial elided SYSML2_-203), Activity internals, Operations, Connectors | 7.7.11.2.x, 7.7.3.3.x, 7.7.4.2.23/.24, 7.7.12.2.14 |
| requirements chain | Requirement, TestCase, Satisfy, Verify, DeriveReqt, Dependency, Allocate | 7.8.8.3.30/.27/.44/.49/.15, 7.7.6.2.9, 7.8.3.3.9/.10 |
| feature plumbing | subsets/redefines/defaultValue, FeatureValue + FeatureReferenceExpression, Subsetting/Redefinition/ReferenceSubsetting | 7.7.4.2.36, 7.7.4.2.16 |
| ports | Port→PortUsage typed by InterfaceBlock's definition | 7.7.12.2.36/.37, 7.8.7.3.16 |

Per §2's mapping-dependency caveat, the claim is scoped: "the
transformation as identified in this implementation's realization table;
unimplemented mappings raise UnmappedFeature naming the v1 metaclass."

**Identified elisions** (all shared with the validated textual emitter,
each with its normative anchor): imports (7.7.9.3.12 — reader gap),
ProxyPort (Table 30 lists no target; SYSML2_-329), interaction
machinery (7.7.8.x — grammar gap), Table-11 interaction elements
(7.7.8.2), via-port receiver machinery (7.7.2.3.1.17-.19),
StateInvariant (7.7.8.3.17), conjugation machinery (ToConjugation
family), multiplicity bounds in AS (derived unions; the textual
pipeline carries them), AssignmentActionUsage/CalculationUsage AS
carriers.

**Honest deviations** (documented, check-visible): 23 derived ends
emitted writable in gen/sysml2.py (the KerML AS carries them as derived
unions; construction needs the carrier — WRITABLE_DERIVED in
generate_sysml2.py); ownedElement computed over the membership chain
(§7.3.2.3); Annotation derived back-ends runtime-elided.

**Reproduce:**
```
python3 check.py && python3 check_profiles.py && \
python3 check_sysml2.py && .venv/bin/python check_v1_to_v2_as.py
# textual pipeline needs sysmlpy on the path:
HOME=<repo-parent> PYTHONPATH=<sysmlpy-venv-site-packages> \
  .venv/bin/python check_v1_to_v2.py
```

## Conformance posture

This software was developed based on the OMG "SysML v2.0 Beta 4, Part 2:
SysML v1 to SysML v2 Transformation" (ptc/2025-04-07) and satisfies its
§2 requirements R1 and R2, and R3 for the identified mapping subset
above. No conformance certification is claimed or implied.
