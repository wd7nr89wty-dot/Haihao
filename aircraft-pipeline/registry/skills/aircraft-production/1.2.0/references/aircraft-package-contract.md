# Aircraft Package Contract v1.2

A stable aircraft package must expose these assets through its signed manifest:

* `rig`
* `profile`
* `lifecycleProfile`
* `systemMap`
* `assemblyProfile`
* `effectsProfile`
* `smokeProfiles`
* `materialCatalog`
* `sourceRegister`
* `model`

Every descriptor records bytes, SHA-256, media type, immutable status, timeout, and one or more ordered sources. The package manifest records application compatibility, previous stable version, and retained verified version count.

All semantic nodes are created once. Projected screen size changes semantic visibility and update budgets. The source aircraft mesh is not replaced through a conventional LOD chain.

The signed control plane verifies timestamp, snapshot, and targets metadata before registry files are accepted. Older verified packages may receive marked compatibility views through the migration registry.
