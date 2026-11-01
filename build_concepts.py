from pathlib import Path
from math import sin, cos, pi
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Line, Circle, String, Polygon

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/pdf'
C=colors.HexColor
styles=getSampleStyleSheet()
for name,size,leading,font,col in [('T',25,28,'Helvetica-Bold','#17343B'),('H',14,18,'Helvetica-Bold','#17343B'),('B',9.5,12.8,'Helvetica','#24353A'),('S',8.5,11.5,'Helvetica','#435C63'),('C',9,12,'Helvetica','#24353A')]:
    styles.add(ParagraphStyle(name=name,fontName=font,fontSize=size,leading=leading,textColor=C(col),spaceAfter=7))
story=[]; notes=[]
def p(t,style='B'):
    story.append(Paragraph(t,styles[style])); notes.append(t.replace('<b>','').replace('</b>','').replace('<br/>','\n')+'\n')
def h(t):
    p(t,'H')
def page(t):
    if story: story.append(PageBreak())
    p(t,'T')
def table(headers,rows,widths):
    data=[[Paragraph('<b>'+escape(v)+'</b>',styles['C']) for v in headers]]+[[Paragraph(escape(v),styles['C']) for v in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C('#DDE9E8')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,C('#F3F6F5')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(t); notes.append('| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(row)+' |' for row in rows)+'\n')
def label(d,x,y,t,col='#435C63',size=9):
    d.add(String(x,y,t,fontName='Helvetica',fontSize=size,fillColor=C(col)))
def arrow(d,x1,y1,x2,y2):
    d.add(Line(x1,y1,x2,y2,strokeColor=C('#D27642'),strokeWidth=2))
    a=__import__('math').atan2(y2-y1,x2-x1)
    d.add(Polygon([x2,y2,x2-8*cos(a-.4),y2-8*sin(a-.4),x2-8*cos(a+.4),y2-8*sin(a+.4)],fillColor=C('#D27642'),strokeColor=None))
def diagram(kind):
    d=Drawing(504,132)
    if kind=='swipe':
        d.add(Rect(12,20,330,93,rx=9,fillColor=C('#F0F4F2'),strokeColor=C('#7F999B')))
        d.add(Rect(35,83,282,14,fillColor=C('#17343B'),strokeColor=None))
        for i in range(9):
            x=45+i*29; d.add(Rect(x,44,9,39,fillColor=C('#9CADA9'),strokeColor=None))
            d.add(Circle(x+4.5,57,3+(i%3),fillColor=C('#D9A65B'),strokeColor=None))
        d.add(Rect(128,30,25,22,rx=3,fillColor=C('#D27642'),strokeColor=None)); arrow(d,51,12,300,12)
        label(d,359,95,'Fixed clamp spine'); label(d,359,75,'Aligned picking tips'); label(d,359,55,'Replaceable pick');label(d,359,35,'Tip weights shown');label(d,359,22,'as a tuning option')
    elif kind=='ring':
        d.add(Circle(92,67,52,fillColor=C('#F0F4F2'),strokeColor=C('#7F999B')))
        d.add(Circle(92,67,29,fillColor=colors.white,strokeColor=C('#7F999B')))
        for i in range(12):
            a=i*2*pi/12; d.add(Line(92+31*cos(a),67+31*sin(a),92+47*cos(a),67+47*sin(a),strokeColor=C('#17343B'),strokeWidth=5))
        d.add(Rect(88,66,8,43,fillColor=C('#D27642'),strokeColor=None));d.add(Circle(92,67,9,fillColor=C('#D27642'),strokeColor=None))
        arrow(d,154,44,154,91);label(d,188,98,'Stationary radial comb cartridge');label(d,188,78,'Thumb dial carries one pick arm');label(d,188,58,'One tine per event, including repeats');label(d,188,38,'Tuning and pick clearance need tests')
    elif kind=='drum':
        d.add(Rect(24,38,270,65,rx=13,fillColor=C('#E6EEEB'),strokeColor=C('#7F999B')))
        for i in range(8):
            x=43+i*31;d.add(Line(x,29,x,58,strokeColor=C('#17343B'),strokeWidth=7))
        for i,j in [(0,1),(1,3),(2,2),(3,1),(4,3),(6,2),(7,1)]:
            d.add(Circle(43+i*31,58+j*11,3.5,fillColor=C('#D27642'),strokeColor=None))
        d.add(Circle(319,70,25,fillColor=C('#D27642'),strokeColor=None));arrow(d,347,45,347,94)
        label(d,365,96,'Swappable pinned drum');label(d,365,76,'Fixed tuned comb');label(d,365,56,'Thumbwheel drives drum');label(d,365,36,'Pin position sets events')
    elif kind=='strip':
        d.add(Rect(15,45,310,50,fillColor=C('#F5EDD9'),strokeColor=C('#B8A782')))
        for i,j in [(0,1),(1,3),(2,2),(3,1),(4,3),(6,2),(7,1)]:
            d.add(Circle(35+i*34,48+j*11,3,fillColor=colors.white,strokeColor=C('#B8A782')))
        d.add(Rect(159,26,72,88,rx=5,fillColor=C('#DDE9E8'),strokeColor=C('#17343B')))
        label(d,168,77,'reader',size=10);label(d,168,62,'+ comb',size=10);arrow(d,45,16,299,16)
        label(d,348,98,'Swap paper song strips');label(d,348,78,'Wheel feeds the strip');label(d,348,58,'Start with an existing');label(d,348,43,'working reader/comb')
    d.scale(1,0.82)
    d.height=109
    return d

page('TINEBOX / improved concepts')
p('Development brief v2 | October 26, 2026 | Mechanism proposals, not print-ready plans','S')
h('What can improve before we know the material')
p('Separate three functions: <b>tuned elements set the available notes; the mechanism chooses when they play; the body shapes how the sound reaches the listener.</b> Different fidget actions need different ways to encode a song. Avoid forcing every option into the original 13-tine slider.')
table(['Concept','Best fit','How songs change','Main unresolved issue'],[
('A. Swipe cartridge','Short hooks and a simple thumb gesture','Swap the tuned event comb; repeated notes get repeated tines.','Reliable pick release; event spacing and hand-controlled tempo.'),
('B. Rotating comb ring','Continuous turning with a short repeating phrase','Swap a radial event-comb cartridge.','More experimental: radial tuning, pick-arm stiffness and ring packing.'),
('C. Thumbwheel drum','Longer phrases and repeated notes using fewer tuned teeth','Swap a pinned drum; keep a compatible tuned comb.','Pin manufacture, alignment, retrigger damping and drive effort.'),
('D. Strip-fed player','Many editable songs and longer arrangements','Swap a punched strip; keep the tuned comb and reader.','Packaging, paper feed and the note set supported by the reader.')
],[94,125,153,132])
h('My starting recommendation')
p('<b>Build A to explore the fidget feel, and develop C for song flexibility.</b> Keep B as a compact rotary experiment. D offers a practical reference mechanism if using bought musical parts is acceptable. An existing working drum or strip mechanism is a stronger baseline than a completely new printed plucking system. [2, 3]')
h('Improvements shared by the concepts')
p('Use a rigid, repeatable comb clamp; a replaceable pick/contact part; accessible adjustment of engagement height; and tactile feedback kept separate from the tuning clamp. Attach sound-body variants to the same structural base so acoustic comparisons do not accidentally change tine free length or clamp stiffness.')
p('A soft mounting layer under the comb may reduce vibration transfer. Keep the comb-to-base path deliberate, and place enclosure seals or anti-rattle features elsewhere unless an isolation experiment is intended. Body volume is one variable alongside panel stiffness, openings and structural coupling. [4]','S')

page('A + B / direct musical fidgets')
h('A. Swipe cartridge - simplify the pick path')
story.append(diagram('swipe'))
p('<b>Action:</b> move one carriage across a stationary row. Start with conventional free-length tuning. Once plucking works, compare an aligned-tip comb with locally shaped flexures or securely attached tip masses. Do not assume that equal-length uniform tines will produce different notes without those other changes. Mass/root-shaping tuning has real music-box precedent. [1]')
p('<b>Song improvement:</b> make each cartridge an event sequence, including repeated-pitch tines and deliberate gaps for timing. Do not force all songs onto evenly spaced teeth. A cartridge-specific tactile strip can follow its event locations.')
p('<b>Return improvement:</b> prototype a thumb-operated lift-to-return pick holder first. That gives a deliberate silent reset without relying on an untested bidirectional ramp. Later test a compliant pick and passive return bypass. If the return does pluck, it plays the notes in reverse order.')
p('<b>First experiment:</b> three notes spanning low, middle and high stiffness, one adjustable replaceable pick, and an exposed bare deck. Check clean release and slider effort before choosing the final number of events. A short event comb will not reproduce an entire song.')
h('B. Rotating comb ring - a short loop without a return stroke')
story.append(diagram('ring'))
p('<b>Action:</b> rotate a central thumb dial carrying a pick past stationary inward-facing tines. The circular cartridge contains the ordered events. A repeated note still needs another tine; this is not a reusable keyboard bank.')
p('<b>Improvements:</b> use an outer locating rim for repeatable cartridge seating, an adjustable pick arm, and an optional detent ring that can be removed during sound testing. Leave an intentional silent sector at the loop join when the arrangement needs a pause.')
p('<b>Tradeoff:</b> a common picking radius simplifies reach, but different tine flexures/masses must fit behind it. Do not bend straight comb geometry into a ring and reuse its tuning table. Begin with a three-tine sector; ring size, event count and tuning range remain open.')
p('Drawings are mechanism maps, not cross-sections or dimensional CAD. They omit guards, bearings, fasteners and contact details.','S')

page('C + D / more flexible song storage')
h('C. Thumbwheel drum - keep the notes, swap the program')
story.append(diagram('drum'))
p('<b>Action:</b> turn a wheel connected to a pinned cylinder beside a fixed tuned comb. Each tine is a pitch; pin position along the cylinder selects it, and angular position sets the onset. The same tine can be used repeatedly, subject to retrigger spacing. This follows an established music-box architecture. [2]')
p('<b>Improvements:</b> key the drum to a start position, provide a protected wheel edge for the thumb, and design the bearing/comb alignment as one rigid module. Start with a one-direction drive and removable end support. Any ratchet or detent must be tested for noise and added torque.')
p('<b>Song change:</b> a compatible drum can change event order and rhythm without retuning the comb. A song requiring an absent pitch still needs transposition, arrangement changes, or a different tuned bank. Do not promise any song on one small comb.')
p('<b>Prototype path:</b> first use an existing working comb/drum module inside a printed ergonomic body if suitable parts are available. For a custom drum, test one pinned track and a single tine, including repeated plucks and damping, before a whole tune. Printed pins and all-printed tines remain experiments.')
h('D. Strip-fed player - editable songs with a rolling action')
story.append(diagram('strip'))
p('<b>Action:</b> a thumbwheel or crank feeds a punched paper strip through a mechanical reader. Holes encode notes and timing; the reader actuates a fixed tuned comb. Commercial paper-strip music boxes demonstrate this approach. [3]')
p('<b>Improvements:</b> add a fold-flat wheel handle, a supported entry guide and a clear start mark. A protective strip sleeve or spool cassette can be explored after straight feeding works. An endless loop needs its own bend-radius, seam and feed test.')
p('<b>Tradeoff:</b> this is a rolling musical object with loose media, rather than the original compact swipe. Using an existing reader/comb avoids inventing the hole-to-pluck mechanism at the same time as tuning the instrument.')
p('For either C or D, hand speed still controls overall tempo. The pattern stores relative timing; a governor, motor or deliberate beat indexing would be an additional subsystem. Closely repeated notes may buzz or fail without appropriate release and damping. [2]','S')

page('Measurements / songs / next steps')
h('What information is needed, and when')
table(['Information','Why it matters'],[
('Printer model, nozzle diameter, filament type/brand; willingness to use metal parts','Chooses a realistic process, clearance trials and the tuning route. No dimensions should be finalized from filament name alone.'),
('If a physical comb exists: free lengths from clamp to tip, width, bending thickness, clamp position and added weights','Provides a first mechanical model. A ruler photo helps with layout; calipers help with thickness. The eBay photograph alone cannot supply these values.'),
('If testing printed tines: orientation, layer height, wall/infill settings and measured sample dimensions','Printed stiffness depends on the actual print. Test with the same process intended for the finished part.'),
('A recording or measured frequency from each mounted test tine','This is the most useful tuning calibration. Use the intended clamp, isolated plucks and a spectrum/tuner; distinguish the fundamental from overtones.'),
('Preferred action, approximate pocket size and 2-3 exact song hooks','Determines whether short event combs are sufficient or a reusable note bank with a drum/strip is the better route.')
],[211,293])
h('How we will choose and fit songs')
p('For each requested excerpt, list the exact pitches, repeated onsets, rests and relative durations. Then check: available pitch range; number of events; shortest time between repeats; comfortable stroke/turn; and whether transposition preserves recognizability. A hook may fit even when the full arrangement does not.')
p('For A/B, count every pluck as an event and duplicate its pitch when needed. For C/D, count unique pitches separately from events and respect the mechanism\'s repeat-rate and media limits. Start with a simple ascending pattern and a repeated-note pattern, then test Take On Me or another chosen hook. No song arrangement is validated yet.')
h('Tuning workflow')
p('Measure three mounted samples before generating a final tuning chart. For an otherwise unchanged uniform tine, L_new = L_old x sqrt(f_measured / f_target) gives a first length estimate. Tip masses, shaped flexures and changing clamps need additional calibration. Reserve a tuning adjustment rather than assuming the first print will be in tune. [1, 5]','S')
h('References and status')
refs=[('1','Muro Box: comb development and mass/root tuning','https://murobox.com/en/our-story/the-comb/'),('2','Music Box Attic: Sankyo movement installation and damping','https://www.bettermusicboxes.com/products/movements/installation/music-box-movement-instructions.asp'),('3','Kikkerland: punched-strip music-box mechanism','https://kikkerland.com/products/make-your-own-music-box-kit'),('4','Reuge: soundboard coupling and enclosure effects','https://www.reuge.com/en/foire-aux-questions'),('5','SOLIDWORKS: uniform cantilever frequency model','https://help.solidworks.com/2026/english/simtutorialonline/Dynamic_Analysis_of_a_Cantilever_Beam.htm?id=1.0.1.3')]
for n,t,u in refs:p(f'{n}. <link href="{escape(u,quote=True)}" color="#246B78">{escape(t)}</link>','S')
p('Original concept improvements in this brief are engineering proposals. Manufacturer references establish underlying principles or existing architectures, not the performance of these proposed fidgets. Exact dimensions, materials, tuning, song compatibility and life testing remain pending.','S')
def footer(c,d):
    c.saveState();c.setStrokeColor(C('#C7D7D5'));c.line(45,40,567,40);c.setFont('Helvetica',8);c.setFillColor(C('#536B72'));c.drawString(45,27,'TINEBOX | Improved concepts v2 | 26 Oct 2026');c.drawRightString(567,27,str(d.page));c.restoreState()
OUT.mkdir(parents=True,exist_ok=True)
SimpleDocTemplate(str(OUT/'TINEBOX-improved-concepts-v2.pdf'),pagesize=(612,792),leftMargin=54,rightMargin=54,topMargin=40,bottomMargin=55,title='TINEBOX - Improved Concepts v2',author='Project development').build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT/'output/TINEBOX-improved-concepts-v2.md').write_text('\n'.join(notes),encoding='utf-8')
print(OUT/'TINEBOX-improved-concepts-v2.pdf')
