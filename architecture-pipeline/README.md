# Historical Architecture Production Line

Parametric historical-building system for the 1940-1945 Raging Coast world.

## Goal

Turn map footprints and regional historical evidence into reproducible Three.js buildings. A building instance references a regional kit, archetype and seed. Geometry is generated from structural rules instead of storing a unique heavy mesh for every house.

## Pipeline

1. `regions/*.json`: regional architectural DNA, materials, roof families, wall systems, openings and evidence confidence.
2. `schemas/*.json`: stable data contracts.
3. `instances/*.json`: map-derived building footprints and per-building overrides.
4. Runtime generator: footprint -> bays/modules -> walls -> roof -> openings -> details -> materials -> weathering.
5. Export/cache: generated geometry can be cached as GLB when useful, while JSON remains the source of truth.

## Historical rules

Every rule carries provenance and confidence. `documented` means directly supported by a source, `regional_inference` means supported by a nearby or broader regional tradition, and `reconstruction_guess` means a controlled visual hypothesis. The runtime must be able to disable low-confidence decorative details.

## Three.js strategy

Use BufferGeometry and merged static geometry for unique buildings, InstancedMesh for repeated doors/windows/tiles/detail modules, shared PBR materials and texture atlases, deterministic seeded variation, and distance-dependent detail generation. Buildings have no skeletal rig. Semantic parts remain addressable through metadata for damage states, roof removal, selection and later editing.

## First regional kit

`regions/kunming-1940-1945.json` starts with the Kunming courtyard dwelling tradition known as Yi Ke Yin. The initial evidence baseline supports a compact square courtyard composition with principal room, wing rooms, opposite building, tile roofs and earthen walls. Exact 1940-1945 street-level variants will be refined with period aerial photographs, maps and archival photographs.
