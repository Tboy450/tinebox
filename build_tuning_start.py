from pathlib import Path
from math import pi, sqrt, log2
from html import escape
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
styles=getSampleStyleSheet()
for n,sz,ld,fn in [('T',24,28,'Helvetica-Bold'),('H',13,17,'Helvetica-Bold'),('B',10,14,'Helvetica'),('S',8.5,11.5,'Helvetica'),('C',9,12,'Helvetica')]:
    styles.add(ParagraphStyle(name=n,fontSize=sz,leading=ld,fontName=fn,textColor=colors.HexColor('#17343B'),spaceAfter=8))
story=[]; md=[]
def p(t,s='B'):
    story.append(Paragraph(t,styles[s])); md.append(t.replace('<b>','').replace('</b>','').replace('<br/>','\n')+'\n')
def h(t):p(t,'H')
def page(t):
    if story:story.append(PageBreak())
    p(t,'T')
def table(head,rows,widths):
    data=[[Paragraph('<b>'+escape(str(c))+'</b>',styles['C']) for c in head]]+[[Paragraph(escape(str(c)).replace('\n','<br/>'),styles['C']) for c in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDE9E8')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F6F5')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6)]));story.append(t)
    md.append('| '+' | '.join(head)+' |\n|'+'|'.join(['---']*len(head))+'|\n'+'\n'.join('| '+' | '.join(str(v).replace('\n','; ') for v in r)+' |' for r in rows)+'\n')

beta=1.8751040687
materials={'PETG example':{'E_Pa':1.7e9,'density_kg_m3':1270},'PLA example':{'E_Pa':3.1e9,'density_kg_m3':1240}}
designs={'Slider S1':{'thickness_mm':1.2,'width_mm':3.2},'Rotary ring R1':{'thickness_mm':1.0,'width_mm':2.4}}
notes=[('C5',72),('D5',74),('E5',76),('F5',77),('G5',79),('A5',81),('B5',83),('C6',84)]
def length(f,h,E,rho):return 1000*sqrt(beta**2/(2*pi)*h/1000*sqrt(E/(12*rho))/f)
rows=[]; records=[]
for note,midi in notes:
    f=440*2**((midi-69)/12); row=[note,f'{f:.2f}']
    for dn,geom in designs.items():
        for mn,mat in materials.items():
            L=length(f,geom['thickness_mm'],mat['E_Pa'],mat['density_kg_m3']); row.append(f'{L:.1f}')
            k=mat['E_Pa']/1e6*geom['width_mm']*geom['thickness_mm']**3/(4*L**3)
            records.append({'design':dn,'material_proxy':mn,'note':note,'frequency_target_Hz':f,'free_length_mm_model':L,**geom,**mat,'tip_lift_test_mm':0.15,'ideal_vertical_force_at_test_lift_N':k*.15,'ideal_surface_strain_at_test_lift_percent':100*3*geom['thickness_mm']*.15/(2*L**2)})
    rows.append(row)

page('U1 / preliminary tuning estimates')
p('Slider + rotating comb | October 26, 2026 | Estimate set 01','S')
h('Known setup and explicit assumptions')
p('<b>Working setup:</b> Snapmaker U1, 0.4 mm nozzle, standard PETG or standard PLA, as requested. Snapmaker lists this nozzle size and PLA/PETG support. [1] Proceed with generic standard-material estimates; a specific brand is not required for this design stage. Printed stiffness will be calibrated with mounted test tines.')
p('<b>Material proxies:</b> PETG E = 1.7 GPa, density = 1.27 g/cm^3; PLA E = 3.1 GPa, density = 1.24 g/cm^3. These are horizontal printed-specimen flexural moduli and densities from Prusament datasheets [2, 3], used as first approximations. They are not measurements of your filament or dynamic modulus at musical frequencies.')
p('<b>Geometry:</b> S1 slider: 1.2 mm thick x 3.2 mm wide uniform rectangular tines. R1 rotary comb: 1.0 mm thick x 2.4 mm wide straight radial tines with individual rigid roots. No added masses, tapered flexures, dampers or plucking contact retained during ringing. Free length is measured from the effective rigid clamp to the free tip.')
h('C-major calibration set: free lengths in millimetres')
table(['Note','Target Hz','Slider\nPETG','Slider\nPLA','Rotary\nPETG','Rotary\nPLA'],rows,[44,72,97,97,97,97])
p('Displayed to 0.1 mm to avoid implying machining precision. This is an eight-note test scale, not a Take On Me arrangement or a final song cartridge. The structured JSON retains the calculation values for later updates.','S')
h('Why the two concepts have different estimates')
p('R1 uses thinner tines to test a smaller radial layout; at the same material and pitch, its length is sqrt(1.0/1.2) = 0.913 times S1. Rotation itself does not change pitch. With the same section, material, free length and clamp, the two mechanisms would share the same ideal-beam estimate. [4]')

page('Individual prototype plans')
h('S1 slider: accessible tuning first')
p('Use removable straight tine coupons clamped to a common stiff bar on a bare deck. Start with one C5, G5 and C6 coupon for the chosen material. Keep a consistent clamp edge and screw seating. A nominal 4.4 mm centre spacing leaves 1.2 mm between 3.2 mm tines; this is a test layout, not a proven clearance.')
p('The carriage needs to reach every actual tip location. For this calibration stage, provide a pick that can be repositioned to each test tip. A production slider must either cover the staggered tips or use an aligned-tip design. Adding tip weights or root-shaping to align tips invalidates this uniform-tine table and requires a new model/calibration.')
p('Use an adjustable, replaceable pick and a manual lift for silent return. Begin with approximately 0.15 mm transverse engagement/lift as a low-deflection experiment, then measure clean release and actual slider force. This value is not a fatigue-safe or final acoustic specification.')
h('R1 rotating comb: tune straight spokes independently')
p('Use stationary inward-facing straight tines and one rotating pick. As a layout study, place every tip on an 18 mm radius. The root radius of each tine is then 18 mm plus its table length. At C5, that is about 36.9 mm for the PETG proxy or 40.1 mm for the PLA proxy. Individual root supports must act as rigid clamps; free spokes must clear the deck below.')
p('Variable root positions let the tips share one picking radius without adding masses. Leave space outside the longest root for clamps and a rim: a roughly 95-105 mm diameter test deck is a packaging allowance, not a dimensioned design. A compact final version would need a revised section, register or mass-loaded geometry.')
p('Print and measure three straight coupons first, then mount them on a radial-sector fixture. Compare frequencies before building a full ring. A flexible common ring, clamp movement or curved tine will need its own correction. Do not use a root radius or circular arc length as the free beam length.')
h('If the rotary choice is the pinned drum instead')
p('A thumbwheel drum can use the S1-style fixed tine bank and its own calibration. The drum stores note order and relative timing; it does not need a different tuning table solely because it rotates. C5-C6 diatonic notes are only a calibration example; select the actual song pitches before committing to a fixed bank.')
h('Force and strain checks at the proposed test lift')
checks=[]
for dn in designs:
    for mn in materials:
        rr=[r for r in records if r['design']==dn and r['material_proxy']==mn]
        checks.append([dn,mn.split()[0],f"{min(r['ideal_vertical_force_at_test_lift_N'] for r in rr):.3f}-{max(r['ideal_vertical_force_at_test_lift_N'] for r in rr):.3f}",f"{max(r['ideal_surface_strain_at_test_lift_percent'] for r in rr):.3f}%"])
table(['Design','Proxy','Vertical tine force, N','Max surface strain'],checks,[116,76,174,138])
p('Small-deflection, ideal tip loading only. These loads exclude pick stiffness, friction, detents and drive geometry; they do not predict measured thumb effort or long-term life.','S')

page('Print, measure, correct')
h('Proposed U1 calibration print')
p('Use the 0.4 mm nozzle and a consistent 0.20 mm layer height, including the first layer. Lay tines flat with bending thickness along Z; nominally 1.2 mm is six layers and 1.0 mm is five. Check the sliced preview for solid sections and continuous lengthwise paths. Use one spool and one toolhead for a comparison set, avoid seams at the flexing root, and keep supports off the free tine.')
p('Use solid geometry/100% infill as the starting trial, then measure actual thickness, width and free length. Start with the calibrated U1 profile for standard PETG or PLA and follow the spool instructions for temperatures, cooling and drying. Keep the same spool and settings throughout each calibration set.')
h('Separate calibration for each design and material')
p('1. Measure and pluck C5, G5 and C6 test tines using the intended clamp and low lift. Record actual Hz, repeatability, and whether the strongest spectral peak is the fundamental or an overtone.<br/>2. Calculate a first length correction: <b>L_new = L_old x sqrt(f_measured / f_target)</b>. This applies only when section, material and clamp remain unchanged.<br/>3. Reprint corrected samples and check the result. Once the three samples behave consistently, generate the full song-specific event comb or pitch bank.')
p('Example: a nominal 20.7 mm PETG S1 C5 tine measured at 480 Hz instead of 523.25 Hz gives L_new about 19.8 mm. This is an illustration, not a measured result. A flat tine needs shortening in this model; a sharp tine needs lengthening or another deliberately modelled tuning change.')
h('How uncertain are these numbers?')
p('Frequency scales as h x sqrt(E/rho) / L^2. A hypothetical 20% decrease/increase in effective stiffness changes frequency by about -10.6%/+9.5%, already around musical semitones. At 15 mm free length, a 0.1 mm length error changes pitch by about 23 cents. These are sensitivity examples, not confidence bounds. [4, 5]')
p('Published standard PETG examples also differ: Polymaker reports about 2.28 GPa horizontal bending modulus and 1.30 g/cm^3 [6], compared with the proxy above. That alone gives roughly 7% longer tine lengths for the same target note in this model. Mounted-sample measurements will correct for the actual printed material.')
h('References / remaining information')
refs=[('1','Snapmaker U1 hotend guide','https://wiki.snapmaker.com/en/snapmaker_u1/hot_end_guide'),('2','Prusament PETG technical datasheet, p. 2','https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf'),('3','Prusament PLA technical datasheet, p. 2','https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf'),('4','SOLIDWORKS: cantilever frequency model','https://help.solidworks.com/2026/english/simtutorialonline/Dynamic_Analysis_of_a_Cantilever_Beam.htm?id=1.0.1.3'),('5','UNSW: pitch and cents conversion','https://newt.phys.unsw.edu.au/jw/notes.html'),('6','Polymaker PETG datasheet v2','https://polymaker.com/wp-content/uploads/lana-downloads/TDS_Polymaker_PETG_V2.0_2025-11-17.pdf')]
for n,t,u in refs:p(f'{n}. <link href="{escape(u,quote=True)}" color="#246B78">{escape(t)}</link>','S')
p('Next useful inputs: chosen song excerpts and mounted-sample frequencies. Continue development with standard PETG and PLA; no exact product identification is required at this stage. Neither the eight-note scale nor either mechanism has been physically validated. Body acoustic tests follow after repeatable plucking and tuning.','S')

def footer(c,d):
    c.saveState();c.setStrokeColor(colors.HexColor('#C7D7D5'));c.line(45,40,567,40);c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#536B72'));c.drawString(45,27,'TINEBOX | U1 tuning estimates 01 | 26 Oct 2026');c.drawRightString(567,27,str(d.page));c.restoreState()
dest=OUT/'pdf/TINEBOX-U1-preliminary-tuning.pdf';dest.parent.mkdir(exist_ok=True)
SimpleDocTemplate(str(dest),pagesize=(612,792),leftMargin=54,rightMargin=54,topMargin=40,bottomMargin=55,title='TINEBOX - U1 Preliminary Tuning Estimates',author='Project development').build(story,onFirstPage=footer,onLaterPages=footer)
(OUT/'TINEBOX-U1-preliminary-tuning.md').write_text('\n'.join(md),encoding='utf-8')
data={'status':'preliminary model only; no physical validation','printer':'Snapmaker U1','nozzle_mm':0.4,'material_scope':'standard PETG and standard PLA; generic estimates requested by user','source_of_properties':'Prusament printed-specimen horizontal flexural modulus and density, used as illustrative proxies; not user spool measurements','model':'uniform rectangular Euler-Bernoulli cantilever, rigid clamp, no tip mass','records':records}
(OUT/'TINEBOX-U1-tuning-estimates.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
(OUT/'TINEBOX-printer-material-record.md').write_text('# User-supplied setup\n\n- Printer: Snapmaker U1\n- Nozzle: 0.4 mm\n- Working materials: standard PETG and standard PLA.\n- User requested ignoring metallic colour and proceeding with standard-material estimates; do not require exact brand/product to continue this stage.\n- Develop a variety of slider, radial-comb, pegged-cylinder and toothed-cylinder concepts with material-specific prototype calibration. See PROJECT_SCOPE.md for the current scope.\n- Metal tines and stringed fidget pluckers are welcome future branches when materials become available; current development remains standard PLA/PETG.\n- Physical-comb ownership and desired songs remain unspecified.\n- Preliminary proxy calculations are in TINEBOX-U1-tuning-estimates.json; do not present them as measured material properties.\n',encoding='utf-8')
print(dest)
print(json.dumps(rows))
