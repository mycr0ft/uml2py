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
