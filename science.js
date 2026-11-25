/**
 * RADIOGENOMA — modelos didácticos. No son predicciones de riesgo humano.
 * Portados sin alterar las ecuaciones de python/modelo.py, del proyecto previo.
 * Mediciones publicadas y parámetros hipotéticos están separados.
 */
export const PHYSICS = Object.freeze({
  I125_HALF_LIFE_D: 59.4, I131_HALF_LIFE_D: 8.021,
  HPRT_TK6_I131_PER_CGY: 0.45e-6,
  DNA_RADIUS_NM: 1.0, DNA_PITCH_NM: 3.4,
  DNA_BP_PER_TURN: 10, MODEL_WINDOW_BP: 60,
  MODEL_MU: 0.48, MODEL_ELL_NM: 1.5,
  DSB_MAX_SEPARATION_BP: 10,
});
export function rate(halfLifeDays){if(!(halfLifeDays>0))throw new RangeError('Semivida positiva');return Math.LN2/halfLifeDays;}
export function survival(tDays, halfLifeDays){if(tDays<0)throw new RangeError('Tiempo positivo');return Math.exp(-rate(halfLifeDays)*tDays);}
/** Fracción inicial que decae ANTES de salir del ADN; riesgos exponenciales constantes, independientes. */
export function decayInDna(halfLifeDays, meanResidenceDays, endDays=Infinity){
  if(!(meanResidenceDays>0)||endDays<0)throw new RangeError('Tiempos positivos');
  const lam=rate(halfLifeDays),k=1/meanResidenceDays, h=lam+k;
  return lam/h*(1-Math.exp(-h*endDays));
}
export function helix(n=PHYSICS.MODEL_WINDOW_BP){
  if(n<11)throw new RangeError('Ventana corta');
  const a=[],b=[];
  for(let j=0;j<n;j++){
    const theta=2*Math.PI*(j-Math.floor(n/2))/PHYSICS.DNA_BP_PER_TURN;
    const z=(j-Math.floor(n/2))*PHYSICS.DNA_PITCH_NM/PHYSICS.DNA_BP_PER_TURN;
    const x=Math.cos(theta)*PHYSICS.DNA_RADIUS_NM,y=Math.sin(theta)*PHYSICS.DNA_RADIUS_NM;
    a.push([x,y,z]);b.push([-x,-y,z]);
  }return {a,b};
}
export function siteProbabilities(offsetNm=0,mu=PHYSICS.MODEL_MU,ellNm=PHYSICS.MODEL_ELL_NM){
  if(offsetNm<0||mu<0||ellNm<=0)throw new RangeError('Parámetros fuera de dominio');
  const {a,b}=helix();const source=[PHYSICS.DNA_RADIUS_NM+offsetNm,0,0];
  const probability=(p)=>{
    const r=Math.hypot(p[0]-source[0],p[1]-source[1],p[2]-source[2]);
    return 1-Math.exp(-mu*Math.exp(-r/ellNm));
  };
  return {pa:a.map(probability),pb:b.map(probability),source};
}
export function scoreDsb(aBreaks,bBreaks,maxSeparationBp=PHYSICS.DSB_MAX_SEPARATION_BP){
  for(let i=0;i<aBreaks.length;i++){
    if(!aBreaks[i])continue;
    for(let j=Math.max(0,i-maxSeparationBp);j<Math.min(bBreaks.length,i+maxSeparationBp+1);j++)
      if(bBreaks[j])return true;
  }return false;
}
export function seededRandom(seed=2026){let s=seed>>>0;return function(){s+=0x6D2B79F5;let t=s;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return((t^(t>>>14))>>>0)/4294967296;};}
export function sampleOneEvent(offsetNm=0,mu=0.48,ellNm=1.5,seed=2026){
  const rng=seededRandom(seed),{pa,pb}=siteProbabilities(offsetNm,mu,ellNm);
  const a=pa.map(p=>rng()<p),b=pb.map(p=>rng()<p);
  return {a,b,dsb:scoreDsb(a,b),nA:a.filter(Boolean).length,nB:b.filter(Boolean).length};
}
/** Cada repetición representa una desintegración con ubicación fija en el modelo; NO un paciente. */
export function monteCarlo(offsetNm=0,mu=0.48,ellNm=1.5,nEvents=3000,seed=2026){
  if(!Number.isInteger(nEvents)||nEvents<=0)throw new RangeError('Número positivo entero');
  const {pa,pb}=siteProbabilities(offsetNm,mu,ellNm),rng=seededRandom(seed);
  let dsb=0,any=0;
  for(let k=0;k<nEvents;k++){
    const a=new Uint8Array(60),b=new Uint8Array(60);let hit=false;
    for(let j=0;j<60;j++){
      a[j]=+(rng()<pa[j]);b[j]=+(rng()<pb[j]);
      hit ||= !!(a[j]||b[j]);
    }
    if(hit)any++;
    if(scoreDsb(a,b))dsb++;
  }
  const p=dsb/nEvents;
  return {dsb:p,any:any/nEvents,sem:Math.sqrt(p*(1-p)/nEvents),n:nEvents};
}
export function anyBreakAnalytic(offsetNm=0,mu=0.48,ellNm=1.5){
  const {pa,pb}=siteProbabilities(offsetNm,mu,ellNm);
  return 1-pa.concat(pb).reduce((s,p)=>s*(1-p),1);
}
/** Modelo de tres procesos competidores, todas las tasas en h^-1. */
export function fates(tHours,kr=.20,km=.02,kd=.03){
  if(tHours<0||Math.min(kr,km,kd)<0||kr+km+kd<=0)throw new RangeError('Datos fuera de dominio');
  const K=kr+km+kd,remaining=Math.exp(-K*tHours),processed=1-remaining;
  return {remaining,repair:kr/K*processed,mutation:km/K*processed,loss:kd/K*processed};
}
export function hprtInduced(doseCgy){if(doseCgy<0)throw new RangeError('Dosis positiva');return PHYSICS.HPRT_TK6_I131_PER_CGY*doseCgy;}
export function poisson(lambda,rng=Math.random){
  if(lambda<0)throw new RangeError('Lambda positivo');
  // Método de Knuth, válido para las pequeñas cuentas de la experiencia didáctica.
  const L=Math.exp(-lambda);let k=0,p=1;
  do{k++;p*=Math.max(rng(),1e-12)}while(p>L);
  return k-1;
}
