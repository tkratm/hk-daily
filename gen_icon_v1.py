"""方案1 — 用像素真实范围居中"""
from PIL import Image, ImageDraw, ImageFont
import os

BASE = r"F:\财富自由团\hk-pages"
OUT = os.path.join(BASE, "icon-previews")
SIZE = 512
R = 80
FONT_PATH = r"C:\Windows\Fonts\msyhbd.ttc"
cx, cy = SIZE // 2, SIZE // 2

def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)

# 1) 暖橙金径向渐变
img = Image.new("RGB", (SIZE, SIZE), (255, 130, 20))
draw = ImageDraw.Draw(img)
for r in range(int(SIZE * 0.8), 0, -1):
    ratio = r / (SIZE * 0.8)
    rr = 255
    gg = int(210 - 60 * (1 - ratio))
    bb = int(110 - 70 * (1 - ratio))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(rr, gg, bb))
for y in range(SIZE // 2, SIZE):
    alpha = (y - SIZE // 2) / (SIZE // 2)
    r_overlay = int(200 * alpha)
    for x in range(SIZE):
        px = img.getpixel((x, y))
        r2 = min(255, px[0] + r_overlay)
        g2 = max(0, px[1] - int(40 * alpha))
        b2 = max(0, px[2] - int(30 * alpha))
        draw.point((x, y), fill=(r2, g2, b2))

# 2) 圆角蒙版
mask = Image.new("L", (SIZE, SIZE), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE-1, SIZE-1], radius=R, fill=255)
img_rgba = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
img_rgba.paste(img, (0, 0))
img_rgba.putalpha(mask)

# 3) 渲染港字到独立图层，测真实像素范围
char_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
char_draw = ImageDraw.Draw(char_layer)

# 用一个偏大的字号测试，但用 measure 像素范围定位
font = load_font(280)
char_draw.text((0, 0), "港", font=font, fill=(0, 0, 0, 255))  # 在临时位置画
# 测像素 bbox
char_bbox = char_layer.getbbox()  # 实际像素覆盖的 bbox
print("测得字符像素 bbox:", char_bbox)

# 字符的视觉 bounding box
if char_bbox:
    cb_x0, cb_y0, cb_x1, cb_y1 = char_bbox
    cb_w = cb_x1 - cb_x0
    cb_h = cb_y1 - cb_y0
    # 居中
    px = (SIZE - cb_w) // 2 - cb_x0
    py = (SIZE - cb_h) // 2 - cb_y0 - 10  # 略上移
    print(f"字符宽高: {cb_w}x{cb_h}, 居中到 ({px}, {py})")

# 清空重新画
char_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
char_draw = ImageDraw.Draw(char_layer)
char_draw.text((px, py), "港", font=font, fill=(255, 255, 255, 255))

# 合并
final = Image.alpha_composite(img_rgba, char_layer)
final.save(os.path.join(OUT, "01-sunrise.png"))
print("Done:", OUT + "/01-sunrise.png")
