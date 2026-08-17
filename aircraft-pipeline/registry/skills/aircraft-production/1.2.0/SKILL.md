---
name: psar-aircraft-production
description: Research, build, validate, publish, and safely upgrade World War II aircraft packages for the Progressive Semantic Aircraft Rig production-line system.
version: 1.2.0
---

# PSAR Aircraft Production

Use this skill for a new aircraft, an aircraft-system revision, a production stage, a progressive semantic rig, an engine lifecycle, effects, materials, source research, or an online registry release.

## Mandatory start and resume procedure

1. Read the selected aircraft catalog entry and active channel manifest.
2. Load the last verified package report and unresolved uncertainty register.
3. Inspect the source GLB inventory before changing semantic mappings.
4. Confirm the target family, variant, individual airframe, and visual restoration identity remain separated.
5. Record the exact package, application, dependency, and skill versions used for the work.
6. Continue from machine-readable project state. Do not reconstruct progress from conversation memory alone.

## Universal aircraft contract

1. Keep one shared fixed-wing runtime. Place aircraft-specific values in a versioned profile.
2. Use projected screen size to reveal semantic structure. Do not switch the aircraft mesh through traditional mesh LODs.
3. Create every semantic joint once when the aircraft package loads. Visibility and update frequency may vary by reveal level.
4. Give every aircraft an airframe, flight-control, propulsion, landing-gear, electrical, fuel, and lifecycle system. Optional payload and defensive systems remain explicit capabilities.
5. Treat every engine as an independent state machine with starting, cold idle, warm idle, run-up, takeoff, climb, cruise, descent, shutdown, windmilling, feathered, failed, and fire states where applicable.
6. Bind smoke, heat distortion, fluid, fire, light, and sound emitters to semantic anchors on the affected engine or compartment.
7. Preserve parked, prestart, engine start, warm-up, taxi, run-up, takeoff, climb, cruise, descent, approach, landing, taxi-in, shutdown, and hot-parked domains.
8. Store production stages as data with stable identifiers, dependencies, evidence, and inspection gates.
9. Use OpenPBR-compatible material data and preserve supported glTF 2.0 KHR extensions.
10. Keep one immutable source-model identity. Store each published package under an immutable version path with byte count and SHA-256.

## Source and uncertainty rules

Prefer primary manuals, manufacturer documentation, museum collections, government archives, period photographs, and official specifications. Record publication date, access date, variant scope, license, confidence, and the exact fields each source supports. Keep simulation tuning visibly separate from historical measurements. Never copy one variant's dimensions, turret fit, startup checklist, control limits, or engine settings into another variant without an explicit compatibility record.

## GLB and procedural reconstruction support

The reviewed img2threejs upstream baseline is pinned in the dependency lock. Use its GLB-mediated workflow for semantic decomposition, render-profile comparison, pivots, sockets, action anchors, and quality gates. The source GLB remains provenance and visual evidence. Do not silently copy questionable topology into the universal procedural factory. Upstream skill changes enter beta only after review and tests.

## Secure online metadata and package gates

Before trusting a remote channel, verify the bundled trusted root, then the unversioned timestamp, the versioned snapshot, and the versioned targets metadata. Enforce expiration, monotonic versions, same-version digest stability, parent length and SHA-256, target authorization, and consistent snapshot paths. Reject rollback, freeze, and mixed-generation metadata. The current starter profile uses one release key for all roles and must remain marked as a known limitation until an offline root threshold and role-specific online keys are deployed.

Package schema migrations may add compatibility views for older verified data. A migration must preserve the original package, mark every inferred field, record confidence, and never overwrite an authoritative profile.

## Online package and signing gates

A package can enter stable only after:

1. schema and hierarchy validation;
2. source-model inventory validation;
3. asset byte-count and SHA-256 validation;
4. ECDSA P-256 signature validation for the registry, channel, catalog, package, skill, and dependency manifests;
5. runtime lifecycle and multi-engine tests;
6. source-license and attribution validation;
7. last-known-good and explicit rollback tests;
8. dependency lock, SBOM, and CI checks;
9. remote mirror and bundled-fallback checks.

Runtime aircraft data may be staged automatically after every integrity and signature gate passes. Activation occurs on a safe reload. Skills use staged atomic replacement with a backup. Core code and dependencies advance through a reviewed pull request and stable application release.

## Expected aircraft package

Each version contains a signed manifest plus semantic rig, aircraft profile, lifecycle profile, universal system map, assembly process, material catalog, effects catalog, source register, compatibility range, rollback metadata, and model references. Every remote binary has a verified fallback. Every inferred field carries confidence or an unresolved uncertainty item.

## B-24 baseline

The first reference package contains 104 semantic joints, five progressive reveal levels, sixteen assembly stages, twenty-two operational phases, four independently controlled R-1830 engine runtimes, ten versioned package assets, and no mesh LOD switching. Package 1.2.0 adds independent assembly and operational-effects profiles, schema migration views, and a timestamp to snapshot to targets verification chain without altering the source GLB geometry.

## Required checks

Run `npm test`, `npm run registry:verify`, the glTF inventory validator, and the signed-manifest validator. Report failed gates directly. A visual blockout or successful download does not count as a stable release.
