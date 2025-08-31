import cv2
import numpy as np
from collections import Counter
import sys


def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[2]), int(color[1]), int(color[0]))


def parse_three_colors(input_path, bg_color=(0, 255, 0), out_file="colors.txt"):
    # 讀圖 (BGR)
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"無法讀取圖片 {input_path}")

    h, w, _ = img.shape
    pixels = img.reshape((-1, 3))

    # 轉成 tuple，方便 Counter
    pixels_list = [tuple(p) for p in pixels]

    # 計算顏色出現頻率
    counts = Counter(pixels_list)

    # 移除背景色
    if bg_color in counts:
        del counts[bg_color]

    # 剩下的顏色群
    unique_colors = list(counts.keys())

    if not unique_colors:
        raise ValueError("找不到非背景顏色")

    # 計算亮度 (line color = 最暗)
    def brightness(c):  # BGR
        return 0.299 * c[2] + 0.587 * c[1] + 0.114 * c[0]

    # 找線條色 (最暗)
    line_color = min(unique_colors, key=brightness)

    # 剩下的顏色當作填色
    fill_candidates = [c for c in unique_colors if c != line_color]
    if not fill_candidates:
        raise ValueError("找不到填色候選")

    # 選最多像素的填色
    fill_color = max(fill_candidates, key=lambda c: counts[c])

    # 輸出
    result = {
        "background": rgb_to_hex((bg_color[2], bg_color[1], bg_color[0])),  # BGR → Hex
        "line": rgb_to_hex(line_color),
        "fill": rgb_to_hex(fill_color),
    }

    # 寫檔
    with open(out_file, "w") as f:
        for k, v in result.items():
            f.write(f"{k}: {v}\n")

    print("檢測結果：")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python parse_colors.py example_rgb.png")
    else:
        parse_three_colors(sys.argv[1])
