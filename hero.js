/** Visualización ornamental de una doble hélice; no es una simulación atómica. */
const canvas=document.getElementById('hero-canvas');
if(canvas){
 const ctx=canvas.getContext('2d');const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 function draw(ms){
   const dpr=Math.min(window.devicePixelRatio||1,2),w=canvas.clientWidth,h=canvas.clientHeight;
   if(canvas.width!==Math.floor(w*dpr)||canvas.height!==Math.floor(h*dpr)){canvas.width=Math.floor(w*dpr);canvas.height=Math.floor(h*dpr)}
   ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
   const t=ms*.00018, cx=w*.5,cy=h*.505,rad=Math.min(w*.22,115),length=Math.min(h*.8,540);
   ctx.save();ctx.globalAlpha=.17;ctx.strokeStyle='#8ec8b5';ctx.lineWidth=1;
   for(let r=rad*.8;r<rad*2.6;r+=rad*.45){ctx.beginPath();ctx.ellipse(cx,cy,r,r*.48,-.26,0,Math.PI*2);ctx.stroke()}
   ctx.restore();
   const n=110,bonds=[];const points=[[],[]];
   for(let i=0;i<=n;i++){
     const u=i/n, y=cy-length*.5+u*length,a=u*Math.PI*8+t*5;
     for(let j=0;j<2;j++){const phase=a+j*Math.PI;const depth=Math.cos(phase),x=cx+Math.sin(phase)*rad;
       points[j].push({x,y,depth});}
     if(i%5===0)bonds.push([points[0][i],points[1][i]]);
   }
   for(const [a,b] of bonds){const alpha=.12+.33*(1+Math.max(a.depth,b.depth))/2;ctx.strokeStyle=`rgba(166,236,212,${alpha})`;ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}
   for(let strand=0;strand<2;strand++){
      const p=points[strand];for(let i=1;i<p.length;i++){
       const z=(p[i].depth+p[i-1].depth)/2,c=strand===0?[167,234,203]:[133,175,240];
       ctx.strokeStyle=`rgba(${c.join(',')},${(.36+.52*(z+1)/2).toFixed(3)})`;ctx.lineWidth=1.5+2.4*(z+1)/2;ctx.lineCap='round';
       ctx.beginPath();ctx.moveTo(p[i-1].x,p[i-1].y);ctx.lineTo(p[i].x,p[i].y);ctx.stroke();}
   }
   for(const i of [8,24,46,59,78,97]){const p=points[i%2][i];const glow=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,13);glow.addColorStop(0,'rgba(184,253,219,.6)');glow.addColorStop(1,'rgba(184,253,219,0)');ctx.fillStyle=glow;ctx.beginPath();ctx.arc(p.x,p.y,13,0,Math.PI*2);ctx.fill();ctx.fillStyle='#c0ffdd';ctx.beginPath();ctx.arc(p.x,p.y,2.3,0,Math.PI*2);ctx.fill()}
   ctx.font='10px DM Sans, sans-serif';ctx.fillStyle='rgba(212,236,231,.53)';ctx.textAlign='center';ctx.fillText('ADN  •  MODELO GEOMÉTRICO',cx,Math.min(h-20,cy+length*.5+30));
   if(!reduced)requestAnimationFrame(draw);
 }
 requestAnimationFrame(draw);
}
