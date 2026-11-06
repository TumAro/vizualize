"""shared SVG helpers"""
import math
C = ["#e45", "#27c", "#2a7", "#c80", "#a4c"]
HEAD = ('<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="12" fill="currentColor">'
        '<defs><marker id="a%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0L10,5L0,10z" fill="context-stroke"/></marker></defs>')
def svg(w, h, body, uid=""): return HEAD % (w, h, uid) + "".join(body) + "</svg>"
def T(x, y, s, a="middle", c="currentColor", sz=None):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" fill="{c}"' + (f' font-size="{sz}"' if sz else "") + f'>{s}</text>'
def L(x1, y1, x2, y2, c="#888", w=1.5, arrow="", dash=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"'
            + (f' marker-end="url(#a{arrow})"' if arrow is not None and arrow != "" else "") + (f' stroke-dasharray="{dash}"' if dash else "") + '/>')
def cut(p, q, d):
    dx, dy = q[0]-p[0], q[1]-p[1]; n = math.hypot(dx, dy) or 1
    return p[0]+dx*d/n, p[1]+dy*d/n, q[0]-dx*d/n, q[1]-dy*d/n

