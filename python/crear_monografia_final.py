"""Compone la monografía extensa desde las fuentes verificadas del repositorio."""
from pathlib import Path
import re
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documentacion'
FIG = OUT / 'figuras_monografia'
FIG.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / 'python'))
from modelo import (sample_lesions, fraction_decay_in_dna, lesion_fates,
                    hprt_induced_frequency, T125_D, T131_D)

plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,
                     'axes.spines.right':False,'font.size':10,'figure.dpi':160})
NAVY='#12263d'; TEAL='#087e83'; GOLD='#bd7040'; PINK='#b46482'

def save(name):
    plt.tight_layout(pad=1.7)
    plt.savefig(FIG/name, dpi=200, facecolor='white', bbox_inches='tight')
    plt.close()

base=sample_lesions()
fig,ax=plt.subplots(figsize=(8.7,4.3))
d=np.array([x['offset_nm'] for x in base]); p=np.array([x['dsb'] for x in base]);
sem=np.array([x['sem'] for x in base]); anyp=np.array([x['any_break'] for x in base])
ax.errorbar(d,p*100,yerr=1.96*sem*100,fmt='o-',lw=2.3,capsize=4,color=TEAL,label='DSB: modelo, IC aproximado ±1,96 SEM')
ax.plot(d,anyp*100,'s--',lw=1.7,color=GOLD,label='Alguna rotura: modelo')
ax.set(xlabel='Distancia adicional d (nm)',ylabel='Eventos simulados (%)',ylim=(-3,105),xticks=d)
ax.grid(alpha=.16);ax.legend(frameon=False,loc='upper right',fontsize=8.7)
save('01_distancia_y_roturas.png')

fig,ax=plt.subplots(figsize=(8.7,4.1))
t=np.linspace(0,24,300); L,R,M,C=lesion_fates(t)
for val,label,col in [(L,'Lesión presente',NAVY),(R,'Reparación',TEAL),(M,'Fijación (supuesto)',PINK),(C,'Pérdida celular',GOLD)]:
    ax.plot(t,val*100,lw=2.3,label=label,color=col)
ax.set(xlabel='Tiempo desde la lesión (h)',ylabel='Fracción del estado inicial (%)',xlim=(0,24),ylim=(0,103))
ax.grid(alpha=.16);ax.legend(frameon=False,fontsize=9)
save('02_destinos_celulares.png')

fig,ax=plt.subplots(figsize=(8.7,4.1))
tau=np.linspace(.2,15,400)
ax.plot(tau,100*np.array([fraction_decay_in_dna(T125_D,x) for x in tau]),color=TEAL,lw=2.3,label='¹²⁵I')
ax.plot(tau,100*np.array([fraction_decay_in_dna(T131_D,x) for x in tau]),color=PINK,lw=2.3,label='¹³¹I')
ax.axvline(2,color=GOLD,ls=':',lw=1.5);ax.set(xlabel='Residencia media supuesta τ (días)',ylabel='Decae antes de salir del ADN (%)',xlim=(0,15),ylim=(0,60))
ax.grid(alpha=.16);ax.legend(frameon=False)
save('03_retencion_hipotetica.png')

fig,ax=plt.subplots(figsize=(8.7,4.1))
dd=np.linspace(0,40,200)
ax.plot(dd,hprt_induced_frequency(dd)*1e6,color=TEAL,lw=2.5,label='Recta TK6 por pendiente publicada')
ax.scatter([38],[17.1],color=GOLD,s=85,zorder=5,label='Extrapolación a 38 cGy, no dato TK6 medido')
ax.set(xlabel='Dosis nuclear D (cGy)',ylabel='Exceso de mutantes HPRT por 10⁶ clonables',xlim=(0,40),ylim=(0,19))
ax.grid(alpha=.16);ax.legend(frameon=False,fontsize=8.5)
save('04_hprt_extrapolacion.png')

plain=subprocess.check_output(['pandoc','-f','latex','-t','markdown','--wrap=none',str(OUT/'guia.tex')],text=True)
plain=plain.split('# El problema, su interés y una respuesta comprobable',1)[1]
plain=plain.split('# Guía de defensa breve: preguntas y respuestas',1)[0]
plain=plain.replace('::: thebibliography','').replace('::: center','').replace(':::','')
plain=re.sub(r'\[@([a-zA-Z0-9]+)\]',lambda m:'['+str({'whaley':1,'martin':2,'lemotte':3,'oneill':4,'gene':5,'iaea125':6,'icrp':7,'iaea131':8,'corrigendum':9,'curso':10,'deteccion':11}.get(m.group(1),'?'))+']',plain)
plain=plain.replace('[[\\[DATO\\]','**[DATO]').replace('[[\\[MODELO\\]','**[MODELO]')
plain=re.sub(r'\]\{\.sans-serif\}\]\{style="color: (?:teal|gold)"\}', '**',plain)
plain=re.sub(r'\[\[\\\[eq:[^]]+\]\]\([^)]*\)\{[^}]*\}', 'ecuación de probabilidad por sitio', plain)
plain=re.sub(r'\\label\{[^}]+\}', '', plain)
plain=re.sub(r'\(\[\\\[eq:ssb\\\]\]\(#eq:ssb\)\{[^}]+\}\)', 'probabilidad por sitio', plain)
plain=re.sub(r'\[9\]\(#sec:hprt\)\{[^}]+\}', '«Del locus HPRT a un conteo interpretable»', plain)
plain=plain.replace('1280$\\times$`<!-- -->`{=html}720', '1280 × 720')
plain=plain.replace('Eq. probabilidad por sitio', 'de la probabilidad por sitio')
plain=plain.replace('ecuación ([\\[eq:nu\\]](#eq:nu){reference-type="ref" reference="eq:nu"})', 'ecuación del balance de energía anterior')
plain=re.sub(r'\$\$\{\}\^\{125\}_\{53\}\\mathrm I\+e\^-_\{\\mathrm\{ligado\}\}\\longrightarrow\{\}\^\{125\}_\{52\}\\mathrm\{Te\}\^\*\+\\nu_e \.\$\$',
             '¹²⁵₅₃I + e⁻(ligado) → ¹²⁵₅₂Te* + νₑ.', plain)
plain=re.sub(r'\$\$\{\}\^\{131\}_\{53\}\\mathrm I\\longrightarrow\{\}\^\{131\}_\{54\}\\mathrm\{Xe\}\^\*\+e\^-\+\\bar\{\\nu\}_e \.\$\$',
             '¹³¹₅₃I → ¹³¹₅₄Xe* + e⁻ + antineutrino electrónico.', plain)
plain=re.sub(r'\$\^\{(125|131)\}\$I', lambda m: {'125':'¹²⁵I','131':'¹³¹I'}[m.group(1)], plain)
plain=re.sub(r'\$\^\{(125|131)\}\$Te',lambda m: {'125':'¹²⁵Te','131':'¹³¹Te'}[m.group(1)],plain)
plain=plain.replace('### Resultados del escenario base y sensibilidad', '### Resultados del escenario base y sensibilidad')
plain=re.sub(r'\n\s+\$d\$ \\?\[nm\\?\].*?\n\s+7\s+0\.12580\s+0\.00200\s+0\.00036\n',
'''\n| d (nm) | P(cualquier rotura) | P(DSB) | SEM |
|---:|---:|---:|---:|
| 0 | 0,99713 | 0,87000 | 0,00275 |
| 1 | 0,98167 | 0,68847 | 0,00378 |
| 2 | 0,90880 | 0,41560 | 0,00402 |
| 4 | 0,55587 | 0,07180 | 0,00211 |
| 7 | 0,12580 | 0,00200 | 0,00036 |\n''',plain,flags=re.S)
plain=re.sub(r'^## (.+)$',r'### \1',plain,flags=re.M)
plain=re.sub(r'^# (.+)$',r'## \1',plain,flags=re.M)
plain='## El problema, su interés y una respuesta comprobable'+plain

cover=r'''# Cuando un núcleo decae dentro del ADN humano

## De la física subatómica a las lesiones, reparación y mutaciones HPRT

**RADIOGENOMA · MONOGRAFÍA CIENTÍFICA DE ENTREGA**  
**Universidad Nacional de Colombia · Física Subatómica**  
**Equipo:** Proyecto de Física Subatómica  
**Bogotá, Colombia · 25 de noviembre de 2026**

Artículo conductor: Whaley y Little, *Radiation Research* **123** (1990), 68–74 [1].

![Portada visual: ADN y radiación local, ilustración original del proyecto](media/01_captura_y_Auger_portada.png)

**Versión:** monografía extensa, seis laboratorios expositivos y anexos de código. El proyecto completo está publicado en [RadioGenoma](https://morganestampadoscol.github.io/radiogenoma-subatomica/) y el [repositorio](https://github.com/MorganEstampadosCol/radiogenoma-subatomica). Las ilustraciones son esquemas; no son micrografías ni registros de pacientes.

# Resumen

El experimento de Whaley y Little [1] estudió muerte celular y mutaciones en el locus *hprt* tras exponer líneas linfoblastoides humanas TK6 y SE30 a iododesoxiuridina marcada con $^{125}$I o $^{131}$I. La diferencia de incorporación al ADN permitió preguntar si importa el lugar donde ocurre una desintegración. Construimos una explicación enlazada desde el proceso nuclear y la semivida hasta la localización de la fuente, la formación simulada de lesiones y el destino de la célula. Contrastamos la pendiente HPRT de $0.45\times10^{-6}$ mutantes inducidos por cGy publicada para $^{131}$I en TK6, sin convertirla en riesgo individual ni en tasa de todo el genoma. El proyecto ofrece seis escenas interactivas, seis vídeos, un modelo Monte Carlo reproducible y verificaciones automáticas. La probabilidad de lesión, el tiempo de residencia, las tasas de reparación y el fondo de mutantes son hipótesis declaradas. La principal conclusión experimental es que la incorporación en ADN modifica la eficacia biológica bajo las condiciones de cultivo estudiadas; la simulación explica una posible cadena causal y sus límites.

**Palabras clave:** captura electrónica, electrones Auger, yodo-125, yodo-131, ADN humano, rotura doble, HPRT, Monte Carlo.

# Contenido y ruta de lectura

**Parte I.** Marco científico, artículo guía, derivaciones y límites (13 temas).  
**Parte II.** Seis apartados de exposición, uno por laboratorio y vídeo (01–06).  
**Parte III.** Métodos computacionales, resultados, sensibilidad y control de calidad.  
**Anexos.** Guion oral, glosario, referencias y código íntegro esencial.

Las etiquetas **[DATO]**, **[MODELO]** y **[EXTRAPOLACIÓN]** identifican la procedencia de cada cifra. Una prueba de que el programa funciona demuestra consistencia interna y reproducibilidad, no validez biológica externa.

# Parte I · Fundamento científico y desarrollo matemático

'''

scenes=r'''# Parte II · Seis apartados para exponer el trabajo

Cada apartado corresponde a una página interactiva y un vídeo corto. En la exposición, el vídeo introduce la idea y los controles permiten probar una pregunta. La duración audiovisual no representa tiempo físico. Es recomendable desarrollar con calma los apartados 04 y 06: son los que muestran con mayor claridad la transición desde la biología del ADN hasta un resultado experimental.

## 01 · Captura electrónica y cascada Auger

![Figura 1. Escena original del cambio nuclear y la desexcitación atómica](media/01_captura_y_Auger_portada.png)

**Pregunta al público.** «Si el yodo está en una molécula del ADN, ¿qué cambia cuando su núcleo se transforma?» La escena empieza con $^{125}_{53}\mathrm I+e^-\to{}^{125}_{52}\mathrm{Te}^{*}+\nu_e$. Dibuje 53 protones antes y 52 después; la suma de nucleones sigue siendo 125. En la pizarra, una captura de un electrón ligado crea una vacante atómica, mientras el núcleo hijo excitado puede desexcitarse. La transferencia de energía de una transición nuclear por conversión interna y la relajación de vacantes por rayos X o electrones Auger no son el mismo paso, aunque una secuencia pueda producir ambos [6].

**Demostración de pantalla.** Abra `01-captura-auger.html`. Mueva únicamente «Velocidad visual» (0,5–2,5×) y pulse «Repetir desintegración». El valor modifica la reproducción, no $\lambda$, la energía ni el número real de emisiones. Señale el neutrino, el núcleo transformado y la cascada. Pregunte dónde se produciría el daño si el padre se encontraba fuera de la célula. **Mensaje comprobable:** el artículo [1] describe el depósito de gran parte de la energía Auger dentro de 20 nm del sitio de desintegración; no afirma que todos los electrones recorran 20 nm exactamente.

**Explicación biológica.** La iododesoxiuridina es un análogo de timidina. En células que la incorporan, el átomo padre puede ocupar una posición próxima a la estructura del ADN. Al decaer nace Te en ese lugar inicial, pero el nuevo elemento no conserva necesariamente el enlace químico. El vídeo ilustra un origen local; no calcula química de radicales, trayectorias ni espectros. Cierre preguntando «¿cuánto debe esperar un átomo hasta decaer?», que enlaza con la escena 02.

## 02 · Semividas y competencia con la salida del ADN

![Figura 2. Dos relojes: desintegración nuclear y permanencia biológica](media/02_semividas_y_retencion_portada.png)

**Derivación en tres líneas.** Para una tasa instantánea constante, $dN/dt=-\lambda N$; integrar da $N(t)=N_0e^{-\lambda t}$ y $\lambda=\ln 2/T_{1/2}$. Las semividas tabuladas son 59,40 días para $^{125}$I y 8,021 días para $^{131}$I [7]. La actividad $A=\lambda N$ se expresa en Bq tras convertir la tasa a segundos. La semivida es una propiedad nuclear; la permanencia en ADN depende de procesos celulares no inferibles de ella.

**Modelo competidor.** Si salir del ADN tiene riesgo constante $k=1/\tau_b$, entonces $n(t)=n_0e^{-(\lambda+k)t}$ y la fracción inicial que decae antes de salir hasta $t$ es $\lambda(1-e^{-(\lambda+k)t})/(\lambda+k)$. Para $t\to\infty$, vale $\lambda/(\lambda+k)$. Con $\tau_b=2$ días **supuestos**, da 2,28 % para $^{125}$I y 14,74 % para $^{131}$I; no son fracciones medidas en TK6 [7]. La mayor probabilidad de decaer antes de salir en el segundo caso no significa por sí sola mayor efecto por desintegración.

**Demostración.** Abra `02-semividas-retencion.html`. Mueva el tiempo transcurrido entre 0 y 120 días: cambian dos curvas $N/N_0$. Mueva residencia media entre 0,5 y 15 días: cambia la fracción calculada antes de la salida, no las semividas. Haga comprobar el límite $k=0$ en la derivación: si no hay salida, todo átomo acaba decayendo allí en este modelo. La pregunta siguiente es «si decae en el ADN, ¿a qué distancia de cada hebra está?».

![Figura 3. Sensibilidad de la fracción local al tiempo medio de residencia hipotético](figuras_monografia/03_retencion_hipotetica.png)

## 03 · Distancia fuente–ADN y probabilidad de lesión

![Figura 4. Geometría esquemática de las dos hebras y la fuente](media/03_distancia_fuente_ADN_portada.png)

**Escala geométrica.** Sitúe una hélice ideal de 60 pares de bases con radio $R=1$ nm, incremento axial $h=0.34$ nm/pb y diez pb por vuelta. Para $j=0,\dots,59$, defina $\theta_j=2\pi(j-30)/10$ y $z_j=h(j-30)$. Las columnas se colocan en $(R\cos\theta_j,R\sin\theta_j,z_j)$ y $(-R\cos\theta_j,-R\sin\theta_j,z_j)$. La fuente se fija en $(R+d,0,0)$. Para $d=0$ coincide con el sitio central de la primera hebra; una fuente en el exterior a $d=4$ nm cambia todas las distancias $r_{X,j}$.

**Hipótesis espacial.** El perfil $q(r)=e^{-r/\ell}$ es un peso elegido. Si las oportunidades locales de daño fueran Poisson de media $\mu q(r)$, la probabilidad de una o más sería $p=1-e^{-\mu e^{-r/\ell}}$. Con $\mu=0.48$ y $\ell=1.5$ nm se ilustra la caída con distancia. $ℓ$ no es una longitud de recorrido único de electrones. Martin y Haseltine encontraron la mayor parte del daño en 15–20 Å y roturas detectables hasta 70 Å en un fragmento experimental diferente [2]; no se ajustó la curva a esos datos.

**Demostración.** Abra `03-distancia-adn.html`. Mueva $d$ (0–7 nm) manteniendo $\mu$ y $\ell$ fijos. Luego mueva $\mu$ (0,12–0,96) y $\ell$ (1–2,5 nm) por separado. La cifra superior es una frecuencia Monte Carlo del modelo, con 3500 ensayos en navegador; no es una observación de laboratorio. Pregunte por qué dos sitios de igual índice pueden tener distinta distancia a la fuente. La respuesta está en el desplazamiento transversal de las hebras. El apartado 04 convierte estas probabilidades en roturas agrupadas.

## 04 · Roturas agrupadas: del ADN lesionado a una DSB operativa

![Figura 5. Las dos hebras y el criterio de pareja de roturas](media/04_roturas_agrupadas_portada.png)

**Experimento virtual, paso a paso.** (1) Para cada una de las 120 posiciones (60 por hebra), calcule $r_j$ y $p_j$. (2) Genere un uniforme $U_j$ entre 0 y 1; marque rotura si $U_j<p_j$. (3) Busque una rotura $i$ en A y una $j$ en B con $|i-j|\leq10$ pb. (4) Registre 1 si existe al menos una pareja, o 0 si no. (5) Repita 15 000 veces en Python y estime $\widehat p=\sum I_k/n$. Se cuentan **eventos con al menos una pareja**; un evento con tres parejas no se cuenta tres veces. El umbral de diez pb es una definición operacional para esta demostración, no un diagnóstico de lesión molecular medido [1,2].

**Ejemplo para la pizarra.** Si A se rompe en 20 y B en 30, $|20-30|=10$: la regla puntúa DSB. Si B se rompe en 31, $|20-31|=11$: no puntúa. Si hay dos roturas en A y ninguna en B, tampoco puntúa. En `04-roturas-agrupadas.html`, pulse «Generar otra desintegración»: verá otra muestra individual. La cifra «P(DSB) Monte Carlo» recoge un conjunto de 3500 muestras con los controles actuales; un solo dibujo no es ese porcentaje. Con $d=0$, $\mu=0.48$ y $\ell=1.5$ nm, Python reporta $0.8700\pm0.00275$ (un error estándar) para 15 000 eventos. A $d=4$ nm reporta $0.07180\pm0.00211$.

**Explicación biológica.** Una lesión agrupada puede ser más difícil de resolver que una lesión aislada, pero el simulador no incluye química del agua, topología de cromatina, reparación real ni correlaciones de depósitos energéticos. Su independencia Bernoulli condicionada a la fuente fija es una simplificación fuerte. Martin y Haseltine [2] sirven para motivar proximidad; no calibran $\mu$, $\ell$ ni la cifra $0.87$. Una DSB tampoco equivale a mutación. Pase a la escena 05 preguntando qué puede hacer la célula con el daño.

![Figura 6. Probabilidad de rotura y DSB según distancia, resultado del modelo](figuras_monografia/01_distancia_y_roturas.png)

## 05 · Reparación, fijación de mutación y pérdida celular

![Figura 7. Cuatro estados de un modelo cinético de lesión](media/05_reparacion_y_mutacion_portada.png)

**Tres posibilidades mutuamente excluyentes en el esquema.** Partimos de $L(0)=1$ lesión no resuelta. Suponga tasas constantes de reparación $k_r=0.20$, fijación $k_m=0.02$ y pérdida celular $k_p=0.03$ h$^{-1}$; $K=0.25$ h$^{-1}$. Entonces $L=e^{-Kt}$ y los acumulados son $R=(k_r/K)(1-e^{-Kt})$, $M=(k_m/K)(1-e^{-Kt})$ y $C=(k_p/K)(1-e^{-Kt})$. Compruebe $L+R+M+C=1$ para cualquier $t\geq0$. A tiempo largo las fracciones elegidas serían 80 %, 8 % y 12 %, respectivamente. Son consecuencias de las tasas **supuestas**, no observaciones celulares.

**Demostración.** Abra `05-reparacion-mutacion.html`; mueva tiempo de 0 a 24 h y cada tasa por separado. Pregunte «¿por qué no puedo multiplicar 0,87 DSB del escenario por el 8 % y anunciar mutaciones HPRT?». Porque el primer número proviene de una hélice hipotética por evento, el segundo de un esquema de destino no calibrado, y HPRT mide un locus seleccionado entre células clonables. El diagrama sirve para separar lesión, reparación, supervivencia y fenotipo; no encadena porcentajes reales. El experimento de Whaley y Little midió muerte y mutación por separado [1].

![Figura 8. Evolución de las cuatro fracciones con tasas constantes supuestas](figuras_monografia/02_destinos_celulares.png)

## 06 · Experimento HPRT: qué se observó y qué se extrapola

![Figura 9. Comparación conceptual del ensayo de HPRT](media/06_experimento_HPRT_portada.png)

**Dos preguntas biológicas distintas.** TK6 incorpora eficientemente el análogo mediante la vía de timidina cinasa; SE30 es deficiente en esa incorporación. Esa es la comparación de *posición de fuente*. HPRT es otra enzima, de rescate de purinas; una pérdida funcional en el locus *hprt* permite detectar clones resistentes a selección con 6-tioguanina en ensayos apropiados [4,5]. Por tanto «SE30 deficiente en TK» no significa «SE30 mutante en HPRT». La supervivencia influye en cuántas células son clonables y debe corregirse en un ensayo real.

**Dato del artículo [1].** Para $^{131}$I–IdUrd en TK6, el resumen comunica $\alpha=0.45\times10^{-6}$ mutantes HPRT inducidos por cGy de dosis depositada en el núcleo. Para SE30 expuesta a actividad en el medio, comunica pocas mutaciones hasta dosis de 38 cGy. No dice que 38 cGy sea un punto medido de TK6 con una frecuencia de 17,1 por millón. **[EXTRAPOLACIÓN]** Si se usa la pendiente TK6 como recta en ese valor, $\Delta f=\alpha D=0.45\times10^{-6}\times38=17.1\times10^{-6}$, esto es 17,1 mutantes inducidos esperados por un millón de células clonables. A 1 Gy, la pendiente equivalente numéricamente es $45\times10^{-6}$ por Gy, pues 1 Gy = 100 cGy.

**Demostración.** Abra `06-experimento-hprt.html`. La dosis deslizable va de 0 a 40 cGy; el número hipotético de células clonables va de 0,5 a 5 millones. Si se duplica el número de células, se duplica el número *esperado* de mutantes inducidos, mientras la frecuencia por célula se conserva. El botón de recuento genera dos Poisson ilustrativos: fondo de $10\times10^{-6}$ por clonable y tratado con fondo + $\alpha D$. No son placas originales, recuentos del artículo, ni incertidumbre de la pendiente publicada. A 38 cGy y un millón, la media del control es 10, la del tratado 27,1 y la diferencia de medias 17,1; una réplica puede fluctuar y producir otra diferencia.

**Pregunta final.** «¿Qué haríamos para verificar el mecanismo en el laboratorio?» Medir incorporación real, dosis nuclear, supervivencia, distribución de roturas y secuenciar clones resistentes, con controles de fondo y eficiencia de clonación. La selección HPRT no informa automáticamente la posición de cada cambio en todo el genoma.

![Figura 10. Recta de la pendiente experimental y punto de extrapolación distinguido](figuras_monografia/04_hprt_extrapolacion.png)

'''

methods=r'''# Parte III · Método, validación y resultados auditables

## Arquitectura de cálculo y correspondencia entre los dos programas

`python/modelo.py` define constantes, funciones puras, geometría y muestreo; `python/verificar.py` controla casos límite, unidades y reproducibilidad. `science.js` reproduce las ecuaciones para navegador con otro generador pseudoaleatorio; `lab.js` conecta los deslizadores y dibuja el Canvas. `python/animar.py` crea seis vídeos pregrabados y portadas a partir de gráficos narrativos; **un MP4 no cambia cuando se mueven los controles**, mientras el Canvas sí. La visualización web ejecuta normalmente 3500 eventos por configuración; la tabla de referencia guardada por Python ejecutó 15 000 por distancia. Los porcentajes no tienen por qué coincidir al último decimal. Ambos programas usan la misma definición de lesión, pero NumPy y JavaScript no comparten secuencia de números aleatorios.

**Pseudocódigo exacto del núcleo Monte Carlo:**

```text
Entrada: d, μ, ℓ, n, semilla.
Calcular 60 coordenadas para cada una de las dos hebras.
Para cada hebra y sitio: r = distancia 3D a la fuente; p = 1 − exp(−μ exp(−r/ℓ)).
Crear n pares de vectores de 60 uniformes independientes con la semilla.
Para cada evento k: rotura_A[j] = (U_A[k,j] < p_A[j]); análogo en B.
Registrar una rotura cualquiera si existe al menos un sitio marcado.
Registrar DSB si existen i,j marcados en hebras opuestas con |i−j| ≤ 10.
Retornar proporciones por n y SEM = sqrt(p̂(1−p̂)/n).
```

Python genera una matriz común de uniformes para comparar distancias en una misma corrida. Esa correlación reduce el ruido de *diferencias entre escenarios*; el SEM mostrado para una proporción individual sigue siendo binomial. Para una comprobación analítica independiente, la independencia de Bernoulli por sitio implica $P(\text{alguna})=1-\prod_j(1-p_{A,j})\prod_j(1-p_{B,j})$. No hay una fórmula simple usada por el programa para el criterio de pareja DSB; se estima por muestreo.

## Tabla reproducible del escenario principal

Parámetros fijos: 60 pb, $R=1$ nm, 10 pb/vuelta, $\mu=0.48$, $\ell=1.5$ nm, criterio de separación $\leq10$ pb, semilla NumPy 2026 y $n=15,000$ eventos por distancia. Resultados extraídos del JSON del repositorio:

| d (nm) | P(al menos una rotura) | P(DSB) | SEM de P(DSB) | Eventos |
|---:|---:|---:|---:|---:|
| 0 | 0,99713 | 0,87000 | 0,00275 | 15 000 |
| 1 | 0,98167 | 0,68847 | 0,00378 | 15 000 |
| 2 | 0,90880 | 0,41560 | 0,00402 | 15 000 |
| 4 | 0,55587 | 0,07180 | 0,00211 | 15 000 |
| 7 | 0,12580 | 0,00200 | 0,00036 | 15 000 |

**Lectura:** el intervalo normal aproximado al 95 % sería $\widehat p\pm1.96\,SEM$ cuando funciona la aproximación; cerca de cero conviene Wilson o binomial exacto. El error de Monte Carlo no incluye la incertidumbre de $\mu$, $\ell$, la independencia por sitio ni la validez de la geometría.

## Sensibilidad: los parámetros importan más que el ruido numérico

Cada fila siguiente usa 6000 eventos en Python, semilla 2026. Al variar una hipótesis, se mantienen las otras en su valor base.

| Variación del modelo | P(DSB), d=0 nm | P(DSB), d=4 nm |
|---|---:|---:|
| $\mu=0.24$, $\ell=1.5$ nm | 0,53083 | 0,02167 |
| $\mu=0.96$, $\ell=1.5$ nm | 0,99333 | 0,21467 |
| $\mu=0.48$, $\ell=1.0$ nm | 0,59250 | 0,00317 |
| $\mu=0.48$, $\ell=2.0$ nm | 0,96250 | 0,30033 |

La distancia tiene un efecto cualitativo robusto dentro de estas elecciones, pero las magnitudes cambian fuertemente. No se ajustó ningún parámetro a un número experimental de DSB. Una predicción cuantitativa requeriría espectros de emisión, transporte a nanoescala, entorno químico, localización real y validación con datos.

## Verificaciones funcionales y límites de lo probado

Se ejecutaron con éxito los cinco controles de `python/verificar.py`, ocho pruebas de `tests/science.test.mjs` y la comprobación de 153 enlaces o recursos locales en siete HTML. Esas pruebas verifican, entre otros aspectos: $N(T_{1/2})=N_0/2$; signo de actividad; competencia temporal y límites; radio y avance de hélice; umbral de 10 frente a 11 pb; semilla reproducible; comparación analítica de alguna rotura; conservación de cuatro destinos; conversión cGy/Gy y el cálculo 17,1. El sitio utiliza HTML/CSS/JavaScript estáticos con Canvas 2D, sin servidor de cálculo ni base de datos. El visor ofrece texto alternativo y controles etiquetados; los vídeos MP4 pueden pausarse. Una prueba automatizada no sustituye leer y evaluar el artículo completo ni valida el modelo contra nuevos experimentos.

**Comandos, desde la raíz del repositorio:**

```bash
python -m pip install -r python/requirements.txt
python python/verificar.py
node --test tests/science.test.mjs
python tests/check_links.py
python python/modelo.py
python -m http.server 8000
```

El último comando permite abrir `http://localhost:8000/`; el sitio publicado está en [GitHub Pages](https://morganestampadoscol.github.io/radiogenoma-subatomica/). `python/modelo.py` crea `resultados/resumen_modelo.json`; el JSON de referencia ya generado reside en `documentacion/resumen_modelo.json`. Las seis portadas y los MP4 se entregan en `media/` y se regeneran con `python python/animar.py` si están instalados sus requisitos y FFmpeg.

## Alcance del resultado y conclusión

**[DATO]** TK6 y SE30 permiten estudiar el efecto de incorporar IdUrd radiactiva en ADN sobre muerte celular y HPRT bajo condiciones de cultivo [1]. **[MODELO]** La dependencia de distancia, la regla DSB, los destinos y la residencia son hipótesis explícitas que ayudan a pensar la causalidad. **[EXTRAPOLACIÓN]** La pendiente TK6 multiplicada por 38 cGy produce 17,1 por millón, pero ese punto no fue informado como medición TK6 en el resumen [1]. Ni la simulación ni el artículo permiten calcular mutación de todo el genoma, pronóstico clínico, riesgo de una persona expuesta o efecto de un accidente nuclear. El aporte académico está en construir una cadena explicativa verificable y reconocer dónde termina cada evidencia.

## Guion oral compacto de 10 minutos

| Minutos | Escena | Frase que se defiende |
|---|---|---|
| 0:00–0:45 | Portada y vídeo completo | «El lugar de la desintegración puede cambiar el efecto en ADN». |
| 0:45–2:00 | 01 | «$^{125}$I captura electrón, nace Te y sigue una relajación atómica». |
| 2:00–3:05 | 02 | «Semivida y residencia compiten, pero son relojes diferentes». |
| 3:05–4:10 | 03 | «La distancia se calcula en una geometría ideal y usa un perfil supuesto». |
| 4:10–5:30 | 04 | «Dos hebras: una pareja a ≤10 pb, repetida miles de veces». |
| 5:30–6:25 | 05 | «Una lesión puede repararse, fijarse o perderse con la célula». |
| 6:25–8:30 | 06 | «TK controla incorporación; HPRT lee mutantes; 17,1 es extrapolación». |
| 8:30–10:00 | Límites y cierre | «Núcleo: qué y cuándo; ADN: dónde; célula: qué persiste». |

**Dos apartados especialmente útiles para una exposición con más biología:** en 04 haga votar si las parejas 20–30 y 20–31 cuentan como DSB; en 06 pregunte qué diferencia hay entre perder una célula y seleccionar un clon mutante. Ambos dan participación sin ocultar el modelo físico.

## Glosario y comprobación de unidades

| Término | Significado en este trabajo |
|---|---|
| Bq | Una desintegración por segundo; actividad, no dosis. |
| Gy y cGy | Energía absorbida por masa, 1 Gy = 1 J/kg = 100 cGy. |
| SSB / DSB | Rotura simple / criterio operativo de roturas en hebras opuestas. |
| pb | Par de bases; 10 pb equivalen aproximadamente a 3,4 nm longitudinales en la hélice ideal. |
| TK / HPRT | Timidina cinasa para incorporación del análogo / enzima distinta cuyo locus se evalúa con mutantes resistentes. |
| SEM | Error estándar de la proporción Monte Carlo, no incertidumbre total del modelo. |
| $\mu$, $\ell$ | Oportunidades de daño (adimensional) y longitud de perfil (nm), elegidas. |
| $\lambda$, $k$ | Tasas de decaimiento y de salida, ambas en d$^{-1}$ en la escena 02. |
| $k_r,k_m,k_p$ | Tasas ilustrativas de destinos, en h$^{-1}$ en la escena 05. |

# Referencias

1. Whaley, J. M. y Little, J. B. (1990). “Efficient mutation induction by 125I and 131I decays in DNA of human cells”. *Radiation Research* **123**(1), 68–74. [PMID 2371380](https://pubmed.ncbi.nlm.nih.gov/2371380/); [DOI 10.2307/3577659](https://doi.org/10.2307/3577659). Los datos numéricos atribuidos se cotejaron con el resumen público; el texto íntegro puede requerir acceso institucional.
2. Martin, R. F. y Haseltine, W. A. (1981). “Range of radiochemical damage to DNA with decay of iodine-125”. *Science* **213**, 896–898. [PMID 7256283](https://pubmed.ncbi.nlm.nih.gov/7256283/); [DOI 10.1126/science.7256283](https://doi.org/10.1126/science.7256283).
3. LeMotte, P. K. y Little, J. B. (1984). “DNA damage induced in human diploid cells by decay of incorporated radionuclides”. *Cancer Research* **44**, 1337–1342. [PMID 6704953](https://pubmed.ncbi.nlm.nih.gov/6704953/).
4. O’Neill, J. P., Sullivan, L. M. y Albertini, R. J. (1990). “In vitro induction, expression and selection of thioguanine-resistant mutants with human T-lymphocytes”. *Mutation Research* **240**, 135–142. [PMID 2300074](https://pubmed.ncbi.nlm.nih.gov/2300074/).
5. NCBI Gene. “HPRT1 hypoxanthine phosphoribosyltransferase 1 [Homo sapiens]”. [Gene ID 3251](https://www.ncbi.nlm.nih.gov/gene/3251).
6. IAEA. *IAEA-TECDOC-1340*, ficha de $^{125}$I, sección 75. [Publicación oficial](https://www-pub.iaea.org/MTCD/publications/PDF/te_1340_web.pdf).
7. ICRP (2017). *Publication 137: Occupational Intakes of Radionuclides, Part 3*, tabla 5.1. [DOI 10.1177/0146645317734963](https://doi.org/10.1177/0146645317734963).
8. IAEA. *IAEA-TECDOC-1608*, sección 12.3: propiedades de $^{131}$I. [Publicación oficial](https://www-pub.iaea.org/MTCD/Publications/PDF/te_1608_web.pdf).
9. Schmitz, S. y colaboradores (2016). Corrección de “Chromosome aberrations induced by the Auger electron emitter 125I”. *Mutation Research* **800–801**, 46. [DOI 10.1016/j.mrgentox.2016.03.003](https://doi.org/10.1016/j.mrgentox.2016.03.003).
10. Sandoval, C. (2025-1). *Decays and scattering*. Diapositivas de Introducción a la física subatómica, Universidad Nacional de Colombia; material aportado al proyecto.
11. Sandoval, C. (2025-1). *Particle Detection, parte 2*. Diapositivas del mismo curso; material aportado al proyecto.

# Anexo A · Código íntegro del modelo Python

El código siguiente se transcribe de `python/modelo.py` en la revisión del repositorio. El bloque es ejecutable al copiarlo en ese archivo con NumPy instalado. La semilla fija permite reproducir el JSON. Los comentarios conservan la terminología del proyecto.

'''

md=cover+plain+'\n'+scenes+methods
md=md.replace('](media/', '](../media/')
md=md.replace('$^{125}$I','$^{125}\\mathrm{I}$').replace('$^{131}$I','$^{131}\\mathrm{I}$')
md=md.replace('$^{125}_{53}\\mathrm I+e^-\\to{}^{125}_{52}\\mathrm{Te}^{*}+\\nu_e$',
              '¹²⁵₅₃I + e⁻ → ¹²⁵₅₂Te* + νₑ')
md=md.replace('s$^{-1}$','s⁻¹').replace('h$^{-1}$','h⁻¹').replace('día$^{-1}$','día⁻¹')
md=md.replace('d$^{-1}$','d⁻¹')
md=md.replace('tiempo$^{-1}$','tiempo⁻¹')
md=md.replace('^{125}\\mathrm I','\\mathrm{I}_{125}').replace('^{131}\\mathrm I','\\mathrm{I}_{131}')
md=md.replace('^{125}\\mathrm{Te}','\\mathrm{Te}_{125}').replace('^{131}\\mathrm{Xe}','\\mathrm{Xe}_{131}')
md=md.replace('$$\\begin{aligned}\n\\frac{dL}{dt}&=-KL,&L(0)&=1,\\\\\n\\frac{dR}{dt}&=k_rL,&\\frac{dM}{dt}&=k_mL,&\\frac{dC}{dt}&=k_cL.\n\\end{aligned}$$',
'''$$\\frac{dL}{dt}=-KL,\\qquad L(0)=1.$$

$$\\frac{dR}{dt}=k_rL,\\qquad \\frac{dM}{dt}=k_mL,\\qquad \\frac{dC}{dt}=k_cL.$$''')
md=md.replace('$$\\begin{aligned}\n\\Delta f&=\\alpha D=(0.45\\times10^{-6}\\,\\mathrm{cGy}^{-1})(38\\,\\mathrm{cGy})\\\\\n&=17.1\\times10^{-6}=17.1\\text{ mutantes inducidos por millón de células clonables},\\\\\n38\\,\\mathrm{cGy}&=0.38\\,\\mathrm{Gy},\\qquad \\alpha=45\\times10^{-6}\\,\\mathrm{Gy}^{-1}.\n\\end{aligned}$$',
'''$$\\Delta f=\\alpha D=(0.45\\times10^{-6}\\,\\mathrm{cGy}^{-1})(38\\,\\mathrm{cGy})=17.1\\times10^{-6}.$$

Esto equivale a 17,1 mutantes inducidos por millón de células clonables. Además, $38\\,\\mathrm{cGy}=0.38\\,\\mathrm{Gy}$ y $\\alpha=45\\times10^{-6}\\,\\mathrm{Gy}^{-1}$.''')
for letter,title,path,language in [
    ('A','Modelo NumPy','python/modelo.py','python'),
    ('B','Verificaciones Python','python/verificar.py','python'),
    ('C','Núcleo de ciencia JavaScript','science.js','javascript'),
    ('D','Conexión de controles y Canvas','lab.js','javascript')]:
    if letter!='A': md+=f'\n# Anexo {letter} · {title}\n\n'
    md+=f'```{language}\n'+(ROOT/path).read_text(encoding='utf-8').rstrip()+'\n```\n'
md+='\n**Fin de la monografía.** Para ejecutar el atlas se requieren también los HTML, CSS y medios enlazados en el repositorio público; los anexos muestran completo el núcleo científico y su integración interactiva.\n'

target=OUT/'Monografia_RadioGenoma_Entrega.md'
target.write_text(md,encoding='utf-8')
print(f'{target}: {len(md.split())} palabras, {len(md.splitlines())} líneas')
