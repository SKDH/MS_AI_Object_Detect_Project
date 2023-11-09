import cv2
import glob
import os
import random
from ultralytics import YOLO

# best.pt 경로
model = YOLO(
    "C:/Users/labadmin/Desktop/MS_AI_Object_Detect_Project/ultralytics-main/runs/detect/train/weights/best.pt"
)

# 특정 폴더 안의 모든 이미지 경로 가져오기
image_paths = glob.glob(
    os.path.join(
        "C:/Users/labadmin/Desktop/MS_AI_Object_Detect_Project/ultralytics-main/ultralytics/cfg/wildLife_dataset/test/images",
        "*",
        "*.jpg",
    ),
    recursive=True,
)

results = []
random_n = 30  # 테스트 할 이미지 개수

# random_n 만큼 이미지를 무작위로 골라 테스트 진행
for i in range(0, random_n):
    results.append(
        model.predict(
            random.choice(image_paths),
            save=False,
            imgsz=640,
            conf=0.5,
            device="cuda",
        )
    )

for result in results:
    for r in result:
        image_path = r.path  # 현재 이미지의 path
        boxes = r.boxes.xyxy  # 현재 이미지의 bbox의 xy좌표값들
        cls = r.boxes.cls  # 현재 이미지의 bbox의 class들
        conf = r.boxes.conf  # 현재 이미지의 bbox의 conf값
        cls_dict = (
            r.names
        )  # 지금 예제는 {0: 'water dear', 1: 'wild boar', 2: 'asian balck bear'}

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, c = image.shape

        image = cv2.resize(image, (640, 640))  # 이미지 사이즈 조정

        print(
            "==================================================================================="
        )
        print(" 정답: " + image_path.split("\\")[-2])

        for box, cls_number, conf in zip(boxes, cls, conf):
            conf_number = float(conf.item())
            cls_number_int = int(cls_number.item())
            cls_name = cls_dict[cls_number_int]
            x1, y1, x2, y2 = box
            x1_int = int(x1.item())
            y1_int = int(y1.item())
            x2_int = int(x2.item())
            y2_int = int(y2.item())

            # 이미지 사이즈를 조정했기 때문에 box 좌표값도 같이 조정 한다
            scale_factor_x = 640 / w
            scale_factor_y = 640 / h
            x1_scale = int(x1_int * scale_factor_x)
            y1_scale = int(y1_int * scale_factor_y)
            x2_scale = int(x2_int * scale_factor_x)
            y2_scale = int(y2_int * scale_factor_y)

            image = cv2.rectangle(
                image, (x1_scale, y1_scale), (x2_scale, y2_scale), (0, 225, 0), 6
            )
            print(f" 추측: {cls_name}")

        cv2.imshow("Test", image)
        key = cv2.waitKey(0) & 0xFF

        # 'd' 키를 누르면 다음 이미지를 표시
        if key == ord("d"):
            break
        # # 'q' 키를 누르면 종료
        # elif key == ord("q"):
        #     break
