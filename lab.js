import {PHYSICS,survival,decayInDna,siteProbabilities,monteCarlo,anyBreakAnalytic,sampleOneEvent,fates,hprtInduced,poisson,seededRandom} from './science.js';
const scene=document.body.dataset.scene;
const canvas=document.getElementById('science-canvas');
const controlRoot=document.getElementById('control-fields');
const mainOutput=document.getElementById('main-result');
const subOutput=document.getElementById('sub-result');
if(!scene||!canvas||!controlRoot)throw new Error('Página de laboratorio incompleta');
const C={mint:'#a7eacb',blue:'#8dbaff',pink:'#eda1bb',amber:'#f8bd7b',white:'#edf4ef',muted:'#98abb8',grid:'rgba(183,211,218,.11)'};
const configs={
 '01':{sliders:[['velocidad','Velocidad visual',.5,2.5,.1,1.0,'×']],action:'Repetir desintegración',flag:'Esquema de procesos, no un espectro de emisiones'},
 '02':{sliders:[['tiempo','Tiempo transcurrido',0,120,1,40,' días'],['residencia','Residencia media hipotética',.5,15,.5,2,' días']],action:'Restablecer parámetros',flag:'Competencia exponencial hipotética por permanencia'},
 '03':{sliders:[['distancia','Distancia adicional fuente–ADN',0,7,.25,2,' nm'],['mu','Oportunidades μ (supuesto)',.12,.96,.04,.48,''],['ell','Escala espacial ℓ (supuesto)',1,2.5,.1,1.5,' nm']],action:'Restablecer escenario',flag:'Geometría + perfil hipotético, no transporte Monte Carlo de electrones'},
 '04':{sliders:[['distancia','Distancia adicional',0,7,.25,0,' nm'],['mu','Oportunidades μ (supuesto)',.12,.96,.04,.48,'']],action:'Generar otra desintegración',flag:'Modelo Bernoulli por sitio; ventana operativa de ≤10 pb'},
 '05':{sliders:[['tiempo','Tiempo desde la lesión',0,24,.5,9,' h'],['kr','Tasa de reparación kᵣ',.02,.50,.01,.20,' h⁻¹'],['km','Tasa de fijación kₘ',0,.10,.005,.02,' h⁻¹'],['kd','Tasa de pérdida kₚ',0,.12,.005,.03,' h⁻¹']],action:'Restablecer tasas',flag:'Tasas constantes ilustrativas, no mediciones celulares'},
 '06':{sliders:[['dosis','Dosis nuclear (escenario TK6)',0,40,1,38,' cGy'],['celulas','Células clonables hipotéticas',.5,5,.5,1,' millones']],action:'Simular recuento ilustrativo',flag:'Pendiente experimental TK6; dosis y fondo del ejemplo son supuestos'}
};
const cfg=configs[scene],state={},fmt=(v,d=1)=>Number(v).toLocaleString('es-CO',{maximumFractionDigits:d,minimumFractionDigits:0});
let rerolls=0,initTime=performance.now(),stats=null,one=null,counts=null;
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function createSliders(){for(const [key,label,min,max,step,initial,unit] of cfg.sliders){state[key]=initial;const wrap=document.createElement('div');wrap.className='slider-field';
 const header=document.createElement('div');header.className='slider-head';const name=document.createElement('label');const id='range-'+key;name.setAttribute('for',id);name.textContent=label;
 const value=document.createElement('strong');value.id=id+'-value';header.append(name,value);
 const input=document.createElement('input');input.id=id;input.type='range';input.min=min;input.max=max;input.step=step;input.value=initial;input.setAttribute('aria-label',label);
 const endpoints=document.createElement('div');endpoints.className='scale';endpoints.innerHTML=`<span>${fmt(min,2)}${unit}</span><span>${fmt(max,2)}${unit}</span>`;
 wrap.append(header,input,endpoints);controlRoot.appendChild(wrap);const update=()=>{state[key]=Number(input.value);value.textContent=fmt(state[key],3)+unit;refresh()};input.addEventListener('input',update);value.textContent=fmt(initial,3)+unit;}}
const action=document.getElementById('control-action');action.textContent=cfg.action;action.addEventListener('click',()=>{
 if(scene==='01'){initTime=performance.now()}else if(scene==='04'||scene==='06'){rerolls++}else{for(const [key,_,min,max,step,initial] of cfg.sliders){state[key]=initial;const i=document.getElementById('range-'+key);i.value=initial;document.getElementById('range-'+key+'-value').textContent=fmt(initial,3)+(cfg.sliders.find(s=>s[0]===key)[6]||'')}}refresh();});
function refresh(){
 switch(scene){
 case '01':mainOutput.textContent='¹²⁵I → ¹²⁵Te';subOutput.textContent='Captura electrónica, neutrino electrónico y relajación atómica Auger';break;
 case '02':{const p125=decayInDna(59.4,state.residencia),p131=decayInDna(8.021,state.residencia);mainOutput.textContent=fmt(100*p131,2)+' %';subOutput.textContent=`Fracción I-131 que decae antes de salir (modelo). Para I-125: ${fmt(100*p125,2)} %`;break;}
 case '03':{stats=monteCarlo(state.distancia,state.mu,state.ell,3500,2026);mainOutput.textContent=fmt(stats.dsb*100,1)+' %';subOutput.textContent=`DSB por desintegración simulada ± ${fmt(stats.sem*100,2)} pp (1 error estándar; n = 3500)`;break;}
 case '04':{stats=monteCarlo(state.distancia,state.mu,1.5,3500,2026);one=sampleOneEvent(state.distancia,state.mu,1.5,2026+rerolls*97);mainOutput.textContent=one.dsb?'DSB en esta muestra':'Sin DSB en esta muestra';subOutput.textContent=`Roturas A: ${one.nA} · B: ${one.nB} · P(DSB) Monte Carlo: ${fmt(stats.dsb*100,1)} %`;break;}
 case '05':{const f=fates(state.tiempo,state.kr,state.km,state.kd);mainOutput.textContent=fmt(f.repair*100,1)+' %';subOutput.textContent=`Reparación acumulada a ${fmt(state.tiempo,1)} h · Fijación: ${fmt(f.mutation*100,1)} % · Pérdida: ${fmt(f.loss*100,1)} %`;break;}
 case '06':{const exp=hprtInduced(state.dosis)*1e6*state.celulas;const rng=seededRandom(2026+rerolls*103);counts={background:poisson(10*state.celulas,rng),treated:poisson((10+hprtInduced(state.dosis)*1e6)*state.celulas,rng)};mainOutput.textContent=fmt(exp,2);subOutput.textContent=`Mutantes inducidos esperados / ${fmt(state.celulas,1)} millón(es) de células clonables (extrapolación, no conteo observado)`;break;}
 }
 if(reduced)requestAnimationFrame(t=>paint(t));
}
createSliders();refresh();
function canvasSetup(){let w=canvas.clientWidth,h=canvas.clientHeight;const ratio=Math.min(window.devicePixelRatio||1,2),cw=Math.round(w*ratio),ch=Math.round(h*ratio);
 if(canvas.width!==cw||canvas.height!==ch){canvas.width=cw;canvas.height=ch}
 const ctx=canvas.getContext('2d');ctx.setTransform(ratio,0,0,ratio,0,0);ctx.clearRect(0,0,w,h);return {ctx,w,h};}
function paintBackground(ctx,w,h){
 const gl=ctx.createRadialGradient(w*.54,h*.48,0,w*.54,h*.48,Math.max(w,h)*.8);gl.addColorStop(0,'rgba(44,91,102,.2)');gl.addColorStop(1,'rgba(5,12,23,0)');ctx.fillStyle=gl;ctx.fillRect(0,0,w,h);
 ctx.strokeStyle='rgba(167,234,203,.055)';ctx.lineWidth=1;for(let x=22;x<w;x+=44){ctx.beginPath();ctx.moveTo(x,20);ctx.lineTo(x,h-24);ctx.stroke()}for(let y=24;y<h;y+=44){ctx.beginPath();ctx.moveTo(20,y);ctx.lineTo(w-20,y);ctx.stroke()}
}
function text(ctx,str,x,y,size=11,color=C.muted,align='left'){ctx.font=`${size}px DM Sans, Arial, sans-serif`;ctx.fillStyle=color;ctx.textAlign=align;ctx.fillText(str,x,y);ctx.textAlign='left'}
function circle(ctx,x,y,r,color,glow=0){ctx.save();if(glow){ctx.shadowBlur=glow;ctx.shadowColor=color;}ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle=color;ctx.fill();ctx.restore()}
function line(ctx,x1,y1,x2,y2,color=C.mint,width=1){ctx.strokeStyle=color;ctx.lineWidth=width;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke()}
function polyline(ctx,points,color,width=2){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineJoin='round';ctx.lineCap='round';ctx.beginPath();for(let i=0;i<points.length;i++){const [x,y]=points[i];if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y)}ctx.stroke();ctx.restore()}
function drawAxes(ctx,x,y,w,h,maxX,maxY,labels={}){
 line(ctx,x,y,x,y+h,'rgba(203,228,231,.48)');line(ctx,x,y+h,x+w,y+h,'rgba(203,228,231,.48)');
 for(let i=0;i<=4;i++){const yy=y+h-(i/4)*h;line(ctx,x,yy,x+w,yy,C.grid);text(ctx,fmt(maxY*i/4,labels.yDigits??1),x-12,yy+4,10,C.muted,'right')}
 for(let i=0;i<=4;i++){const xx=x+(i/4)*w;text(ctx,fmt(maxX*i/4,labels.xDigits??0),xx,y+h+19,10,C.muted,'center')}
 text(ctx,labels.x||'',x+w/2,y+h+42,11,C.muted,'center');text(ctx,labels.y||'',x+3,y-13,10,C.muted);
}
function plot(ctx,rect,maxX,maxY,fn,color,width=2.5){const pts=[];for(let i=0;i<=240;i++){const x=(i/240)*maxX,y=fn(x);pts.push([rect.x+x/maxX*rect.w,rect.y+rect.h-Math.max(0,Math.min(1,y/maxY))*rect.h]);}polyline(ctx,pts,color,width);}
function isotope(ctx,w,h,sec){
 const cx=w*.49,cy=h*.505,r=Math.min(w,h)*.13,period=(sec*state.velocidad)%3.8;
 for(let i=0;i<5;i++){ctx.strokeStyle=`rgba(177,226,228,${.08+i*.05})`;ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(cx,cy,r*(1.48+i*.42),r*(.77+i*.29),i*.35,0,Math.PI*2);ctx.stroke()}
 const g=ctx.createRadialGradient(cx-r*.4,cy-r*.4,4,cx,cy,r);g.addColorStop(0,'#b4fce4');g.addColorStop(.5,'#6acbbd');g.addColorStop(1,'#235b61');circle(ctx,cx,cy,r,'#308e88',22);ctx.fillStyle=g;ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.fill();
 text(ctx,period<1.18?'¹²⁵I':'¹²⁵Te',cx,cy+7,23,'#071d28','center');
 if(period<1.18){const q=period/1.18;const sx=cx-r*2.8,sy=cy-r*.25;const xx=sx+(cx-sx)*q,yy=sy+(cy-sy)*q;circle(ctx,xx,yy,5,C.amber,18);line(ctx,sx,sy,cx-r*1.1,cy,'rgba(248,189,123,.28)',1);text(ctx,'e⁻',xx-4,yy-18,11,C.amber,'center');}
 if(period>1.18){const q=Math.min((period-1.18)/1.7,1);for(let k=0;k<13;k++){
   const a=k*Math.PI*2/13+k*.15,dist=r*1.2+q*(w*.26)*(0.35+.65*((k*7)%13)/13);
   const px=cx+Math.cos(a)*dist,py=cy+Math.sin(a)*dist*.77;
   line(ctx,cx+Math.cos(a)*r,cy+Math.sin(a)*r*.83,px,py,`rgba(167,234,203,${.34*(1-q)+.05})`,1.2);
   circle(ctx,px,py,2.5, k%2?C.mint:C.blue,8);
 }text(ctx,'CASCADA AUGER',w*.08,h*.19,11,C.mint);}
 if(period>1.03&&period<2.4){const q=(period-1.03)/1.4;circle(ctx,cx+q*w*.28,cy-q*h*.24,3,C.pink,6);text(ctx,'νₑ',cx+q*w*.28+12,cy-q*h*.24-8,12,C.pink)}
 text(ctx,'CAPTURA ELECTRÓNICA',w*.06,h*.85,10,C.amber);text(ctx,'Z: 53 → 52   |   A = 125',w*.06,h*.91,11,C.white);
}
function decays(ctx,w,h){const rect={x:w*.12,y:h*.18,w:w*.74,h:h*.57};drawAxes(ctx,rect.x,rect.y,rect.w,rect.h,120,1,{x:'Tiempo desde t₀ (días)',y:'N / N₀'});
 plot(ctx,rect,120,1,t=>survival(t,59.4),C.mint,3);plot(ctx,rect,120,1,t=>survival(t,8.021),C.pink,3);
 const x=rect.x+state.tiempo/120*rect.w,y1=rect.y+rect.h*(1-survival(state.tiempo,59.4)),y2=rect.y+rect.h*(1-survival(state.tiempo,8.021));
 line(ctx,x,rect.y,x,rect.y+rect.h,'rgba(245,240,221,.35)');circle(ctx,x,y1,4,C.mint,12);circle(ctx,x,y2,4,C.pink,12);
 text(ctx,'¹²⁵I  ·  59,40 días',rect.x+8,rect.y+27,12,C.mint);text(ctx,'¹³¹I  ·  8,021 días',rect.x+8,rect.y+49,12,C.pink);
 text(ctx,`N(¹²⁵I) = ${fmt(100*survival(state.tiempo,59.4),1)} %`,rect.x,rect.y+rect.h+79,12,C.mint);
 text(ctx,`N(¹³¹I) = ${fmt(100*survival(state.tiempo,8.021),1)} %`,rect.x+rect.w,rect.y+rect.h+79,12,C.pink,'right');
}
function helixView(ctx,w,h){
 const cx=w*.42,top=h*.17,height=h*.68,amp=Math.min(w*.105,68),pa=siteProbabilities(state.distancia,state.mu,state.ell);
 const ptA=[],ptB=[];
 for(let j=0;j<60;j++){
  const a=(j-30)*Math.PI*2/10,yy=top+(j/59)*height;
  ptA.push([cx+Math.sin(a)*amp,yy]);ptB.push([cx-Math.sin(a)*amp,yy]);
  const strength=Math.min(1,(pa.pa[j]+pa.pb[j])*3.0);
  line(ctx,ptA[j][0],yy,ptB[j][0],`rgba(177,220,218,${.13+.32*strength})`,1.3);
  if(j%5===0){const rgba=`rgba(248,189,123,${Math.min(.85,pa.pa[j]*1.7+.08)})`;circle(ctx,ptA[j][0],yy,2.5,rgba,3)}
 }
 polyline(ctx,ptA,C.mint,2.7);polyline(ctx,ptB,C.blue,2.7);
 const sy=top+height*.51,sx=w*.62+state.distancia*w*.021;
 const glow=ctx.createRadialGradient(sx,sy,0,sx,sy,38);glow.addColorStop(0,'rgba(248,189,123,.32)');glow.addColorStop(1,'rgba(248,189,123,0)');ctx.fillStyle=glow;ctx.beginPath();ctx.arc(sx,sy,38,0,Math.PI*2);ctx.fill();circle(ctx,sx,sy,7,C.amber,18);text(ctx,'¹²⁵I',sx+14,sy+4,12,C.amber);
 line(ctx,cx+amp,sy,sx-8,sy,'rgba(248,189,123,.4)',1);
 text(ctx,'B-ADN IDEALIZADO',w*.1,h*.12,10,C.mint);text(ctx,`r adicional = ${fmt(state.distancia,2)} nm`,w*.63,h*.86,12,C.amber);
 const paMax=Math.max(...pa.pa),pbMax=Math.max(...pa.pb);text(ctx,`P(SSB) máx. / A: ${fmt(paMax*100,1)} %`,w*.1,h*.91,10,C.muted);
 text(ctx,`P(SSB) máx. / B: ${fmt(pbMax*100,1)} %`,w*.63,h*.91,10,C.muted);
}
function breaks(ctx,w,h){const x0=w*.11,x1=w*.88,yyA=h*.35,yyB=h*.63,dx=(x1-x0)/59;
 text(ctx,'HEBRA A',x0,yyA-35,11,C.mint);text(ctx,'HEBRA B',x0,yyB+53,11,C.blue);
 line(ctx,x0,yyA,x1,yyA,C.mint,3);line(ctx,x0,yyB,x1,yyB,C.blue,3);
 for(let j=0;j<60;j++){
   const x=x0+j*dx;
   line(ctx,x,yyA-3,x,yyA+3,'rgba(217,236,233,.45)',1);
   line(ctx,x,yyB-3,x,yyB+3,'rgba(217,236,233,.45)',1);
 }
 const marks=(list,y,color)=>list.forEach((v,j)=>{if(!v)return;const x=x0+j*dx;line(ctx,x-8,y-9,x+8,y+9,color,3);line(ctx,x+8,y-9,x-8,y+9,color,3);circle(ctx,x,y,3,C.amber,8)});
 marks(one.a,yyA,C.amber);marks(one.b,yyB,C.pink);
 const ai=one.a.findIndex(Boolean),bi=one.b.findIndex(Boolean);
 if(ai>=0&&bi>=0){const xA=x0+ai*dx,xB=x0+bi*dx;line(ctx,xA,yyA+20,xB,yyB-20,'rgba(241,207,169,.28)',1);text(ctx,`Separación ejemplo = ${Math.abs(ai-bi)} pb`,w*.50,h*.17,11,C.amber,'center');}
 text(ctx,one.dsb?'✓  PAR DE ROTURAS COMPATIBLE CON DSB':'SIN PAR DSB EN ESTA DESINTEGRACIÓN',w*.5,h*.83,12,one.dsb?C.mint:C.pink,'center');
 text(ctx,'Criterio: una rotura por hebra, separación ≤ 10 pb',w*.5,h*.9,11,C.muted,'center');
}
function repair(ctx,w,h){const rect={x:w*.12,y:h*.17,w:w*.74,h:h*.6};drawAxes(ctx,rect.x,rect.y,rect.w,rect.h,24,1,{x:'Tiempo desde la lesión (h)',y:'Fracción del estado inicial'});
 const F=t=>fates(t,state.kr,state.km,state.kd);
 const curves=[['remaining',C.white],['repair',C.mint],['mutation',C.pink],['loss',C.amber]];
 for(const [key,col] of curves)plot(ctx,rect,24,1,t=>F(t)[key],col,2.5);
 const x=rect.x+state.tiempo/24*rect.w;line(ctx,x,rect.y,x,rect.y+rect.h,'rgba(255,255,255,.32)');
 for(const [key,col] of curves){const v=F(state.tiempo)[key];circle(ctx,x,rect.y+rect.h-v*rect.h,3.4,col,7)}
 const labels=[['Lesión',C.white],['Reparación',C.mint],['Fijación',C.pink],['Pérdida',C.amber]];
 labels.forEach(([s,c],i)=>{const xx=rect.x+ i*rect.w/4;circle(ctx,xx+5,rect.y+rect.h+79,4,c);text(ctx,s,xx+14,rect.y+rect.h+83,10,C.white)});
}
function experiment(ctx,w,h){const rect={x:w*.13,y:h*.20,w:w*.71,h:h*.51};drawAxes(ctx,rect.x,rect.y,rect.w,rect.h,40,18,{x:'Dosis depositada en el núcleo (cGy)',y:'Mutantes inducidos esperados / 10⁶',yDigits:0});
 plot(ctx,rect,40,18,d=>hprtInduced(d)*1e6,C.mint,3.4);
 const x=rect.x+state.dosis/40*rect.w,y=rect.y+rect.h-(hprtInduced(state.dosis)*1e6/18)*rect.h;
 line(ctx,x,rect.y,x,rect.y+rect.h,'rgba(204,228,224,.32)');line(ctx,rect.x,y,x,y,'rgba(204,228,224,.25)');circle(ctx,x,y,5,C.amber,15);
 text(ctx,'TK6 · ¹³¹I–IdUrd',rect.x,rect.y-31,13,C.mint);text(ctx,'Pendiente publicada: 0,45 × 10⁻⁶ / cGy',rect.x,rect.y-12,11,C.muted);
 text(ctx,`Simulación Poisson (fondo supuesto): control ${counts.background} · tratado ${counts.treated}`,rect.x,rect.y+rect.h+80,11,C.amber);
 text(ctx,'SE30: sin curva cuantitativa publicada aquí; pocas mutaciones hasta 38 cGy.',rect.x,rect.y+rect.h+105,10,C.muted);
}
function paint(ms){const {ctx,w,h}=canvasSetup();paintBackground(ctx,w,h);const sec=(ms-initTime)/1000;
 switch(scene){case '01':isotope(ctx,w,h,sec);break;case '02':decays(ctx,w,h);break;case '03':helixView(ctx,w,h);break;case '04':breaks(ctx,w,h);break;case '05':repair(ctx,w,h);break;case '06':experiment(ctx,w,h);break;}
 if(!reduced)requestAnimationFrame(paint);
}
requestAnimationFrame(paint);
