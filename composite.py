import cv2
import numpy as np
import sys

def hex_to_rgb(hex_str: str):
    """把 '#RRGGBB' 或 'RRGGBB' 轉換成 (R,G,B)"""
    hex_str = hex_str.lstrip("#")
    if len(hex_str) != 6:
        raise ValueError("Hex color 必須是 6 位，例如 #ff00ff")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    return (r, g, b)

def composite(lineart_path, mask_path, output_path, fill_color=(255,0,255)):
    # 讀取線稿 (RGBA)
    line_img = cv2.imread(lineart_path, cv2.IMREAD_UNCHANGED)
    if line_img is None or line_img.shape[2] != 4:
        raise ValueError("線稿必須是 RGBA 圖片")

    # 讀取 mask (黑白圖)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise ValueError("無法讀取 mask 圖片")

    h, w = mask.shape

    # === 1. 填色層 (RGBA) ===
    fill_layer = np.zeros((h, w, 4), dtype=np.uint8)
    fill_layer[mask > 0] = (*fill_color, 255)

    # === 2. 背景 = 填色層 ===
    result = fill_layer.copy().astype(float)

    # === 3. 疊加線條 (保證在線稿最上層) ===
    line_rgb = line_img[:, :, :3].astype(float)
    line_a = (line_img[:, :, 3].astype(float) / 255.0)[:, :, None]

    bg_rgb = result[:, :, :3]
    bg_a   = (result[:, :, 3:4].astype(float) / 255.0)

    out_rgb = line_a * line_rgb + (1 - line_a) * bg_rgb
    out_a   = np.clip(line_a + bg_a * (1 - line_a), 0, 1)

    result = np.dstack((out_rgb, out_a * 255)).astype(np.uint8)

    cv2.imwrite(output_path, result)
    print(f"合成結果已輸出: {output_path} (填色={fill_color})")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python composite.py lineart.png mask.png output.png [#RRGGBB]")
    else:
        fill_color = (255, 0, 255)  # 預設桃紅
        if len(sys.argv) == 5:
            fill_color = hex_to_rgb(sys.argv[4])
        composite(sys.argv[1], sys.argv[2], sys.argv[3], fill_color=fill_color)
