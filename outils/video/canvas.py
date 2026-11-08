# -*- coding: utf-8 -*-
"""Primitives de dessin pour les images de la vidéo (1920x1080)."""
import math

W, H = 1920, 1080
BG   = "#fbf7ef"
INK  = "#1d1d20"
MUT  = "#55606e"
POS  = "#c0392b"
NEG  = "#1d4ed8"
ACC  = "#0a7f52"
SOFT = "#9aa1ab"
OR   = "#ee7d23"
PALE = "#efe7d8"
SANS = "DejaVu Sans, Verdana, sans-serif"
SERIF = "DejaVu Serif, Georgia, serif"

def ease(t):                      # 0..1 -> 0..1, doux aux deux bouts
    return t * t * (3 - 2 * t)

def pingpong(t):                  # 0..1 -> 0..1..0
    return ease(2 * t) if t < 0.5 else ease(2 - 2 * t)

def clamp(x, a=0.0, b=1.0):
    return a if x < a else (b if x > b else x)

def seg(t, t0, t1):               # progression de 0 a 1 entre t0 et t1
    return 0.0 if t <= t0 else (1.0 if t >= t1 else ease((t - t0) / (t1 - t0)))


class C:
    def __init__(self):
        self.el = []

    # ---------- primitives ----------
    def rect(self, x, y, w, h, fill="none", col=None, sw=2.0, rx=0, op=None, dash=None):
        a = ' rx="%g"' % rx if rx else ''
        a += ' stroke="%s" stroke-width="%g"' % (col, sw) if col else ''
        a += ' opacity="%g"' % op if op is not None else ''
        a += ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"%s/>'
                       % (x, y, w, h, fill, a))

    def line(self, x1, y1, x2, y2, col=MUT, sw=3.0, dash=None, op=None, cap="round"):
        a = ' stroke-dasharray="%s"' % dash if dash else ''
        a += ' opacity="%g"' % op if op is not None else ''
        self.el.append('<path d="M%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="%g" '
                       'stroke-linecap="%s"%s/>' % (x1, y1, x2, y2, col, sw, cap, a))

    def path(self, d, col=MUT, sw=3.0, fill="none", dash=None, op=None):
        a = ' stroke-dasharray="%s"' % dash if dash else ''
        a += ' opacity="%g"' % op if op is not None else ''
        self.el.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%g" stroke-linecap="round" '
                       'stroke-linejoin="round"%s/>' % (d, fill, col, sw, a))

    def arrow(self, x1, y1, x2, y2, col=MUT, sw=5.0, head=20.0, op=None, dash=None):
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        if L < 1e-6:
            return
        ux, uy = dx / L, dy / L
        bx, by = x2 - ux * head, y2 - uy * head
        px, py = -uy, ux
        a = ' opacity="%g"' % op if op is not None else ''
        d = ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<path d="M%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" stroke-width="%g" '
                       'stroke-linecap="round"%s%s/>' % (x1, y1, bx, by, col, sw, a, d))
        self.el.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="%s" stroke="none"%s/>'
                       % (x2, y2, bx + px * head * 0.42, by + py * head * 0.42,
                          bx - px * head * 0.42, by - py * head * 0.42, col, a))

    def circle(self, cx, cy, r, col=MUT, sw=3.0, fill="none", op=None, dash=None):
        a = ' opacity="%g"' % op if op is not None else ''
        a += ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" '
                       'stroke-width="%g"%s/>' % (cx, cy, r, fill, col, sw, a))

    def ell(self, cx, cy, rx, ry, col=SOFT, sw=2.0, dash="8 10", op=None):
        a = ' opacity="%g"' % op if op is not None else ''
        a += ' stroke-dasharray="%s"' % dash if dash else ''
        self.el.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" '
                       'stroke-width="%g"%s/>' % (cx, cy, rx, ry, col, sw, a))

    def dot(self, cx, cy, r, col=INK, op=None):
        a = ' opacity="%g"' % op if op is not None else ''
        self.el.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (cx, cy, r, col, a))

    def txt(self, x, y, s, size=34, col=INK, anchor="middle", it=False, bold=False, op=None,
            family=None):
        a = ' opacity="%g"' % op if op is not None else ''
        a += ' font-style="italic"' if it else ''
        a += ' font-weight="bold"' if bold else ''
        self.el.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-family="%s" font-size="%g" '
                       'fill="%s"%s>%s</text>'
                       % (x, y, anchor, family or (SERIF if it else SANS), size, col, a, esc(s)))

    def charge(self, cx, cy, sign, r=30, col=None, op=None, lw=3.2):
        c = col or (POS if sign > 0 else (NEG if sign < 0 else SOFT))
        self.circle(cx, cy, r, col=c, sw=lw, fill="#ffffff", op=op)
        self.line(cx - r * 0.5, cy, cx + r * 0.5, cy, col=c, sw=lw + 0.6, op=op)
        if sign > 0:
            self.line(cx, cy - r * 0.5, cx, cy + r * 0.5, col=c, sw=lw + 0.6, op=op)

    def label(self, x, y, s, size=26, col=MUT, anchor="middle", op=None):
        self.txt(x, y, s, size=size, col=col, anchor=anchor, op=op)

    # encadré avec un liseré, pour poser une formule ou une idée
    def card(self, x, y, w, h, col=OR, fill="#ffffff", op=None, sw=3.0):
        self.rect(x, y, w, h, fill=fill, col=col, sw=sw, rx=10, op=op)

    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
                '<rect width="%d" height="%d" fill="%s"/>%s</svg>'
                % (W, H, W, H, W, H, BG, "".join(self.el)))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def head(c, titre, numero=None, total=None):
    """bandeau du haut + barre de progression"""
    c.rect(0, 0, W, 112, fill="#ffffff")
    c.line(0, 112, W, 112, col=PALE, sw=4, cap="butt")
    c.txt(70, 56, "Champ électrique", size=27, col=MUT, anchor="start")
    c.txt(70, 90, "Olivier Wulveryck · Creative Commons", size=20, col=SOFT, anchor="start")
    c.txt(W - 70, 74, titre, size=40, col=INK, anchor="end", bold=True)
    if numero is not None:
        c.rect(0, H - 8, W, 8, fill=PALE)
        c.rect(0, H - 8, W * clamp(numero / float(total)), 8, fill=OR)

def formule(c, s, y=985, col=INK, size=46, sub=None, op=None):
    """bande de formule en bas de l'image"""
    c.txt(W / 2, y, s, size=size, col=col, it=True, op=op)
    if sub:
        c.txt(W / 2, y + 42, sub, size=25, col=MUT, op=op)
