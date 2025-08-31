import cv2
import numpy as np
import os
import glob
import subprocess
import tempfile
import sys


# === Step 1. 從 example 取顏色 ===
def get_fill_color(example_path):
    return (255, 255, 255)


def run_pipeline(color_config, lineart_dir, output_dir):
    # 取顏色
    fill_color = get_fill_color(color_config)
    print(f"使用填色顏色: {fill_color}")

    os.makedirs(output_dir, exist_ok=True)

    # 處理每張線稿
    for path in glob.glob(os.path.join(lineart_dir, "*.png")):
        fname = os.path.splitext(os.path.basename(path))[0]
        tmp_mask = os.path.join(tempfile.gettempdir(), f"{fname}_mask.png")
        out_path = os.path.join(output_dir, f"{fname}_out.png")

        print(f"處理 {path} ...")

        # Step 2. 產生 mask
        subprocess.run(
            [sys.executable, "find_fill_area.py", path, tmp_mask, "--shrink=1"],
            check=True,
        )

        # Step 3. 合成
        hex_color = "#{:02x}{:02x}{:02x}".format(*fill_color)
        subprocess.run(
            [sys.executable, "composite.py", path, tmp_mask, out_path, hex_color],
            check=True,
        )

        # Step 4. 移除暫存 mask
        os.remove(tmp_mask)
        print(f"完成 {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python run_pipeline.py color.txt linearts_dir output_dir")
    else:
        run_pipeline(sys.argv[1], sys.argv[2], sys.argv[3])
