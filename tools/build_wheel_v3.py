"""v3 wheel: AI ring with one continuous gem track + medallion on top.
usage: build_wheel_v3.py SRC_RING.png OUTDIR [RM]
Ring is resampled to a perfect circle (outer radius ROUT, centre 500,500), hole cut out,
medallion (violet/green, from wheel-v2) drawn over the inner part of the track with a bronze edge."""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
S=1000; C=500.0; ROUT=497.0
src,out=sys.argv[1],sys.argv[2]; RM=float(sys.argv[3]) if len(sys.argv)>3 else 285.0
BW=float(sys.argv[4]) if len(sys.argv)>4 else 20.0   # outer border width after squeezing (source ~45)

def load(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)/255
def save(a,p): Image.fromarray((np.clip(a,0,1)*255+.5).astype(np.uint8),'RGBA').save(p)

im=np.asarray(Image.open(src).convert('RGB')).astype(np.float32)/255
nonw=im.sum(2)<2.8
ys,xs=np.nonzero(nonw); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
cx=(x0+x1+1)/2; cy=(y0+y1+1)/2; rx=(x1-x0+1)/2; ry=(y1-y0+1)/2
yy,xx=np.mgrid[0:S,0:S].astype(np.float32); dx=xx+.5-C; dy=yy+.5-C; rho=np.hypot(dx,dy)
# radial remap: track grows outward, outer border squeezed to BW px
K=rx/ROUT; B0=414.0/(rx/ROUT)/ (rx/ROUT) if False else None
SB=414.0                       # source radius where the outer border starts (px of source, x-axis)
O0=400.0; O1=ROUT-BW
f=np.where(rho<=O0,rho*K,np.where(rho<=O1,O0*K+(rho-O0)/(O1-O0)*(SB-O0*K),SB+(rho-O1)/BW*(rx-SB)))
sc=f/np.maximum(rho,1e-3)
sx=cx+dx*sc; sy=cy+dy*sc*(ry/rx)   # elliptical -> circular
ring=np.dstack([map_coordinates(im[...,c],[sy,sx],order=1,mode='nearest') for c in range(3)])
# hole: inner white disc of the source, found from the centre row
row=nonw[int(round(cy))]; mid=int(round(cx)); k=mid
while not row[k]: k+=1
hole=(k-mid)*ROUT/rx
alpha=np.clip(ROUT-rho+.5,0,1)*np.clip(rho-hole+.5,0,1)
ring=np.dstack([ring,alpha])
print('hole radius (1000px space)',round(hole,1),'RM',RM)

def medal(name):
    m=load(f'assets/wheel-v2/medallion_{name}.png'); k=322.0/RM        # v2 medallion radius 322
    sxm=C+dx*k; sym=C+dy*k
    o=np.dstack([map_coordinates(m[...,c],[sym,sxm],order=1,mode='constant') for c in range(4)])
    o[...,3]=np.clip(RM-8-rho+.5,0,1)*o[...,3].max()
    # bronze edge ring RM-8 .. RM+7 with a vertical-light gradient, soft shadow outside
    t=np.clip((rho-(RM-8))/15,0,1); inring=(rho>=RM-8)&(rho<=RM+7)
    lit=.5+.5*(-dy/np.maximum(rho,1))*np.cos(t*np.pi)           # light from top
    bronze=np.stack([.55+.35*lit,.36+.25*lit,.14+.12*lit],-1)
    a=np.clip(RM+7.5-rho,0,1)*np.clip(rho-(RM-8.5),0,1)
    base=np.dstack([o[...,:3],o[...,3]])
    top=np.dstack([bronze,a])
    ta=top[...,3:4]; ba=base[...,3:4]; oa=ta+ba*(1-ta)
    rgb=np.where(oa>1e-5,(top[...,:3]*ta+base[...,:3]*ba*(1-ta))/np.maximum(oa,1e-5),0)
    return np.dstack([rgb,oa[...,0]])

def over(top,bot):
    ta=top[...,3:4]; ba=bot[...,3:4]; oa=ta+ba*(1-ta)
    rgb=np.where(oa>1e-5,(top[...,:3]*ta+bot[...,:3]*ba*(1-ta))/np.maximum(oa,1e-5),0)
    return np.dstack([rgb,oa[...,0]])

import os; os.makedirs(out,exist_ok=True)
save(ring,f'{out}/ring.png')
for n,key in (('violet','left'),('green','right')):
    w=over(medal(n),ring); save(w,f'{out}/wheel_{key}.png')
    Image.fromarray((np.clip(w,0,1)*255+.5).astype(np.uint8),'RGBA').save(f'{out}/wheel_{key}.webp',quality=92)
