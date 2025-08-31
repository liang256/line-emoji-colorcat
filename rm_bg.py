import cv2
import numpy as np
import sys

def remove_bg(input_path, output_path):
    # 讀取 RGB
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"無法讀取圖片 {input_path}")

    # 轉 HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 綠色範圍 (可調整)
    lower_green = np.array([50, 50, 50])
    upper_green = np.array([80, 255, 255])

    # 找背景
    bg_mask = cv2.inRange(hsv, lower_green, upper_green)

    # alpha: 非綠色=255, 綠色=0
    alpha = cv2.bitwise_not(bg_mask)

    # 合成 RGBA
    b, g, r = cv2.split(img)
    rgba = cv2.merge([b, g, r, alpha])

    cv2.imwrite(output_path, rgba)
    print(f"已輸出 {output_path} (背景轉透明)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python remove_bg.py input.png output.png")
    else:
        remove_bg(sys.argv[1], sys.argv[2])
