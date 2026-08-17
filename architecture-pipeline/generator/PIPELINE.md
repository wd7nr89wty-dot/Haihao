# Footprint to Historical Building Pipeline v0.1

## Goal
Convert a georeferenced building polygon plus a regional 1940-1945 architecture DNA file into deterministic semantic Three.js geometry.

## Stages
1. Validate footprint and region/time metadata.
2. Normalize polygon into a local meter coordinate frame.
3. Extract oriented bounding box, principal axis, area, compactness, concavities and likely access/street edge.
4. Sample DEM when available and calculate slope/aspect.
5. Score regional archetypes. Never select an archetype below its evidence/confidence threshold.
6. Infer courtyard probability from footprint geometry and visible holes. Preserve explicit observed courtyards.
7. Generate a semantic massing graph: building bars, courtyard, gate/access, structural bays, floor levels and roof zones.
8. Fit structural bay spacing to the footprint while preserving the external historic footprint as the hard constraint.
9. Solve roofs per regional DNA. Roofs are independent semantic surfaces so pitch, ridge and tile treatment can be revised without rebuilding walls.
10. Generate openings using facade role. Street/exterior and courtyard/interior facades use separate density rules.
11. Add regional material IDs and deterministic weathering from building-id seed.
12. Tag every inferred property with evidence class and confidence.
13. Compile render representation.

## Render representation
Use one semantic source model with progressive render detail. Large shells use BufferGeometry. Repeated columns, rafters, tiles and simple openings use InstancedMesh where visually justified. Far views collapse details into simplified geometry/material response. Close views may expand semantic components without changing the building's dimensions or historical identity. WebGPU is preferred when supported, with WebGL fallback retained during early development.

## Hard rules
* Satellite/aerial footprint dimensions are immutable unless source correction is explicitly recorded.
* Random variation must be seeded by building ID.
* Variation cannot cross archetype boundaries.
* No decorative element may be invented at high confidence.
* Unknown information remains unknown and receives a reconstruction_guess tag.
* Do not generate hidden interiors by default.
* Terrain adaptation happens before roof solving.
* A building must remain reconstructible from JSON alone.

## Archetype scoring v0.1
`score = footprintFit*0.35 + courtyardFit*0.20 + terrainFit*0.15 + streetFit*0.10 + periodEvidence*0.20`

If two archetypes are within 0.08 score, retain both candidates and use the less-specific geometry until additional evidence is supplied.

## Progressive semantic detail
D0: footprint mass only.
D1: storeys and roof silhouette.
D2: courtyard, eaves, main openings.
D3: structural bays, doors/windows, ridge/eave details.
D4: local tile/timber components and weathering.

The D-level changes representation detail while preserving one semantic building graph. It is intended to avoid maintaining separate hand-authored LOD models.