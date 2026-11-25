"""PDF de lectura del manuscrito LaTeX sin depender de una instalación TeX."""
from pathlib import Path
import html,re,subprocess,tempfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextParser
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate,Frame,Image,PageBreak,PageTemplate,Paragraph,Spacer,Table,TableStyle

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'documentacion'
PDF=DOC/'Guia_Proyecto_ADN_Subatomica.pdf'
BUILD=DOC/'.build'
BUILD.mkdir(exist_ok=True)
PLAIN=BUILD/'_lectura_pandoc.txt'
FORMULAS=BUILD/'formulas'
FORMULAS.mkdir(exist_ok=True)
citations={'whaley':'Whaley y Little, 1990','martin':'Martin y Haseltine, 1981',
 'lemotte':'LeMotte y Little, 1984','iaea125':'IAEA, TECDOC-1340',
 'iaea131':'IAEA, TECDOC-1608','icrp':'ICRP, 2017','curso':'Sandoval, 2025-1',
 'deteccion':'Sandoval, 2025-1','corrigendum':'Schmitz et al., 2016',
 'oneill':'O’Neill et al., 1990','gene':'NCBI Gene, HPRT1'}
tex=(DOC/'guia.tex').read_text(encoding='utf8')
tex=re.sub(r'\\cite\{([^}]+)\}',lambda m:' ('+'; '.join(citations.get(k,k) for k in m.group(1).split(','))+')',tex)
with tempfile.TemporaryDirectory() as temp:
    source=Path(temp)/'lectura.tex'
    source.write_text(tex,encoding='utf8')
    subprocess.run(['pandoc','-f','latex','-t','plain','--wrap=none',str(source),'-o',str(PLAIN)],check=True,stderr=subprocess.DEVNULL)
plain=PLAIN.read_text(encoding='utf8')
pdfmetrics.registerFont(TTFont('DejaVu',str(Path(matplotlib.get_data_path())/'fonts/ttf/DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',str(Path(matplotlib.get_data_path())/'fonts/ttf/DejaVuSans-Bold.ttf')))
NAVY=colors.HexColor('#0B1D32'); TEAL=colors.HexColor('#087E83'); MID=colors.HexColor('#53717B')
styles={
'text':ParagraphStyle('text',fontName='DejaVu',fontSize=9.05,leading=14.4,alignment=TA_JUSTIFY,spaceAfter=7),
'h1':ParagraphStyle('h1',fontName='DejaVu-Bold',fontSize=16,leading=20,textColor=NAVY,spaceBefore=18,spaceAfter=10,keepWithNext=True),
'h2':ParagraphStyle('h2',fontName='DejaVu-Bold',fontSize=11,leading=15,textColor=TEAL,spaceBefore=12,spaceAfter=6,keepWithNext=True),
'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8,leading=12,textColor=MID,spaceAfter=6),
'coverTitle':ParagraphStyle('coverTitle',fontName='DejaVu-Bold',fontSize=27,leading=35,textColor=colors.white,spaceAfter=10),
'coverSub':ParagraphStyle('coverSub',fontName='DejaVu',fontSize=13,leading=21,textColor=colors.HexColor('#BFD6D9'),spaceAfter=8)}
SECTIONS=['El problema, su interés y una respuesta comprobable','Artículo guía: diseño, resultados y lectura crítica',
'Núcleo y curso: de la tasa a la actividad','¹²⁵I: captura electrónica y cascada Auger',
'¹³¹I: beta menos y un espectro continuo','Un átomo puede abandonar el ADN antes de decaer',
'Geometría del ADN y modelo explícito de daño','Después del daño: tres destinos que compiten',
'Del locus HPRT a un conteo interpretable','Resultados reproducibles y lectura de las seis animaciones',
'Vínculo preciso con el programa','Utilidad, analogías prudentes y limitaciones',
'Conclusión defendible','Guía de defensa breve: preguntas y respuestas']
SUBSECTIONS=['Motivación','Pregunta y objetivos','Hipótesis y resultado principal','Derivación completa de la ley exponencial',
'Ramas de decaimiento y amplitud cuántica','Conservación de números cuánticos',
'Balance de energía, sin simplificar electrones inexistentes','¿Se queda el núcleo hijo unido al ADN?','Tiempo físico','Escala y coordenadas',
'De un peso espacial a una Bernoulli de rotura','Criterio DSB y estimación Monte Carlo',
'De energía a dosis: qué representa un gray','Control analítico: rotura en cualquier sitio',
'Resultados del escenario base y sensibilidad']
def norm(s):return ' '.join(s.replace('\u2005',' ').replace('\u2006',' ').split())
def parag(s,style='text'):
    s=html.escape(s).replace('[DATO]','<font color="#087E83"><b>[DATO]</b></font>').replace('[MODELO]','<font color="#AF642B"><b>[MODELO]</b></font>')
    return Paragraph(s,styles[style])
def formula_png(raw,index):
    t=raw.strip().removeprefix('$$').removesuffix('$$').strip()
    t=re.sub(r'\\begin\{(?:aligned|gathered|split)\}|\\end\{(?:aligned|gathered|split)\}','',t)
    t=re.sub(r'\\label\{[^}]*\}','',t).replace('\\boxed{','{').replace('\\qquad','\\;\\;')
    t=t.replace('\\text{','\\mathrm{').replace('\\textbf{','\\mathrm{')
    t=t.replace('\\bigl','').replace('\\bigr','')
    lines=[l.strip().replace('&','').strip().rstrip(',.') for l in re.split(r'\\\\|\n',t) if l.strip()]
    parser=MathTextParser('agg');good=[]
    for l in lines:
        if 'mutantes' in l:
            l=r'=17.1\times10^{-6}=17.1/10^{6}'
        try: parser.parse('$'+l+'$',dpi=110);good.append(('$'+l+'$',True))
        except Exception:good.append((l.replace('\\,',' ').replace('\\;',' '),False))
    if not good:good=[('(ver la fuente LaTeX)',False)]
    fig=plt.figure(figsize=(10,max(.65,.46*len(good))),dpi=170,facecolor='white')
    for j,(line,is_math) in enumerate(good):
        fig.text(.015,1-(j+.65)/len(good),line,fontsize=13 if is_math else 10,fontfamily='DejaVu Sans',color='#0b4257',va='center')
    path=FORMULAS/f'ecuacion_{index:02d}.png';fig.savefig(path,dpi=170,bbox_inches='tight',pad_inches=.18);plt.close(fig)
    return path
class Guide(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=A4,leftMargin=54,rightMargin=54,topMargin=54,bottomMargin=53,
                         title='Cuando un núcleo decae dentro del ADN humano',author='Equipo de Física Subatómica')
        w,h=A4;frame=Frame(54,53,w-108,h-104,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='normal',frames=[frame],onPage=self.background)])
    def background(self,canvas,doc):
        w,h=A4
        if doc.page==1:
            canvas.setFillColor(NAVY);canvas.rect(0,0,w,h,fill=1,stroke=0)
            canvas.setFillColor(colors.HexColor('#54D9CA'));canvas.rect(0,0,12,h,fill=1,stroke=0)
            canvas.setStrokeColor(colors.HexColor('#17314A'))
            for j in range(13):canvas.line(85,85+j*23,w-60,85+j*23)
            canvas.setFillColor(colors.HexColor('#1C5065'));canvas.circle(w-120,h-180,72,fill=1,stroke=0)
            canvas.setFillColor(colors.HexColor('#54D9CA'));canvas.circle(w-120,h-180,43,fill=1,stroke=0)
        else:
            canvas.setFillColor(NAVY);canvas.rect(0,h-29,w,29,fill=1,stroke=0)
            canvas.setFont('DejaVu',7.5);canvas.setFillColor(colors.white);canvas.drawString(54,h-19,'FÍSICA SUBATÓMICA  /  ADN HUMANO')
            canvas.setFillColor(TEAL);canvas.rect(54,35,w-108,2,fill=1,stroke=0)
            canvas.setFont('DejaVu',8);canvas.setFillColor(MID);canvas.drawRightString(w-54,23,str(doc.page))
story=[Spacer(1,105),parag('UNIVERSIDAD NACIONAL DE COLOMBIA','coverSub'),Spacer(1,38),
       parag('Cuando un núcleo decae dentro del ADN humano','coverTitle'),
       parag('De la captura electrónica a las lesiones, la reparación y las mutaciones HPRT','coverSub'),
       Spacer(1,66),parag('Guía científica y matemática · exposición tipo congreso','coverSub'),
       parag('Artículo guía: Whaley y Little, 1990','coverSub'),Spacer(1,80),
       parag('Equipo de Física Subatómica · Noviembre de 2026','coverSub'),PageBreak()]
story += [parag('Resumen','h1'),parag('Una fuente radiactiva incorporada en ADN humano puede producir efectos distintos de la misma actividad situada en el medio. Whaley y Little (1990) compararon las células TK6 y SE30 con iododesoxiuridina marcada con yodo-125 o yodo-131. Esta guía deriva el decaimiento, explora la distancia fuente–ADN con una simulación identificada como hipótesis y distingue daño, reparación y mutación HPRT. La pendiente experimental de 0,45 × 10⁻⁶ mutantes inducidos por cGy corresponde a yodo-131 en TK6; ninguna frecuencia simulada se presenta como medida humana.'),
          Spacer(1,10),parag('Mapa de lectura','h1')]
for idx,name in enumerate(SECTIONS,1):story.append(parag(f'{idx:02d}   {name}','small'))
story.append(PageBreak())
body='El problema, su interés y una respuesta comprobable\n\n'+plain.split('El problema, su interés y una respuesta comprobable',1)[1]
parts=re.split(r'(\$\$.*?\$\$)',body,flags=re.S)
formula_index=0;section_num=0
for part in parts:
    if part.startswith('$$'):
        formula_index+=1;path=formula_png(part,formula_index)
        from PIL import Image as PILImage
        im=PILImage.open(path);natural_w,natural_h=im.size
        width=min(480,natural_w*.35);height=width*natural_h/natural_w
        story.extend([Spacer(1,3),Image(str(path),width=width,height=height),Spacer(1,7)]);continue
    for block in part.split('\n\n'):
        block=block.strip()
        if not block:continue
        line=norm(block)
        if line.startswith('99 J. M. Whaley'):
            story.append(parag('Referencias y artículo guía','h1'))
            for r in [
                'Whaley, J. M. y Little, J. B. (1990). Efficient mutation induction by 125I and 131I decays in DNA of human cells. Radiation Research 123, 68–74. DOI 10.2307/3577659. PMID 2371380.',
                'Martin, R. F. y Haseltine, W. A. (1981). Range of radiochemical damage to DNA with decay of iodine-125. Science 213, 896–898. DOI 10.1126/science.7256283.',
                'LeMotte, P. K. y Little, J. B. (1984). DNA damage induced in human diploid cells by decay of incorporated radionuclides. Cancer Research 44, 1337–1342. PMID 6704953.',
                'O’Neill, J. P., Sullivan, L. M. y Albertini, R. J. (1990). In vitro induction, expression and selection of thioguanine-resistant mutants with human T-lymphocytes. Mutation Research 240, 135–142. PMID 2300074.',
                'NCBI Gene. HPRT1, Homo sapiens. Gene ID 3251.',
                'IAEA: TECDOC-1340 (yodo-125); TECDOC-1608 (yodo-131). ICRP Publication 137 (2017).',
                'Schmitz et al. (2016). Corrigendum. DOI 10.1016/j.mrgentox.2016.03.003.',
                'Sandoval, C. (2025-1). Decays and scattering; Particle Detection, parte 2. UNAL.']:
                story.append(parag(r,'small'))
            continue
        if line in SECTIONS:
            section_num+=1;story.append(parag(f'{section_num:02d}  {line}','h1'))
            if section_num==2:
                rows=[['Sistema','Ubicación','Hallazgo del artículo'],
                    ['TK6 + ¹²⁵IIdUrd','ADN','Efectos tóxicos y mutagénicos.'],
                    ['SE30 + ¹²⁵IIdUrd','Incorporación deficiente','Prácticamente sin efecto descrito.'],
                    ['TK6 + ¹³¹IIdUrd','ADN','Pendiente 0,45 × 10⁻⁶ por cGy.'],
                    ['SE30 + ¹³¹IIdUrd','Medio','Pocas mutaciones hasta 38 cGy.']]
                data=[[parag(c,'small') for c in row] for row in rows]
                tbl=Table(data,colWidths=[125,120,235],repeatRows=1,hAlign='LEFT')
                tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DBF3F0')),
                  ('GRID',(0,0),(-1,-1),.4,colors.HexColor('#B4C9C9')),('VALIGN',(0,0),(-1,-1),'TOP'),
                  ('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5)]))
                story.extend([tbl,Spacer(1,11)])
            if section_num==10:
                details=[['Escena','Modelo visual','Explicación breve'],
                  ['01  Captura','I-125 a Te-125','Captura, vacante y Auger.'],
                  ['02  Relojes','N(t), salida biológica','Semivida y residencia difieren.'],
                  ['03  Geometría','q(r) elegido','Peso espacial hipotético.'],
                  ['04  Roturas','Bernoulli por sitio','Parejas en hebras opuestas.'],
                  ['05  Destinos','L + R + M + C = 1','Daño no significa mutación.'],
                  ['06  HPRT','TK6 frente a SE30','Dato observado y extrapolación.']]
                visual=Table([[parag(v,'small') for v in row] for row in details],colWidths=[107,168,205],repeatRows=1)
                visual.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DBF3F0')),
                  ('GRID',(0,0),(-1,-1),.4,colors.HexColor('#B4C9C9')),('VALIGN',(0,0),(-1,-1),'TOP'),
                  ('LEFTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),4)]))
                story.extend([visual,Spacer(1,11)])
            if section_num==7:story.append(Image(str(ROOT/'media'/'04_roturas_agrupadas_portada.png'),width=475,height=267))
            continue
        if line in SUBSECTIONS:
            story.append(parag(line,'h2'))
            if line=='Resultados del escenario base y sensibilidad':
                rows=[['d [nm]','P(al menos una)','P(DSB)','SEM'],
                   ['0','0,99713','0,87000','0,00275'],['1','0,98167','0,68847','0,00378'],
                   ['2','0,90880','0,41560','0,00402'],['4','0,55587','0,07180','0,00211'],
                   ['7','0,12580','0,00200','0,00036']]
                t=Table([[parag(c,'small') for c in row] for row in rows],colWidths=[82,150,120,128])
                t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DBF3F0')),
                  ('GRID',(0,0),(-1,-1),.4,colors.HexColor('#B4C9C9')),('LEFTPADDING',(0,0),(-1,-1),6),
                  ('TOPPADDING',(0,0),(-1,-1),3)]))
                story.extend([t,Spacer(1,10)])
            continue
        if block.startswith('Sistema') or block.startswith('TK6 + ¹²⁵IIdUrd') or block.startswith('-------------------------------------------------'):continue
        if line.startswith('La regla sobre dos hebras') or line.startswith('Escena Lo que cambia') or line.startswith('d [nm] P(') or line=='[]':continue
        story.append(parag(line))
Guide(PDF).build(story)
print(f'Guía PDF: {PDF} | fórmulas: {formula_index}')
