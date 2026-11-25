"""Verifica destinos relativos de vínculos, vídeos e imágenes en las páginas."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
P=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if d.get('id'):self.ids.add(d['id'])
  for key in ('href','src','poster'):
   if key in d:self.refs.append((tag,key,d[key]))

def check():
 failures=[];total=0
 for html in P.glob('*.html'):
  doc=Links();doc.feed(html.read_text(encoding='utf-8'))
  for tag,key,raw in doc.refs:
   url=urlsplit(raw)
   if url.scheme or url.netloc or raw.startswith('data:'):continue
   rel=unquote(url.path)
   target=(html.parent/rel) if rel else html
   if not target.exists():failures.append(f'{html.name}: {key} {raw} no existe')
   elif target.suffix=='.html' and url.fragment:
    parser=Links();parser.feed(target.read_text(encoding='utf-8'))
    if url.fragment not in parser.ids:failures.append(f'{html.name}: ancla #{url.fragment} no existe en {target.name}')
   total+=1
 print('Enlaces y recursos locales comprobados:',total,'| archivos HTML:',len(list(P.glob('*.html'))))
 assert not failures,'\n'.join(failures)
if __name__=='__main__':check()
