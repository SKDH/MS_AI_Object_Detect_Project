from ultralytics import YOLO

if __name__ == "__main__":
    # model = YOLO("yolov8s.pt") # YOLO 모델 설정
    # model.train(data="./wildLife.yaml", epochs=100, batch=16)

    # resume
    model = YOLO("./runs/detect/train/weights/last.pt")  # .pt 파일 확인 요망
    model.train(resume=True)
