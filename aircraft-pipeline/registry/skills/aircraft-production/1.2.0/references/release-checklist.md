# Stable Release Checklist v1.2

1. Confirm the aircraft ID and variant scope.
2. Validate all ten required package assets.
3. Validate semantic hierarchy, joint limits, progressive reveal, assembly stages, and lifecycle phases.
4. Verify each asset byte count and SHA-256.
5. Verify trusted root, timestamp, snapshot, targets, registry, channel, catalog, package, skill, and dependency signatures. Test expiry, rollback, same-version mutation, and mixed-snapshot rejection.
6. Verify source licenses, attribution, confidence, and unresolved uncertainty entries.
7. Run multi-engine, update staging, explicit rollback, cache corruption, remote failure, and bundled fallback tests.
8. Run the source GLB inventory test and confirm mesh LOD switching remains disabled.
9. Run dependency signature audit, security audit, SBOM generation, and release attestation.
10. Promote beta to stable only after the full report passes.
