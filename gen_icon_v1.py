"""主屏幕图标 — 旭日东升：暖橙金径向渐变 + 白色港字数学居中"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = r"F:\财富自由团\hk-pages"
OUT = os.path.join(BASE, "icon-previews")
SIZE = 512
R = 80
FONT_PATH = r"C:\Windows\Fonts\msyhbd.ttc"
CX, CY = SIZE // 2, SIZE // 2

# ===== 1. 暖橙金径向渐变背景 =====
img = Image.new("RGB", (SIZE, SIZE), (255, 130, 20))
draw = ImageDraw.Draw(img)
max_r = int(SIZE * 0.75)
for r in range(max_r, 0, -1):
    ratio = r / max_r
    rr = 255
    gg = int(200 - 50 * (1 - ratio))
    bb = int(100 - 60 * (1 - ratio))
    draw.ellipse([CX - r, CY - r, CX + r, CY + r], fill=(rr, gg, bb))

# ===== 2. 圆角蒙版 =====
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=R, fill=255)
img_rgba = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
img_rgba.paste(img, (0, 0))
img_rgba.putalpha(mask)

# ===== 3. 白色"港"字，textbbox 精确居中 =====
font = ImageFont.truetype(FONT_PATH, 280)
char_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
char_draw = ImageDraw.Draw(char_layer)

bbox = char_draw.textbbox((0, 0), "港", font=font)
tw = bbox[2] - bbox[0]  # 文字实际宽度
th = bbox[3] - bbox[1]  # 文字实际高度
px = (SIZE - tw) // 2 - bbox[0]
py = (SIZE - th) // 2 - bbox[1]

char_draw.text((px, py), "港", font=font, fill=(255, 255, 255, 255))

# ===== 4. 合并输出 =====
final = Image.alpha_composite(img_rgba, char_layer)
os.makedirs(OUT, exist_ok=True)
final.save(os.path.join(OUT, "01-sunrise.png"))
print(f"Done: {OUT}/01-sunrise.png  tw={tw} th={th} pos=({px},{py})")
