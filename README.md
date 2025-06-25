# Evangelion-Style Condensed Font

This repo demonstrates how to generate a “tall & narrow” variant of the classic **TT-JTCウインM9P** (a.k.a. **NIS-JTC-Win-M9**) font—famously seen in _Neon Genesis Evangelion_ designs—by applying horizontal and vertical scaling to its Latin glyphs.

---

## 1. Download the Original Font

You must have a valid license (e.g. via NIS Ticket) to use or redistribute this font. Fetch it directly from Internet Archive:

[Download **TT-JTCウインM9P** (NIS-JTC-Win-M9)](https://archive.org/compress/NISFonts)

---

## 2. Generate the Condensed Variant

I've provide a simple Python script (`main.py`) based on [fontTools] that:

1. Reads your downloaded `NIS-JTC-Win-M9.ttf`  
2. Scales _only_ the Basic-Latin glyphs by your chosen X/Y factors  
3. Outputs a new TTF ready to install

```
pip install fonttools

#python main.py NIS-JTC-Win-M9.ttf NIS-JTC-Win-M9-shrink.ttf <scale_x> <scale_y>
#<scale_x>  0.78 (78 %)
#<scale_y>  1.15 (115 %)

python main.py NIS-JTC-Win-M9.ttf NIS-JTC-Win-M9-shrink.ttf 0.78 1.15
```

before:  
![Font-original](font-original.png)
   
after:   
![Font](font-new.png)


