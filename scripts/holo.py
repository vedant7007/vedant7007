HOLO = ["#38BDF8", "#7DD3FC", "#A78BFA", "#F472B6", "#FBBF24", "#34D399", "#38BDF8"]
SKY = "#0EA5E9"

def holo(gid, dur=12, shimmer=9, x2="1", y2="0.35"):
    vals = ";".join(HOLO)
    stops = ""
    for k, off in enumerate((0, 0.5, 1)):
        begin = -dur * k / 3
        stops += (f'<stop offset="{off}" stop-color="{HOLO[0]}">'
                  f'<animate attributeName="stop-color" values="{vals}" dur="{dur}s" begin="{begin:.2f}s" repeatCount="indefinite"/></stop>')
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}" spreadMethod="reflect">{stops}'
            f'<animateTransform attributeName="gradientTransform" type="translate" values="0 0;2 0" dur="{shimmer}s" repeatCount="indefinite"/>'
            f'</linearGradient>')
