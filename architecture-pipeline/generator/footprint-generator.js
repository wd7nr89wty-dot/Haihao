export function analyzeFootprint(input) {
  const pts = input.polygon.map(([x,z]) => ({x,z}));
  const xs = pts.map(p=>p.x), zs = pts.map(p=>p.z);
  const bounds = {minX:Math.min(...xs),maxX:Math.max(...xs),minZ:Math.min(...zs),maxZ:Math.max(...zs)};
  let twiceArea = 0;
  for (let i=0;i<pts.length;i++) { const a=pts[i], b=pts[(i+1)%pts.length]; twiceArea += a.x*b.z-b.x*a.z; }
  const area = Math.abs(twiceArea)*0.5;
  const width=bounds.maxX-bounds.minX, depth=bounds.maxZ-bounds.minZ;
  return {bounds,area,width,depth,aspect:Math.max(width,depth)/Math.max(0.001,Math.min(width,depth)),hasExplicitCourtyard:Boolean(input.holes?.length||input.observations?.courtyardVisible)};
}

export function scoreArchetype(analysis, archetype, input) {
  let footprintFit = analysis.aspect < 1.55 ? 0.9 : analysis.aspect < 2.4 ? 0.65 : 0.35;
  const courtyardExpected = /courtyard/.test(archetype.footprint?.family||archetype.id);
  const courtyardFit = analysis.hasExplicitCourtyard === courtyardExpected ? 1 : analysis.hasExplicitCourtyard ? 0.35 : 0.65;
  const slope = input.terrain?.slopeDegrees ?? 0;
  const terrainFit = archetype.footprint?.terrainResponse === 'very-high' ? Math.min(1,0.45+slope/20) : slope < 12 ? 0.9 : 0.6;
  const streetFit = 0.7;
  const periodEvidence = archetype.evidence?.confidence ?? 0.5;
  return footprintFit*.35+courtyardFit*.20+terrainFit*.15+streetFit*.10+periodEvidence*.20;
}

export function chooseArchetype(regionDNA, input) {
  const analysis=analyzeFootprint(input);
  const ranked=regionDNA.archetypes.map(a=>({archetype:a,score:scoreArchetype(analysis,a,input)})).sort((a,b)=>b.score-a.score);
  if (!ranked.length) throw new Error('No regional archetypes available');
  const floor=regionDNA.generationDefaults?.historicalConfidenceFloor ?? .55;
  const viable=ranked.filter(x=>x.score>=floor);
  return {analysis, ranked, selected:viable[0]||null, ambiguous:viable.length>1 && viable[0].score-viable[1].score<.08};
}

export function buildSemanticMassing(regionDNA,input) {
  const choice=chooseArchetype(regionDNA,input);
  if(!choice.selected) return {id:input.id,status:'insufficient-evidence',choice};
  const a=choice.selected.archetype, b=choice.analysis.bounds;
  const floorH=((a.generator?.floorHeightM?.min||2.8)+(a.generator?.floorHeightM?.max||3.2))/2;
  const storeys=input.observations?.storeys || a.storeys?.min || 1;
  return {id:input.id,regionId:input.regionId,archetypeId:a.id,status:choice.ambiguous?'ambiguous':'generated',confidence:choice.selected.score,dimensions:{width:choice.analysis.width,depth:choice.analysis.depth,height:floorH*storeys},origin:{x:(b.minX+b.maxX)/2,y:0,z:(b.minZ+b.maxZ)/2},semantic:{shell:{polygon:input.polygon,storeys,floorHeightM:floorH},courtyard:choice.analysis.hasExplicitCourtyard?{source:input.holes?.length?'observed-hole':'observation'}:{source:'inferred',confidence:.45},roof:{family:a.roof?.family||'pitched',pitchDegrees:a.roof?.pitchDegrees||null}},evidence:{class:choice.ambiguous?'regional_inference':'documented_or_regional',archetypeConfidence:a.evidence?.confidence||.5},candidates:choice.ranked.slice(0,3).map(x=>({id:x.archetype.id,score:x.score}))};
}