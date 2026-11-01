"""Fit measured mounted tines and export a predicted seven-event Twinkle comb.
No example frequency is a physical measurement. Run with --help for usage.
"""
from pathlib import Path
import argparse, json, math, statistics, sys
ROOT=Path(__file__).resolve().parent

def fit(data):
    if data.get('material') not in ('PLA','PETG'):
        raise ValueError('Set material to PLA or PETG; measure each separately.')
    if data.get('fundamentals_checked') is not True:
        raise ValueError('Confirm measured fundamentals, rather than strongest harmonics, first.')
    if data.get('fixture') != 'A_manual_v02_v03':
        raise ValueError('This export requires the shared mounted manual fixture.')
    for key,target in [('tine_thickness_mm',1.2),('tine_width_mm',3.2)]:
        if not isinstance(data.get(key),(int,float)) or abs(data[key]-target)>.01:
            raise ValueError('This export requires nominal 1.2 mm thickness and 3.2 mm width.')
    rows=data.get('measurements',[])
    if len(rows)<3: raise ValueError('Supply at least three distinct measured free lengths.')
    for row in rows:
        for k in ('free_length_mm','fundamental_Hz'):
            v=row.get(k)
            if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0:
                raise ValueError('Every length and measured fundamental must be a positive finite number.')
    if len(set(r['free_length_mm'] for r in rows))<3:
        raise ValueError('At least three distinct lengths are required.')
    c=statistics.median(r['fundamental_Hz']*r['free_length_mm']**2 for r in rows)
    residuals=[dict(r,predicted_Hz=c/r['free_length_mm']**2,
        relative_error=abs(c/r['free_length_mm']**2/r['fundamental_Hz']-1)) for r in rows]
    if max(r['relative_error'] for r in residuals)>.05:
        raise ValueError('Measurements disagree with the inverse-square model by over 5%. Check harmonics, mounting and geometry; no comb exported.')
    sequence=['C5','C5','G5','G5','A5','A5','G5']
    hz={'C5':523.2511306,'G5':783.990872,'A5':880.0}
    events=[{'note':n,'target_Hz':hz[n],'free_length_mm':math.sqrt(c/hz[n]),'centre_x_mm':22+5*i} for i,n in enumerate(sequence)]
    if any(not 14<=e['free_length_mm']<=27 for e in events):
        raise ValueError('This pitch range needs lengths outside this fixture\'s 14–27 mm design range. Change register/section in a separate design; no silent clipping.')
    return {'status':'Prediction from measurements; final comb must be measured again.',
        'material':data['material'],'model':'f_Hz = C_Hz_mm2 / free_length_mm squared',
        'C_Hz_mm2':c,'screening_limit_relative':.05,'measurements':residuals,'events':events,
        'timing':'Equal 5 mm event spacing; rhythm is controlled by the hand, not mechanically encoded.',
        'limits':'Screening residual is not a confidence bound. Duplicate tines, different roots and slider mounting can shift pitch.'}

def export(data,out):
    result=fit(data) # Validate before creating output or loading CAD dependencies.
    sys.path.insert(0,str(ROOT/'tmp/cad-libs'))
    import cad_geometry as g
    out=Path(out);g.configure(out)
    parts=[g.box(10,8,4,70,16,8)]
    for e in result['events']:
        x=e['centre_x_mm'];root=44-e['free_length_mm']
        parts.extend([g.box(x-1.6,15.9,4,x+1.6,root,8),g.box(x-1.6,root-.01,6.8,x+1.6,44,8)])
    comb=g.cut(g.union(*parts),*[g.cyl(1.7,3.9,8.1,x,12) for x in (14,66)])
    g.export('PREDICTED_twinkle_'+data['material'],comb,flip_x=True)
    result['mesh_checks']=g.VALID
    (out/'prediction.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out/'measurement-input.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('measurements',type=Path)
    ap.add_argument('--output',type=Path,default=ROOT/'output/measured-song-comb')
    args=ap.parse_args()
    try:
        result=export(json.loads(args.measurements.read_text(encoding='utf-8-sig')),args.output)
    except (ValueError,KeyError,TypeError) as exc: ap.exit(2,str(exc)+'\n')
    print(json.dumps(result,indent=2))
