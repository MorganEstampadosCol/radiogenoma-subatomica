"""Cuatro figuras vectoriales para el desarrollo nuclear y microdosimétrico.

Las curvas son cálculos pedagógicos, no espectros medidos ni transporte de electrones.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parents[1]/'documentacion'/'figuras_monografia'
OUT.mkdir(parents=True, exist_ok=True)
NAVY='#183247'; TEAL='#0a8589'; RUST='#b36c42'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,
                     'axes.spines.top':False,'axes.spines.right':False,
                     'axes.edgecolor':NAVY,'axes.labelcolor':NAVY,
                     'xtick.color':NAVY,'ytick.color':NAVY,
                     'savefig.facecolor':'white'})
def save(fig,name):
    fig.tight_layout(pad=1.4);fig.savefig(OUT/name,bbox_inches='tight');plt.close(fig)

T=np.linspace(0,606.3,3001)
m=510.99895
p=np.sqrt(T*(T+2*m))
# F(Z,T)=1; una sola rama permitida con endpoint de 606,3 keV.
raw=p*(T+m)*(606.3-T)**2
pdf=raw/np.trapezoid(raw,T)
cdf=np.r_[0,np.cumsum((pdf[1:]+pdf[:-1])/2*np.diff(T))]
cdf/=cdf[-1]
q={v:np.interp(v,cdf,T) for v in (.1,.5,.9)}
fig,ax=plt.subplots(1,2,figsize=(10,3.2))
ax[0].plot(T,pdf*100,TEAL,lw=2.3)
ax[0].fill_between(T,pdf*100,color=TEAL,alpha=.12)
ax[0].set(xlabel='Energía cinética beta T (keV)',ylabel='Densidad por 100 keV',title='Una rama ilustrativa de $^{131}$I')
ax[0].text(.03,.96,'$T_0=606,3$ keV; $F(Z,T)=1$',transform=ax[0].transAxes,va='top',color=NAVY)
ax[1].plot(T,cdf,TEAL,lw=2.3)
for v,energy in q.items():
    ax[1].plot([energy],[v],'o',color=RUST)
    ax[1].annotate(f'{int(v*100)} %: {energy:.0f} keV',(energy,v),xytext=(5,-19 if v>.5 else 8),textcoords='offset points',fontsize=8)
ax[1].set(xlabel='Energía cinética beta T (keV)',ylabel='Probabilidad acumulada',ylim=(0,1.05),title='Cuantiles del modelo, no de datos')
save(fig,'05_beta_modelo.pdf')

days=np.linspace(0,80,500)
lam125=np.log(2)/59.4;lam131=np.log(2)/8.021
fig,ax=plt.subplots(figsize=(8.2,3.7))
for lam,name,c in [(lam125,'$^{125}$I · 59,40 d',TEAL),(lam131,'$^{131}$I · 8,021 d',RUST)]:
    ax.plot(days,np.exp(-lam*days),lw=2.4,label=name,color=c)
ax.axhline(.5,ls=':',color=NAVY,alpha=.55)
ax.set(xlabel='Tiempo desde la incorporación (días)',ylabel='Fracción de núcleos sin decaer',ylim=(0,1.02),title='Reloj nuclear: sin eliminación biológica')
ax.legend(frameon=False)
save(fig,'06_semividas_fisicas.pdf')

radius=np.geomspace(3,100,300) # nm
energy=16.51e3*1.602176634e-19 # J, escenario ilustrativo
mass=1000*4*np.pi/3*(radius*1e-9)**3
dose=energy/mass
fig,ax=plt.subplots(figsize=(8.2,3.7))
ax.loglog(radius,dose,TEAL,lw=2.4)
ax.scatter([10],[energy/(1000*4*np.pi/3*(10e-9)**3)],color=RUST,zorder=3)
ax.annotate('10 nm: $6,315\\times10^5$ Gy (promedio de esfera)',(10,6.315e5),xytext=(13,1.1e6),fontsize=8,color=NAVY)
ax.set(xlabel='Radio supuesto de la esfera (nm)',ylabel='E/m, promedio formal (Gy)',title='Supuesto: 16,51 keV depositados por completo en agua')
ax.text(.02,.04,'No representa la dosis del núcleo ni una traza real',transform=ax.transAxes,color=RUST)
save(fig,'07_esfera_energia.pdf')

half_b=np.geomspace(.05,100,300)
lb=np.log(2)/half_b
fig,ax=plt.subplots(figsize=(8.2,3.7))
for ln,name,c in [(lam125,'$^{125}$I',TEAL),(lam131,'$^{131}$I',RUST)]:
    pr=ln/(ln+lb)
    ax.semilogx(half_b,pr,lw=2.4,label=name,color=c)
ax.set(xlabel='Semivida biológica hipotética en ADN (días)',ylabel='P(decaimiento antes de salida)',ylim=(0,1),title='Relojes competidores: hipótesis de residencia')
ax.legend(frameon=False)
save(fig,'08_competencia_biologica.pdf')
print('Cuantiles beta:',q)
