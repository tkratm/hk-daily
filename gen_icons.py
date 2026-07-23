"""生成4个方向的APP图标预览 — 不同位置布局"""
from PIL import Image, ImageDraw, ImageFont
import os, math

BASE = r"F:\财富自由团\hk-pages"
OUT = os.path.join(BASE, "icon-previews")
os.makedirs(OUT, exist_ok=True)

SIZE = 512
FONT_PATH = r"C:\Windows\Fonts\msyhbd.ttc"
R = 80  # 圆角半径

def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)

def text_bbox(txt, font):
    b = font.getbbox(txt)
    return b[2] - b[0], b[3] - b[1]

def draw_text_at(draw, x, y, txt, font, color):
    """左上角定位"""
    draw.text((x, y), txt, font=font, fill=color)

def draw_text_center(draw, w, txt, font, color, y_offset=0):
    """水平居中，y_offset 相对于顶部"""
    tw, th = text_bbox(txt, font)
    x = (w - tw) // 2
    y = y_offset
    draw.text((x, y), txt, font=font, fill=color)

def draw_text_vcenter(draw, w, h, txt, font, color, offset_y=0):
    """完全居中 + 偏移"""
    tw, th = text_bbox(txt, font)
    x = (w - tw) // 2
    y = (h - th) // 2 + offset_y
    draw.text((x, y), txt, font=font, fill=color)

def round_mask(img):
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE-1, SIZE-1], radius=R, fill=255)
    rgba = img if img.mode == "RGBA" else img.convert("RGBA")
    rgba.putalpha(mask)
    return rgba

def draw_up_arrow(draw, cx, cy, size, color):
    points = [
        (cx, cy - size),
        (cx + size, cy + int(size * 0.5)),
        (cx + int(size * 0.35), cy + int(size * 0.5)),
        (cx + int(size * 0.35), cy + size),
        (cx - int(size * 0.35), cy + size),
        (cx - int(size * 0.35), cy + int(size * 0.5)),
        (cx - size, cy + int(size * 0.5)),
    ]
    draw.polygon(points, fill=color)

# =====================================================================
# 方案1: 旭日东升 — 港字偏上1/3，底部留白呼吸
# =====================================================================
img1 = Image.new("RGB", (SIZE, SIZE), (255, 130, 20))
draw1 = ImageDraw.Draw(img1)

# 径向渐变：中央亮金 -> 边缘深橙
cx, cy = SIZE // 2, SIZE // 2
for r in range(int(SIZE * 0.8), 0, -1):
    ratio = r / (SIZE * 0.8)
    rr = 255
    gg = int(210 - 60 * (1 - ratio))
    bb = int(110 - 70 * (1 - ratio))
    draw1.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(rr, gg, bb))

# 底部微暗渐变条 — 突出上半部分的朝阳感
for y in range(SIZE // 2, SIZE):
    alpha = (y - SIZE // 2) / (SIZE // 2)
    r_overlay = int(200 * alpha)
    row = [(min(255, rr + r_overlay), max(0, gg - int(40 * alpha)), max(0, bb - int(30 * alpha)))
           for x in range(SIZE)]
    for x in range(SIZE):
        draw1.point((x, y), fill=row[x])

img1 = round_mask(img1)
draw1 = ImageDraw.Draw(img1)

# 港字：偏上1/3处，大字号
font1 = load_font(200)
draw_text_center(draw1, SIZE, "港", font1, (255, 255, 255), y_offset=42)

# 底部留白 — 只在最底部加一个淡淡的光点暗示
draw1.ellipse([cx-30, SIZE-100, cx+30, SIZE-40], fill=(255, 255, 255, 50))

img1.save(os.path.join(OUT, "01-sunrise.png"))

# =====================================================================
# 方案2: 红金涨停 — 放大溢出，港字撑满
# =====================================================================
img2 = Image.new("RGB", (SIZE, SIZE), (185, 22, 32))
draw2 = ImageDraw.Draw(img2)

# 微妙的暗角
for r in range(int(SIZE * 0.85), SIZE // 2, -1):
    ratio = (r - SIZE // 2) / (SIZE * 0.35)
    alpha = int(30 * ratio)
    draw2.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(0, 0, 0), width=1)

# 圆角蒙版
img2 = round_mask(Image.new("RGBA", (SIZE, SIZE)).convert("RGBA"))
# 先画背景到RGBA
bg2 = Image.new("RGBA", (SIZE, SIZE), (185, 22, 32, 255))
draw2 = ImageDraw.Draw(bg2)

# 港字：超大号，无圆角限制感 — 在蒙版里，超出部分自然裁掉即可
# 用260号字体让它尽量撑满可用空间
font2 = load_font(280)
tw2, th2 = text_bbox("港", font2)
x2 = (SIZE - tw2) // 2
y2 = (SIZE - th2) // 2 - 30  # 微调上移
draw2.text((x2, y2), "港", font=font2, fill=(255, 210, 85))

# 上涨箭头在字下方
draw_up_arrow(draw2, SIZE // 2, y2 + th2 + 40, 36, (255, 210, 85))

bg2 = round_mask(bg2)
bg2.save(os.path.join(OUT, "02-red-gold.png"))

# =====================================================================
# 方案3: 青绿向上 — 缩小港字 + 周围光圈
# =====================================================================
img3 = Image.new("RGB", (SIZE, SIZE), (28, 162, 118))
draw3 = ImageDraw.Draw(img3)

# 纵向渐变
for y in range(SIZE):
    ratio = y / SIZE
    r = int(28 - 10 * ratio)
    g = int(162 + 30 * ratio)
    b = int(118 - 25 * ratio)
    draw3.rectangle([0, y, SIZE, y + 1], fill=(r, g, b))

# 外围光圈 — 两层同心圆
for ring_r in [210, 195]:
    draw3.ellipse(
        [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
        outline=(255, 255, 255, 0),
        width=2
    )

img3 = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw3 = ImageDraw.Draw(img3)

# 画背景
for y in range(SIZE):
    ratio = y / SIZE
    r = int(28 - 10 * ratio)
    g = int(162 + 30 * ratio)
    b = int(118 - 25 * ratio)
    draw3.rectangle([0, y, SIZE, y+1], fill=(r, g, b, 255))

# 外围光圈
for ring_r in [215, 198]:
    draw3.ellipse(
        [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
        outline=(255, 255, 255, 60),
        width=3
    )

# 缩小港字
font3 = load_font(140)
draw_text_vcenter(draw3, SIZE, SIZE, "港", font3, (255, 255, 255, 255))

# 缩小箭头
draw_up_arrow(draw3, SIZE // 2, cy + 100, 28, (255, 255, 255))

img3 = round_mask(img3)
img3.save(os.path.join(OUT, "03-teal.png"))

# =====================================================================
# 方案4: 极简白金 — 左偏 + 右下小标
# =====================================================================
img4 = Image.new("RGB", (SIZE, SIZE), (22, 28, 38))
draw4 = ImageDraw.Draw(img4)

# 细金外边框
draw4.rounded_rectangle([20, 20, SIZE-21, SIZE-21], radius=R-10, outline=(200, 170, 100), width=6)

# 港字左偏
font4 = load_font(180)
tw4, th4 = text_bbox("港", font4)
x4 = int(SIZE * 0.12)  # 偏左
y4 = int(SIZE * 0.2)   # 中上偏左
draw4.text((x4, y4), "港", font=font4, fill=(210, 180, 110))

# 文字下方一个精致的小光条
bar_x, bar_y = x4, y4 + th4 + 16
draw4.rounded_rectangle([bar_x, bar_y, bar_x + int(tw4 * 0.7), bar_y + 5], radius=3, fill=(210, 180, 110, 120))

# 右下小标"打卡"
font4b = load_font(48)
tw4b, th4b = text_bbox("打卡", font4b)
x4b = SIZE - tw4b - 50
y4b = SIZE - th4b - 50
draw4.text((x4b, y4b), "打卡", font=font4b, fill=(180, 160, 110))

# 右下角一条细细的下划线
draw4.rounded_rectangle(
    [x4b, y4b + th4b + 8, x4b + tw4b, y4b + th4b + 10],
    radius=2, fill=(180, 160, 110)
)

img4 = round_mask(Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0)))
bg4 = Image.new("RGBA", (SIZE, SIZE), (22, 28, 38, 255))
draw4 = ImageDraw.Draw(bg4)
draw4.rounded_rectangle([20, 20, SIZE-21, SIZE-21], radius=R-10, outline=(200, 170, 100, 255), width=6)
draw4.text((x4, y4), "港", font=font4, fill=(210, 180, 110, 255))
draw4.rounded_rectangle([bar_x, bar_y, bar_x + int(tw4 * 0.7), bar_y + 5], radius=3, fill=(210, 180, 110, 120))
draw4.text((x4b, y4b), "打卡", font=font4b, fill=(180, 160, 110, 255))
draw4.rounded_rectangle([x4b, y4b + th4b + 8, x4b + tw4b, y4b + th4b + 10], radius=2, fill=(180, 160, 110, 255))
bg4 = round_mask(bg4)
bg4.save(os.path.join(OUT, "04-platinum.png"))

print("4 icons regenerated in", OUT)

# =====================================================================
# 对比HTML
# =====================================================================
html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>图标方案对比</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'Microsoft YaHei',sans-serif;background:#F2F2F7;padding:20px;min-height:100vh}
h1{text-align:center;font-size:20px;margin:10px 0 6px;color:#1C1C1E}
.sub{text-align:center;font-size:12px;color:#8E8E93;margin-bottom:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;max-width:620px;margin:0 auto}
.card{background:#FFF;border-radius:16px;padding:18px 14px 14px;box-shadow:0 2px 8px rgba(0,0,0,.06);text-align:center}
.card img{width:110px;height:110px;border-radius:24px;margin-bottom:12px}
.card .name{font-size:15px;font-weight:700;color:#1C1C1E;margin-bottom:3px}
.card .pos{font-size:11px;color:#007AFF;margin-bottom:3px}
.card .desc{font-size:11px;color:#8E8E93;line-height:1.4}
</style>
</head>
<body>
<h1>主屏幕图标 — 4种配色 × 4种布局</h1>
<p class="sub">左滑查看全部 · 点击编号即定稿</p>
<div class="grid">
<div class="card">
  <img src="01-sunrise.png">
  <div class="name">01 旭日东升</div>
  <div class="pos">港字偏上 · 底部流白</div>
  <div class="desc">暖橙金渐变<br>呼吸感，不拥挤</div>
</div>
<div class="card">
  <img src="02-red-gold.png">
  <div class="name">02 红金涨停</div>
  <div class="pos">超大港字 · 撑满溢出</div>
  <div class="desc">深红底+金字+↑<br>霸气，一眼"涨"</div>
</div>
<div class="card">
  <img src="03-teal.png">
  <div class="name">03 青绿向上</div>
  <div class="pos">缩小聚焦 · 外围光圈</div>
  <div class="desc">青绿渐变+光晕<br>精致、现代、耐看</div>
</div>
<div class="card">
  <img src="04-platinum.png">
  <div class="name">04 极简白金</div>
  <div class="pos">左偏构图 · 右下「打卡」</div>
  <div class="desc">深色+烫金+小标<br>高级感，有叙事</div>
</div>
</div>
</body>
</html>"""
with open(os.path.join(OUT, "compare.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("compare.html updated")
