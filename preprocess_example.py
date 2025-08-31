import cv2
import numpy as np
import sys

def rgba_to_rgb_with_bg(input_path, output_path, bg_color=(0, 255, 0)):
    # 讀取 RGBA
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"無法讀取圖片 {input_path}")

    if img.shape[2] != 4:
        raise ValueError("圖片沒有 alpha channel (不是 RGBA)")

    # 分離通道
    b, g, r, a = cv2.split(img)

    # 建立背景 (RGB)
    h, w = img.shape[:2]
    background = np.zeros((h, w, 3), dtype=np.uint8)
    background[:] = bg_color  # 整張圖填充綠色

    # 前景 (去掉 alpha)
    foreground = cv2.merge([b, g, r])

    # 建立 mask
    mask = a > 0  # True=前景, False=透明

    # 合成
    result = background.copy()
    result[mask] = foreground[mask]

    # 儲存
    cv2.imwrite(output_path, result)
    print(f"已輸出 {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python rgba_to_rgb.py input.png output.png")
    else:
        rgba_to_rgb_with_bg(sys.argv[1], sys.argv[2])
