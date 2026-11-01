from pathlib import Path
import math, hashlib
import numpy as np
import trimesh as tm
import manifold3d as m3d
from shapely.geometry import box as polybox, Polygon
from PIL import Image, ImageDraw, ImageFont
FONT='C:/Windows/Fonts/segoeui.ttf'
BOLD='C:/Windows/Fonts/segoeuib.ttf'
VALID=[]
STL=None
def configure(output):
    global STL
    STL=Path(output)/'stl'
    STL.mkdir(parents=True,exist_ok=True)
    VALID.clear()

def box(x0,y0,z0,x1,y1,z1):
    assert x1>x0 and y1>y0 and z1>z0
    m=tm.creation.box([x1-x0,y1-y0,z1-z0]);m.apply_translation([(x0+x1)/2,(y0+y1)/2,(z0+z1)/2]);return m

def cyl(r,z0,z1,x=0,y=0,sections=64):
    m=tm.creation.cylinder(radius=r,height=z1-z0,sections=sections);m.apply_translation([x,y,(z0+z1)/2]);return m

def xcyl(r,x0,x1,y,z,sections=64):
    m=tm.creation.cylinder(radius=r,height=x1-x0,sections=sections);m.apply_transform(tm.transformations.rotation_matrix(math.pi/2,[0,1,0]));m.apply_translation([(x0+x1)/2,y,z]);return m

def union(*parts):return tm.boolean.union(list(parts),engine='manifold') if len(parts)>1 else parts[0].copy()

def cut(main,*parts):return tm.boolean.difference([main,*parts],engine='manifold')

def rounded_plate(w,d,h,r=3):
    p=polybox(r,r,w-r,d-r).buffer(r,quad_segs=8);return tm.creation.extrude_polygon(p,h,engine='earcut')

def yz_extrude(points,y0,y1):
    # Polygon coordinates are x,z. Transform extrusion axis into world Y.
    m=tm.creation.extrude_polygon(Polygon(points),y1-y0,engine='earcut');T=np.array([[1,0,0,0],[0,0,1,y0],[0,1,0,0],[0,0,0,1]],float);m.apply_transform(T);return m

def join_volume(a,b):
    q=tm.boolean.intersection([a,b],engine='manifold')
    if not len(q.faces):return 0.
    tri=q.triangles
    return abs(float(np.einsum('ij,ij->i',tri[:,0],np.cross(tri[:,1],tri[:,2])).sum()/6))

def component_count(m):
    parent=list(range(len(m.vertices)))
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]];a=parent[a]
        return a
    for a,b,c in m.faces:
        ra=find(int(a));rb=find(int(b));rc=find(int(c));parent[rb]=ra;parent[rc]=ra
    return len({find(i) for i in range(len(parent))})

def export(name,m,flip_x=False,axis_x_to_z=False):
    q=m.copy()
    if flip_x:q.apply_transform(tm.transformations.rotation_matrix(math.pi,[1,0,0]))
    if axis_x_to_z:q.apply_transform(tm.transformations.rotation_matrix(math.pi/2,[0,1,0]))
    q.apply_translation(-q.bounds[0]);q.remove_unreferenced_vertices()
    # Remove sub-micron boolean slivers before binary STL's float32 round trip.
    clean=m3d.Manifold(m3d.Mesh(np.asarray(q.vertices,dtype=np.float32),np.asarray(q.faces,dtype=np.uint32))).simplify(.0001).to_mesh()
    q=tm.Trimesh(vertices=np.asarray(clean.vert_properties)[:,:3],faces=np.asarray(clean.tri_verts),process=True)
    assert q.is_watertight and q.is_winding_consistent and q.volume>0,name
    assert component_count(q)==1,(name,'not a single connected part')
    assert max(q.extents)<=270,name
    p=STL/(name+'.stl');q.export(p)
    reread=tm.load_mesh(p);assert reread.is_watertight and reread.is_winding_consistent
    VALID.append({'part':name,'size_mm':q.extents.round(3).tolist(),'volume_mm3':round(q.volume,3),'triangles':len(q.faces),'watertight':True,'consistent_winding':True,'connected_components':1,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return m

def render_scene(items,dest,title,subtitle):
    width,height=1700,1050;im=Image.new('RGB',(width,height),'#F7F7F1');dr=ImageDraw.Draw(im)
    dr.text((50,28),title,font=ImageFont.truetype(BOLD,38),fill='#173D43');dr.text((50,83),subtitle,font=ImageFont.truetype(FONT,21),fill='#61777C')
    # Camera basis, Z positive up and front (low Y) visible.
    view=np.array([[.8660254,.5,0],[-.3830222,.6634139,.6427876],[.3213938,-.5566704,.7660444]])
    merged=np.vstack([m.vertices for m,_ in items]);proj=merged@view.T;lo=proj[:,:2].min(0);hi=proj[:,:2].max(0);scale=min((width-140)/(hi[0]-lo[0]),(height-260)/(hi[1]-lo[1]))
    light=np.array([-.2,-.6,.8]);light/=np.linalg.norm(light)
    # Per-pixel depth avoids painter-order artefacts on large deck faces.
    canvas=np.array(im);depth=np.full((height,width),-np.inf)
    for m,col in items:
        rgb=np.array(tuple(bytes.fromhex(col.lstrip('#'))),float)
        for vv,norm in zip(m.triangles,m.face_normals):
            if np.dot(norm,view[2])<-.01:continue
            pp=vv@view.T;xy=np.c_[70+(pp[:,0]-lo[0])*scale,height-100-(pp[:,1]-lo[1])*scale]
            xmin=max(0,int(np.floor(xy[:,0].min())));xmax=min(width-1,int(np.ceil(xy[:,0].max())));ymin=max(0,int(np.floor(xy[:,1].min())));ymax=min(height-1,int(np.ceil(xy[:,1].max())))
            if xmax<xmin or ymax<ymin:continue
            x,y=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
            a,b,c=xy;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-10:continue
            wa=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den;wb=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den;wc=1-wa-wb;z=wa*pp[0,2]+wb*pp[1,2]+wc*pp[2,2]
            dd=depth[ymin:ymax+1,xmin:xmax+1];mask=(wa>=-1e-8)&(wb>=-1e-8)&(wc>=-1e-8)&(z>dd)
            shade=.55+.45*max(0,np.dot(norm,light));color=(rgb*shade).clip(0,255).astype(np.uint8);canvas[ymin:ymax+1,xmin:xmax+1][mask]=color;dd[mask]=z[mask]
    im=Image.fromarray(canvas);dr=ImageDraw.Draw(im)
    dr.text((50,height-49),'RENDERED FROM EXPORTED PART GEOMETRY | Bench prototype - tuning, fit and sound untested',font=ImageFont.truetype(FONT,19),fill='#61777C');im.save(dest)
