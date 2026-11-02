import numpy as np
from PIL import Image
from scipy import ndimage as ndi
BG=np.array([30,30,30],float)
def remove(src,out):
    im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(float)
    d=np.abs(a-BG).max(axis=2)
    cand=d<14                      # near-background pixels
    lab,n=ndi.label(cand)
    border=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(border))
    # soft edge: distance from bg region, alpha ramps over ~2px
    dist=ndi.distance_transform_edt(~bg)
    alpha=np.clip((dist-0.5)/2.0,0,1)
    alpha[bg]=0
    # decontaminate edge colour (remove dark bg bleed)
    al=np.maximum(alpha,1e-3)[...,None]
    edge=(alpha>0)&(alpha<1)
    rgb=a.copy()
    rgb[edge]=np.clip((a[edge]-(1-al[edge])*BG)/al[edge],0,255)
    outim=np.dstack([rgb,alpha*255]).astype(np.uint8)
    Image.fromarray(outim,'RGBA').save(out,'WEBP',quality=92,method=6)
    return bg.mean()
import sys
for name in ['gold.d53168443bfda397846e','green.f25c93dd911fde41af2f','blue.52c7c705f881c6ec951f','pink.8cfdeb4e09969b101163','violet.fe2430dc563bad88d219']:
    print(name, round(remove(f'orig/game/static/media/{name}.webp',f'new/game/static/media/{name}.webp'),3))
