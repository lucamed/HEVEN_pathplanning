
# SKKU - HEVEN at PAMS
2019 제 3회 판교 자율주행 모터쇼(PAMS 2019, Pangyo Autonomous Motor Show 2019)의<br /> 대학생 자동차 융합기술 경진대회 자율주행 부문에 출전한 성균관대학교 HEVEN 입니다.

<hr/>

### 대회 개요
* 대회명: PAMS 2019 대학생 자동차 융합기술 경진대회 / 자율주행 부문
* 일시: 2019년 11월 1일 (금) ~ 3일 (일)
* 장소: 판교 제2테크노밸리
* 주최: 경기도
* 주관: 차세대융합기술연구원, KINTEX

### 팀원 (15)
유정현 김유빈 김지훈 Luca 박선우 김경수 차민지 한일석<br />
신동한 오혜준 장윤진 홍주용 김민제 서채연 차동훈

### 대회 결과
성균관대학교 HEVEN 팀 2위 (총 7개 팀 중)

### 후기
* [HEVEN 자율차팀의 PAMS 진행 로그 및 리뷰](https://github.com/x2ever/skku-pams-2019/wiki/HEVEN-%EC%9E%90%EC%9C%A8%EC%B0%A8%ED%8C%80%EC%9D%98-PAMS-%EC%A7%84%ED%96%89-%EB%A1%9C%EA%B7%B8-%EB%B0%8F-%EB%A6%AC%EB%B7%B0)

<hr/>

# Project Directory
* [src]()
  * [AAA]()
    * [aaa]()
* [Path](https://github.com/x2ever/skku-pams-2019#2-path)
  * [BBB]()
    * [bbb]()
* [YOLO](https://github.com/x2ever/skku-pams-2019#3-yolo)
  * [CCC]()
    * [ccc]()
* [Parking]()
  * [DDD]()
    * [ddd]()
* [Control](https://github.com/x2ever/skku-pams-2019#5-control)
  * [Control.py](https://github.com/x2ever/skku-pams-2019#51-controlpy)
    * [미션별 제어 함수 호출](https://github.com/x2ever/skku-pams-2019#511-미션별-제어-함수-호출)
    * [차량 주행 제어 함수 호출](https://github.com/x2ever/skku-pams-2019#512-차량-주행-제어-함수-호출)
* [Record](https://github.com/x2ever/skku-pams-2019#6-record)

<hr/>

## 1. src

`src` 디렉터리에는<br />
각 센서에서 받아온 데이터를 저장하는 `Database` 디렉터리와<br />
미션 별 Mission class가 있는 `Mission.py`<br />
그리고 각 디렉터리에 있는 모듈을 이용하여 시스템을 작동시키는 `main.py`가 있습니다.
```python
[src]
│  main.py
│  Mission.py
│  test.py  # 매크로 테스트를 위해 만들어 놓은 임시 파일
│
├─Database
│  │  Authority.py
│  │  CAM.py
│  │  ControlData.py
│  │  Database.py
│  │  Flag.py
│  │  GPS.py
│  │  imu.py
│  │  LiDAR.py
│  │  Platform.py
│  │  Screens.py
│  │  __init__.py
```

### &nbsp;&nbsp;1.1 Database

&nbsp;&nbsp;&nbsp;&nbsp; comments

#### &nbsp;&nbsp;&nbsp;&nbsp;1.1.1 aaa1

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; comments

#### &nbsp;&nbsp;&nbsp;&nbsp;1.1.2 aaa2

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; comments

<hr/>

## 2. Path

Path 디렉토리에는 image_function, Line, Obstacle, Parking, Path 파일이 들어 있습니다.
이 파일들은 장애물(Line, Obstacle)과 주행에 필요한 정보(position, degree)를 추출하기 위해 사용됩니다.

```python
[Path]
│  image_function.py
│  Line.py
│  Obstacle.py
│  Parking.py
│  Path.py
│  __init__.py
```

### &nbsp;&nbsp;2.1 image_function

&nbsp;&nbsp;&nbsp;&nbsp; Path의 핵심기능인 라인검출에 필요한 모든 유틸함수들이 들어 있는 파일입니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.1.1 transform

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 원근변환을 수행합니다. 이때, 각 transform 함수별로 원근변환의 목적이 다름을 인지해야 합니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.1.2 get_stop_line, get_parking_line

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 정지선과 주차선을 검출하는 함수입니다. 둘 모두 리턴은 불리안 값 입니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.1.3 combine

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 좌우 레인의 카메라 law값을 합치는 함수입니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.1.4 detect

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 영상을 이진화 하는 함수입니다. 편의를 위해 HSV채널을 사용합니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.1.5 detectcolor

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 원하는 색상만을 추출하는 함수입니다. 대회에서는 노란색과 흰색만을 추출하였습니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.1.6 lane_detect

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 라인을 검출하는 함수입니다. 이진화된 좌우 레인이 합쳐진 이미지를 넣으면, position, degree, ret_img(모니터링 이미지)가 리턴됩니다.

### &nbsp;&nbsp;2.2 Line

&nbsp;&nbsp;&nbsp;&nbsp; image_function을 이용하여 라인을 추출하고, 얻어낸 position과 degree를 db에 넣습니다. 또, 정지선을 검출하여 리턴합니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.2.1 set_info

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; image_function 함수들을 이용하여 position과 degree 값을 얻고, 이를 db에 삽입합니다. 따라서 position과 degree 값을 얻으려면 Line의 set_info 함수를 호출하고, db에서 꺼내 사용합니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.2.2 check_stop_line

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 정지선을 검출하여 불리안 값을 리턴합니다.

### &nbsp;&nbsp;2.4 Parking

&nbsp;&nbsp;&nbsp;&nbsp; 주차선을 검출하여 불리안 값을 리턴합니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;2.4.1 check_park_line

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; image_function의 get_parking_line 함수를 이용하여 주차선을 검출하여 불리안 값을 리턴합니다. 이 함수 내부에는 주차캠 원근변환, 밝기보정이 들어 있습니다.

<hr/>

## 3. YOLO

YOLO (You Only Look Once), is a network for object detection. The object detection task consists in determining the location on the image where certain objects are present, as well as classifying those objects. In this project YOLO is used to classify and track traffic signs and traffic lights.
<br />
<br />
`YOLO` directory contains: <br />
&nbsp;&nbsp;&nbsp;&nbsp; Implementation of the model for python `thread_yolo.py` -> a buffer to increase the trustworthiness of the model. <br />
&nbsp;&nbsp;&nbsp;&nbsp; In the folder `Data-Augmentation_for_Yolo` has all the needed programs to perform data augmentation on a target-background setting.<br />
&nbsp;&nbsp;&nbsp;&nbsp; `needed_files` contains an example of yolo configuration files.<br />
<br />
```python
[YOLO]
│  buffer_yolo(CAR).py
│  buffer_yolo.py
│  README.md
│  Split_Train_Test.py
│  thread_yolo.py
│  traffic_hsv.py
│
├─Data-Augmentation_for_Yolo
│      BackgroundFileInterface.py
│      brt_augmentation.py
│      CreateSamples.py
│      CreateSamples_blackBG.py
│      image_transformer.py
│      negativeSample_txt.py
│      Parameters.config
│      Parameters_blackBG.config
│      README.md
│      SampleImgInterface.py
│      util.py
│      utility.py
│
├─needed_files
│      obj.data
│      obj.names
│      yolov3.cfg
```

### &nbsp;&nbsp;3.1 Training YOLO from custom dataset

&nbsp;&nbsp;&nbsp;&nbsp; In order to train a successful model, a good non-skewed distribution of images.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1. First step is to find all the target traffic signs and a few background images<br />

#### &nbsp;&nbsp;&nbsp;&nbsp;3.1.1 Data Augmentation

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; comments

#### &nbsp;&nbsp;&nbsp;&nbsp;3.1.2 Parameters Configuration

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; comments

#### &nbsp;&nbsp;&nbsp;&nbsp;3.1.3 Training/Buffer

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; comments
<hr/>

## 4. Parking

comments
```python
[Parking]
    new_parking.py
    parking.py
```

### &nbsp;&nbsp;4.1 DDD

&nbsp;&nbsp;&nbsp;&nbsp; comments

#### &nbsp;&nbsp;&nbsp;&nbsp;4.1.1 ddd1

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; comments

#### &nbsp;&nbsp;&nbsp;&nbsp;4.1.2 ddd2

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; comments

<hr/>

## 5. Control

`Control` 디렉터리 내에는 위의 `Path`, `YOLO` 등에서 생성된 결과값을 이용하여<br>
차량을 제어하는 함수들이 들어 있습니다.
```python
[Control]
│  Control.py
│  Lane_tracking.py
│  __init__.py
```

### &nbsp;&nbsp;5.1 Control.py

&nbsp;&nbsp;&nbsp;&nbsp; Control.py 내에는 차량 제어에 사용되는 `Control` 클래스가 정의되어 있습니다.<br>
&nbsp;&nbsp;&nbsp;&nbsp; 기본 주행을 위한 `main` 함수와 미션 별 행동 제어를 위한 함수들이 있습니다.<br>
&nbsp;&nbsp;&nbsp;&nbsp; 한번 사용한 매크로 값들을 초기화하지 않게 하기 위해, 매크로 변수들을 하나의 클래스 내에 정의해 놓았습니다.<br>


#### &nbsp;&nbsp;&nbsp;&nbsp;5.1.1 미션별 제어 함수 호출

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `Mission.py`에서 각 미션별로 함수를 호출할 때는<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `self.control.미션이름()`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 와 같은 형태로 호출하여 사용했습니다.

#### &nbsp;&nbsp;&nbsp;&nbsp;5.1.2 차량 주행 제어 함수 호출

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 차량을 차선에 맞게 정렬할 때는<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `self.control.main(speed=A, brake=B, portion_offset=C)`<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 와 같은 형태로 호출하면 됩니다.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (이때 각각의 input들은 목표 제어값)<br>

### &nbsp;&nbsp;5.2 Lane_tracking.py

&nbsp;&nbsp;&nbsp;&nbsp; 차량 제어에 관한 조향각 결정 model이 들어있습니다.<br>
&nbsp;&nbsp;&nbsp;&nbsp; [주행 알고리즘 설계 : 자세한 내용](https://www.slideshare.net/JeonghyunRyu2/control-team-study)<br>
<hr/>

## 6. Record

주차 미션과 표지판 미션을 위해 필요한 영상들을 녹화하는 데에 사용했습니다.<br />
Database와 병합되어 있지 않고, 카메라를 직접 `cv2` 모듈로 호출하여 사용했습니다.<br />
대회 당일날 `main.py`를 실행하면 자동으로 녹화를 시작하도록 변경하였습니다.
```python
[Record]
    record_video.py
```

### &nbsp;&nbsp;6.1 record_video.py

&nbsp;&nbsp;&nbsp;&nbsp; 실행하면 카메라에 촬영된 영상이 녹화됩니다.


<hr/>
