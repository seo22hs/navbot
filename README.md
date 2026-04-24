# ROS 기반 실내 자율 주행 및 전시 부스 위치 안내 시스템

## 1. 프로젝트 개요

- 목표: Gazebo 시뮬레이션 환경에서 전시장 안내 로봇을 구현한다.
- 시나리오: 사용자가 부스를 선택하면 로봇이 해당 위치까지 자율 주행하고, 안내 종료 후 출입구로 복귀한다.
- 개발 환경: `ROS Noetic`, `Ubuntu 20.04`, `Gazebo`, `RViz`, `Python`
- 로봇 플랫폼: `TurtleBot3` 기반 활용 예정

## 2. 최종 목표

최종 시연에서는 아래 흐름이 동작하는 것을 목표로 한다.

1. Gazebo 전시장 월드 실행
2. 로봇 스폰 및 센서 데이터 확인
3. 저장된 지도 기반 Navigation 실행
4. 사용자가 `A/B/C/.. 부스` 중 하나를 선택
5. 로봇이 해당 부스로 이동
6. 도착 메시지 출력
7. 출입구로 복귀

## 3. 현재 워크스페이스 구조

패키지 이름은 `exhibition_guide`

### 폴더 역할

- `config/`: 목적지 좌표, costmap, navigation 관련 설정 파일 저장
- `launch/`: Gazebo, RViz, Navigation, 안내 노드 실행용 launch 파일 저장
- `maps/`: SLAM으로 생성 후 저장한 지도 파일(`.pgm`, `.yaml`) 저장
- `rviz/`: RViz 시각화 설정 파일 저장
- `scripts/`: Python 기반 ROS 노드 저장
- `src/`: 필요 시 C++ 소스 또는 패키지 내부 모듈 저장
- `worlds/`: Gazebo 전시장 월드 파일 저장

## 4. 현재 진행 상황

### 완료된 항목

- `navbot` 워크스페이스 생성
- `exhibition_guide` ROS 패키지 생성
- 기본 디렉터리 구조 생성
- `worlds/exhibition_hall.world` 기본 전시장 월드 파일 작성
- `launch/exhibition_world.launch` Gazebo 월드 실행용 launch 파일 작성
- `launch/spawn_turtlebot3.launch` TurtleBot3 스폰용 launch 파일 작성
- `launch/exhibition_world_with_robot.launch` 월드 + 로봇 통합 실행 launch 파일 작성
- `launch/exhibition_slam.launch` SLAM 실행용 launch 파일 작성
- `package.xml`에 일부 Python/Navigation 관련 의존성 선언
  <!-- - `rospy`
  - `actionlib`
  - `gazebo_ros`
  - `gmapping`
  - `geometry_msgs`
  - `joint_state_publisher`
  - `map_server`
  - `move_base_msgs`
  - `robot_state_publisher`
  - `std_msgs`
  - `turtlebot3_description`
  - `turtlebot3_slam`
  - `turtlebot3_teleop`
  - `xacro` -->

### 4/24 완료 사항

- 루트 구조와 패키지 뼈대는 준비됨
- Gazebo에서 사용할 전시장 기본 월드 추가
- Gazebo 월드 실행용 launch 파일 추가
- TurtleBot3를 월드에 스폰하는 launch 파일 추가
- SLAM 실행용 launch 파일 추가
- SLAM 으로 지도 생성 후 `maps/`에 저장

### 아직 필요한 핵심 구현

<!-- - Gazebo 전시장 월드 제작
- RViz 설정 파일 작성
- SLAM 지도 생성 및 저장 -->
- Navigation 실행 구성
- 부스 좌표 설정 파일 작성
- 목적지 이동 Python 노드 작성
- 도착 확인 및 복귀 로직 작성
- 사용자 UI 연동

## 5. 개발 범위

이번 프로젝트는 실제 하드웨어 제작보다 `시뮬레이션 기반 안내 로봇 구현`에 집중한다.

### 포함 범위

- 전시장 형태의 실내 월드 구성
- 저장된 지도 기반 위치 추정 및 경로 계획
- 부스 선택 후 목적지 이동
- 도착 확인 및 출입구 복귀
- RViz를 통한 시각화

### 제외 또는 후순위 범위

- 실제 Raspberry Pi 하드웨어 제어
- 고급 음성 안내 시스템
- 복잡한 동적 장애물 시뮬레이션
- 실제 전시장 수준의 정밀 모델링

<!-- ## 6. 권장 구현 순서

1. `worlds/`에 단순 전시장 월드 작성
2. Gazebo에서 TurtleBot3 실행 확인
3. RViz 연동 및 센서 시각화 확인
4. SLAM으로 지도 생성 후 `maps/`에 저장
5. Navigation 실행 환경 구성
6. `config/`에 부스 좌표 등록
7. `scripts/`에 목적지 이동 노드 작성
8. 도착 후 복귀 기능 추가
9. 필요 시 간단한 Tkinter UI 연결 -->

## 7. 당장 해야 할 일

<!-- - `README.md`를 기준 문서로 유지하면서 작업 내용 계속 기록
- Gazebo에서 SLAM 실행 확인하기
- 실제 맵 생성 후 `maps/`에 저장하기 -->
- `scripts/`와 `config/`에 최소 실행 가능한 파일부터 추가하기
- 부스 좌표 체계를 먼저 정하고 문서에 반영하기

<!-- ## 8. 비고

- 현재 문서는 프로젝트 진행상황 정리용 초안이다.
- 실제 파일이 추가되면 실행 명령어, 패키지 구성도, 테스트 결과를 계속 업데이트할 예정이다.

## 9. 맵핑 작업 정리

맵핑은 전시장 월드와 로봇이 Gazebo에서 정상적으로 실행된 뒤 진행한다. -->


<!-- ## 10. 맵핑 실행 방법

### 1. 빌드 및 환경 설정

```bash
cd /home/seohee/navbot_ws
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=burger
```

### 2. SLAM 실행

```bash
roslaunch exhibition_guide exhibition_slam.launch
```

### 3. 로봇 수동 조작

새 터미널에서 아래 명령어를 실행한다.

```bash
cd /home/seohee/navbot_ws
source devel/setup.bash
export TURTLEBOT3_MODEL=burger
roslaunch exhibition_guide exhibition_teleop.launch
```

기본 TurtleBot3 teleop보다 더 천천히 움직이도록 조정한 맵핑용 키보드 조작 노드다.

### 4. 지도 저장

맵이 충분히 생성되면 새 터미널에서 아래 명령어로 저장한다.

```bash
cd /home/seohee/navbot_ws
source devel/setup.bash
rosrun map_server map_saver -f src/exhibition_guide/maps/exhibition_map
```

저장 결과:

- `src/exhibition_guide/maps/exhibition_map.pgm`
- `src/exhibition_guide/maps/exhibition_map.yaml` -->

