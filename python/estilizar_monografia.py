"""Aplica diseño editorial a la monografía DOCX creada con Pandoc."""
from pathlib import Path
import sys
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
file=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'documentacion'/'Monografia_RadioGenoma_Entrega.docx'
doc=Document(file)
styles_by_name={s.name:s for s in doc.styles}
sec=doc.sections[0]
sec.top_margin=Cm(2.1);sec.bottom_margin=Cm(2.05)
sec.left_margin=Cm(2.3);sec.right_margin=Cm(2.1)
sec.header_distance=Cm(.9);sec.footer_distance=Cm(.95)
sec.different_first_page_header_footer=True

NAVY=RGBColor(18,38,61);TEAL=RGBColor(8,126,131);MID=RGBColor(74,93,108)
for name in ['Normal','Body Text','First Paragraph']:
    s=styles_by_name[name];s.font.name='DejaVu Serif';s.font.size=Pt(9.7);s.font.color.rgb=NAVY
    s.paragraph_format.space_after=Pt(6);s.paragraph_format.line_spacing=1.16
for name,size,color in [('Heading 1',16,NAVY),('Heading 2',12.6,TEAL),('Heading 3',10.7,NAVY)]:
    s=styles_by_name[name];s.font.name='DejaVu Sans';s.font.bold=True;s.font.size=Pt(size);s.font.color.rgb=color
    s.paragraph_format.space_before=Pt(17 if name=='Heading 1' else 11)
    s.paragraph_format.space_after=Pt(7);s.paragraph_format.keep_with_next=True
for name in ['Image Caption','Captioned Figure','Compact']:
    s=styles_by_name[name];s.font.name='DejaVu Sans';s.font.size=Pt(8.4);s.font.color.rgb=MID
    s.paragraph_format.space_after=Pt(6)
code=styles_by_name['Source Code'];code.font.name='DejaVu Sans Mono';code.font.size=Pt(7.4);code.font.color.rgb=NAVY
code.paragraph_format.line_spacing=1.0;code.paragraph_format.space_after=Pt(5)

for i,p in enumerate(doc.paragraphs):
    if i==0:
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(46)
        for run in p.runs:run.font.size=Pt(22);run.font.color.rgb=NAVY
    elif i==1:
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:run.font.size=Pt(13.2);run.font.color.rgb=TEAL
    elif i in (2,3,5,6):
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after=Pt(15)
        if i==2:
            for run in p.runs:run.font.name='DejaVu Sans';run.font.size=Pt(9.4)
    if p.text=='Resumen':p.paragraph_format.page_break_before=True
    if p.style.name=='Heading 1' and p.text.startswith(('Parte I','Parte II','Parte III','Referencias','Anexo ')):
        p.paragraph_format.page_break_before=True
    if p.style.name=='Source Code':
        pPr=p._p.get_or_add_pPr();shd=OxmlElement('w:shd');shd.set(qn('w:fill'),'F2F6F6');pPr.append(shd)
        for r in p.runs:r.font.name='DejaVu Sans Mono';r.font.size=Pt(7.4)

for t in doc.tables:
    t.autofit=True
    for idx,row in enumerate(t.rows):
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_after=Pt(2)
                for r in p.runs:
                    r.font.name='DejaVu Sans';r.font.size=Pt(8.3);r.font.color.rgb=NAVY
                    if idx==0:r.font.bold=True
            if idx==0:
                tcPr=cell._tc.get_or_add_tcPr();shd=OxmlElement('w:shd');shd.set(qn('w:fill'),'DFF0EF');tcPr.append(shd)

header=sec.header.paragraphs[0]
header.text='RADIOGENOMA  /  FÍSICA SUBATÓMICA  ·  ADN HUMANO'
header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for run in header.runs:run.font.name='DejaVu Sans';run.font.size=Pt(7.5);run.font.color.rgb=MID
footer=sec.footer.paragraphs[0]
footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
run=footer.add_run('UNAL · 2026   |   ')
run.font.name='DejaVu Sans';run.font.size=Pt(8);run.font.color.rgb=MID
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
doc.save(file)
print(file)
