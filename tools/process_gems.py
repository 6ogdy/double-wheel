import glob, numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageChops
Image.MAX_IMAGE_PIXELS=None
SRC='assets/orig/'; OUT='assets/gems/'
def load(n): return Image.open(glob.glob(SRC+n+'.*.webp')[0]).convert('RGBA')
def clean(im):
    a=np.asarray(im).astype(np.float32)/255; rgb=a[...,:3]; al=a[...,3:]
    # lift shadows: black point up, gamma brighter
    rgb=np.clip((rgb-0.04)/0.96,0,1)**0.72
    # shadow tint -> pull darkest areas toward the gem's own hue (avoid muddy dark)
    lum=(rgb*[0.299,0.587,0.114]).sum(-1,keepdims=True)
    mx=rgb.max(-1,keepdims=True); hue=rgb/np.maximum(mx,1e-4)
    dark=np.clip(1-lum/0.45,0,1)
    rgb=rgb*(1-0.55*dark)+hue*0.55*dark*0.62
    out=np.concatenate([np.clip(rgb,0,1),al],-1)
    im=Image.fromarray((out*255).astype(np.uint8),'RGBA')
    im=ImageEnhance.Color(im).enhance(1.25)
    return ImageEnhance.Contrast(im).enhance(1.08)
def bold_wild(im):
    al=im.getchannel('A'); big=al.filter(ImageFilter.MaxFilter(9))
    pad=14; W,H=im.size
    canvas=Image.new('RGBA',(W+2*pad,H+2*pad),(0,0,0,0))
    # dark gold outline
    stroke=Image.new('RGBA',im.size,(92,45,0,255)); stroke.putalpha(big.filter(ImageFilter.MaxFilter(7)))
    canvas.alpha_composite(stroke,(pad,pad))
    # fill thickened letters with bright gold gradient, then original detail on top
    ys=np.linspace(0,1,H)[:,None,None]
    top=np.array([255,240,150]); bot=np.array([245,170,20])
    g=(top*(1-ys)+bot*ys)*np.ones((H,W,1)); gi=Image.fromarray(g.astype(np.uint8),'RGB').convert('RGBA'); gi.putalpha(big)
    canvas.alpha_composite(gi,(pad,pad))
    orig=ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(1.2)).enhance(1.12)
    canvas.alpha_composite(orig,(pad,pad))
    return canvas
names=['gold','green','blue','pink','violet']
rows=[]
for n in names:
    o=load(n); c=clean(o); c.save(OUT+n+'.png'); rows.append((o,c))
w=load('wild'); wb=bold_wild(w); wb.save(OUT+'wild.png')
wf=load('wildFlipped'); bold_wild(wf).save(OUT+'wildFlipped.png')
rows.append((w,wb))
