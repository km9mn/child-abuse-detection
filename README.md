# AI CCTV System Child Abuse Detection

2021 빅데이터 청년인재 고려대과정 10조 - 괴도키즈
---

팀원 : 김규민, 김규원, 김석기, 김호준, 이은서


# Repository


```
└── biconvlstm_model
     └── acc_graph
     └── data
     └── networks
└── data
     └── ipynb
└── deep-learning-server
└── presentation
└── web
     └── static
     └── templates
└── webcam live test
```

# BiConvLSTM Model

## acc_graph

학습 결과를 graph로 저장하는 폴더

## data

### 데이터 가공

- `data_reader` : 데이터를 불러오는 부분
- `data_label_factory` : 데이터 파일명을 통해 데이터 라벨링
- `data_split` : 데이터셋 Split에 이용
- `data_transform_factory` : 데이터 편집 관련 함수
- `data_transformer` : 데이터와 데이터 라벨 관리 
- `transform` : 다양한 변환 클래스

## network

### 사용된 네트워크 관리
- `ConvLSTM` : Conv Layer + LSTM Cell
- `BiConvLSTM` : Conv Layer + BiLSTM Cell
- `resnet_bilstm` : RESNET + BiLSTM 네트워크
- `resnet_lstm` : RESNET + LSTM 네트워크
- `E` : VGG19 + LSTM 네트워크
- `E_bi_max_pool` : VGG19 + BiLSTM 네트워크

# Data

### iypnb



# Presentation

# Web

```
python app.py
```

`Google Colab`에서 구동

# Deep Learning Server

`deep learning server.ipynb`로 `Google Colab`에서 `ngrok`을 이용하여 `colab`의 로컬 네트워크에 터널을 생성하여 외부에서 접근할 수 있도록 구현  

# Webcam Live Test

```
python "NUMBER OF FRAMES" "SERVER PATH" "TEST VIDEO PATH"
```
으로 실행 가능합니다

- NUMBER OF FRAMES - 모델의 입력을 몇초 단위로 넣을지 정해집니다.

- SERVER PATH - 딥러닝 모델의 서버의 주소를 받습니다.

- TEST VIDEO PATH 
     - '0' : webcam을 source로 사용
     - 'path' : 해당된 주소의 영상을 source로 사용  

