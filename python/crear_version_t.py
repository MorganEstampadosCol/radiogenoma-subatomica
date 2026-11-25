"""Construye la versión T en prosa académica desde la monografía auditada."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'documentacion'
source=(OUT/'Monografia_RadioGenoma_Entrega.md').read_text(encoding='utf-8')
foundation=source.split('# Parte I · Fundamento científico y desarrollo matemático',1)[1].split('# Parte II · Seis apartados para exponer el trabajo',1)[0]
foundation=re.sub(r'## Resultados reproducibles y lectura de las seis animaciones.*?(?=## Vínculo preciso con el programa)', '',foundation,flags=re.S)
foundation=foundation.replace('## Conclusión defendible','## Síntesis del marco teórico')
methods=source.split('# Parte III · Método, validación y resultados auditables',1)[1]
methods=re.sub(r'## Guion oral compacto de 10 minutos.*?(?=## Glosario y comprobación de unidades)', '',methods,flags=re.S)
methods=methods.replace('## Arquitectura de cálculo y correspondencia entre los dos programas','## Arquitectura de cálculo y correspondencia entre los dos programas')
methods=methods.replace('**Dos apartados especialmente útiles para una exposición con más biología:** en 04 haga votar si las parejas 20–30 y 20–31 cuentan como DSB; en 06 pregunte qué diferencia hay entre perder una célula y seleccionar un clon mutante. Ambos dan participación sin ocultar el modelo físico.','')

front=r'''# Cuando un núcleo decae dentro del ADN humano

## Versión T · Monografía teórica, matemática y computacional

**RADIOGENOMA · VERSIÓN T DE ENTREGA**  
**Universidad Nacional de Colombia · Física Subatómica**  
**Equipo:** Proyecto de Física Subatómica  
**Bogotá, Colombia · 25 de noviembre de 2026**

**Artículo conductor:** Whaley y Little, *Radiation Research* **123** (1990), 68–74 [1].

![Esquema original del proyecto: localización de la desintegración y ADN](../media/01_captura_y_Auger_portada.png)

**Objeto de estudio.** La eficacia biológica de una desintegración de yodo radiactivo cuando el átomo padre está incorporado en un análogo de nucleósido del ADN humano. Se estudian explícitamente la física nuclear, la localización de la fuente, la formación idealizada de roturas, la reparación y la lectura de mutantes HPRT. El código científico íntegro se transcribe en los anexos y el programa completo permanece en el [repositorio RadioGenoma](https://github.com/MorganEstampadosCol/radiogenoma-subatomica).

# Resumen

Esta monografía reconstruye una cadena causal desde la captura electrónica de $^{125}$I y el decaimiento beta menos de $^{131}$I hasta los efectos celulares observables cuando estos radionúclidos se incorporan a iododesoxiuridina. El experimento de Whaley y Little [1] comparó dos líneas linfoblastoides humanas con diferente capacidad de incorporar el análogo al ADN, TK6 y SE30, y cuantificó supervivencia y mutantes del locus *hprt*. Se deriva la ley exponencial y un modelo de dos riesgos competitivos para distinguir semivida de residencia celular. Una geometría idealizada de 60 pares de bases permite definir distancias tridimensionales, probabilidades fenomenológicas de rotura y un criterio operacional de rotura doble. Se implementan simulaciones Monte Carlo con semilla fija, error estándar, control analítico, sensibilidad de parámetros y pruebas automatizadas. Las ecuaciones de reparación y mutación representan estados competidores con tasas declaradamente hipotéticas. La única pendiente experimental de mutantes utilizada como dato numérico es $0.45\times10^{-6}$ por cGy para $^{131}$I–IdUrd en TK6 [1]. Se documenta por qué el producto de esta pendiente por 38 cGy es una extrapolación aritmética y no un dato experimental de TK6 a 38 cGy. El resultado es una herramienta explicativa reproducible, sin atribución de riesgo clínico ni de mutaciones del genoma completo.

**Palabras clave:** física subatómica; captura electrónica; beta menos; Auger; daño agrupado; ADN; HPRT; Monte Carlo; riesgos competitivos.

# Estructura de la versión T

La primera parte establece la evidencia, las definiciones y las ecuaciones físicas. La segunda desarrolla seis capítulos científicos enlazados, cada uno con mecanismos, derivación e interpretación. La tercera presenta resultados, verificación y limitaciones. Los anexos contienen referencias y código completo del modelo numérico, sus pruebas y la implementación interactiva. En todo momento se distingue entre **dato publicado**, **hipótesis de modelo** y **extrapolación**.

# Parte I · Contexto experimental y fundamentos

'''

chapters=r'''# Parte II · Desarrollo científico de seis mecanismos

## Capítulo 1. Captura electrónica, transmutación y relajación atómica

El primer nivel de descripción consiste en identificar qué cambia dentro del núcleo. Un isótopo conserva su número de protones $Z$ y se diferencia por su número de neutrones. El yodo tiene $Z=53$. En $^{125}$I, una transformación por captura electrónica toma un electrón de una capa ligada y convierte un protón nuclear en neutrón. Así, el número de nucleones $A=125$ permanece constante, mientras el núcleo resultante tiene $Z=52$ y pertenece al elemento telurio. Escribimos el proceso, omitiendo en esta línea las energías de excitación y retroceso, como

$$\mathrm I(125,53)+e^-_{\rm ligado}\longrightarrow \mathrm{Te}^{*}(125,52)+\nu_e.$$

La carga inicial total del sistema «núcleo + electrón» es $+53e-e=+52e$; el núcleo final tiene carga $+52e$ y el neutrino no lleva carga. El electrón inicial tiene número leptónico electrónico $+1$ y el neutrino final también. Esta contabilidad evita interpretar la captura como una emisión de electrón beta. La interacción débil gobierna la transformación protón–neutrón. La relajación posterior de la configuración atómica y la conversión interna involucran interacciones electromagnéticas y deben describirse por separado [6,10].

Si $M_a$ indica la masa del átomo neutro en estado fundamental, la energía disponible se define por $Q_{EC}=[M_a(\mathrm I_{125})-M_a(\mathrm{Te}_{125})]c^2$. Para la captura desde una capa de energía de enlace $B_i$, y un estado nuclear hijo de excitación $E_*$, el balance esquemático es

$$Q_{EC}=E_{\nu,i}+E_*+B_i+T_R+\delta_{\rm at},$$

donde $T_R$ es el retroceso y $\delta_{\rm at}$ representa correcciones atómicas pequeñas según la convención de masas y vacantes usada. Reordenar da $E_{\nu,i}\simeq Q_{EC}-E_*-B_i-T_R$ cuando se desprecia $\delta_{\rm at}$. La igualdad no adjudica a cada electrón Auger una energía igual a $Q_{EC}$. El neutrino transporta parte de la energía; el núcleo puede desexcitarse por emisión gamma o por conversión interna; la vacante electrónica se rellena mediante radiación característica o transferencia de energía a otro electrón. Cada vacante adicional puede alimentar una nueva transición. La ficha de IAEA para $^{125}$I da la semivida y la línea gamma de aproximadamente 35,49 keV con intensidad minoritaria [6]. Una línea gamma nuclear no es la energía común de los electrones Auger.

La posición inicial del núcleo hijo coincide con la posición del padre en el instante de la transformación dentro de la precisión de escala molecular pertinente. Esto permite afirmar que las emisiones y la relajación comienzan localmente si el padre estaba en ADN. No permite afirmar que Te permanezca químicamente enlazado después de la ionización múltiple, ni que los electrones sigan trayectorias radiales rectas. En Whaley y Little, el contraste central no es la persistencia del enlace del hijo, sino la diferencia de efecto entre desintegraciones de un análogo incorporado y actividad extracelular [1].

![Figura T1. Esquema narrativo original de captura y cascada; no representa un espectro medido](../media/01_captura_y_Auger_portada.png)

## Capítulo 2. Dos escalas temporales: desintegración y permanencia

Para derivar la ley nuclear no se presupone que todos los átomos decaigan en un momento único. Se supone una probabilidad condicional $\lambda\,dt+o(dt)$ de que un átomo todavía no desintegrado decaiga entre $t$ y $t+dt$, con $\lambda$ constante. En un conjunto de $N(t)$ núcleos, el número medio de pérdidas en ese intervalo es $\lambda N(t)dt$. Se obtiene sucesivamente

$$N(t+dt)-N(t)=-\lambda N(t)dt+o(dt),$$

$$\frac{dN}{dt}=-\lambda N,\qquad \frac{dN}{N}=-\lambda dt,$$

$$\ln N(t)-\ln N_0=-\lambda t,\qquad N(t)=N_0e^{-\lambda t}.$$

La semivida se define por $N(T_{1/2})/N_0=1/2$. Por tanto $\exp(-\lambda T_{1/2})=1/2$, de donde $-\lambda T_{1/2}=-\ln2$ y finalmente $\lambda=\ln2/T_{1/2}$. La vida media temporal $\tau_n=1/\lambda$ no coincide con la semivida: $\tau_n=T_{1/2}/\ln2$. La actividad $A=-dN/dt=\lambda N$ es positiva. Cuando $\lambda$ se ha obtenido en días$^{-1}$, la actividad en Bq requiere dividir la tasa por 86 400 segundos/día. Las semividas físicas tabuladas de 59,40 y 8,021 días para $^{125}$I y $^{131}$I, respectivamente, proceden de ICRP [7].

Ahora se introduce un segundo mecanismo: un átomo incorporado puede abandonar el compartimento que llamamos «ADN» antes de decaer. Si la salida es exponencial con riesgo constante $k$ por día e independiente del mecanismo nuclear, la fracción que todavía está incorporada y sin decaer al tiempo $t$ cumple $dn/dt=-(\lambda+k)n$. La solución $n(t)=n_0e^{-(\lambda+k)t}$ describe la población que conserva ambas condiciones. El número medio de decaimientos locales que ocurre en un intervalo $dt$ es $\lambda n(t)dt$. Al integrar desde 0 hasta $t$ y dividir por $n_0$,

$$P_{\rm local}(t)=\frac{1}{n_0}\int_0^t\lambda n_0e^{-(\lambda+k)s}ds
=\frac{\lambda}{\lambda+k}\left(1-e^{-(\lambda+k)t}\right).$$

El límite de tiempo largo es $P_{\rm local}(\infty)=\lambda/(\lambda+k)$. Si se habla de **residencia media** $\tau_b$, la tasa correspondiente es $k=1/\tau_b$; sólo si se hablara de una *semivida biológica* sería $k=\ln2/T_{b,1/2}$. Confundir esos dos tiempos introduciría un factor $\ln2$ erróneo. Para $\tau_b=2$ días elegidos hipotéticamente, $k=0.5$ d$^{-1}$ y resultan $P_{125}=0.022806$ y $P_{131}=0.147364$. El segundo átomo tiene, en ese esquema de salida, mayor posibilidad de desintegrarse antes de abandonar el ADN por su semivida nuclear más corta; la intensidad del daño **por decaimiento local** sigue siendo otra pregunta. Este modelo no ajusta una cinética biológica de las líneas TK6 o SE30.

![Figura T2. Predicción de los dos riesgos en función de una residencia media supuesta](figuras_monografia/03_retencion_hipotetica.png)

## Capítulo 3. Geometría del ADN y ley fenomenológica de lesión

La proximidad requiere una definición geométrica y una unidad. «Diez pares de bases» cuenta posiciones sucesivas en la secuencia; «diez nanómetros» expresa una longitud. En la representación ideal escogida, el avance axial es $h=0.34$ nm por par, de modo que una separación de diez índices corresponde a 3,4 nm **axiales**. Las hebras se sitúan también a distintas coordenadas transversales. Se modelan 60 posiciones por hebra y una vuelta cada diez pares de bases. Para $j\in\{0,\ldots,59\}$ se fija

$$\theta_j=\frac{2\pi(j-30)}{10},\qquad z_j=0.34(j-30)\,\mathrm{nm}.$$

Con un radio $R=1$ nm, las coordenadas de las dos columnas ideales son $\mathbf x_{A,j}=(R\cos\theta_j,R\sin\theta_j,z_j)$ y $\mathbf x_{B,j}=(-R\cos\theta_j,-R\sin\theta_j,z_j)$. El código ubica la fuente en $\mathbf s=(R+d,0,0)$, con $d\geq0$ en nm. Para cada sitio, $r_{X,j}=\|\mathbf x_{X,j}-\mathbf s\|$ se calcula mediante la raíz de la suma de cuadrados de las tres diferencias de coordenadas. Si $d=0$, $\mathbf x_{A,30}=\mathbf s$ y $r_{A,30}=0$, mientras $r_{B,30}=2R=2$ nm. Es una comprobación de geometría del código, no la distancia de un átomo real a una estructura atómica resuelta.

Se necesita convertir las distancias en probabilidades para simular lesiones. El proyecto elige un peso $q(r)=\exp(-r/\ell)$, donde $\ell>0$ controla qué tan rápido decrece el peso. La función no es un espectro de electrones ni la ley de atenuación de un material macroscópico. Postulamos que en un sitio existen oportunidades de rotura con conteo Poisson de media $\mu q(r)$, con $\mu\geq0$ adimensional. En una Poisson de media $a$, $P(K=0)=e^{-a}$. Por complemento,

$$P(K\geq1)=1-P(K=0)=1-e^{-a}
=1-\exp\left[-\mu\exp(-r/\ell)\right].$$

Esta última expresión define $p_{X,j}$ para cada hebra y cada índice. En $r=0$ vale $1-e^{-\mu}$ y cuando $r\to\infty$ tiende a cero. Para valores pequeños de $\mu q$, la expansión $e^{-x}=1-x+O(x^2)$ da $p\simeq\mu e^{-r/\ell}$; cuando $\mu$ crece mucho, $p$ se satura hacia uno y deja de aumentar linealmente. Martin y Haseltine [2] observaron la mayor parte del daño a 15–20 Å y roturas detectables hasta 70 Å en otro sistema experimental. Esa observación motiva una pregunta espacial, pero no determina $\ell=1.5$ nm ni $\mu=0.48$ utilizados en la figura. No se ha ajustado ninguno de ellos a datos del artículo guía.

![Figura T3. Esquema de hélice ideal y distancia de la fuente](../media/03_distancia_fuente_ADN_portada.png)

## Capítulo 4. De roturas simples a una rotura doble operacional

Una variable de Bernoulli toma los valores 0 o 1. Para cada sitio simulado, el programa obtiene un uniforme $U_{X,j}$ entre cero y uno y define $B_{X,j}=1$ si $U_{X,j}<p_{X,j}$, o $B_{X,j}=0$ en otro caso. Condicionadas a los parámetros fijos, estas variables se sortean independientemente. Una rotura simple queda representada por un 1 en una hebra. La simplificación separa los sitios matemáticamente, aunque una cascada real puede producir daños correlacionados por electrones, radicales y estructura de cromatina.

La DSB de este trabajo es una variable indicadora de evento. Vale 1 exactamente si **existe** al menos una pareja de posiciones $(i,j)$ tales que $B_{A,i}=B_{B,j}=1$ y $|i-j|\leq10$. Vale cero si no existe tal pareja. Una rotura en A20 y otra en B30 da distancia de índices 10 y cumple la regla; B31 produciría 11 y no la cumple. Dos roturas en la misma hebra no la cumplen. La expresión «existe» importa porque un evento puede contener numerosas parejas: el programa cuenta una sola vez que **hubo** DSB y no confunde el número de parejas con la probabilidad del evento.

Para $n$ repeticiones del mismo escenario se define $I_k\in\{0,1\}$ como resultado del evento $k$. El estimador es $\widehat p=n^{-1}\sum_{k=1}^{n}I_k$. Bajo independencia entre repeticiones, $E(\widehat p)=p$ y $\mathrm{Var}(\widehat p)=p(1-p)/n$. Se reemplaza $p$ por $\widehat p$ para informar $SEM=\sqrt{\widehat p(1-\widehat p)/n}$. El «intervalo» $\widehat p\pm1.96SEM$ es una aproximación normal de incertidumbre **de muestreo**; si $p$ está muy cerca de cero o uno, conviene un intervalo de Wilson o exacto. No cubre el error de un modelo físico inadecuado.

Hay un control independiente para «alguna rotura». Dado que cada sitio se sortea de manera independiente, la probabilidad de no romper ninguno es $\prod_{X,j}(1-p_{X,j})$; por complemento $P(\text{alguna rotura})=1-\prod_{X,j}(1-p_{X,j})$. Para DSB no basta multiplicar probabilidades de parejas y sumar: dos o más parejas pueden coexistir. El algoritmo busca si aparece al menos una pareja y repite miles de veces. Con 15 000 eventos por distancia y semilla 2026, el escenario base da $\widehat p_{DSB}(0)=0.8700$ y $\widehat p_{DSB}(4)=0.0718$. Como cambiar $\mu$ y $\ell$ modifica mucho esos valores, no se interpretan como rendimientos biológicos universales.

![Figura T4. Definición operacional de pareja en dos hebras](../media/04_roturas_agrupadas_portada.png)

![Figura T5. Estimaciones del Monte Carlo según distancia, con error de muestreo](figuras_monografia/01_distancia_y_roturas.png)

## Capítulo 5. Cinética de lesión, reparación y destinos competidores

La ocurrencia de un daño no equivale a una mutación detectada. Una célula puede reparar la lesión, fijar un cambio heredable en una descendencia clonable o perderse del conjunto que se puede evaluar. La simulación representa estas alternativas con un estado inicial $L(0)=1$ y tres salidas acumuladas $R(0)=M(0)=C(0)=0$. Se postulan riesgos constantes no negativos $k_r$, $k_m$ y $k_c$ por hora y se define $K=k_r+k_m+k_c$. En un intervalo $dt$, la lesión no resuelta pierde una fracción $KLdt$. Por ello

$$\frac{dL}{dt}=-KL,\qquad L(t)=e^{-Kt}.$$

La probabilidad acumulada de reparación cambia a razón $dR/dt=k_rL(t)$. Integrando desde cero,

$$R(t)=\int_0^tk_re^{-Ks}ds
=\frac{k_r}{K}\left(1-e^{-Kt}\right).$$

Con idéntico procedimiento se obtienen $M(t)=k_m(1-e^{-Kt})/K$ y $C(t)=k_c(1-e^{-Kt})/K$. La conservación se demuestra sin datos empíricos: $L+R+M+C=e^{-Kt}+(k_r+k_m+k_c)(1-e^{-Kt})/K=1$. El tiempo característico de resolución del estado inicial es $1/K$. Para $k_r=0.20$, $k_m=0.02$ y $k_c=0.03$ h$^{-1}$ elegidos, $K=0.25$ h$^{-1}$ y $1/K=4$ h. Al tomar $t\to\infty$, las fracciones resultan 0,80, 0,08 y 0,12. Éstas se fijaron indirectamente al elegir las tasas; no son frecuencias medidas de los cultivos del artículo [1].

La variable $M$ debe leerse como estado de «fijación» dentro de un esquema matemático. Para demostrar una mutación experimental hay que dejar transcurrir expresión fenotípica, corregir supervivencia y selección, y analizar clones. Una DSB puede repararse fielmente, repararse con cambio, participar en un reordenamiento o impedir la clonación. Por eso no se multiplica la probabilidad DSB simulada por $0.08$ y se afirma haber predicho la frecuencia de HPRT. Las dos cantidades provienen de módulos con supuestos diferentes y sin calibración conjunta.

![Figura T6. Estados celulares acumulados bajo tasas ilustrativas](figuras_monografia/02_destinos_celulares.png)

## Capítulo 6. Ensayo HPRT: diseño celular, dosis y estadística del recuento

La pregunta experimental exige separar la vía de incorporación de la variable de salida. La timidina cinasa (TK) permite incorporar el análogo nucleosídico mediante la ruta de salvamento de timidina. TK6 es competente y SE30 es deficiente para esa capacidad en el diseño descrito por Whaley y Little [1]. Esta comparación cambia la probabilidad de situar la fuente en el ADN. En cambio, *hprt* designa un locus distinto: HPRT participa en el rescate de purinas y puede utilizarse en la selección de clones resistentes a 6-tioguanina cuando se pierde función. HPRT1 humano está en el cromosoma X [4,5]. La deficiencia de TK en SE30 no significa que HPRT sea la misma enzima o que todos sus clones ya sean HPRT mutantes.

En un ensayo de clonación idealizado, si se siembran $n$ células por pocillo, cada una tiene frecuencia $f$ de fenotipo resistente y probabilidad $\varepsilon$ de generar una colonia bajo selección. Para eventos raros e independientes se aproxima el número de clones resistentes por Poisson de media $nf\varepsilon$. La probabilidad de no observar colonia es $P_0=e^{-nf\varepsilon}$. Al tomar logaritmo y despejar,

$$\ln P_0=-nf\varepsilon,\qquad f=-\frac{\ln P_0}{n\varepsilon}.$$

Así se hace visible por qué el número de células sembradas y la eficiencia de clonación importan. La ecuación describe un mecanismo de lectura posible, no reconstruye los pocillos específicos del artículo de Whaley y Little. La frecuencia mutante se estima entre células capaces de crecer bajo condiciones apropiadas; la muerte celular es otro resultado experimental [1,4].

El resumen público de Whaley y Little informa una pendiente inducida de $\alpha=0.45\times10^{-6}$ mutantes HPRT por cGy de dosis nuclear para $^{131}$I–IdUrd en células TK competentes [1]. El mismo resumen señala pocas mutaciones en células TK deficientes hasta 38 cGy cuando las desintegraciones de $^{131}$I ocurren en el medio. Para explorar unidades se define $f(D)=f_0+\alpha D$. El fondo $f_0=10\times10^{-6}$ usado en el código es una hipótesis didáctica. En $D=38$ cGy, el exceso **calculado** sería $\alpha D=17.1\times10^{-6}$, equivalente a 17,1 por millón de células clonables; no se presenta como dato TK6 medido exactamente a 38 cGy. La dosis es una energía absorbida por masa: $1$ Gy = $1$ J/kg y $1$ Gy = 100 cGy. La pendiente numérica por Gy correspondiente es $45\times10^{-6}$, porque $\alpha_{Gy}(0.38\,Gy)=\alpha_{cGy}(38\,cGy)$.

El recuento ilustrativo usa $Y_0\sim\mathrm{Poisson}(nf_0)$ y $Y_D\sim\mathrm{Poisson}(n[f_0+\alpha D])$. Si ambos son independientes, $E(Y_D-Y_0)=n\alpha D$ y $\mathrm{Var}(Y_D-Y_0)=n(2f_0+\alpha D)$. Con $n=10^6$ y el fondo supuesto, las medias son 10 y 27,1, pero un par de recuentos generados puede diferir de esas medias. El proyecto no reestima $\alpha$ ni su incertidumbre a partir de datos crudos. Una extrapolación lineal tampoco permite convertir mutantes HPRT en riesgo de cáncer, secuencia de todo el genoma o frecuencia de mutación humana individual.

![Figura T7. Comparación conceptual de las dos líneas celulares y la selección HPRT](../media/06_experimento_HPRT_portada.png)

![Figura T8. Pendiente experimental informada y punto extrapolado a 38 cGy](figuras_monografia/04_hprt_extrapolacion.png)

'''

doc=front+foundation+'\n'+chapters+'# Parte III · Resultados, implementación y crítica\n\n'+methods
doc=doc.replace('_{\\rm ligado}','_{\\mathrm{ligado}}').replace('_{\\rm at}','_{\\mathrm{at}}').replace('_{\\rm local}','_{\\mathrm{local}}')
doc=doc.replace('La entrega incluye código, resultados y seis vídeos narrativos aptos para proyección.','La entrega incluye código, resultados y figuras reproducibles.')
doc=doc.replace('exposición tipo congreso','análisis académico')
doc=doc.replace('Qué explicar frente al público','Interpretación científica')
doc=doc.replace('guion','esquema')
path=OUT/'Monografia_RadioGenoma_Version_T.md'
path.write_text(doc,encoding='utf-8')
print(path,len(doc.split()),'palabras',len(doc.splitlines()),'líneas')
