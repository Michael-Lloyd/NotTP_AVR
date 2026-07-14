#!/usr/bin/env python3
"""JAE AA01B-S040VA1 : 40-pin, 0.5mm pitch, dual-row SMT keyboard/BtB connector.
Land pattern derived from JAE drawing SJ036740 (AA01A/B-S040VA1).
Coordinate origin = connector centre. Units mm. +Y downward (KiCad).

Datasheet-exact:
  pitch 0.5 ; 20 pads/row ; row X-span A = 9.5 (centres +/-4.75)
  overall land height 5.3 (mounting outer-outer) ; mounting inner gap 3.3
  mounting pad width 1.55 ; mounting inner edge to 1st signal pad 0.5
  body B = 13.6 (mounting outer edge = B/2 = 6.8, cross-checks 4.75+0.5+1.55)
  resist/centre keep-out D = 4.0 wide x 3.0 tall (signal pad inner edges = +/-1.5)
Measured from drawing (+/-0.1): signal pad 0.20(w) x 1.00(l); rows +/-2.0 (c-c 4.0).
"""
OUT="/home/micl/Work/Electronics/Personal/tpavr/TP_AVR/lib/footprints.pretty/JAE_AA01B-S040VA1.kicad_mod"

# ---- geometry ----
P=0.5; NCOL=20
X0=-4.75                      # first pad centre X
SIG_W=0.20; SIG_L=1.00        # signal pad width(X) x length(Y)
ROW_Y=2.00                    # signal row centre |Y|
MP_W=1.55; MP_L=1.00          # mounting pad
MP_X=6.025; MP_Y=2.15         # mounting pad centres
BODY_L=13.6; BODY_W=4.5       # connector body (fab)
CY_X=7.05; CY_Y=2.95          # courtyard half-extents

def f(v): return f"{v:.4f}".rstrip('0').rstrip('.') if v==v else v

pads=[]
# signal pads: odd = top(-Y), even = bottom(+Y), pin1 top-left
for i in range(NCOL):
    x=round(X0+P*i,4)
    n_top=2*i+1; n_bot=2*i+2
    for n,y in ((n_top,-ROW_Y),(n_bot,ROW_Y)):
        pads.append(f'\t(pad "{n}" smd roundrect (at {f(x)} {f(y)}) (size {f(SIG_W)} {f(SIG_L)}) '
                    f'(layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.25))')
# mounting pads (mechanical hold-downs) named "MP"
for sx in (-MP_X,MP_X):
    for sy in (-MP_Y,MP_Y):
        pads.append(f'\t(pad "MP" smd roundrect (at {f(sx)} {f(sy)}) (size {f(MP_W)} {f(MP_L)}) '
                    f'(layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.15))')

def line(x1,y1,x2,y2,layer,w):
    return (f'\t(fp_line (start {f(x1)} {f(y1)}) (end {f(x2)} {f(y2)}) '
            f'(stroke (width {w}) (type solid)) (layer "{layer}"))')

fab=[]
# fab body outline
fab.append(line(-BODY_L/2,-BODY_W/2, BODY_L/2,-BODY_W/2,"F.Fab",0.1))
fab.append(line( BODY_L/2,-BODY_W/2, BODY_L/2, BODY_W/2,"F.Fab",0.1))
fab.append(line( BODY_L/2, BODY_W/2,-BODY_L/2, BODY_W/2,"F.Fab",0.1))
fab.append(line(-BODY_L/2, BODY_W/2,-BODY_L/2,-BODY_W/2,"F.Fab",0.1))
# fab pin1 chamfer marker
fab.append(line(-BODY_L/2,-BODY_W/2+0.8,-BODY_L/2+0.8,-BODY_W/2,"F.Fab",0.1))

silk=[]
# silk end brackets (outside courtyard-ish, clear of pads). Ends at |X|~6.9..7.0
for sx in (-1,1):
    ex=sx*7.0
    silk.append(line(ex,-CY_Y+0.1, ex, CY_Y-0.1,"F.SilkS",0.12))
# top & bottom silk near ends only (avoid pads): short segments beyond mounting pads
for sy in (-1,1):
    y=sy*(CY_Y-0.1)
    silk.append(line(-7.0,y,-4.9,y,"F.SilkS",0.12))
    silk.append(line( 4.9,y, 7.0,y,"F.SilkS",0.12))
# pin1 silk dot (triangle) near pin1 (top-left, -4.75,-2.0)
silk.append(f'\t(fp_poly (pts (xy -5.15 -2.6) (xy -4.85 -2.6) (xy -5.0 -2.35)) '
            f'(stroke (width 0.1) (type solid)) (fill solid) (layer "F.SilkS"))')

crt=[]
crt.append(line(-CY_X,-CY_Y, CY_X,-CY_Y,"F.CrtYd",0.05))
crt.append(line( CY_X,-CY_Y, CY_X, CY_Y,"F.CrtYd",0.05))
crt.append(line( CY_X, CY_Y,-CY_X, CY_Y,"F.CrtYd",0.05))
crt.append(line(-CY_X, CY_Y,-CY_X,-CY_Y,"F.CrtYd",0.05))

body="\n".join([
 '(footprint "JAE_AA01B-S040VA1"',
 '\t(version 20240108)',
 '\t(generator "tp_avr_gen")',
 '\t(layer "F.Cu")',
 '\t(descr "JAE AA01B-S040VA1, 40-pin 0.5mm-pitch dual-row SMT board-to-board / ThinkPad keyboard FPC connector. Land pattern per JAE SJ036740.")',
 '\t(tags "JAE AA01B 0.5mm 40pin board-to-board thinkpad keyboard FPC")',
 '\t(attr smd)',
 '\t(fp_text reference "REF**" (at 0 -3.7 0) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))',
 '\t(fp_text value "AA01B-S040VA1" (at 0 3.7 0) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))',
 "\n".join(fab),
 "\n".join(silk),
 "\n".join(crt),
 "\n".join(pads),
 ')',
])
open(OUT,"w").write(body+"\n")
print("wrote",OUT)
print("signal pads:",NCOL*2,"+ 4 mounting")
