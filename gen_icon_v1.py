"""方案1 旭日东升 — 港字居中放大，无圆点"""
from PIL import Image, ImageDraw, ImageFont
import os, math

BASE = r"F:\财富自由团\hk-pages"
OUT = os.path.join(BASE, "icon-previews")
os.makedirs(OUT, exist_ok=True)

SIZE = 512
FONT_PATH = r"C:\Windows\Fonts\msyhbd.ttc"
R = 80
cx, cy = SIZE // 2, SIZE // 2

def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)

# 暖橙金径向渐变
img = Image.new("RGB", (SIZE, SIZE), (255, 130, 20))
draw = ImageDraw.Draw(img)

for r in range(int(SIZE * 0.8), 0, -1):
    ratio = r / (SIZE * 0.8)
    rr = 255
    gg = int(210 - 60 * (1 - ratio))
    bb = int(110 - 70 * (1 - ratio))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(rr, gg, bb))

# 底部微暗
for y in range(SIZE // 2, SIZE):
    alpha = (y - SIZE // 2) / (SIZE // 2)
    r_overlay = int(200 * alpha)
    for x in range(SIZE):
        px = img.getpixel((x, y))
        r2 = min(255, px[0] + r_overlay)
        g2 = max(0, px[1] - int(40 * alpha))
        b2 = max(0, px[2] - int(30 * alpha))
        draw.point((x, y), fill=(r2, g2, b2))

# 圆角蒙版
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE-1, SIZE-1], radius=R, fill=255)
img_rgba = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
img_rgba.paste(img, (0, 0))
img_rgba.putalpha(mask)

# 港字居中放大
draw = ImageDraw.Draw(img_rgba)
font = load_font(280)
bbox = font.getbbox("港")
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = (SIZE - tw) // 2
y = (SIZE - th) // 2
draw.text((x, y), "港", font=font, fill=(255, 255, 255))

path = os.path.join(OUT, "01-sunrise.png")
img_rgba.save(path)
print("Done:", path)
