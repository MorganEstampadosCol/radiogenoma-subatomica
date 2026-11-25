# RADIOGENOMA · Atlas interactivo de Física Subatómica

**Cuando un núcleo decae dentro del ADN humano** — proyecto de Física Subatómica, Universidad Nacional de Colombia, noviembre de 2026.

Una web estática, adaptable al móvil y compatible con **GitHub Pages**, con portada editorial, doble hélice animada en Canvas 2D, seis laboratorios ajustables, seis MP4 originales y un desarrollo matemático en PDF, LaTeX y Python. **No requiere servidor, base de datos, claves ni compilación.**

## Recorrido propuesto

| Escena | Animación interactiva | Qué es observado y qué es supuesto |
|---|---|---|
| [01 · Captura electrónica](./01-captura-auger.html) | ¹²⁵I → ¹²⁵Te; captura y emisión Auger | Modo de decaimiento nuclear conocido; trayectorias ilustrativas |
| [02 · Semividas y retención](./02-semividas-retencion.html) | ¹²⁵I / ¹³¹I, N/N₀ y competencia con salida | Semividas tabuladas; residencia en ADN **hipotética** |
| [03 · Distancia al ADN](./03-distancia-adn.html) | Modelo B-ADN 60 pb; distancia, μ, ℓ ajustables | Geometría ideal y perfil de daño **propuesto**, no transporte de electrones |
| [04 · Roturas agrupadas](./04-roturas-agrupadas.html) | Monte Carlo de SSB y DSB con criterio ≤10 pb | Modelo probabilístico Bernoulli **didáctico** |
| [05 · Reparación y mutación](./05-reparacion-mutacion.html) | Riesgos competitivos de tres salidas | Tasas **hipotéticas**, no estimaciones clínicas |
| [06 · Ensayo HPRT](./06-experimento-hprt.html) | Pendiente experimental TK6 y recuentos Poisson | Pendiente real publicada; proyecciones y fondo **ilustrativos** |

## Artículo científico conductor

> Whaley, J. M., & Little, J. B. (1990). **Efficient mutation induction by 125I and 131I decays in DNA of human cells.** *Radiation Research, 123*(1), 68–74. DOI: [10.2307/3577659](https://doi.org/10.2307/3577659); [PubMed PMID 2371380](https://pubmed.ncbi.nlm.nih.gov/2371380/).

El estudio comparó líneas celulares humanas **TK6** (competentes para incorporar el análogo vía timidina cinasa) y **SE30** (deficientes) con iododesoxiuridina marcada con ¹²⁵I y ¹³¹I, midiendo efectos sobre supervivencia y mutaciones HPRT. La pendiente informada para ¹³¹I-IdUrd en TK6 fue de **0,45 × 10⁻⁶ mutantes inducidos/cGy** de dosis nuclear. Las pocas mutaciones observadas hasta 38 cGy pertenecen al escenario **SE30**; multiplicar la pendiente TK6 por 38 cGy y obtener 17,1 mutantes inducidos por millón es **una extrapolación aritmética**, **no una medición directa de TK6 a 38 cGy**.

Referencias de soporte: [Martin & Haseltine (1981), PMID 7256283](https://pubmed.ncbi.nlm.nih.gov/7256283/) y [ICRP Publication 137](https://doi.org/10.1177/0146645317734963).

## Repositorio y archivos

```text
RADIOGENOMA_GitHubPages/
├── index.html                   ← portada y recorrido
├── 01-captura-auger.html        ← laboratorios 01–06, páginas independientes
├── 02-semividas-retencion.html
├── 03-distancia-adn.html
├── 04-roturas-agrupadas.html
├── 05-reparacion-mutacion.html
├── 06-experimento-hprt.html
├── styles.css                   ← sistema visual adaptable
├── hero.js                      ← hélice portada
├── science.js                   ← ecuaciones puras y muestreo reproducible
├── lab.js                       ← visualizaciones y controles Canvas 2D
├── media/                       ← 6 MP4 + portadas + vídeo completo
├── documentacion/               ← PDF, LaTeX, artículo guía, guion, auditoría, JSON
├── python/                      ← modelo original, animador y verificaciones
├── tests/                       ← tests Node y smoke test en navegador
├── .github/workflows/ci.yml     ← pruebas automáticas en GitHub Actions
└── .nojekyll                    ← GitHub Pages publica todo el sitio tal cual
```

## Publicarlo en GitHub Pages

**Si se acaba de crear un repositorio nuevo, se recomienda hacerlo público para que la web sea accesible a cualquiera**. No se debe modificar ni reutilizar ningún repositorio comercial preexistente.

1. En la cuenta deseada de GitHub, crea un repositorio **nuevo y vacío** llamado `radiogenoma-subatomica` (puede ser público). No actives README automático.
2. **Descomprime** este ZIP y sube **el contenido de la carpeta raíz** del paquete al repositorio, manteniendo la estructura (especialmente `index.html` en la raíz). Mediante interfaz de GitHub: `Add file → Upload files`, arrastra los archivos y carpetas descomprimidos y confirma `Commit changes`. Git en terminal también sirve.
3. En el repositorio entra a `Settings → Pages`. En `Build and deployment`, selecciona `Deploy from a branch`, rama `main`, carpeta `/ (root)` y guarda.
4. La dirección esperada será `https://TU_USUARIO.github.io/radiogenoma-subatomica/`. **Esta URL no se considera publicada hasta que GitHub Pages la confirme.**
5. La acción de verificación en `.github/workflows/ci.yml` valida los modelos y enlaces internos en cada `push`.

Para ejecutar localmente, basta con abrir `index.html`. Algunos navegadores pueden aplicar restricciones a módulos ES cuando usan `file://`; en ese caso usa:

```sh
python -m http.server 8000
# abre http://localhost:8000/
```

No se requiere ningún `npm install`; únicamente Node.js para las pruebas:

```sh
npm test
python -m pip install numpy
python python/verificar.py
python tests/check_links.py
```

Para regenerar los resultados del proyecto original:

```sh
python -m pip install -r python/requirements.txt
python python/modelo.py
python python/animar.py
```

**Nota:** el modelo original guarda sus resultados en `resultados/` al ejecutarse. El archivo de referencia que acompaña esta entrega está conservado en `documentacion/resumen_modelo.json`. Las animaciones MP4 incluidas ya están codificadas; regenerarlas requiere FFmpeg instalado.

## Qué calculan realmente las seis escenas

La probabilidad del modelo espacial es

\[
 p_j=1-\exp\left[-\mu\exp(-r_j/\ell)\right]
\]

con `μ=0.48`, `ℓ=1.5 nm`, radio ideal del ADN `R=1 nm`, avance `0.34 nm/bp` y ventana de `60 bp`. Se generan Bernoulli independientes por sitio y se declara DSB **solo si** hay al menos una rotura de cada hebra a una distancia longitudinal de `≤10 bp`. El porcentaje resultante es un valor **condicional al escenario elegido**, no una predicción del rendimiento físico real.

La fracción de emisores que decae antes de salir del ADN se representa con dos riesgos exponenciales independientes:

\[
 P_{\mathrm{decae\ antes\ de\ salir}}=\frac{\lambda}{\lambda+k_s},\qquad
 \lambda=\frac{\ln 2}{T_{1/2}},\quad k_s=\frac{1}{\tau}.
\]

La reparación se representa como tres salidas competitivas de una lesión inicial. Las tasas elegidas, `kᵣ=0.20/h`, `kₘ=0.02/h` y `kₚ=0.03/h`, son **supuestos pedagógicos**.

## Alcance y límites

- **Sí**: modos de desintegración, constante de decaimiento, actividad, geometría, probabilidades, estadísticas, procesos competitivos, comparación con una fuente experimental publicada y derivaciones.
- **No**: dosimetría individual, daño cuantitativo del genoma humano completo, radiobiología clínica, simulación Geant4/track-structure, predicción de cáncer, tasas de mutaciones en personas o riesgo de exposición en Chernóbil.
- Se conservan los artículos **como enlaces**; no se redistribuye el PDF de la revista.

**Correspondencia de datos:** `science.js` es una traducción didáctica de ecuaciones en `python/modelo.py`; sus números de sorteo no tienen por qué coincidir bit a bit con NumPy porque emplean generadores pseudoaleatorios distintos. Las propiedades analíticas y el orden esperado sí se prueban automáticamente.

## Validación

- Pruebas JavaScript: **7** controles de tasas, semivida, conservación, geometría, muestreo y unidades.
- Pruebas Python originales: **5** controles, con modelo reproducible.
- Prueba automatizada de enlaces locales: `python tests/check_links.py`.
- Prueba de interfaz: `python tests/browser_smoke.py` (opcional; usa Chromium + Playwright), realizada para tamaños **1440 × 900** y **390 × 844**.

Material preparado como proyecto educativo de Física Subatómica, no como producto sanitario o calculadora de riesgos.
