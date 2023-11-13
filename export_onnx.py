from ultralytics import YOLO

model = YOLO("./ultralytics-main/runs/detect/train/weights/best.pt") 
model.export(format="onnx", imgsz=[480,640])