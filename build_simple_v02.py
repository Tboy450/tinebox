"""Two small first-build fixtures. PLA/PETG; mm; physical tests still required."""
from pathlib import Path
import sys, math, json, zipfile, shutil
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tmp/cad-libs'))
import numpy as np
import trimesh as tm
from PIL import Image, ImageDraw, ImageFont
from xml.etree import ElementTree as ET
import cad_geometry as g

O=ROOT/'output/simple-v02';g.configure(O)
W=80.;TIP=44.;TOP=8.;H=1.2;B=3.2;BOTTOM=TOP-H
MOUNTS=[(14.,12.),(66.,12.)]
MATS={'PETG':{'E':1.7e9,'rho':1270},'PLA':{'E':3.1e9,'rho':1240}}
HZ={'C5':523.2511306,'G5':783.990872,'A5':880.}
def length(note,mat):
    m=MATS[mat];return 1000*math.sqrt(1.8751040687**2/(2*math.pi)*H/1000*math.sqrt(m['E']/(12*m['rho']))/HZ[note])
def holes(m,z0,z1):return g.cut(m,*[g.cyl(1.7,z0,z1,x,y) for x,y in MOUNTS])
def shifted(m,x=0,y=0,z=0):q=m.copy();q.apply_translation([x,y,z]);return q

# Common clamp and aligned-tip comb interface. Free tines print flat after flipping.
def comb(entries):
    parts=[g.box(10,8,4,70,16,TOP)]
    for x,L in entries:
        root=TIP-L;assert root>=17 and root<TIP
        parts.extend([g.box(x-B/2,15.9,4,x+B/2,root,TOP),g.box(x-B/2,root-.01,BOTTOM,x+B/2,TIP,TOP)])
    return holes(g.union(*parts),3.9,8.1)
sample=comb([(22,26.),(37,22.),(52,18.)])
g.export('01_shared_three_length_comb_26_22_18mm',sample,flip_x=True)
clamp=holes(g.box(10,8,8,70,16,10),7.9,10.1);g.export('02_shared_clamp_bar',clamp)

def deck(nrail):
    d=g.rounded_plate(W,50 if not nrail else 64,4)
    if nrail:d=g.union(d,g.box(0,0,4,W,6,14),g.box(0,52,4,W,58,14))
    for x,y in MOUNTS:d=g.cut(d,g.cyl(1.7,-.1,4.1,x,y),g.cyl(3.3,-.1,2.5,x,y,6))
    return d
manual=deck(False);slider=deck(True)
g.export('A_01_manual_base',manual);g.export('B_01_dual_rail_base',slider)
fit=g.box(0,0,0,60,24,4)
for x,diam,af in [(10,3.2,5.7),(30,3.4,5.9),(50,3.6,6.1)]:
    fit=g.cut(fit,g.cyl(diam/2,-.1,4.1,x,6),g.cyl(af/math.sqrt(3),-.1,2.5,x,17,6),g.cyl(1.7,-.1,4.1,x,17))
g.export('00_M3_fit_coupon',fit)

# The carriage has two widely separated support lands. Roof undersides sit on
# rail tops at Z=14; the old floating 0.3 mm roof gap is removed.
pieces=[g.box(-7,-1.3,14,7,59.3,16.4)]
for a,b in [(-1.3,-.3),(6.3,7.3),(50.7,51.7),(58.3,59.3)]:pieces.append(g.box(-7,a,5,7,b,16.4))
shoe=g.union(*pieces,g.box(-6,45,5,6,51.7,13.4))
# Pick floor at Z=6 is a seating datum; roof/side clearance is elsewhere.
shoe=g.cut(shoe,g.box(-4.2,44.9,6,4.2,51.8,8.6))
NUT_Y=48.35
shoe=g.cut(shoe,g.cyl(1.7,8.5,13.5,0,NUT_Y),g.cyl(3.3,9.8,12.4,0,NUT_Y,6),g.box(-6.1,NUT_Y-2.86,9.8,0,NUT_Y+2.86,12.4),g.cyl(3.6,13.35,16.5,0,NUT_Y))
g.export('B_02_bridge_carriage',shoe,flip_x=True)
picks={}
for lift in [-.2,0.,.2,.4]:
    crest=BOTTOM+lift
    blade=g.yz_extrude([(-.8,6),(.8,6),(.8,6.4),(-.8,crest)],42.8,46.1)
    p=g.union(g.box(-4,46,6,4,51.5,8.4),blade)
    tag=('minus_' if lift<0 else '')+str(abs(lift)).replace('.','p')
    g.export('B_03_pick_lift_'+tag,p);picks[lift]=p

song_combs={}
for mat in MATS:
    # The seven-note opening of Twinkle uses three repeated target pitches.
    ns=['C5','C5','G5','G5','A5','A5','G5']
    c=comb([(22+5*i,length(n,mat)) for i,n in enumerate(ns)])
    g.export('OPTIONAL_twinkle_opening_'+mat,c,flip_x=True);song_combs[mat]=c

# Reserved hardware envelopes, included in clearance checks rather than omitted
# from the model. Check actual fasteners against these maxima before assembly.
heads=[g.cyl(3,10,13.2,x,y) for x,y in MOUNTS]
studs=[g.cyl(1.5,0,10,x,y) for x,y in MOUNTS]
pick_screw=g.union(g.cyl(1.5,8.4,14.4,0,NUT_Y),g.cyl(3,14.4,17.6,0,NUT_Y))
# Nut/thread engagement is intentionally not treated as free-space clearance.
checks=[]
def clear(label,a,b,tol=2e-5):
    v=g.join_volume(a,b);assert v<tol,(label,v);checks.append({'check':label,'intersection_mm3':v,'passed':True})
for xc in np.arange(17,57.00001,.5):
    carrier=shifted(shoe,xc);pick=shifted(picks[.2],xc);screw=shifted(pick_screw,xc)
    clear('carriage_to_deck_x_'+str(xc),carrier,slider)
    clear('carriage_to_comb_x_'+str(xc),carrier,sample)
    clear('carriage_to_clamp_x_'+str(xc),carrier,clamp)
    clear('carriage_to_seated_pick_x_'+str(xc),carrier,pick)
    clear('carriage_to_pick_screw_x_'+str(xc),carrier,screw)
    for i,head in enumerate(heads):clear('carriage_to_clamp_screw_'+str(i)+'_x_'+str(xc),carrier,head)

# Gravity support: ideal rail and pick-floor contact faces coincide (zero gap).
support={'rail_top_z_mm':14.,'carriage_roof_underside_z_mm':14.,'pick_floor_z_mm':6.,'pick_base_bottom_z_mm':6.,'front_and_rear_rail_centres_y_mm':[3.,55.],'pick_contact_y_mm':43.4,'front_rail_reaction_fraction':(43.4-3)/52,'rear_rail_reaction_fraction':(55-43.4)/52,'note':'Ideal static vertical force lies inside the support span. Printed flatness, operator load, rocking and friction remain unmeasured.'}
assert support['front_rail_reaction_fraction']>0 and support['rear_rail_reaction_fraction']>0

# Rigid contact-envelope sketch: maximum ramp intrusion into one undeflected tine.
# This can identify a release edge, not prove elastic/acoustic release behaviour.
profile=[]
for x in np.arange(-4,4.0001,.01):
    left=max(-B/2,x-.8);right=min(B/2,x+.8)
    height=0. if left>=right else max(0.,7.-(left-(x-.8))*(.6/1.6)-BOTTOM)
    profile.append({'relative_pick_x_mm':round(float(x),3),'nominal_tine_lift_mm':round(height,5)})
assert abs(max(v['nominal_tine_lift_mm'] for v in profile)-.2)<1e-6
clear('manual_base_to_comb',manual,sample);clear('manual_clamp_to_comb',clamp,sample)

validation={'status':'digital checks only; not sliced or physically validated','parts':g.VALID,'sampled_clearance_checks':checks,'support_datums':support,'reserved_clamp_head_diameter_mm':6.,'reserved_clamp_head_height_mm':3.2,'contact_model_limit':'Rigid unflexed geometry only. Tine/pick overlap is deliberate; no contact-force, vibration, fatigue or FDM simulation.'}
(O/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
(O/'contact-envelope.json').write_text(json.dumps(profile,indent=2),encoding='utf-8')
old={'P1_nominal_lift_mm':.3,'P1_two_radial_clearances_mm':[.3,.3],'P1_gravity_settled_lift_mm':-.3,'S2_nominal_lift_mm':.2,'S2_roof_seating_gap_mm':.3,'S2_after_seating_lift_mm':-.1,'decision':'Supersede the old slider and cylinder assemblies as first-build recommendations. Keep rotor layouts as exploration.'}
(O/'v01-audit-findings.json').write_text(json.dumps(old,indent=2),encoding='utf-8')

g.render_scene([(manual,'#647E7E'),(sample,'#CCAB67'),(clamp,'#263F49'),*[(h,'#AEB8BE') for h in heads]],O/'A-manual-sound-test.png','A / three-tine sound test','First print: fixed lengths, no assumed notes | Support the spine and pluck by hand')
xc=37
g.render_scene([(slider,'#647E7E'),(sample,'#CCAB67'),(clamp,'#263F49'),(shifted(shoe,xc),'#D1834B'),(shifted(picks[.2],xc),'#C65442'),(shifted(pick_screw,xc),'#AEB8BE'),*[(h,'#AEB8BE') for h in heads]],O/'B-dual-rail-slider.png','B / supported slider bench','Shared comb and clamp | Positive seating datums | Hardware envelopes included')
canvas=Image.new('RGB',(1700,620),'#F7F7F1')
ImageDraw.Draw(canvas).text((30,15),'Simple first builds / v0.2 / start with A',font=ImageFont.truetype(g.BOLD,28),fill='#173D43')
for i,p in enumerate(['A-manual-sound-test.png','B-dual-rail-slider.png']):canvas.paste(Image.open(O/p).resize((850,525)),(i*850,70))
canvas.save(O/'two-simple-builds.png')

# Nominal dimensions from model only; the first trial records actual frequencies.
parameters={'date':'2026-10-27','printer':'Snapmaker U1','nozzle_mm':.4,'units':'mm','tine_thickness_mm':H,'tine_width_mm':B,'sample_free_lengths_mm':[26.,22.,18.],'sample_pitch_status':'unassigned; measure after clamping','material_proxies_for_optional_song':MATS,'manual_size_mm':manual.extents.round(3).tolist(),'slider_size_mm':slider.extents.round(3).tolist(),'pick_lifts_mm':list(picks),'nominal_twinkle_frequencies_Hz':HZ,'manual_cantilever_clearance_below_mm':BOTTOM-4}
(O/'parameters.json').write_text(json.dumps(parameters,indent=2),encoding='utf-8')

# Core 3MF containers: geometry and arrangement only, without printer settings.
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',NS)
def print_plate(name,items):
    model=ET.Element('{'+NS+'}model',{'unit':'millimeter'})
    res=ET.SubElement(model,'{'+NS+'}resources');build=ET.SubElement(model,'{'+NS+'}build')
    info=[];meshes=[]
    for oid,(part,x,y) in enumerate(items,1):
        m=tm.load_mesh(O/'stl'/(part+'.stl'));m.apply_translation([x,y,0]);meshes.append(m)
        assert m.bounds[0,2]>=-1e-5 and max(m.bounds[1,:2])<270
        obj=ET.SubElement(res,'{'+NS+'}object',{'id':str(oid),'name':part,'type':'model'});mesh=ET.SubElement(obj,'{'+NS+'}mesh');verts=ET.SubElement(mesh,'{'+NS+'}vertices');faces=ET.SubElement(mesh,'{'+NS+'}triangles')
        for xx,yy,zz in m.vertices:ET.SubElement(verts,'{'+NS+'}vertex',{'x':str(float(xx)),'y':str(float(yy)),'z':str(float(zz))})
        for a,b,c in m.faces:ET.SubElement(faces,'{'+NS+'}triangle',{'v1':str(a),'v2':str(b),'v3':str(c)})
        ET.SubElement(build,'{'+NS+'}item',{'objectid':str(oid)})
        info.append({'part':part,'bounds_mm':m.bounds.round(3).tolist(),'vertices':len(m.vertices),'triangles':len(m.faces)})
    for i,a in enumerate(meshes):
        for b in meshes[i+1:]:assert g.join_volume(a,b)<1e-5
    out=O/(name+'.3mf')
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
        z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    # Round-trip with a separate importer; verify object counts and millimetre bounds.
    loaded=tm.load_scene(out);assert len(loaded.geometry)==len(items)
    expected=np.array([np.vstack([m.vertices for m in meshes]).min(0),np.vstack([m.vertices for m in meshes]).max(0)])
    assert np.allclose(loaded.bounds,expected,atol=1e-4)
    return {'file':out.name,'objects':info,'round_trip_import_passed':True,'units':'millimeter','printer_profile':'not included'}
plates=[print_plate('A_manual_test_plate', [('A_01_manual_base',0,0),('01_shared_three_length_comb_26_22_18mm',90,0),('02_shared_clamp_bar',90,42)]),print_plate('B_slider_test_plate',[('B_01_dual_rail_base',0,0),('01_shared_three_length_comb_26_22_18mm',90,0),('02_shared_clamp_bar',90,42),('B_02_bridge_carriage',0,74),('B_03_pick_lift_minus_0p2',24,74),('B_03_pick_lift_0p2',38,74)])]
(O/'print-plate-checks.json').write_text(json.dumps(plates,indent=2),encoding='utf-8')
with zipfile.ZipFile(O/'TINEBOX-simple-v02.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in (O/'stl').glob('*.stl'):z.write(p,'stl/'+p.name)
    for n in ['README-FIRST.md','PRINT-CHECKLIST.md','validation.json','parameters.json','v01-audit-findings.json','contact-envelope.json','print-plate-checks.json','A_manual_test_plate.3mf','B_slider_test_plate.3mf','A-manual-sound-test.png','B-dual-rail-slider.png','two-simple-builds.png']:
        if (O/n).exists():z.write(O/n,n)
    for n in ['build_simple_v02.py','cad_geometry.py']:z.write(ROOT/n,n)
    z.write(ROOT/'output/prototypes-v01/requirements-cad.txt','requirements-cad.txt')
print(json.dumps({'parts':len(g.VALID),'sampled_clearance_checks_passed':len(checks),'output':str(O)},indent=2))
