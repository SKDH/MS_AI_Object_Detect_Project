# MS_AI_Object_Detect_Project

Object detection team project at MS AI School

## 사용한 데이터 셋

[AI Hub 야생동물 활동 영상 데이터](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=645)
이 중 **고라니, 멧돼지, 반달가슴곰**의 원천데이터(이미지), 라벨 데이터 사용

## 사용한 학습 모델

YOLO V8
[Git](https://github.com/ultralytics/ultralytics)
[Document](https://docs.ultralytics.com/)

## 데이터 셋 전처리 과정

1.  다운받은 데이터를 다음과 같은 구조로 압축해제 함

    - wildLife_dataset
      - train
        - images (원천데이터)
          - water_dear (고라니)
          - wild_boar (멧돼지)
          - asian_black_bear (반달가슴곰)
        - labels (라벨데이터)
          - water_dear
          - wild_boar
          - asian_black_bear
      - valid
        - images
          - water_dear
          - wild_boar
          - asian_black_bear
        - labels
          - water_dear
          - wild_boar
          - asian_black_bear

2.  일부 json 라벨 데이터의 annotaion이 동일 이미지 데이터 속 동물과 맞지 않음을 확인
3.  annoation 을 이미지 속 동물로 수정하는 `animals_list.py` 실행
4.  `data_split.py` 을 실행하여 train 데이터 중 일부를 test 데이터로 분리
5.  `jsonToYOlov8Txt.py` 을 실행하여 기존 json 라벨 데이터를 기반으로 Yolo v8 용 txt 라벨 데이터 생성
6.  생성된 txt 라벨 데이터를 기존 json 라벨 데이터와 교체
7.  고라니 데이터 중 A01_G22_C024_D_211118_2033_59S_000049.254라는 이름을 가진 이미지와 라벨에 문제가 있어 삭제
8.  train, valid, test 모두 images와 labels에 동물별로 나눠져 있는 데이터를 모두 하나도 합침, **images와 labels 폴더내 동물 폴더 없음**
