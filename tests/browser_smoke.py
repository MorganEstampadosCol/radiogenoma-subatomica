"""QA sin red: inspecciona HTML + CSS y ejecuta los módulos inline en Chromium.
Opcional: pip install playwright; requiere navegador Chromium instalado.
"""
from pathlib import Path
import re,base64,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
PAGES=['index.html','01-captura-auger.html','02-semividas-retencion.html','03-distancia-adn.html','04-roturas-agrupadas.html','05-reparacion-mutacion.html','06-experimento-hprt.html']
css=re.sub(r"@import url\('.*?'\);",'',(ROOT/'styles.css').read_text(),count=1)
science_data='data:text/javascript;base64,'+base64.b64encode((ROOT/'science.js').read_bytes()).decode()
with sync_playwright() as p:
 launch={'headless':True,'args':['--no-sandbox']}
 if os.environ.get('CHROMIUM_PATH'):launch['executable_path']=os.environ['CHROMIUM_PATH']
 browser=p.chromium.launch(**launch)
 for w,h in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  for name in PAGES:
   html=(ROOT/name).read_text()
   html=html.replace('<link rel="stylesheet" href="./styles.css">','<style>'+css+'</style>')
   html=re.sub(r'<script type="module" src="\./(?:hero|lab)\.js"></script>','',html)
   def embed(m):
    f=ROOT/m.group(1)
    return 'src="data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()+'"'
   html=re.sub(r'src="\./(media/[^" ]+\.png)"',embed,html)
   page.set_content(html,wait_until='domcontentloaded')
   code=(ROOT/('hero.js' if name=='index.html' else 'lab.js')).read_text()
   if name!='index.html':code=code.replace("from './science.js'",f"from '{science_data}'")
   page.add_script_tag(type='module',content=code)
   page.wait_for_timeout(250)
   assert page.locator('h1').count()==1,(name,'h1')
   if name!='index.html':
    assert page.locator('#main-result').inner_text()!='—',(name,'no outputs')
    assert page.locator('input[type=range]').count()>=1,(name,'no sliders')
    first=page.locator('input[type=range]').first
    first.evaluate('(el) => {el.value=el.min;el.dispatchEvent(new Event("input",{bubbles:true}))}')
    assert page.locator('#main-result').inner_text()!='—',(name,'no updates')
   else:assert page.locator('.chapter-card').count()==6
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'),(w,name,'horizontal scroll')
   if name in ('index.html','03-distancia-adn.html','06-experimento-hprt.html'):
    path=ROOT/'tests'/f'screenshot_{w}_{name.replace(".html", "")}.png'
    page.screenshot(path=str(path),full_page=name!='index.html')
   if errors:raise AssertionError((w,name,errors))
  print('QA navegador OK',w,'x',h)
  page.close()
 browser.close()
