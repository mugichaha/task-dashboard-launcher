#!/usr/bin/env python3
"""タスクダッシュボード アイコン生成（ターゲット×チェック）。
4倍解像度で描画→縮小でアンチエイリアス。リング3本・間隔広め・輪郭ぼかし。"""
from PIL import Image, ImageDraw, ImageFilter

S = 4               # スーパーサンプリング倍率
BASE = 192
N = BASE * S        # 描画キャンバス 768

BG    = (30, 58, 95)      # #1e3a5f ネイビー
RING  = (120, 175, 235)   # 明るいブルー（ぼかしても残るよう明度高め）
CHECK = (255, 255, 255)   # 白

cx = cy = N // 2

# --- 背景（角まで塗る。iOS が自動で角丸マスクするため自前で丸めない） ---
img = Image.new("RGB", (N, N), BG)

# --- リング層（別レイヤに描いてぼかす） ---
rings = Image.new("RGBA", (N, N), (0, 0, 0, 0))
rd = ImageDraw.Draw(rings)
ring_w = 9 * S
# 外側にもう1本追加して計3本・間隔広め（半径 38/56/74 を ×S）
for r in (38, 56, 74):
    R = r * S
    rd.ellipse([cx - R, cy - R, cx + R, cy + R], outline=RING, width=ring_w)
# 輪郭をぼやかす（弱め＝消えない程度のソフトさ）
rings = rings.filter(ImageFilter.GaussianBlur(radius=1.6 * S))
img.paste(rings, (0, 0), rings)

# --- チェックマーク（白・くっきり寄り。中央に収める） ---
chk = Image.new("RGBA", (N, N), (0, 0, 0, 0))
cd = ImageDraw.Draw(chk)
pts = [(62, 100), (86, 126), (134, 66)]   # 192基準。中心(96,96)付近・外周内に収まる
pts = [(x * S, y * S) for x, y in pts]
cw = 12 * S
cd.line(pts, fill=CHECK, width=cw, joint="curve")
# 端を丸く
for (x, y) in (pts[0], pts[2]):
    cd.ellipse([x - cw // 2, y - cw // 2, x + cw // 2, y + cw // 2], fill=CHECK)
chk = chk.filter(ImageFilter.GaussianBlur(radius=0.6 * S))  # ごく軽くだけ
img.paste(chk, (0, 0), chk)

# --- 書き出し（192 と apple-touch 用 180） ---
for size, name in ((192, "icon-192.png"), (180, "icon-180.png")):
    out = img.resize((size, size), Image.LANCZOS)
    out.save(name, "PNG")
    print("wrote", name, out.size)
