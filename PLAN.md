# PLAN — XMI/CMOF/EMOF exporters, stereotype writing, derived-union eval, query helpers

Waves E1–E6. Companion to REPORT.md (Parts 1–8 = completed work); each wave
lands as one commit with its check suite green, then gets a REPORT part.

## Goal

Close the write-path and QoL gaps identified in the OpenAPI-coverage survey:

1. **E1** EMF-dialect XMI 2.1 **instance writer** (`xmi_write.py`) — the write
   half of what `xmi21.py` reads; round-trip oracle against OMG-published
   instance corpora.
2. **E2** **Stereotype-application + profile-application writing** (extends
   `xmi_write.py`), incl. the reader extension needed to parse
   MeasurementsLibrary.xmi (prefixed UAF applications).
3. **E3** **Spec-normative derived properties and derived-union evaluation**
   (`derived.py`) — implement the tractable OCL derivations from UML 2.5.1;
   UnmappedFeature-elide the rest with anchors.
4. **E4** **Query helpers** (`query.py`) — walk/find/exists over loaded
   instance graphs; qualified names via E3.
5. **E5** **CMOF writer** (`mm_write.py`, CMOF mode) — BPMN20.cmof round-trip
   parity (parse → gen.bpmn → write → canonical-compare vs original).
6. **E6** **EMOF writer** (`mm_write.py`, EMOF mode) — verification-grade
   round-trip of a small package.

### Non-goals

- Full OCL engine (only tractable normative derivations; the rest elided).
- EMF EPackage/ecore-style *metamodel* writer (Eclipse-ecosystem-specific;
  CMOF/EMOF are the OMG-normative metamodel interchange).
- Diagram/DI writing; Teamwork/DataHub/simulation; byte-parity as a gate
  (structural parity is the gate; byte parity is a documented stretch goal,
  as in pyusm2idl).
- Profile-as-CMOF export (profiles are Extensions-based, not Associations).

## Current state (verified in code)

- `gen/uml25.py:280` `_union(name)` already aggregates **stored** subset
  values; `_Ref.__set__` stores per-property in `_vals` (redefines are
  metadata, not storage aliases), and the settable-guard (line 151) blocks
  derived/union/readonly writes — so `_vals` is exactly the writable surface
  a writer should emit.
- `xmi21.py` (257 lines, reader-only): `XMI21Model.apps` maps base xmi:id →
  `[(profile, stereo, app_id)]`; `Element._applied_stereotypes` carries the
  resolved list; `appliedProfile` hrefs are parsed. Applications are
  root-level non-metamodel elements (UML 2.1-style unprefixed dialect).
- `gen/{standard_profile,sysml,uaf}.py` carry **no profile `uri`** metadata —
  required for E2 application namespaces.
- `gen/bpmn.py` loses the parse-time `synthesized` flag (only a source
  comment survives) — required for E5 to know which class-attrs were
  association-owned ends.
- Writers will use lxml (~/ams-gra-sim/.venv); runtime modules
  (`derived.py`, `query.py`, `canon.py`) stay stdlib-only.

## Corpus & normative sources

Repo stays OMG-corpus-clean; spec texts live locally (gitignored, like
transition.txt), downloaded to `/mnt/TBFox/` or `~/uml2py/*.txt`:

- **Instance corpora** (already on disk): `/mnt/TBFox/DoDAFLibrary.xmi`,
  `/mnt/TBFox/uml_xmi/MeasurementsLibrary.xmi` (UAF applications),
  metamodel refs `UML.xmi`, `PrimitiveTypes.xmi`, `sysml.xmi`, `UAF.xmi`.
- **CMOF corpus**: `/mnt/TBFox/uml_xmi/BPMN20.cmof` (+ DC/DI/BPMNDI.cmof as
  external-href cases).
- **To fetch (normative prose)**:
  - UML 2.5.1 spec (formal/2017-12-05) — OCL for Element/NamedElement/
    Namespace/Classifier derivations (E3 anchors).
  - MOF 2.0/XMI Mapping spec v2.1 (formal/05-07-04) — EMOF/CMOF XML
    mappings, primitive hrefs, Tag/Constraint elements (E5/E6).
  - XMI 2.1 spec (formal/03-05-02) — xmi:id/href semantics (reference only).

## Shared tool: `canon.py`

Canonical structural comparison used by all exporter suites: parse two XML
docs → sort attributes, drop comments/PIs, resolve every idref to a
canonical containment path (so xmi:id values are ignored), normalize
whitespace, apply per-dialect absent-attr == default rules → compare trees.
Reports first divergence with path. This is the exporter analogue of the
pyface black-box parity discipline.

## Dialect decisions to pin (probe before implementing)

| # | Question | Resolve by |
|---|----------|------------|
| P1 | Non-containment many-refs: single attribute with space-separated idrefs vs repeated elements | Probe DoDAFLibrary.xmi |
| P2 | Enum serialization: literal name vs member value (verify `value == name` in generated enums) | Probe + grep gen/uml25 enums |
| P3 | Redefined-alias duplication: if a redefining prop and its target both store the same value, emit both or dedupe? | Probe DoDAFLibrary.xmi occurrences; default: emit stored, let canon decide, document |
| P4 | Required extensions: does the original file auto-emit applications for required-extension stereotypes? | Count apps in DoDAF/ML vs `_EXTENSIONS` required flags |
| P5 | Profile-application recording form (appliedProfile serialization observed by xmi21) | Mirror DoDAFLibrary.xmi exactly |
| P6 | Namespace URIs: default OMG `http://www.omg.org/spec/UML/20131001` + `.../XMI/20131001`; writer flag for eclipse-uml2 URIs | Fixed; reader is dialect-tolerant |
| P7 | xmi:id scheme: deterministic `_N` in traversal order (diffable round-trips; canon ignores ids) | Fixed |
| P8 | CMOF absent-vs-default multiplicity attrs (omit upper when 1, omit lower when 0-or-1 by convention) | Probe BPMN20.cmof; mirror source convention |
| P9 | EMOF association handling (no cmof:Association; how are opposites represented — two independent props vs `opposite` attr) | Extract from MOF 2.0/XMI spec text |
| P10 | MeasurementsLibrary prefixed-application dialect (element names, xmi:type placement, namespaces) | Probe ML |

## Waves

### E1 — EMF instance XMI writer (`xmi_write.py` + `canon.py`)

- `write(root, uri=UML_20131001, xmi_uri=XMI_20131001) -> bytes/str`.
- Traversal: DFS from root over composite `_props` in `_DECL` order;
  deterministic ids (P7).
- Emission: containment = feature-named nested elements (composite=True);
  non-containment = idref attribute(s) (P1); primitives = attributes
  (bool `true`/`false`, int, quoted str) (P2); enums = literal form (P2);
  derived/union/readonly never emitted (they are not stored); empty
  collections omitted; redefined-alias handling per P3.
- Oracle: read(DoDAFLibrary.xmi) → write → read → graph-compare
  (applications excluded until E2); plus canon-compare written file vs
  original (modulo ids, per dialect table). Every non-round-tripping
  feature gets an UnmappedFeature note with anchor.
- `check_xmi_write.py`: ~18–25 checks (round-trips, id determinism,
  canon idempotence, dialect conventions).

### E2 — Stereotype & profile application writing (in `xmi_write.py`)

- Generator change: `generate_profiles.py` parses each profile Package's
  `uri` and emits `_URI` into `gen/{standard_profile,sysml,uaf}.py`;
  regenerate; suites must stay green (one-time output change; idempotence
  rule still holds for unchanged inputs).
- Reader change: extend `xmi21.py` for the ML prefixed-application dialect
  (P10); MeasurementsLibrary.xmi must parse with applications.
- Writer: applications as root-level children in the stereotype's profile
  namespace, `base_<Meta>` properties from `_EXTENSIONS` (most-general
  extended metaclass wins when a stereotype folds several), tagged values
  as application attributes; profile-application recording per P5;
  required-extension behavior per P4.
- Cross-profile note: UAF stereotypes extending SysML stereotypes emit one
  application element with the UAF URI (matches EMF practice); verify vs ML.
- Oracle: read(ML) → write → canon-compare vs original (applications
  included); same for DoDAF. `check_xmi_write.py` += ~12–18 checks.

### E3 — Derived properties & union evaluation (`derived.py`)

- Fetch UML 2.5.1 text; extract OCL; implement tractable normative
  derivations as free functions over `gen.uml25` objects (generated modules
  stay byte-frozen):
  - `owner`, `all_owned_elements`, `must_be_owned`
  - `qualified_name` (namespace chain, `::` separator, spec special cases)
  - `all_namespaces`, `get_names_of_member` (if tractable)
  - `parents` / `all_parents` (generalization walk)
- Union evaluation: `union(el, name)` — reuse `_union` aggregation, then
  add contributions of subset props that are themselves derived unions
  (recursive, cycle-guarded); redefinition-aware subset closure.
- Honest elisions: derivations needing a real OCL engine (iterate/let/
  intersections) → UnmappedFeature notes with spec anchors in REPORT.
- `check_derived.py` (stdlib-only, ams-gra-sim venv): normative examples +
  constructed graphs; ~12–20 checks.

### E4 — Query helpers (`query.py`)

- API sketch (stdlib-only, operates on `gen.uml25` objects):

  ```python
  walk(root)            # DFS over composite containment, yields Elements
  find(root, metaclass=None, stereotype=None, name=None,
       qualified=None, pred=None, deep=True)   -> list
  of_type(root, cls)    # class object or metaclass name string
  stereotypes(el)       # resolved labels ("Profile::Pkg::Name" from _STEREO)
  exists(...), count(...)
  ```

- `qualified` uses E3 `qualified_name`; `metaclass` accepts a generated
  class or name string (isinstance over MRO); `stereotype` accepts label
  or (profile, name).
- `check_query.py`: dogshow/wave graphs + DoDAF library graph; ~10–15 checks.

### E5 — CMOF writer (`mm_write.py`, CMOF mode)

- Generator change: `generate_bpmn.py` emits a `_SYNTH = {"Partner": ("backRef", ...)}` table (association-owned ends recovered from the parse-time
  `synthesized` flags); regenerate `gen/bpmn.py`; `check_bpmn.py` green.
- Writer reconstructs `cmof:Package` per the BPMN20.cmof dialect: classes
  with `superClass` attrs, `ownedAttribute` with full multiplicity
  (P8 absent-vs-default mirroring), enums with `ownedLiteral`, href
  primitives (`cmof.xml#String` etc.), synthesized ends back as
  association-owned `ownedEnd` + `memberEnd` name-pairs, deterministic
  `A_*` association ids; external BPMNDI href preserved.
- Oracle: parse(BPMN20.cmof) → gen.bpmn → write → canon-compare vs
  original. Gate: structural parity; stretch: byte parity (documented, not
  gating). `check_cmof_write.py`: ~15–20 checks.

### E6 — EMOF writer (`mm_write.py`, EMOF mode)

- Pin EMOF conventions from MOF 2.0/XMI text (P9): `emof.xml` namespace,
  primitive hrefs, Property serialization, absence of Associations.
- Target: round-trip a small OMG-normative package (trimmed BPMN subset or
  a package constructed from the spec's own example); verification-grade,
  clearly labeled. `check_emof_write.py`: ~8–12 checks.

## Sequencing & conventions

- Order: E1 → E2 → E5 → E3 → E4 → E6 (E5 only needs the small `_SYNTH`
  generator change and slots naturally after the instance writer; E3/E4 are
  writer-independent and can be pulled earlier if a writer dialect stalls).
- One wave = one commit; all five existing suites (189 checks) green before
  each commit; REPORT.md part per wave; README rows updated.
- Suite projection: 189 → ~250–270 across six new/extended suites.
- Repo hygiene: spec texts and any new OMG downloads stay local
  (gitignored); no No Magic-derived text ever enters the repo (OpenAPI
  javadoc used only as a behavioral checklist, per the coverage survey).