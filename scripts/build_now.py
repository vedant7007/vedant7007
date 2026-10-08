"""Redraws assets/now.svg from now.md. Run: python scripts/build_now.py"""
import base64, html, io, os, re, sys
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from holo import holo  # noqa: E402

INK = "#101A33"
FONTS = os.path.join(ROOT, "scripts", "fonts")


def read_lines():
    text = open(os.path.join(ROOT, "now.md"), encoding="utf-8").read()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = [l.strip().lstrip("-*").strip() for l in text.splitlines() if l.strip()]
    if not 1 <= len(lines) <= 4:
        sys.exit(f"now.md needs 1 to 4 lines, found {len(lines)}")
    return lines


def font(path, text):
    f = TTFont(path)
    o = subset.Options(); o.flavor = "woff2"; o.layout_features = ["kern", "liga"]
    s = subset.Subsetter(o); s.populate(text=text + "’"); s.subset(f)
    b = io.BytesIO(); f.flavor = "woff2"; f.save(b)
    return base64.b64encode(b.getvalue()).decode()


def wrap(t, n=38):
    out, cur = [], ""
    for w in t.split():
        if cur and len(cur) + len(w) + 1 > n:
            out.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    return out[:2]


def e(s):
    return html.escape(s, quote=True).replace("'", "&#8217;")


def build():
    lines = read_lines()
    disp = font(os.path.join(FONTS, "big-shoulders-display-latin-900-normal.woff2"), "Right now")
    body = font(os.path.join(FONTS, "atkinson-hyperlegible-latin-700-normal.woff2"), "".join(lines))
    W, H = 1200, 330
    items = ""
    for i, t in enumerate(lines):
        col, row = divmod(i, 2)
        x, y = 64 + col * 560, 160 + row * 84
        items += (f'<circle class="ring" style="animation-delay:{i * 0.6}s" cx="{x}" cy="{y-7}" r="6" fill="none" stroke="{INK}" stroke-width="2"/>'
                  f'<circle cx="{x}" cy="{y-7}" r="6" fill="{INK}"/>'
                  f'<text x="{x+26}" y="{y}" class="b7" font-size="22" fill="{INK}">'
                  + "".join(f'<tspan x="{x+26}" dy="{0 if k == 0 else 30}">{e(l)}</tspan>' for k, l in enumerate(wrap(t)))
                  + "</text>")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Right now: {e('; '.join(lines))}.">
  <defs>
    <style>
      @font-face {{ font-family: "BSD"; src: url(data:font/woff2;base64,{disp}) format("woff2"); font-weight: 900; }}
      @font-face {{ font-family: "AH"; src: url(data:font/woff2;base64,{body}) format("woff2"); font-weight: 700; }}
      .d {{ font-family: "BSD", "Arial Narrow", sans-serif; font-weight: 900; }}
      .b7 {{ font-family: "AH", Verdana, sans-serif; font-weight: 700; }}
      .ring {{ transform-box: fill-box; transform-origin: center; animation: ring 2.4s ease-out infinite; }}
      @keyframes ring {{ from {{ transform: scale(1); opacity: .9; }} to {{ transform: scale(3); opacity: 0; }} }}
      .drift {{ animation: drift 18s ease-in-out infinite alternate; }}
      @keyframes drift {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-120px); }} }}
      @media (prefers-reduced-motion: reduce) {{ .ring, .drift {{ animation: none; }} }}
    </style>
    <clipPath id="c"><rect width="{W}" height="{H}" rx="24"/></clipPath>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="{INK}" fill-opacity="0.12"/></pattern>
    {holo("holo", dur=14, shimmer=12, x2="0.6", y2="0.6")}
  </defs>
  <g clip-path="url(#c)">
    <rect width="{W}" height="{H}" fill="url(#holo)"/>
    <rect class="drift" x="0" y="0" width="{W+240}" height="{H}" fill="url(#dots)"/>
    <text x="56" y="96" class="d" font-size="56" fill="{INK}">Right now</text>
    {items}
    <rect x="0" y="{H-8}" width="{W}" height="8" fill="{INK}"/>
  </g>
</svg>
'''
    open(os.path.join(ROOT, "assets", "now.svg"), "w", encoding="utf-8").write(svg)
    print("assets/now.svg rebuilt with", len(lines), "lines")


if __name__ == "__main__":
    build()
