# The Semantic Content Hash for MagicDraw/Cameo Projects

**Design and rationale — uml2py `mdzip_diff.model_hash()`**

Jon R. Fox (github.com/mycr0ft) · September 2026 · MIT

---

## 1. The problem: no version, no identity, no diff

A `.mdzip` file has three properties that defeat every conventional
versioning mechanism:

1. **No in-file version.** There is no version number, no content
   digest, no build id anywhere in the archive. Two files that differ
   only by a re-save look identical to `unzip -l`; two files that differ
   by a thousand moved elements look different to `diff` but not at all
   to a human.

2. **Wholesale identity churn.** Every element carries an `xmi:id`, and
   every save is free to change them: Cameo's delta-snapshot persistence
   re-emits subtrees, TeamworkCloud assigns fresh server IDs to every
   element on check-in, and profile libraries embed IDs inherited from
   whichever MagicDraw release produced them (a single file can carry
   ID eras from 2004 to today — our corpus shows 47 distinct eras in
   one file). Any scheme keyed on IDs — which is exactly what XML diff,
   XSLT-based differencing, and Teamwork Cloud's own history all do —
   tracks the *serialization*, not the *model*.

3. **Order without meaning.** Members of the ZIP, elements within a
   member, and features within an element are all serialized in
   tool-internal order that changes between saves without semantic
   meaning. A byte-identical model can serialize two different ways.

The result is dependency hell with no exit: you cannot tell whether the
`SafetyProfile.mdzip` you depend on changed when it was "updated" last
Tuesday, and you cannot number your own releases by content.

**Claim of this document:** a reliable *semantic content hash* is
computable from any .mdzip, is stable under re-save and tool upgrades,
and changes if and only if the model's meaning changes. It is the
missing version number — computable, not declared.

## 2. What "semantic content" means

The hash deliberately covers a precise slice of reality:

**Included (the model's meaning):**
- every named model element, identified by *metaclass + qualified path*
  (`Package::Subsystem::Sensor::temperature`);
- every scalar feature that affects interpretation: name, visibility,
  multiplicity bounds, aggregation, isAbstract, isDerived, default
  values, and similar;
- every reference feature, resolved to the *target's qualified path*
  (so "this Property's type is `ScalarValues::Real`" is content, while
  "this Property's type points at xmi:id `_17_0_4_…`" is not);
- the profile layer, treated as first-class: Stereotypes and Profiles
  are elements with paths; their tag definitions are Properties.

**Excluded (the serialization's accidents):**
- all `xmi:id` / `xmi:uuid` / server IDs;
- ZIP member order and membership (delta snapshots, BINARY-*
  presentation blobs, options payloads);
- element order within a package (lines are sorted before hashing);
- diagram presentation (`BINARY-*` members are drawing instructions,
  not model);
- tool version fingerprints (ID-era prefixes — recorded as *provenance
  metadata*, deliberately not hashed).

The exclusion list is not a limitation; it is the point. Two files with
equal hashes are interchangeable as *models* even if their bytes differ
completely — which is exactly the property Teamwork Cloud cannot give
you and git cannot give you.

## 3. Construction

The hash is built on the same normalization pipeline as the importer
(`mdzip_import`), because the only way to diff or hash mdzips reliably
is to first *understand* them:

```
.mdzip (both persistence styles, delta snapshots, dialect spellings)
  → mdzip.py scrape            (member selection, namespace aliasing)
  → mdzip_import               (type coercion, ref scrubbing, profile
                                harvest, keep-last dedup)
  → gen.uml25 objects          (one in-memory model)
  → records: (metaclass, qualified path, feature dict)
       · reference features resolved to qualified paths
       · xmi:ids dropped entirely
  → one line per element:
        metaclass ␟ qualpath ␟ feature=value ␟ ...
       (features sorted, lines sorted, SHA-256 over the stream)
```

Key decisions, each with a reason:

- **Qualified path as identity.** Names within a namespace are what
  modelers actually control. The path is stable across tool upgrades,
  survives TeamworkCloud (which preserves names but not IDs), and is
  what every model diagram displays.
- **References become paths, not IDs.** `type` on a Property hashes as
  the target's path. Otherwise a save-order change in the target's
  serialization would not register, while a genuine retarget would be
  invisible.
- **Sort everything.** Element lines and features are sorted before
  hashing. Any serialization order — member order, snapshot delta
  order, attribute order — becomes irrelevant by construction.
- **Scalar-only similarity, path-aware hashing.** Identity matching
  (the diff's pairing stage) deliberately ignores path-valued and
  name-valued features, because those change on move/rename while the
  element stays the same. The hash is the opposite: it *includes*
  everything, because the hash answers "did anything change?", not
  "which element is which?".

## 4. What the hash guarantees

Each guarantee is pinned by a check in `check_mdzip_diff.py` against
real before/after revision pairs fetched from public git history.

| Guarantee | Evidence (public corpus) |
|---|---|
| **Re-save invariance** — save twice, hash once | SAF-Cameo-Profile SCM profile: commit fc25ce→fdb39c differs only in diagram/options members; hash is bit-identical |
| **Tool-upgrade invariance for unchanged models** | stuartfowler CEMT Cyber_Profile a7aba7→323ec4 ("2022xR2" → "2024x"): profile models unchanged → zero semantic delta reported |
| **Regeneration invariance** | openEHR AM→AM14 regeneration: 49+48 raw churn collapses to 1 add + 230 identity repairs; hash moves only for the genuinely changed element |
| **Change detection** | DLR "Add the ControlledProcessSTPA stereotype": hash differs; the diff reports exactly stereotype + base_Class + base_Property |
| **Rename ≠ change of identity** | NIST "Renamed top-level container DELS → Data": 0 false adds, 11 elements re-matched, hash changes (the name is content) |
| **Determinism** | Same file hashed twice → same digest (pinned) |

In other words: **equal hash ⇒ interchangeable models; different hash ⇒
the diff explains exactly why.** The hash is the summary; `mdzip_diff`
is the receipt.

## 5. Operational uses (the point of the exercise)

1. **In-file version stamp.** The hash belongs in the release record of
   every model artifact: `SensorModel.mdzip  sha256:9c4f…  built 2026-09-19`.
   It is computable from the file alone, needs no tool cooperation, and
   answers "did the content change?" for the cost of one import.

2. **Dependency pinning (dependency hell, mitigated).** Today a usage
   reference is `local:/PROJECT-<opaque-id>?resource=…` — no version,
   no content identity. With the hash, a dependent project can pin
   `shared_libs.mdzip@sha256:…`, and any consumer can *verify* the pin
   offline. A mismatch is a red flag before opening the model, not a
   surprise after an hour of diagram archaeology.

3. **Change tracking without Teamwork Cloud.** Two saves of the same
   project (e.g. attached to a ticket, mailed by a colleague, checked
   into git as opaque binaries) become comparable. CI can refuse a
   model PR whose hash moved without a changelog entry — the same gate
   source code has had for decades.

4. **Provenance alongside the hash.** The pipeline already extracts
   version-era fingerprints (ID prefixes → 47 tool eras) and the
   project-usage list. A release record should carry:
   `content-hash, tool-eras, usages, element-count` — all computable,
   all currently absent from the format.

5. **Baseline for the GTRI bug reports.** "No in-file versioning for
   dependency" stops being an opinion and becomes a demonstration: here
   is the hash, here is the diff, here are two files that Cameo will
   happily open but cannot itself distinguish.

## 6. Failure modes and honest limits

- **Anonymous elements.** Unnamed elements are labeled by a
  serialization-derived placeholder in the qualified path. Where a
  modeler relies on anonymous parts (occasional in generated models),
  reordering them can move the hash without semantic meaning. Named
  elements — the overwhelming majority, and the ones in requirements —
  are immune.
- **Comment/diagram content is not hashed.** A "documentation-only"
  change (ownedComment) is invisible to the hash. That is deliberate
  (comments churn constantly and carry no formal semantics), but it
  should be stated in any workflow that relies on the stamp.
- **Deliberately excluded features.** `appliedStereotype` and
  `taggedValue` features are harvested into the importer's application
  maps but are excluded from the current hash input; stereotype
  *definitions* (the Profile/Stereotype elements themselves) are
  included. Extending the hash to include applied-stereotype links is a
  one-line change to `FEATURE_SKIP` once the GT corpus lets us verify
  the encoding at scale.
- **Not a semantic three-way merge.** The hash and diff detect
  divergence; they do not reconcile it. Merging mdzips remains Cameo's
  job until the usage-merging increment lands.
- **Collisions.** SHA-256 makes cryptographic collision a non-issue;
  the realistic hazard is *semantic* collision — two different models
  with equal qualified paths and features. The path discipline makes
  this no more likely than two files with equal content lines.

## 7. Implementation notes

- `model_hash(records)` lives in `mdzip_diff.py`, ~20 lines, stdlib.
- The line format (`metaclass ␟ qualpath ␟ feat=value…`) is
  deliberately stable: hashes computed by this version of the tool
  remain comparable to hashes computed later, as long as the line
  format does not change. If it must change, bump a `v1`/`v2` prefix
  into the digest input.
- Cost: dominated by import (seconds for 100 MB models); hashing
  itself is linear and negligible.
- The same record stream feeds the diff, the hash, and (next
  increment) the SysML v2 emitter — one normalization, three products.

## 8. Where this goes next

1. **`mdzip stamp` CLI**: hash + era fingerprint + usages, one line,
   for scripts and CI.
2. **Usage-merging increment**: when Distro A files arrive, the hash
   extends to per-usage sub-hashes — a dependency manifest for the
   project, hashed per referenced project.
3. **The webinar demo**: two saves of the same Cameo project, one
   meaningful edit — byte diff = 3,000 lines of noise; `mdzip_diff` =
   3 lines of truth; hash = one changed character. That is the entire
   argument for treating models as code.