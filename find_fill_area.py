import cv2
import numpy as np
import sys

def find_fill_area(input_path, output_path, fill_color=(255, 0, 255)):
    # 讀取 RGBA
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"無法讀取圖片 {input_path}")

    if img.shape[2] != 4:
        raise ValueError("圖片沒有 alpha channel (不是 RGBA)")

    # 取 alpha channel
    alpha = img[:, :, 3]

    # 二值化 (把 alpha > 0 當成線條)
    _, thresh = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)

    # 找輪廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("沒有找到任何封閉輪廓")

    # 選擇最大輪廓 (最外圍造型)
    max_contour = max(contours, key=cv2.contourArea)

    # 建立空白 RGB 圖
    h, w = alpha.shape
    result = np.zeros((h, w, 3), dtype=np.uint8)

    # 填色 (桃紅色)
    cv2.drawContours(result, [max_contour], -1, fill_color, thickness=cv2.FILLED)

    # 儲存
    cv2.imwrite(output_path, result)
    print(f"填色區域已輸出: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python find_fill_area.py input.png output.png")
    else:
        find_fill_area(sys.argv[1], sys.argv[2])
