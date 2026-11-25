"""Genera dos fuentes XeLaTeX formales a partir de los textos auditados."""
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'documentacion'

PREAMBLE=r'''\documentclass[11pt,a4paper,oneside]{article}
\usepackage[margin=2.35cm,top=2.4cm,bottom=2.45cm,headheight=16pt]{geometry}
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{spanish}
\setmainfont{Noto Serif}
\setsansfont{DejaVu Sans}
\setmonofont{Noto Sans Mono}[Scale=0.83]
\usepackage{amsmath,amssymb,mathtools}
\usepackage{graphicx,xcolor,booktabs,longtable,array,tabularx,calc}
\usepackage{microtype,enumitem,fancyhdr,titlesec,caption,float}
\usepackage{hyperref}
\usepackage{minted}
\usepackage{newunicodechar}
\newunicodechar{✓}{{\fontspec{DejaVu Sans}✓}}
\definecolor{navy}{HTML}{142C40}
\definecolor{teal}{HTML}{087E83}
\definecolor{ochre}{HTML}{A76439}
\definecolor{codebg}{HTML}{F2F6F6}
\hypersetup{colorlinks=true,linkcolor=teal,urlcolor=teal,citecolor=teal,
 pdfauthor={Jhasbleidy Rodríguez Cárdenas; Sebastián Palacio},pdftitle={Cuando un radionúclido decae dentro del ADN humano}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus 1pt}
\emergencystretch=3em
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.17}
\titleformat{\section}{\sffamily\Large\bfseries\color{navy}}{\thesection}{.7em}{}
\titleformat{\subsection}{\sffamily\normalsize\bfseries\color{teal}}{\thesubsection}{.65em}{}
\titleformat{\subsubsection}{\sffamily\normalsize\bfseries\color{navy}}{\thesubsubsection}{.65em}{}
\titlespacing*{\section}{0pt}{21pt}{9pt}
\titlespacing*{\subsection}{0pt}{15pt}{6pt}
\captionsetup{font=small,labelfont={bf,color=teal},skip=6pt}
\renewcommand{\figurename}{Figura}
\renewcommand{\contentsname}{Índice general}
\renewcommand{\listfigurename}{Lista de figuras}
\setcounter{tocdepth}{2}
\setcounter{secnumdepth}{3}
\setkeys{Gin}{width=.94\linewidth,height=.31\textheight,keepaspectratio}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\sffamily\footnotesize\color{teal} RADIOGENOMA · FÍSICA SUBATÓMICA}
\fancyhead[R]{\sffamily\footnotesize\color{navy} ADN HUMANO}
\fancyfoot[C]{\sffamily\footnotesize\color{navy}\thepage}
\renewcommand{\headrulewidth}{.4pt}
\setminted{fontsize=\footnotesize,breaklines,breakanywhere,linenos,numbersep=5pt,
 tabsize=2,frame=lines,framesep=2mm,bgcolor=codebg,baselinestretch=1.0}
\begin{document}
'''

def clean_body(body: str) -> str:
    # El resumen y el índice se componen aparte; queda sólo el texto de fondo.
    body=body.split('# Resumen',1)[1]
    if '# Estructura de la versión T' in body:
        summary,rest=body.split('# Estructura de la versión T',1)
        body='# Resumen'+summary+'# Parte I'+rest.split('# Parte I',1)[1]
    else:
        summary,rest=body.split('# Contenido y ruta de lectura',1)
        body='# Resumen'+summary+'# Parte I'+rest.split('# Parte I',1)[1]
    body=body.split('# Anexo A',1)[0]
    return body

def fix_tables(tex: str) -> str:
    # Pandoc no puede recuperar las tres columnas de una tabla antigua
    # exportada a Markdown de ancho fijo; se restituye desde la fuente.
    pattern=r'\\begin\{longtable\}\[\]\{@\{\}lll@\{\}\}.*?\\end\{longtable\}'
    table=r'''\begin{table}[htbp]\centering\small
\begin{tabularx}{\linewidth}{@{}p{.20\linewidth}p{.28\linewidth}X@{}}
\toprule Sistema & Posición de la fuente & Resultado documentado en el resumen [1]\\\midrule
TK6 + $^{125}$I--IdUrd & Incorporación en ADN & Efectos tóxicos y mutagénicos pronunciados.\\
SE30 + $^{125}$I--IdUrd & Incorporación deficiente; actividad en el medio & Prácticamente sin efecto bajo las condiciones descritas.\\
TK6 + $^{131}$I--IdUrd & Incorporación en ADN & Pendiente HPRT inducida $0.45\times10^{-6}$ por cGy.\\
SE30 + $^{131}$I--IdUrd & Actividad en el medio & Pocas mutaciones hasta 38 cGy de dosis nuclear.\\\bottomrule
\end{tabularx}
\caption{Comparación de las dos líneas celulares en Whaley y Little [1].}
\end{table}'''
    tex,count=re.subn(pattern,lambda _:table,tex,count=1,flags=re.S)
    if count!=1: raise ValueError('No se encontró la tabla comparativa original')
    # La tabla de seis escenas sufrió el mismo problema en la exportación previa.
    pattern2=r'\\begin\{longtable\}\[\]\{@\{\}lll@\{\}\}.*?\\end\{longtable\}'
    if re.search(pattern2,tex,flags=re.S):
        scene=r'''\begin{table}[htbp]\centering\footnotesize
\begin{tabularx}{\linewidth}{@{}p{.20\linewidth}p{.34\linewidth}X@{}}
\toprule Escena & Representación & Interpretación\\\midrule
01 Captura y Auger & $^{125}$I a $^{125}$Te y cascada atómica & Se separan cambio nuclear y relajación electrónica.\\
02 Dos relojes & $N/N_0$ y salida hipotética & Semivida nuclear y residencia no son iguales.\\
03 Distancia & Geometría y perfil $q(r)$ & La longitud $\ell$ es un parámetro ilustrativo.\\
04 Dos hebras & Bernoulli por sitio y ventana de 10 pb & La DSB es un criterio operacional del modelo.\\
05 Destinos & $L+R+M+C=1$ & Lesión, reparación y mutación son variables distintas.\\
06 HPRT & TK6 frente a SE30 & Se distingue pendiente publicada y extrapolación.\\\bottomrule
\end{tabularx}
\caption{Correspondencia entre las seis visualizaciones y las cantidades científicas.}
\end{table}'''
        tex=re.sub(pattern2,lambda _:scene,tex,count=1,flags=re.S)
    return tex

def make(stem: str, version: str):
    md=(DOC/f'{stem}.md').read_text(encoding='utf-8')
    source=DOC/f'{stem}.tex'
    body=clean_body(md)
    body=body.replace('⁻', '$^{-}$')
    body=body.replace('¹²⁵₅₃I + e$^{-}$(ligado) → ¹²⁵₅₂Te* + νₑ',
                      '$^{125}_{53}\\mathrm{I}+e^-_{\\mathrm{ligado}}\\to{}^{125}_{52}\\mathrm{Te}^*+\\nu_e$')
    tmp=DOC/f'.{stem}_cuerpo.md'
    tmp.write_text(body,encoding='utf-8')
    try:
        tex=subprocess.check_output(['pandoc','-f','markdown+tex_math_dollars','-t','latex','--no-highlight','--wrap=none',str(tmp)],text=True)
    finally: tmp.unlink()
    tex=fix_tables(tex)
    tex=tex.replace('→', r'\(\to\)').replace('≤', r'\(\leq\)')
    tex=tex.replace(r'\(ℓ\)',r'\(\ell\)')
    tex=tex.replace('ℓ','ell')
    tex=tex.replace(r'\texttt{python/modelo.py}',r'\path{python/modelo.py}')
    tex=tex.replace(r'\texttt{python/verificar.py}',r'\path{python/verificar.py}')
    tex=tex.replace(r'\texttt{resultados/resumen\_modelo.json}',r'\path{resultados/resumen_modelo.json}')
    tex=tex.replace(r'\texttt{resultados/resumen_modelo.json}',r'\path{resultados/resumen_modelo.json}')
    tex=tex.replace('\\texttt{tests/science.test.mjs}', r'\path{tests/science.test.mjs}')
    tex=tex.replace(r'\href{https://doi.org/10.1016/j.mrgentox.2016.03.003}{DOI 10.1016/j.mrgentox.2016.03.003}',
                    r'\href{https://doi.org/10.1016/j.mrgentox.2016.03.003}{\nolinkurl{DOI 10.1016/j.mrgentox.2016.03.003}}')
    tex=tex.replace('.png}', '.png}')
    for name in ['01_distancia_y_roturas','02_destinos_celulares','03_retencion_hipotetica','04_hprt_extrapolacion']:
        tex=tex.replace(f'figuras_monografia/{name}.png',f'figuras_monografia/{name}.pdf')
    tex=tex.replace('\\begin{figure}', '\\begin{figure}[htbp]')
    tex=re.sub(r'\\caption\{Figura (?:T)?\d+\. ',r'\\caption{',tex)
    # El resumen queda fuera de la numeración principal, como en una monografía.
    tex=tex.replace('\\section{Resumen}\\label{resumen}',
                    '\\section*{Resumen}\\addcontentsline{toc}{section}{Resumen}')
    extra=(DOC/'desarrollo_extenso.tex').read_text(encoding='utf-8')
    heading_refs=r'\section{Referencias}\label{referencias}'
    if heading_refs not in tex: raise ValueError('No se encontró bibliografía')
    tex=tex.replace(heading_refs,extra+'\n'+heading_refs,1)
    refs=r'''
\item Schmitz, S., Oskamp, D., Pomplun, E. y Kriehuber, R. (2015).
``Chromosome aberrations induced by the Auger electron emitter 125I''.
\emph{Mutation Research} \textbf{793}, 64--70.
\href{https://pubmed.ncbi.nlm.nih.gov/26520374/}{PMID 26520374};
\href{https://doi.org/10.1016/j.mrgentox.2015.08.007}{DOI 10.1016/j.mrgentox.2015.08.007}.
Debe leerse junto con el corrigendum [9].
\item Mariani, G. y colaboradores (1993). ``Tumor targeting in vivo and metabolic
fate of 5-[iodine-125]iodo-2'-deoxyuridine following intratumoral injection in
patients with colorectal cancer''. \emph{Journal of Nuclear Medicine} \textbf{34},
1175--1183. \href{https://pubmed.ncbi.nlm.nih.gov/8315499/}{PMID 8315499}.
\item Rebischung, C. y colaboradores (2008). ``First human treatment of resistant
neoplastic meningitis by intrathecal administration of MTX plus 125IUdR''.
\emph{International Journal of Radiation Biology} \textbf{84}, 1123--1129.
\href{https://pubmed.ncbi.nlm.nih.gov/19061137/}{PMID 19061137};
\href{https://doi.org/10.1080/09553000802395535}{DOI 10.1080/09553000802395535}.
\item IAEA, material técnico de medicina nuclear. Esquema de ramas de
$^{131}$I con endpoint beta de 606,3 keV y rama intensa de aproximadamente
89,9\%. \href{https://www.iaea.org/sites/default/files/22/06/drls_and_activity_calibrators.pdf}{Presentación técnica oficial}.
'''
    head,sep,tail=tex.rpartition('\\end{enumerate}')
    if not sep: raise ValueError('No se encontró cierre de referencias')
    tex=head+refs+sep+tail
    heading='Versión T · desarrollo teórico y computacional' if version=='T' else 'Monografía y seis apartados de exposición'
    cover=rf'''\begin{{titlepage}}
\thispagestyle{{empty}}
\color{{navy}}
\vspace*{{1cm}}
{{\sffamily\large\bfseries UNIVERSIDAD NACIONAL DE COLOMBIA\par}}
{{\sffamily Departamento de Física · Física Subatómica\par}}
\vspace{{1.6cm}}
{{\sffamily\Huge\bfseries Cuando un radionúclido decae dentro del ADN humano\par}}
\vspace{{.5cm}}
{{\sffamily\Large\color{{teal}} {heading}\par}}
\vspace{{.8cm}}
\color{{teal}}\rule{{\linewidth}}{{1.4pt}}\color{{navy}}
\vspace{{.5cm}}
\begin{{center}}\includegraphics[width=.88\textwidth]{{../media/04_roturas_agrupadas_portada.png}}\end{{center}}
\vfill
{{\sffamily\large Proyecto RadioGenoma\par}}
{{\sffamily Jhasbleidy Rodríguez Cárdenas · Sebastián Palacio\par}}
{{\sffamily Profesor: Jhon Morales Aponte\par}}
{{\sffamily Bogotá, Colombia · 25 de noviembre de 2026\par}}
\vspace{{.5cm}}
{{\small Artículo conductor: Whaley y Little (1990). Figuras y simulaciones propias;
las estimaciones del modelo se distinguen de datos publicados.\par}}
\end{{titlepage}}
\pagenumbering{{roman}}
\begingroup\footnotesize\tableofcontents\endgroup
\clearpage
\listoffigures
\clearpage
\pagenumbering{{arabic}}
'''
    appendix=r'''\clearpage
\appendix
\section{Código completo del modelo Python}
El siguiente archivo se reproduce literalmente desde el repositorio y genera el
resumen numérico con NumPy. Los parámetros no ajustados permanecen identificados
en los comentarios.
\inputminted{python}{../python/modelo.py}
\clearpage
\section{Pruebas de conservación, unidades y reproducibilidad}
\inputminted{python}{../python/verificar.py}
\clearpage
\section{Núcleo científico interactivo en JavaScript}
Este núcleo usa las mismas ecuaciones que Python. El navegador y NumPy emplean
generadores de números pseudoaleatorios distintos.
\inputminted{javascript}{../science.js}
\clearpage
\section{Controles y visualizaciones Canvas}
\inputminted{javascript}{../lab.js}
\clearpage
\section{Generación de las figuras físicas ampliadas}
\inputminted{python}{../python/figuras_ampliacion.py}
\clearpage
\section{Generación de las seis animaciones MP4}
\inputminted{python}{../python/animar.py}
\end{document}
'''
    source.write_text(PREAMBLE+cover+tex+'\n'+appendix,encoding='utf-8')
    print(source, len(tex.split()),'palabras en cuerpo')

make('Monografia_RadioGenoma_Entrega','E')
make('Monografia_RadioGenoma_Version_T','T')
