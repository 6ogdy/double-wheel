"""Rebuild the Aztec wheel as separate, perfectly centred layers.
ring.png      transparent hole, 20 segments, exact circular edges, centre at (500,500)
medallion_*.png  circle of radius RM, centre at (500,500), tinted
wheel_left/right.webp  = medallion under ring (what the game shows rotating)"""
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates, gaussian_filter1d
S=1000; C=500.0
RIN=312.0; SPLIT=470.0; ROUT=497.0; RM=RIN+10   # medallion slides under the ring lip
NSEG_T=20

def rgba(p): return np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)/255

def boundary(alpha,cx,cy,n=1440):
    th=np.linspace(0,2*np.pi,n,endpoint=False); rs=np.arange(0,540,0.5); ro=[];ri=[]
    for t in th:
        p=map_coordinates(alpha,[cy+rs*np.sin(t),cx+rs*np.cos(t)],order=1,mode='constant',cval=0)
        i=np.nonzero(p>0.5)[0]; ro.append(rs[i.max()]); ri.append(rs[i.min()])
    return th,np.array(ro),np.array(ri)

def fit_center(alpha):
    ys,xs=np.nonzero(alpha>0.5); cx=(xs.min()+xs.max())/2; cy=(ys.min()+ys.max())/2
    for _ in range(4):
        th,ro,_ri=boundary(alpha,cx,cy); X=cx+ro*np.cos(th); Y=cy+ro*np.sin(th)
        s=np.linalg.lstsq(np.c_[2*X,2*Y,np.ones_like(X)],X**2+Y**2,rcond=None)[0]; cx,cy=s[0],s[1]
    return cx,cy

def sample(img,x,y):
    out=np.zeros(x.shape+(4,),np.float32)
    prem=img.copy(); prem[...,:3]*=prem[...,3:4]
    for c in range(4): out[...,c]=map_coordinates(prem[...,c],[y,x],order=1,mode='constant',cval=0)
    a=out[...,3:4]; out[...,:3]=np.where(a>1e-4,out[...,:3]/np.maximum(a,1e-4),0)
    return out

def build_ring(src='b/n0.png'):
    img=rgba(src); al=img[...,3]; cx,cy=fit_center(al)
    th,ro,ri=boundary(al,cx,cy); sm=lambda v: gaussian_filter1d(v,3,mode='wrap')
    ro,ri=sm(ro),sm(ri); deg=np.degrees(th)
    gray=np.asarray(Image.open(src).convert('L')).astype(np.float32)
    t2=np.linspace(0,2*np.pi,4096,endpoint=False); F=0
    for r in range(300,440,10): F=F+np.fft.rfft(map_coordinates(gray,[cy+r*np.sin(t2),cx+r*np.cos(t2)],order=1)-gray.mean())[18]
    th_bar=np.degrees(-np.angle(F)/18)%20.0          # a bar centre (source, deg)
    th_pc=th_bar+10.0                                  # panel centre
    yy,xx=np.mgrid[0:S,0:S].astype(np.float32); dx=xx+0.5-C; dy=yy+0.5-C
    rho=np.hypot(dx,dy); phi=np.degrees(np.arctan2(dy,dx))%360
    interp=lambda arr,a: np.interp(a%360,np.r_[deg,360],np.r_[arr,arr[0]])
    # zone A: tiled band (20 segments), zone B: continuous greca border
    local=phi%(360/NSEG_T); thA=(th_pc+local*(20.0/(360/NSEG_T)))%360
    tA=np.clip((rho-RIN)/(SPLIT-RIN),0,1)
    rsA=interp(ri,thA)+tA*((interp(ro,thA)-27)-interp(ri,thA))
    tB=np.clip((rho-SPLIT)/(ROUT-SPLIT),0,1)
    rsB=(interp(ro,phi)-27)+tB*27
    zoneB=rho>=SPLIT; ths=np.where(zoneB,phi,thA); rs=np.where(zoneB,rsB,rsA)
    out=sample(img,cx+rs*np.cos(np.radians(ths)),cy+rs*np.sin(np.radians(ths)))
    cov=np.clip(rho-RIN+0.5,0,1)*np.clip(ROUT-rho+0.5,0,1)
    out[...,3]*=cov
    print('src centre',round(cx,2),round(cy,2),'bar deg',round(th_bar,2))
    return out

def build_medallion(src='b/n3.png'):
    img=rgba(src); al=img[...,3]; cx,cy=fit_center(al)
    th,ro,_=boundary(al,cx,cy); r_src=np.median(ro)
    yy,xx=np.mgrid[0:S,0:S].astype(np.float32); dx=xx+0.5-C; dy=yy+0.5-C; rho=np.hypot(dx,dy)
    k=r_src/RM; out=sample(img,cx+dx*k,cy+dy*k)
    out[...,3]=np.clip(RM-rho+0.5,0,1)
    return out

def tint(med,dark,light,edge=0.45):
    g=(0.299*med[...,0]+0.587*med[...,1]+0.114*med[...,2]); m=med[...,3]>0.5
    lo,hi=np.percentile(g[m],[3,97]); L=np.clip((g-lo)/(hi-lo),0,1)**1.15
    yy,xx=np.mgrid[0:S,0:S]; rho=np.hypot(xx+0.5-C,yy+0.5-C)/RM
    shade=1-edge*np.clip((rho-0.80)/0.20,0,1)**1.5
    d=np.array(dark,np.float32)/255; l=np.array(light,np.float32)/255
    rgb=(d+(l-d)*L[...,None])*shade[...,None]
    out=np.dstack([np.clip(rgb,0,1),med[...,3]]); return out

def over(top,bottom):
    ta=top[...,3:4]; ba=bottom[...,3:4]; oa=ta+ba*(1-ta)
    rgb=np.where(oa>1e-5,(top[...,:3]*ta+bottom[...,:3]*ba*(1-ta))/np.maximum(oa,1e-5),0)
    return np.dstack([rgb,oa[...,0]])

def save(a,p,**kw): Image.fromarray((np.clip(a,0,1)*255+0.5).astype(np.uint8),'RGBA').save(p,**kw)

if __name__=='__main__':
    ring=build_ring(); med=build_medallion()
    g=ring[...,:3].mean(axis=2,keepdims=True); ring[...,:3]=np.clip((g+(ring[...,:3]-g)*0.9)*0.70,0,1)   # darker, calmer bronze
    violet=tint(med,(5,1,9),(70,20,74)); green=tint(med,(1,7,3),(14,62,27)); neutral=tint(med,(10,10,10),(130,125,118))
    save(ring,'out/ring.png'); save(violet,'out/medallion_violet.png'); save(green,'out/medallion_green.png'); save(neutral,'out/medallion_neutral.png')
    save(over(ring,violet),'out/wheel_left.png'); save(over(ring,green),'out/wheel_right.png')
    a=ring[...,3]; ys,xs=np.mgrid[0:S,0:S]; w=a.sum()
    print('ring alpha centroid',((xs+0.5)*a).sum()/w,((ys+0.5)*a).sum()/w)
