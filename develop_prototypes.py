"""Historical v0.1 bench prototypes. Millimetres. Not physically validated.

The S2/P1 first-build recommendations were superseded on October 27, 2026
after gravity-seating errors were found. Use build_simple_v02.py for current
first-build fixtures. This file remains available as a development snapshot.

Run with the bundled Python. CAD libraries are isolated in tmp/cad-libs.
Exported meshes are printable parts; assembly transforms are retained separately.
"""
from pathlib import Path
import sys, json, math, wave, struct, zipfile, hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tmp/cad-libs'))
import numpy as np
import trimesh as tm
import manifold3d as m3d
from shapely.geometry import box as polybox, Polygon
from PIL import Image, ImageDraw, ImageFont

O=ROOT/'output/prototypes-v01'; O.mkdir(parents=True,exist_ok=True)
STL=O/'stl'; STL.mkdir(exist_ok=True)
SONGS={
 'twinkle':{'title':'Twinkle, Twinkle - opening two phrases','notes':['C5','C5','G5','G5','A5','A5','G5','F5','F5','E5','E5','D5','D5','C5'],'ticks':[1,1,1,1,1,1,2,1,1,1,1,1,1,2],'seconds_per_tick':.6,'loop_rest_ticks':2,'source':'https://www.mutopiaproject.org/ftp/MozartWA/KV265/guitar-duo-complete/guitar-duo-complete-a4.pdf','source_detail':'Printed page 7, section 9 Allegro/Thema; relative melody transposed to C5; accompaniment and ornamentation omitted.'},
 'ode':{'title':'Ode to Joy - opening four bars','notes':['E5','E5','F5','G5','G5','F5','E5','D5','C5','C5','D5','E5','E5','D5','D5'],'ticks':[2,2,2,2,2,2,2,2,2,2,2,2,3,1,4],'seconds_per_tick':.3,'loop_rest_ticks':4,'source':'https://www.mutopiaproject.org/ftp/BeethovenLv/ode/ode-a4.pdf','source_detail':'First four bars, upper melody, transposed from G major to C major and moved to C5-G5; accompaniment omitted.'},
 'elise':{'title':'Fur Elise - opening nine-note hook','notes':['E5','D#5','E5','D#5','E5','B4','D5','C5','A4'],'ticks':[1,1,1,1,1,1,1,1,2],'seconds_per_tick':.25,'loop_rest_ticks':2,'source':'https://www.mutopiaproject.org/ftp/BeethovenLv/WoO59/fur_Elise_WoO59/fur_Elise_WoO59-a4.pdf','source_detail':'First nine upper melody events; accompaniment omitted; A4 held for an eighth-note unit, followed by an arranged loop pause.'}}
MATS={'PETG':{'E':1.7e9,'rho':1270},'PLA':{'E':3.1e9,'rho':1240}}
HZ={n:440*2**((m-69)/12) for n,m in [('A4',69),('B4',71),('C5',72),('D5',74),('D#5',75),('E5',76),('F5',77),('G5',79),('A5',81),('C6',84)]}
H=1.2; B=3.2
def free_length(note,mat):
    q=MATS[mat];return 1000*math.sqrt(1.8751040687**2/(2*math.pi)*H/1000*math.sqrt(q['E']/(12*q['rho']))/HZ[note])
for s in SONGS.values():
    starts=np.r_[0,np.cumsum(s['ticks'])[:-1]].tolist();s['events']=[{'note':n,'tick':int(t),'duration_ticks':d,'frequency_Hz':HZ[n]} for n,t,d in zip(s['notes'],starts,s['ticks'])]
    s['event_count']=len(starts);s['unique_pitch_count']=len(set(s['notes']));s['total_ticks']=sum(s['ticks']);s['minimum_linear_pitch_mm']=5.;s['linear_span_mm']=float(starts[-1]*5)
    s['peg_angles_degrees']=[round(360*(e['tick']+1)/(s['total_ticks']+s['loop_rest_ticks']+1),6) for e in s['events']]
    assert min(np.diff(starts)*5)>=B+1.2
(O/'song-programs.json').write_text(json.dumps(SONGS,indent=2),encoding='utf-8')

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
VALID=[]; ASSEMBLIES={}
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

# S2 aligned-tip slider bench: standard common mounting points for all song combs.
W,D=184.,66.;TIP=44.;TOP=8.;UNDERSIDE=TOP-H
deck=union(rounded_plate(W,D,4),box(0,52,4,W,58,12))
mounts=[(14,12),(170,12)]
holes=[]
for x,y in mounts:holes.extend([cyl(1.7,-.1,4.2,x,y),cyl(3.3,-.1,2.5,x,y,6)])
deck=cut(deck,*holes);export('S2_01_common_deck',deck)
clamp=box(10,8,8,174,16,10)
clamp=cut(clamp,*[cyl(1.7,7.9,10.1,x,y) for x,y in mounts]);export('S2_02_clamp_bar',clamp)
shoe=box(-7,49.7,5,7,60.3,14.3)
shoe=cut(shoe,box(-7.1,51.7,4.9,7.1,58.3,12.3))
shoe=union(shoe,box(-4.5,45,5.8,4.5,51,8.6))
shoe=cut(shoe,box(-3.2,44.9,6.1,3.2,51.1,7.9),cyl(.8,5.5,8.8,0,48))
export('S2_03_carriage',shoe,flip_x=True)
picks={}
for lift in [0.,.2,.4]:
    crest=UNDERSIDE+lift
    blade=yz_extrude([(-.8,6.2),(.8,6.2),(.8,6.4),(-.8,crest)],42.8,46.1)
    pick=union(box(-3,46,6.2,3,50.7,7.8),blade);pick=cut(pick,cyl(.85,6.1,7.9,0,48))
    export('S2_04_pick_lift_'+str(lift).replace('.','p'),pick);picks[lift]=pick

def event_comb(key,mat):
    pieces=[box(10,8,4,174,16,TOP)]
    for e in SONGS[key]['events']:
        x=22+e['tick']*5;root=TIP-free_length(e['note'],mat)
        assert root>16 and root<TIP
        pieces.extend([box(x-B/2,15.9,4,x+B/2,root,TOP),box(x-B/2,root-.01,UNDERSIDE,x+B/2,TIP,TOP)])
    m=union(*pieces);return cut(m,*[cyl(1.7,3.9,8.1,x,y) for x,y in mounts])
combs={}
for mat in MATS:
    for key in SONGS:
        comb=event_comb(key,mat);combs[(key,mat)]=comb
        export('S2_05_'+key+'_comb_'+mat,comb,flip_x=True)
    # Three isolated tuning tines on the same root geometry; no complete song yet.
    old=SONGS.get('calibration'); SONGS['calibration']={'events':[{'note':n,'tick':t} for n,t in [('C5',0),('G5',3),('C6',6)]]}
    comb=event_comb('calibration',mat);export('S2_00_calibration_comb_'+mat,comb,flip_x=True);del SONGS['calibration']

sx=22
def shifted(m,x):q=m.copy();q.apply_translation([x,0,0]);return q
ASSEMBLIES['S2_slider']=[(deck,'#647E7E'),(combs[('twinkle','PETG')],'#CCAB67'),(clamp,'#263F49'),(shifted(shoe,sx),'#D1834B'),(shifted(picks[.2],sx),'#C65442')]

# P1: one-note cylinder release fixture, with fixed shaft and rotating thumb drum.
CY,CZ=45.,20.;R=12.;PIN=1.2;BOT=CZ+R+PIN-.3;CTOP=BOT+H;CROOT=CTOP-4
base=rounded_plate(84,66,4)
bearing1=box(9,34,4,15,56,29);bearing2=box(69,34,4,75,56,29)
base=union(base,bearing1,bearing2)
base=cut(base,xcyl(3.3,8.9,15.1,CY,CZ),xcyl(3.3,68.9,75.1,CY,CZ))
export('P1_01_bearing_deck',base)
shaft=xcyl(3,-3,87,CY,CZ);export('P1_02_shaft',shaft,axis_x_to_z=True)
drums={}
for kind in ['peg','tooth']:
    drum=union(xcyl(R,20,62,CY,CZ),xcyl(15,62,66,CY,CZ))
    if kind=='peg':feature=cyl(.8,CZ+R-.25,CZ+R+PIN,40,CY,24)
    else:feature=yz_extrude([(39.2,CZ+R-.25),(40.8,CZ+R-.25),(40.8,CZ+R+PIN),(39.2,CZ+R+PIN)],CY-.65,CY+.65)
    drum=union(drum,feature);drum=cut(drum,xcyl(3.3,19.9,66.1,CY,CZ))
    export('P1_03_single_'+kind+'_drum',drum,axis_x_to_z=True);drums[kind]=drum
wash=xcyl(5,0,1,CY,CZ);wash=cut(wash,xcyl(3.3,-.1,1.1,CY,CZ));export('P1_04_washer_print_2',wash,axis_x_to_z=True)
cap=xcyl(6,0,6,CY,CZ);cap=cut(cap,xcyl(3.2,-.1,6.1,CY,CZ),cyl(1.25,CZ,CZ+6.2,3,CY))
export('P1_05_shaft_collar_print_2',cap,axis_x_to_z=True)
for mat in MATS:
    # P1 tip is at CY=45; preserve true free length instead of S2 tip datum.
    root=CY-free_length('C5',mat)
    comb=union(box(30,8,CROOT,50,16,CTOP),box(38.4,15.9,CROOT,41.6,root,CTOP),box(38.4,root-.01,BOT,41.6,CY,CTOP))
    comb=cut(comb,*[cyl(1.7,CROOT-.1,CTOP+.1,x,12) for x in [34,46]])
    export('P1_07_C5_tine_'+mat,comb,flip_x=True)
    if mat=='PETG':pcomb=comb
pclamp=box(30,8,CTOP,50,16,CTOP+2);pclamp=cut(pclamp,*[cyl(1.7,CTOP-.1,CTOP+2.1,x,12) for x in [34,46]])
export('P1_08_clamp_bar',pclamp)
# Accessible attachment ears secure each material-specific root stand to the deck.
for mat in MATS:
    root=CY-free_length('C5',mat)
    stand=box(30,8,4,50,root,CROOT)
    stand=union(stand,box(25,8,4,30.1,16,8),box(49.9,8,4,55,16,8))
    for x in [27.5,52.5]:stand=cut(stand,cyl(1.7,3.9,8.1,x,12))
    for x in [34,46]:stand=cut(stand,cyl(1.7,CROOT-8,CROOT+.1,x,12),cyl(3.3,CROOT-6,CROOT-3.2,x,12,6),box(x-3.3,7.9,CROOT-6,x+3.3,12,CROOT-3.2))
    export('P1_06_root_stand_'+mat,stand)
    if mat=='PETG':pstand=stand
for x in [27.5,52.5]:base=cut(base,cyl(1.7,-.1,4.1,x,12),cyl(3.3,-.1,2.5,x,12,6))
VALID[:]=[v for v in VALID if v['part']!='P1_01_bearing_deck'];export('P1_01_bearing_deck',base)
washer1=wash.copy();washer1.apply_translation([17,0,0]);washer2=wash.copy();washer2.apply_translation([67,0,0]);cap1=cap.copy();cap1.apply_translation([-3,0,0]);cap2=cap.copy();cap2.apply_translation([81,0,0])
ASSEMBLIES['P1_cylinder']=[(base,'#647E7E'),(pstand,'#263F49'),(pcomb,'#CCAB67'),(pclamp,'#263F49'),(drums['peg'],'#D1834B'),(shaft,'#AEC2C3'),(washer1,'#263F49'),(washer2,'#263F49'),(cap1,'#263F49'),(cap2,'#263F49')]

# Independent fit coupon for 6 mm shaft and 3 mm hardware.
coupon=box(0,0,0,64,20,5)
for i,r in enumerate([3.1,3.2,3.3]):coupon=cut(coupon,cyl(r,-.1,5.1,10+20*i,10))
export('00_fit_coupon_6p2_6p4_6p6_bores',coupon)

# Compact material samples. These do not replace tuning in the final mount.
for mat in MATS:
    pieces=[box(0,8,4,60,16,8)]
    for x,n in [(12,'C5'),(28,'G5'),(44,'C6')]:
        root=TIP-free_length(n,mat)
        pieces.extend([box(x-B/2,15.9,4,x+B/2,root,8),box(x-B/2,root-.01,6.8,x+B/2,TIP,8)])
    q=union(*pieces);q=cut(q,cyl(1.7,3.9,8.1,4,12),cyl(1.7,3.9,8.1,56,12));export('00_compact_tuning_sample_'+mat,q,flip_x=True)

# W1 and T1 rotate the tines themselves past a future fixed pick.
# These are rotor layout studies, not complete supported mechanisms.
LO=O/'rotating-tine-layouts';LO.mkdir(exist_ok=True)
wheel_items=[];cylinder_items=[]
def rz(m,angle):q=m.copy();q.apply_transform(tm.transformations.rotation_matrix(angle,[0,0,1]));return q
def rx(m,angle):q=m.copy();q.apply_transform(tm.transformations.rotation_matrix(angle,[1,0,0]));return q
short_notes=['C5','C5','G5','G5','A5','A5','G5']
short_angles=[i*36 for i in range(7)] # Seven onsets; the remaining arc supplies the held note and loop pause.
for mat in MATS:
    ring=cut(cyl(49,1.6,5.6),cyl(44,1.5,5.7))
    parts=[ring]
    for n,deg in zip(short_notes,short_angles):
        root=18+free_length(n,mat)
        parts.extend([rz(box(root,-B/2,1.6,44.2,B/2,5.6),math.radians(deg)),rz(box(18,-B/2,4.4,root+.01,B/2,5.6),math.radians(deg))])
    wheel=union(*parts)
    for deg in [0,120,240]:
        a=math.radians(deg);wheel=cut(wheel,cyl(1.7,1.5,5.7,46.5*math.cos(a),46.5*math.sin(a)))
    export('W1_LAYOUT_rotating_tine_wheel_'+mat,wheel,flip_x=True)
    if mat=='PETG':wheel_items.append((wheel,'#CCAB67'))
    # Core and flange support axial tines with a common plucking station at X=48.
    core=union(xcyl(9,0,52,0,0),xcyl(15,0,8,0,0));pieces=[core]
    for n,deg in zip(short_notes,short_angles):
        root=48-free_length(n,mat)
        pieces.extend([rx(box(7.9,-B/2,8.5,root,B/2,13.6),math.radians(deg)),rx(box(root-.01,-B/2,12.4,48,B/2,13.6),math.radians(deg))])
    rotor=union(*pieces);rotor=cut(rotor,xcyl(3.3,-.1,52.1,0,0));export('T1_LAYOUT_rotating_tine_cylinder_'+mat,rotor,axis_x_to_z=True)
    if mat=='PETG':cylinder_items.append((rotor,'#CCAB67'))
carrier=union(cyl(8,0,1.6),*[rz(box(5,-4,0,49,4,1.6),math.radians(deg)) for deg in [0,120,240]])
carrier=cut(carrier,cyl(3.3,-.1,1.7),*[cyl(1.7,-.1,1.7,46.5*math.cos(math.radians(a)),46.5*math.sin(math.radians(a))) for a in [0,120,240]])
export('W1_LAYOUT_wheel_carrier',carrier);wheel_items.append((carrier,'#263F49'))
assert join_volume(carrier,wheel_items[0][0])<1e-5

# Meaningful digital checks: fixed-body clearance and deliberate tine interference.
CHECKS={'units':'mm','physical_validation':False,'checks':[]}
for x in [17,22,57,92,162,167]:
    body=shifted(shoe,x);pick=shifted(picks[.2],x)
    for label,a,b in [('deck_to_carriage',deck,body),('carriage_to_pick',body,pick),('comb_to_carriage',combs[('ode','PETG')],body)]:
        v=join_volume(a,b);assert v<1e-5,(x,label,v);CHECKS['checks'].append({'system':'S2','x_mm':x,'pair':label,'intersection_mm3':v})
contact=join_volume(combs[('twinkle','PETG')],shifted(picks[.2],22));assert 0<contact<3
CHECKS['checks'].append({'system':'S2','pair':'pick_to_tine_intended_deflection','intersection_mm3':contact,'nominal_lift_mm':.2,'status':'intentional elastic-contact interference; no deformation simulation'})
for kind,drum in drums.items():
    peak=0
    for angle in range(0,360,10):
        q=drum.copy();q.apply_transform(tm.transformations.rotation_matrix(math.radians(angle),[1,0,0],[0,CY,CZ]))
        for label,other in [('deck_and_bearings',base),('root_stand',pstand),('shaft',shaft),('clamp',pclamp)]:
            v=join_volume(q,other);assert v<1e-4,(kind,angle,label,v)
        peak=max(peak,join_volume(q,pcomb))
    assert 0<peak<5,(kind,peak)
    CHECKS['checks'].append({'system':'P1','drum':kind,'angle_samples':36,'unintended_fixed_body_intersection_mm3':0,'maximum_intended_tine_intersection_mm3':peak,'nominal_lift_mm':.3,'status':'rigid geometry screening only; compliant release must be observed physically'})

# Actual mesh previews, orthographic camera with depth-sorted shaded triangles.
FONT='C:/Windows/Fonts/segoeui.ttf'; BOLD='C:/Windows/Fonts/segoeuib.ttf'
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
for key,items in ASSEMBLIES.items():
    render_scene(items,O/(key+'-assembly.png'),key.replace('_',' / '),'Standard PLA / PETG | Parametric development v0.1 | No screws shown')
    # Assembly GLB is for viewing only, not a combined print plate.
    scene=tm.Scene()
    for i,(m,col) in enumerate(items):
        q=m.copy();q.visual.vertex_colors=np.tile(tuple(bytes.fromhex(col.lstrip('#')))+(255,),(len(q.vertices),1));q.apply_scale(.001);scene.add_geometry(q,node_name=str(i))
    scene.export(O/(key+'-assembly-view.glb'))
render_scene(wheel_items,LO/'W1-rotating-tine-wheel.png','W1 / wheel carries the tines','Rotor layout only | Fixed-pick mount and bearings still to design | PETG proxy shown')
render_scene(cylinder_items,LO/'T1-rotating-tine-cylinder.png','T1 / cylinder carries the tines','Rotor layout only | Axial tines meet a future fixed pick | PETG proxy shown')

# Synthetic melody auditions: arrangements, not predicted printed-instrument sound.
for key,s in SONGS.items():
    rate=22050;length=(s['total_ticks']+s['loop_rest_ticks'])*s['seconds_per_tick']+1.;audio=np.zeros(int(length*rate))
    for e in s['events']:
        start=int(e['tick']*s['seconds_per_tick']*rate);t=np.arange(int(.9*rate))/rate;f=e['frequency_Hz'];env=(1-np.exp(-t/.003))*np.exp(-t/.24);tone=env*(np.sin(2*np.pi*f*t)+.23*np.sin(4*np.pi*f*t)+.08*np.sin(6*np.pi*f*t));audio[start:start+len(tone)]+=tone[:len(audio)-start]
    audio=np.int16(audio/max(abs(audio).max(),1)*.8*32767)
    with wave.open(str(O/(key+'-synthetic-melody.wav')),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(rate);w.writeframes(audio.tobytes())

(O/'mesh-validation.json').write_text(json.dumps({'parts':VALID,'checks':CHECKS},indent=2),encoding='utf-8')
(O/'model-parameters.json').write_text(json.dumps({'printer':'Snapmaker U1','nozzle_mm':.4,'units':'mm','material_proxies':MATS,'tine_thickness_mm':H,'tine_width_mm':B,'mesh_cleanup_tolerance_mm':.0001,'slider':{'deck_width_mm':W,'deck_depth_mm':D,'tip_y_mm':TIP,'tine_top_z_mm':TOP,'rail_side_clearance_mm':.3,'rail_top_clearance_mm':.3,'default_lift_mm':.2},'cylinder':{'radius_mm':R,'axis_y_mm':CY,'axis_z_mm':CZ,'pin_height_mm':PIN,'default_lift_mm':.3,'shaft_diameter_mm':6,'bore_mm':6.6,'tine_bottom_z_mm':BOT},'rotating_tines':{'status':'layout only; fixed plucker and support assembly pending','notes':short_notes,'onset_angles_degrees':short_angles,'total_ticks_per_revolution':10,'wheel_outside_diameter_mm':98,'wheel_tip_radius_mm':18,'wheel_tine_thickness_mm':H,'cylinder_length_mm':52,'cylinder_tip_station_x_mm':48,'cylinder_tine_thickness_mm':H}},indent=2),encoding='utf-8')
with zipfile.ZipFile(O/'TINEBOX-v01-STL-and-source.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(STL.glob('*.stl')):z.write(f,'stl/'+f.name)
    for n in ['mesh-validation.json','model-parameters.json','song-programs.json','README-FIRST.md','SONG-SHORTLIST.md','NEXT-STEPS.md','requirements-cad.txt']:
        if (O/n).is_file():z.write(O/n,n)
    for f in O.glob('*-synthetic-melody.wav'):z.write(f,'melody-auditions/'+f.name)
    for f in O.glob('*-assembly.png'):z.write(f,'previews/'+f.name)
    for f in LO.glob('*.png'):z.write(f,'rotating-tine-layouts/'+f.name)
    z.write(Path(__file__),'develop_prototypes.py')
print(json.dumps({'part_count':len(VALID),'mesh_checks_passed':True,'collision_screen_passed':True,'song_programs':list(SONGS),'output':str(O)},indent=2))
