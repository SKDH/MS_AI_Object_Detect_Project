# 필요한 모듈을 임포트합니다.
import cv2
import numpy as np
import onnxruntime as rt

# ONNX 런타임 세션을 로드합니다.
sess = rt.InferenceSession("./ultralytics-main/runs/detect/train/weights/best.onnx")

# 비디오를 로드합니다.
cap = cv2.VideoCapture('asian_black_bear_clip.mp4')

while(cap.isOpened()):
    # 비디오에서 프레임을 읽습니다.
    ret, frame = cap.read()
    if not ret:
        break

    # 이미지를 전처리합니다.
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 480))
    img = img.astype(np.float32)  # 이미지를 float 유형으로 변환합니다.
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)

    # 객체 감지를 수행합니다.
    boxes = sess.run(None, {"images": img})

    # 감지된 객체를 그립니다.
    for box in boxes[0][0]:
        x1, y1, x2, y2 = map(int, box[:4])  # 좌표를 정수로 변환합니다.
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # 결과를 표시합니다.
    cv2.imshow('frame', frame)

    # 'q' 키를 누르면 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오를 해제하고 창을 닫습니다.
cap.release()
cv2.destroyAllWindows()
