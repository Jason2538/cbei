from tkinter import *
from tkinter.font import *
import cv2  # 영상을 내맘대로 하는 신!!!
import mediapipe as mp  # 손가락 마디마디 인식하는 인공지능
import os  # 윈도우를 내맘대로!! 프린터 동작
from PIL import ImageTk, Image  # 사진 컨트롤
import playsound   ## 소리 나오게 해주는 라이브러리
import time        ## 몇 초 뒤에 동작 등 시간과 관련된 라이브러리
import pyautogui   ## 키보드를 내 마음대로 동작을 시키는 라이브러리

앱 = Tk()
폰트 = Font(family="맑은 고딕", size=60)
폰트2 = Font(family="맑은 고딕", size=20)
앱.geometry("1080x720")  # 앱의 크기와 위치 잡기
앱.title("제30대 대통령선거 투표")
배경 = Image.open('bg.png')
배경 = ImageTk.PhotoImage(배경)
label = Label(앱, image=배경)
label.place(x=0, y=0)
# 캠이 보여질 화면 ( 프레임 속에 레이블 )
집프레임 = Frame(앱)
프캠 = Label(집프레임)
프캠.pack()
집프레임.pack(pady=270)
# 초를 셀 초 변수
초 = 0
# 손신호를 저장할 변수
손신호 = 0
# 진행 단계를 표시할 변수
단계 = 0    ## 아직 시작을 안했으므로 0단계
# 고른 후보를 저장할 변수
선택 = 0
캠 = cv2.VideoCapture(0)
그림 = mp.solutions.drawing_utils  # 인공지능에서 검색된 그림 그려줌
손인식 = mp.solutions.hands  # 손동작 인식 모듈 불러오기
### 스페이스 바를 눌러서 시작하는 함수 ###
def 단계1(e):    ## e는 무슨 키를 눌렀는지 키 정보가 들어감
    global 단계, 초
    초 = 52      ## 52초로 시작 
    단계 = 1     ## 1단계 시작
def 시작():
    global 초, 단계, 손신호, 선택
    성공, 사진 = 캠.read()  # 프레임이 올바르게 읽히면 ret은 True
    if not 성공:
        캠.release()  # 작업 완료 후 해제
        return
    with 손인식.Hands() as 손들:
        # convert 변경 bgr ==> rgb
        사진 = cv2.cvtColor(사진, cv2.COLOR_BGR2RGB)
        # flip 뒤집다 후라이팬  거울모드 만듦
        사진 = cv2.flip(사진, 1)  # 좌우변경
        # process 인공지능을 돌림
        손들 = 손들.process(사진)  # 손동작을 인식
        # multi 여러개의 손 중요지점
        if 손들.multi_hand_landmarks:
            손신호 = 0
            for hand_landmarks in 손들.multi_hand_landmarks:
                # print(hand_landmarks)
                finger1 = int(hand_landmarks.landmark[4].x * 1000)  # 엄지손끝 x좌표
                finger2 = int(hand_landmarks.landmark[1].x * 1000)  # 엄지맨 아래 x좌표
                finger3 = int(hand_landmarks.landmark[8].y * 1000)  # 검지손끝 y좌표
                finger4 = int(hand_landmarks.landmark[5].y * 1000)  # 검지맨 아래 y좌표
                finger5 = int(hand_landmarks.landmark[12].y * 1000)  # 중지손끝 y좌표
                finger6 = int(hand_landmarks.landmark[9].y * 1000)   # 중지맨 아래 y좌표
                finger7 = int(hand_landmarks.landmark[16].y * 1000)  # 약지손끝 y좌표
                finger8 = int(hand_landmarks.landmark[13].y * 1000)  # 약지맨 아래 y좌표
                finger9 = int(hand_landmarks.landmark[20].y * 1000)  # 새끼손끝 y좌표
                finger10 = int(hand_landmarks.landmark[17].y * 1000)  # 새끼맨 아래 y좌표
                finger11 = int(hand_landmarks.landmark[4].y * 1000)  # 엄지 끝 y 좌표
                finger12 = int(hand_landmarks.landmark[1].y * 1000)  # 엄지 맨 아래 y 좌표
                finger13 = int(hand_landmarks.landmark[9].x * 1000)  # 중지 맨 아래 x 좌표
                # 펼치고 있는 손가락 개수 ==> 수
                수 = 0
                # 엄지손가락 끝과 맨 아래의 x좌표가 높아졌는지 판단한다음 약지와 엄지가 먼 상태여야지만 판단
                if 40 < abs(finger2 - finger1) and 50 < abs(finger1 - finger13):
                    수 = 수 + 1
                # 엄지를 위로 세웠을 때
                # 먼저 엄지끝과 맨 아래의 y 좌표가 높아졌다면
                # 손을 붙인게 아닌지 확인 중지와 엄지가 먼 상태여야지만 숫자를 세는 것이므로 손가락 든게 맞음!!
                elif 50 < finger12 - finger11 and 50 < abs(finger1 - finger13):
                    수 = 수 + 1
                # 검지손가락 확인
                if 50 < finger4 - finger3:
                    수 = 수 + 1
                # 중지손가락 확인
                if 50 < finger6 - finger5:
                    수 = 수 + 1
                # 약지손가락 확인
                if 50 < finger8 - finger7:
                    수 = 수 + 1
                # 새끼손가락 확인
                if 40 < finger10 - finger9:
                    수 = 수 + 1
                # 전체 손가락 든 갯수 합!!!! 왼손 + 오른손
                손신호 = 손신호 + 수
                그림.draw_landmarks(사진, hand_landmarks,
                                손인식.HAND_CONNECTIONS)  # 손 가락 모형 그림 그려주기
            # put 집어넣다 text
            cv2.putText(
                사진, text=f'{손신호}', org=(30, 60),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=2,
                color=(0, 0, 255), thickness=2)
    #### tkinter에 비디오를 넣는 코드 ####
    # 사진을 끌어오기 위해 그안에 있는 숫자를 끄집어냄
    사진 = Image.fromarray(사진)  # Image 객체로 변환
    # 숫자 ==> tkinter 전용 이미지로 바꿈
    사진 = ImageTk.PhotoImage(image=사진)  # ImageTk 객체로 변환
    # OpenCV 동영상
    집프레임.imgtk = 사진  # 프레임속에 이미지 넣기
    프캠["image"] = 사진  # 들어온 이미지를 레이블에 넣기
    #### tkinter에 비디오를 넣는 코드 끝 ####
    # 1단계 시작여부 판단(시작하려면 숫자 2)
    if 단계 == 1:
        초 = 초 - 2
        print("단계1", 초)
        # 10분의 1초 단위므로 진짜 초를 구할려면 나누기 10을 해야함!!
        if 초 % 10 == 0:  # 초가 50, 40, 30, 20, 10 이라면
            진초 = 초 / 10  # 초를 50이면 5, 40이면 4로 변환
            if 진초 == 5:  ### 5초라면
                playsound.playsound("start1.mp3")
                playsound.playsound("su"+str(int(진초))+".mp3")
            elif 진초 < 5:  ### 5초 이하라면
                playsound.playsound("su"+str(int(진초))+".mp3")
            if 진초 == 0:   ### 0초가 되었다면
                if 손신호 == 2:
                    단계 = 2
                    초 = 52
                else:
                    단계 = 1
                    초 = 52

    # 2단계 선택할 후보 판단(숫자 1-10이면 다음단계 0이면 다시)
    if 단계 == 2:
        초 = 초 - 2
        print("단계2", 초)
        if 초 % 10 == 0:
            진초 = 초 / 10
            if 진초 == 5:
                playsound.playsound("start2.mp3")
                playsound.playsound("su"+str(int(진초))+".mp3")
            elif 진초 < 5:
                playsound.playsound("su"+str(int(진초))+".mp3")
            if 진초 == 0:
                if 손신호 != 0:
                    선택 = 손신호
                    단계 = 3
                    초 = 52
                else:
                    초 = 52

    # 3단계 선택한 후보가 맞는지 판단 맞으면 투표용지 출력 틀리면 2단계로)
    if 단계 == 3:
        초 = 초 - 2
        print("단계3", 초)
        if 초 % 10 == 0:
            진초 = 초 / 10
            if 진초 == 5:
                playsound.playsound("choice" + str(선택) + ".mp3")
                playsound.playsound("su"+str(int(진초))+".mp3")
            elif 진초 < 5:
                playsound.playsound("su"+str(int(진초))+".mp3")
            if 진초 == 0:
                if 손신호 == 1:
                    playsound.playsound("print" + str(선택) + ".mp3")
                    os.startfile("투표용지\투표" + str(선택) + ".PNG", "print")
                    time.sleep(6)
                    pyautogui.press("Enter")

                    단계 = 0
                else:
                    단계 = 2
                    초 = 52
    앱.after(30, 시작)   ### 천분의 30 초당 한번씩 다시 시작하도록 만듦 

앱.bind("<space>", 단계1)  ## tkinter에서 키보드 이벤트 만듦(스페이스바를 누르면 단계1 함수 실행)
시작()
앱.mainloop()

# pip install opencv-python==4.6.0.66

# pip install playsound==1.2.2

# pip install mediapipe