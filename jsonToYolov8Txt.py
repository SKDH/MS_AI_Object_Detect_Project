"""
기존 데이터 셋 폴더와 다른 새로운 txt 라벨 폴더 생성 후 txt 라벨 생성

Class
고라니      : 1 -> 0
멧돼지      : 2 -> 1
반달가슴곰  : 6 -> 2
"""
import os
import json
import glob
from tqdm import tqdm

CLASS = {1: 0, 2: 1, 6: 2}  # 넣을 동물에 대해 맞춰야 함

if __name__ == "__main__":
    json_root = "./wildLife_dataset" # 기존 데이터 셋 폴더
    txt_root = "./txt_label" # txt 라벨 데이터 폴더

    # 기존 데이터 셋 폴더에서 라벨 폴더 내 동물 폴더 경로 대로 txt라벨 폴더 생성
    for path in glob.glob(f"{json_root}/*/**/", recursive=True):
        if "labels" in path.split("\\")[2]:
            os.makedirs(
                os.path.join(txt_root, "\\".join(path.split("\\")[1:])), exist_ok=True
            )

    json_files = glob.glob(os.path.join(json_root, "**", "*.json"), recursive=True)
    
    # txt 라벨 데이터 생성
    for json_path in tqdm(json_files):
        txt_file = "\\".join(json_path[:-5].split("\\")[1:]) + ".txt"
        txt_path = os.path.join(txt_root, txt_file)

        with open(json_path, "r", encoding="utf-8") as j:
            json_data = json.load(j)

        width = json_data["images"][0]["width"]
        height = json_data["images"][0]["height"]

        annotations = json_data["annotations"]  # list
        with open(txt_path, "w", encoding="utf-8") as f:
            for annotation in annotations:
                category_id = annotation["category_id"]
                if category_id in [1, 2, 6]:
                    bbox = annotation["bbox"]
                    if bbox == None:
                        continue
                    x1, y1 = bbox[0]
                    x2, y2 = bbox[1]

                    # x, y, w, h
                    x = (x1 + x2) // 2
                    y = (y1 + y2) // 2
                    w = x2 - x1
                    h = y2 - y1

                    x, w = x / width, w / width
                    y, h = y / height, h / height

                    category_id = CLASS[category_id]
                    f.write(f"{category_id} {x} {y} {w} {h}\n")
