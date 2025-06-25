#!/usr/bin/env python3
"""
main.py

Usage:
    python main.py input.ttf output.ttf [scale_x] [scale_y]

scale_x: horizontal scale factor (e.g. 0.78 for 78%)
scale_y: vertical   scale factor (e.g. 1.15 for 115%)
"""

import sys
from fontTools.ttLib import TTFont

def squash_latin(in_path, out_path, scale_x=0.78, scale_y=1.15):
    font = TTFont(in_path)
    glyf = font["glyf"]
    hmtx = font["hmtx"].metrics
    vmtx = font.get("vmtx")               # optional vertical metrics
    cmap = font["cmap"].getBestCmap()

    # de-serialize all glyf records so .components or .coordinates exist
    glyf.ensureDecompiled()

    for codepoint, glyphName in cmap.items():
        if 0x0020 <= codepoint <= 0x007E:  # Basic Latin range
            glyph = glyf[glyphName]

            # 1) SCALE THE OUTLINE ----------------------------------------
            if glyph.isComposite():
                # composite: scale each component’s transform
                for comp in glyph.components:
                    comp.xScale  *= scale_x
                    comp.yScale  *= scale_y
                    comp.xOffset *= scale_x
                    comp.yOffset *= scale_y
                glyph.recalcBounds(glyf)

            else:
                # simple: only if there *are* contours to scale
                if getattr(glyph, "numberOfContours", 0) > 0:
                    coords, endPts, flags = glyph.getCoordinates(glyf)
                    for i, (x, y) in enumerate(coords):
                        coords[i] = (
                            int(round(x * scale_x)),
                            int(round(y * scale_y))
                        )
                    glyph.coordinates       = coords
                    glyph.endPtsOfContours  = endPts
                    glyph.flags             = flags
                    glyph.recalcBounds(glyf)
                # else: empty glyphs (e.g. space) → no outlines to touch

            # 2) SCALE HORIZONTAL METRICS ---------------------------------
            aw, lsb             = hmtx[glyphName]
            hmtx[glyphName]     = (
                int(round(aw  * scale_x)),
                int(round(lsb * scale_x))
            )

            # 3) SCALE VERTICAL METRICS (if present) --------------------
            if vmtx:
                advH, tsb         = vmtx.metrics[glyphName]
                vmtx.metrics[glyphName] = (
                    int(round(advH * scale_y)),
                    int(round(tsb  * scale_y))
                )

    font.save(out_path)
    print(f"Wrote squashed font to {out_path!r}")

if __name__ == "__main__":
    if not (3 <= len(sys.argv) <= 5):
        print(__doc__)
        sys.exit(1)
    _, infile, outfile, *factors = sys.argv
    sx = float(factors[0]) if len(factors) >= 1 else 0.78
    sy = float(factors[1]) if len(factors) >= 2 else 1.15
    squash_latin(infile, outfile, sx, sy)
