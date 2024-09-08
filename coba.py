import base64
import json
import os
import os.path as osp

import PIL.Image

from labelme import utils
from labelme.logger import logger


def process_json_file(json_file, img_output_dir, img_index):
    data = json.load(open(json_file))
    imageData = data.get("imageData")

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
        with open(imagePath, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
    img = utils.img_b64_to_arr(imageData)

    # Simpan gambar dengan nama imgX.png, di mana X adalah img_index
    img_output_path = osp.join(img_output_dir, f"img{img_index}.png")
    PIL.Image.fromarray(img).save(img_output_path)

    logger.info(f"Saved image: {img_output_path}")


def main():
    logger.warning(
        "DEPRECATED: This script will be removed in the near future. "
        "Please use `labelme_export_json` instead."
    )

    # Tentukan direktori tempat JSON files berada
    json_dir = r"C:\\Users\\ACER\\Downloads\\Compressed\\json-20240814T102919Z-001\\json"

    # Tentukan direktori output untuk semua gambar
    img_output_dir = r"C:\\Users\\ACER\\Downloads\\Compressed\\json-20240814T102919Z-001\\json"

    if not osp.exists(img_output_dir):
        os.makedirs(img_output_dir)  # Membuat direktori jika belum ada

    # Loop untuk memproses file dari frame_1.json hingga frame_100.json
    for i in range(1, 101):
        json_file = osp.join(json_dir, f"frame_{i}.json")
        process_json_file(json_file, img_output_dir, i)

if __name__ == "__main__":
    main()