"""Seis secuencias de congreso renderizadas en Python/Pillow y codificadas H.264.

Escena=representacion didactica. El tiempo cinematografico no es tiempo fisico;
las trayectorias de fotones/electrones no son trazas Geant4 ni datos medidos.
"""
from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib

from modelo import (T125_D, T131_D, decay_rate, fraction_decay_in_dna,
                    sample_lesions, lesion_fates, hprt_induced_frequency)

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "animaciones"
FPS = 20
W, H = 1280, 720
INK = (7, 15, 32)
WHITE = (239, 247, 247)
MUTED = (151, 175, 189)
TEAL = (83, 230, 209)
GOLD = (255, 204, 132)
PINK = (242, 132, 174)
BLUE = (126, 165, 255)
FONT_R = str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans.ttf")
FONT_B = str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans-Bold.ttf")
f12, f17, f20, f24, f31, f40, f54 = [ImageFont.truetype(FONT_R, n) for n in (12,17,20,24,31,40,54)]
b17, b22, b31 = [ImageFont.truetype(FONT_B, n) for n in (17,22,31)]


def ease(x):
    x = np.clip(x, 0, 1)
    return x*x*(3-2*x)


def at(x, y, t):
    return x + (y-x)*ease(t)


def clamp(x):
    return max(0, min(255, round(x)))


def base(scene, t, title, kicker, subtitle):
    # Fondo texturizado determinista, uniforme en todos los cuadros de escena.
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im, "RGB")
    for y in range(H):
        wave = 5*math.sin(y/98 + scene*0.9)
        d.line([(0,y),(W,y)], fill=(clamp(7+wave),clamp(15+y/100),clamp(34+y/37)))
    # rejilla discreta de instrumento
    for x in range(68, W, 48):
        d.line([(x,124),(x,625)], fill=(17,33,52), width=1)
    for y in range(132,626,48):
        d.line([(62,y),(1218,y)], fill=(17,33,52), width=1)
    d.rounded_rectangle((54,116,1226,631),radius=26,fill=(11,24,44),outline=(37,61,79),width=2)
    d.text((64,31), "RADIONÚCLIDOS  /  ADN HUMANO", font=b17, fill=TEAL)
    d.text((64,58), title, font=f31, fill=WHITE)
    d.text((1128,38), f"0{scene} / 06", font=f20, fill=MUTED)
    d.rounded_rectangle((74,574,1206,610), radius=10, fill=(18,38,58))
    d.text((92,583), subtitle, font=f17, fill=WHITE)
    d.text((76,642), kicker, font=f17, fill=MUTED)
    d.rounded_rectangle((74,678,1206,683), radius=2, fill=(30,50,65))
    d.rounded_rectangle((74,678,round(74+1132*t),683),radius=2,fill=TEAL)
    return im, d


def card(d, box, label, value, color=TEAL):
    d.rounded_rectangle(box,radius=14,fill=(18,39,60),outline=(46,76,91),width=2)
    x,y,_,_=box
    d.text((x+18,y+13),label,font=f17,fill=MUTED)
    d.text((x+18,y+43),value,font=f24,fill=color)


def orbit(d, x, y, rad, color, step=0):
    for k in range(5,0,-1):
        rr = rad+k*7
        col = tuple(clamp(c*(.15+.08*(6-k))) for c in color)
        d.ellipse((x-rr,y-rr,x+rr,y+rr),outline=col,width=2)
    d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=color)


def frame1(t):
    im,d=base(1,t,"Un núcleo cambia: captura electrónica","FÍSICA NUCLEAR   •   CAPTURA ELECTRÓNICA   •   CASCADA ATÓMICA",
              "El yodo unido al ADN captura un electrón; la relajación emite electrones Auger.")
    cx,cy=394,356
    for r in (96,151,209):
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(41,76,93),width=2)
    nucleus=(GOLD if t<.4 else TEAL)
    orbit(d,cx,cy,60,nucleus)
    d.text((cx-43,cy-15),"I-125" if t<.43 else "Te-125",font=b22,fill=INK)
    phase=ease((t-.13)/.27)
    ex=round(at(cx-214,cx-65,phase))
    orbit(d,ex,cy-55,7,BLUE)
    if t>.36:
        n=ease((t-.36)/.36)
        for k,angle in enumerate((-2.5,-1.5,-.5,.4,1.2,2.1)):
            length=at(10,190,n)*(.55+.12*k)
            x2=cx+math.cos(angle)*length
            y2=cy+math.sin(angle)*length
            d.line([(cx,cy),(x2,y2)],fill=TEAL,width=3)
            orbit(d,x2,y2,4,TEAL)
    card(d,(745,187,1174,277),"REACCIÓN NUCLEAR","I-125 + e  →  Te-125* + νe",GOLD)
    card(d,(745,304,1174,394),"DESINTEGRACIÓN","T½ = 59,4 días",TEAL)
    card(d,(745,421,1174,511),"DESPUÉS","Auger + rayos X / γ",PINK)
    return im


def frame2(t):
    im,d=base(2,t,"Dos relojes nucleares, dos escalas","RESULTADO NUCLEAR   •   SEMIVIDA FÍSICA   •   ACTIVIDAD",
              "Semivida física ≠ tiempo de permanencia del radionúclido en ADN.")
    x0,x1,y0,y1=130,774,517,180
    d.line([(x0,y1),(x0,y0),(x1,y0)],fill=(110,140,158),width=3)
    for day in (0,30,60,90,120):
        x=x0+(x1-x0)*day/120
        d.line([(x,y0),(x,y0+9)],fill=MUTED,width=2)
        d.text((x-12,y0+14),str(day),font=f17,fill=MUTED)
    for val in (0,.5,1):
        y=y0-(y0-y1)*val
        d.text((86,y-10),f"{val:.1f}",font=f17,fill=MUTED)
        d.line([(x0,y),(x1,y)],fill=(27,52,71))
    prog=at(0,120,t)
    tt=np.linspace(0,prog,350)
    for hl,col in ((T125_D,TEAL),(T131_D,PINK)):
        pts=[(x0+(x1-x0)*q/120,y0-(y0-y1)*math.exp(-decay_rate(hl)*q)) for q in tt]
        if len(pts)>1: d.line(pts,fill=col,width=5,joint="curve")
        orbit(d,*pts[-1],6,col)
    d.text((348,555),"Tiempo desde la incorporación  [días]",font=f17,fill=MUTED)
    card(d,(850,191,1175,278),"I-125  •  captura electrónica","59,4 días",TEAL)
    card(d,(850,306,1175,393),"I-131  •  beta menos","8,021 días",PINK)
    v=fraction_decay_in_dna(T125_D,2)
    d.text((858,430),f"Ejemplo: residencia media 2 d",font=f17,fill=WHITE)
    d.text((858,457),f"P(decay en ADN, I-125) = {v:.1%}",font=f17,fill=GOLD)
    d.text((858,484),"Residencia: valor hipotético",font=f17,fill=MUTED)
    return im


def helix_drawing(d, x0, y0, width, turns, reveal, highlight=False):
    ylo,yhi=y0-172,y0+172
    ptsa,ptsb=[],[]
    for i in range(151):
        u=i/150
        yy=ylo+(yhi-ylo)*u
        theta=u*2*math.pi*turns
        ptsa.append((x0+width*math.cos(theta),yy))
        ptsb.append((x0-width*math.cos(theta),yy))
    n=max(1,round(reveal*150))
    for i in range(0,n,6):
        a=ptsa[i];b=ptsb[i]
        d.line((a,b),fill=(75,112,137),width=2)
    if n>1:
        d.line(ptsa[:n+1],fill=TEAL,width=6,joint="curve")
        d.line(ptsb[:n+1],fill=BLUE,width=6,joint="curve")
    return ptsa,ptsb


def frame3(t):
    im,d=base(3,t,"La posición cambia la energía local","ESCALA MOLECULAR   •   DISTANCIA FUENTE–ADN   •   GEOMETRÍA",
              "El alcance ilustrado muestra la geometría; no representa trazas Monte Carlo físicas.")
    cx,cy=359,362
    a,b=helix_drawing(d,cx,cy,96,3.0,1)
    off=at(5,180,ease((t-.28)/.5))
    sx,sy=cx+96+off,cy
    for radius in (32,68,112):
        d.ellipse((sx-radius,sy-radius,sx+radius,sy+radius),outline=(36,94,103),width=2)
    orbit(d,sx,sy,14,GOLD)
    d.text((123,152),"ADN esquemático",font=b17,fill=TEAL)
    d.text((564,362),"I-125",font=f20,fill=GOLD)
    x0,x1,y0,y1=752,1162,482,199
    d.line([(x0,y0),(x1,y0)],fill=MUTED,width=2)
    d.line([(x0,y0),(x0,y1)],fill=MUTED,width=2)
    xx=np.linspace(0,7,190)
    d.line([(x0+(x1-x0)*v/7,y0-(y0-y1)*math.exp(-v/1.5)) for v in xx],fill=GOLD,width=5,joint="curve")
    dx=off/180*7
    orbit(d,x0+(x1-x0)*dx,y0-(y0-y1)*math.exp(-dx/1.5),7,TEAL)
    d.text((757,151),"Peso espacial del modelo",font=b17,fill=WHITE)
    d.text((824,511),"Separación adicional  [nm]",font=f17,fill=MUTED)
    d.text((772,234),"q(r) = exp(−r / ℓ)",font=f20,fill=GOLD)
    d.text((772,260),"ℓ = 1,5 nm  •  hipótesis",font=f17,fill=MUTED)
    return im


LESIONS=sample_lesions(n_events=15000)


def frame4(t):
    im,d=base(4,t,"De roturas individuales a una rotura doble","SIMULACIÓN   •   DOS HEBRAS   •   CRITERIO OPERATIVO DE 10 PB",
              "DSB: al menos una rotura en cada hebra dentro de una ventana de 10 pares de bases.")
    start,end=160,740
    for strand,y,c in (("A",265,TEAL),("B",401,BLUE)):
        d.line([(start,y),(end,y)],fill=c,width=6)
        d.text((108,y-17),strand,font=f31,fill=c)
        for j in range(25):
            x=start+(end-start)*j/24
            d.ellipse((x-3,y-3,x+3,y+3),fill=WHITE)
    p=ease((t-.23)/.26)
    if p>.05:
        xA=430;xB=480
        for x,y,c in ((xA,265,TEAL),(xB,401,BLUE)):
            d.line([(x-11,y-22),(x+11,y+22)],fill=GOLD,width=7)
            d.line([(x+11,y-22),(x-11,y+22)],fill=GOLD,width=7)
        d.line([(xA,343),(xB,343)],fill=PINK,width=4)
        d.text((380,351),"≤ 10 pb",font=f17,fill=PINK)
    x0,x1,y0,y1=835,1175,479,220
    d.line([(x0,y1),(x0,y0),(x1,y0)],fill=MUTED,width=2)
    mx=max(v["dsb"] for v in LESIONS)*1.15
    for i,v in enumerate(LESIONS):
        x=x0+30+i*66
        hh=(y0-y1)*v["dsb"]/mx*ease((t-.13-i*.065)/.4)
        d.rounded_rectangle((x,y0-hh,x+32,y0),radius=5,fill=TEAL if i==0 else BLUE)
        d.text((x-5,y0+12),str(int(v["offset_nm"])),font=f17,fill=MUTED)
    d.text((836,174),"P(DSB | 1 evento)",font=b17,fill=WHITE)
    d.text((878,516),"Separación [nm]",font=f17,fill=MUTED)
    d.text((820,544),"Valores: Monte Carlo ilustrativo",font=f17,fill=GOLD)
    return im


def frame5(t):
    im,d=base(5,t,"Una lesión tiene varios destinos","CINÉTICA HIPOTÉTICA   •   REPARACIÓN   •   MUTACIÓN   •   PÉRDIDA CELULAR",
              "L(t) + R(t) + M(t) + C(t) = 1 por construcción del modelo.")
    hours=at(0,24,t)
    vals=[float(x) for x in lesion_fates(hours)]
    x0,x1,y0,y1=128,797,502,190
    d.line([(x0,y1),(x0,y0),(x1,y0)],fill=MUTED,width=2)
    ts=np.linspace(0,hours,190)
    for idx,col in ((0,WHITE),(1,TEAL),(2,GOLD),(3,PINK)):
        arr=lesion_fates(ts)[idx]
        pts=[(x0+(x1-x0)*q/24,y0-(y0-y1)*v) for q,v in zip(ts,arr)]
        if len(pts)>1:d.line(pts,fill=col,width=4,joint="curve")
        orbit(d,*pts[-1],5,col)
    d.text((373,525),"Tiempo del modelo [h]",font=f17,fill=MUTED)
    labels=["Lesión presente","Reparación","Mutación fijada","Pérdida celular"]
    for i,(label,val,col) in enumerate(zip(labels,vals,(WHITE,TEAL,GOLD,PINK))):
        yy=215+i*79
        d.ellipse((858,yy+4,870,yy+16),fill=col)
        d.text((886,yy),label,font=f17,fill=WHITE)
        d.text((1091,yy),f"{val:.1%}",font=f17,fill=col)
    d.text((867,535),"Tasas: 0,20 / 0,02 / 0,03 h⁻¹",font=f17,fill=MUTED)
    return im


def frame6(t):
    im,d=base(6,t,"La pregunta experimental: ¿hay mutación?","ARTÍCULO GUÍA   •   WHALEY Y LITTLE (1990)   •   HPRT HUMANO",
              "38 cGy se usa como extrapolación TK6; ese valor no es una medida TK6 del artículo.")
    d.rounded_rectangle((115,181,588,473),radius=22,fill=(21,50,68),outline=TEAL,width=3)
    d.rounded_rectangle((697,181,1170,473),radius=22,fill=(28,40,63),outline=BLUE,width=3)
    d.text((148,210),"TK6  •  incorpora IdUrd",font=b22,fill=TEAL)
    d.text((731,210),"SE30  •  deficiente en TK",font=b22,fill=BLUE)
    d.text((148,261),"Fuente en el ADN",font=f20,fill=WHITE)
    d.text((731,261),"Fuente en el medio",font=f20,fill=WHITE)
    for i in range(6):
        x=195+55*i;y=348+18*math.sin(i*1.8)
        d.ellipse((x-9,y-9,x+9,y+9),fill=TEAL)
        if t>.25 and i<round(at(0,4,(t-.25)/.5)):
            d.ellipse((x-15,y-15,x+15,y+15),outline=GOLD,width=3)
    for i in range(6):
        x=767+55*i;y=354+16*math.sin(i*1.8)
        d.ellipse((x-9,y-9,x+9,y+9),fill=BLUE)
    alpha=round(at(0,17.1,ease((t-.42)/.43)),1)
    d.text((144,410),"I-131: 0,45 × 10⁻⁶ por cGy",font=f17,fill=GOLD)
    d.text((723,410),"Pocas mutaciones hasta 38 cGy",font=f17,fill=BLUE)
    d.text((143,495),f"Ejemplo TK6 a 38 cGy: +{alpha:.1f} por millón",font=f24,fill=GOLD)
    d.text((146,532),"Valor calculado con la pendiente publicada; no lectura experimental directa.",font=f17,fill=MUTED)
    return im


FRAMES=(frame1,frame2,frame3,frame4,frame5,frame6)
NAMES=("01_captura_y_Auger","02_semividas_y_retencion","03_distancia_fuente_ADN",
       "04_roturas_agrupadas","05_reparacion_y_mutacion","06_experimento_HPRT")


def render(seconds=7.0, preview_only=False):
    VIDEO.mkdir(exist_ok=True)
    for index,(scene,name) in enumerate(zip(FRAMES,NAMES),1):
        scene(.72).save(VIDEO / (name+"_portada.png"))
        if preview_only:
            continue
        path=VIDEO/(name+".mp4")
        command=["ffmpeg","-loglevel","error","-y","-f","rawvideo","-vcodec","rawvideo",
                 "-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
                 "-an","-c:v","libx264","-preset","fast","-crf","23","-pix_fmt","yuv420p",
                 "-movflags","+faststart",str(path)]
        proc=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for k in range(round(seconds*FPS)):
                proc.stdin.write(scene(k/(round(seconds*FPS)-1)).tobytes())
        except BrokenPipeError as ex:
            raise RuntimeError(f"Fallo ffmpeg en {name}") from ex
        finally:
            proc.stdin.close()
            result=proc.wait()
        if result:
            raise RuntimeError(f"Fallo ffmpeg {result} en {name}")
        print(f"{index}/6 {path.name}",flush=True)
    if not preview_only:
        # Archivo de concatenación de nombres internos generados por nosotros.
        listing=VIDEO/"_concat.txt"
        listing.write_text("".join(f"file '{name}.mp4'\n" for name in NAMES),encoding="utf8")
        subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i",
                        str(listing),"-c","copy",str(VIDEO/"EXPOSICION_COMPLETA.mp4")],check=True)
        listing.unlink()


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--solo-portadas",action="store_true")
    parser.add_argument("--segundos",type=float,default=7)
    args=parser.parse_args()
    render(args.segundos,args.solo_portadas)
