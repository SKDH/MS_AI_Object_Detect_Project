"""
class number : 3
    asian_black_bear : 반달가슴곰
    water_dear : 고라니
    wild_boar : 멧돼지
dataset ratio 8:2
dataset
    train
        images
            asian_black_bear
            water_dear
            wild_boar
        labels
            asian_black_bear
            water_dear
            wild_boar
    test
        images
            asian_black_bear
            water_dear
            wild_boar
        labels
            asian_black_bear
            water_dear
            wild_boar
"""
import os
import glob
import shutil
from tqdm import tqdm
from sklearn.model_selection import train_test_split

ANIMALS = ["asian_black_bear", "water_dear", "wild_boar"]  # 동물 목록

if __name__ == "__main__":
    train_data_path = "wildLife_dataset/train"

    for animal in tqdm(ANIMALS):
        img_data_list = glob.glob(
            os.path.join(f"{train_data_path}/images", f"{animal}", "*.jpg")
        )
        label_data_list = glob.glob(
            os.path.join(f"{train_data_path}/labels", f"{animal}", "*.txt")
        )

        # 이미지 데이터와 라벨링 데이터를 zip으로 묶은 후 list로 변환
        data_list = list(zip(img_data_list, label_data_list))

        # 데이터 zip을 훈련 데이터와 테스트 데이터로 분할
        train_list, test_list = train_test_split(
            data_list, test_size=0.2, random_state=777
        )

        # 테스트 데이터를 다시 이미지 데이터와 라벨링 데이터로 분리
        X_test_list, Y_test_list = zip(*test_list)

        for image_lists in X_test_list:
            os.makedirs(f"wildLife_dataset/test/images/{animal}", exist_ok=True)
            # wildLife_dataset/test/image/{animal}/~.jpg
            image_name = os.path.basename(image_lists)
            # shutil.move로 파일 이동(.copy 사용시 파일 복사)
            shutil.move(
                image_lists, f"wildLife_dataset/test/images/{animal}/{image_name}"
            )
        for label_lists in Y_test_list:
            os.makedirs(f"wildLife_dataset/test/labels/{animal}", exist_ok=True)
            # wildLife_dataset/test/label/{animal}/~.txt
            image_name = os.path.basename(label_lists)
            shutil.move(
                label_lists, f"wildLife_dataset/test/labels/{animal}/{image_name}"
            )
