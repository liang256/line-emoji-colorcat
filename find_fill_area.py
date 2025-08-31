import cv2
import numpy as np
import sys

def find_fill_area(input_path, output_path,
                   fill_color=(255, 0, 255),
                   bg_color=(0, 255, 0),
                   preview=False,
                   shrink=0):
    # 讀取 RGBA
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"無法讀取圖片 {input_path}")

    if img.shape[2] != 4:
        raise ValueError("圖片沒有 alpha channel (不是 RGBA)")

    # 分離 RGBA
    b, g, r, a = cv2.split(img)
    line_rgb = cv2.merge([b, g, r]).astype(float)
    alpha = a.astype(float) / 255.0  # 正規化 alpha

    h, w = alpha.shape

    # 找最大輪廓 (填色區域)
    _, thresh = cv2.threshold(a, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise ValueError("沒有找到任何封閉輪廓")

    max_contour = max(contours, key=cv2.contourArea)

    # 建立 mask
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(mask, [max_contour], -1, 255, thickness=cv2.FILLED)

    # 縮小 mask
    if shrink > 0:
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=shrink)

    if not preview:
        # === 正常模式：輸出黑白 mask ===
        cv2.imwrite(output_path, mask)
        print(f"黑白 mask 已輸出: {output_path} (shrink={shrink})")
        return

    # === 預覽模式：輸出彩色合成 ===
    result = np.zeros((h, w, 3), dtype=float)
    result[:] = bg_color

    # 用縮小後的 mask 填色
    colored = result.copy()
    colored[mask > 0] = fill_color

    # 疊加線條 (alpha blending)
    alpha = alpha[:, :, None]
    result = alpha * line_rgb + (1 - alpha) * colored

    result = result.astype(np.uint8)
    cv2.imwrite(output_path, result)
    print(f"預覽合成結果已輸出: {output_path} (shrink={shrink})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python find_fill_area.py input.png output.png [--preview] [--shrink N]")
    else:
        preview = ("--preview" in sys.argv)
        shrink = 0
        for arg in sys.argv:
            if arg.startswith("--shrink"):
                parts = arg.split("=")
                if len(parts) == 2:
                    shrink = int(parts[1])

        find_fill_area(sys.argv[1], sys.argv[2], preview=preview, shrink=shrink)
