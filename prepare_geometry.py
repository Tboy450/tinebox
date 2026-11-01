"""Extract shared helpers from our own procedural CAD source without running it."""
from pathlib import Path
import ast
s=Path('develop_prototypes.py').read_text(encoding='utf-8')
names={'box','cyl','xcyl','union','cut','rounded_plate','yz_extrude','join_volume','component_count','export','render_scene'}
functions=[ast.get_source_segment(s,n) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name in names]
header='''from pathlib import Path
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

'''
Path('cad_geometry.py').write_text(header+'\n\n'.join(functions)+'\n',encoding='utf-8')
print('Extracted',len(functions),'shared functions; no prototype generator executed.')
