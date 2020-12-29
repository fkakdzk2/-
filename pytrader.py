import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from kiwoom import *
import pandas as pd
import time


#실제 실행시는 파일

form_class = uic.loadUiType("pytrader.ui")[0] #잘 실행되고 있는지 확인을 위한 ui

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self) #ui 실행

        self.kiwoom = Kiwoom() #kiwoom 인스턴스생성
        self.kiwoom.comm_connect() #로그인창 실행

        self.trade_stocks_done = False #거래를 실행했는지 확인하기 위한 변수 >> false값 일단 저장

        #self.start_date = QDate.currentDate() #처음 실행 했을 때의 날짜를 저장함 >> 이후 날짜와 비교하여 조건부로 매매 매쏘드를 실행시키기 위함

        self.timer = QTimer(self) #시간 확인을 위한 Qtimer 객체의 인스턴스 생성
        self.timer.start(1000)



        self.timer.timeout.connect(self.timeout) #밑에 있는 timeout 함수 실행 >> 실제 주요 매쏘드 실행


    def send_order(self):
        account = self.kiwoom.get_login_info(["ACCNO"]) #계좌정보 호출
        account = account.rstrip(';') #호출된 계좌정보에는 맨 뒤에 ';' 이 붙어있어서 이것을 제거함


        #print(account)

        hoga_lookup = {'지정가': "00", '시장가': "03"} #send_order 매쏘드에서 매매유형을 선택할 때 좀 더 직관적으로 처리하기 위함


        f = open("buy_list.txt", 'rt') #buy_list에서 매매정보를 가져옴 (read)
        buy_list = f.readlines() #buy_list를 한줄씩 가져와서 list 형식의 buy_list에 하나씩 넣는다.
        f.close() #buy_list 파일 닫기

        #print(len(buy_list))

        # buy list
        for row_data in buy_list: #buy_list갯수 만큼 반복문 실행
            split_row_data = row_data.split(';') # ';'으로 각 정보를 구분했기 때문에 이것을 기준으로 list에 넣는다.


            #각 정보를 담는 변수
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]



            if split_row_data[-1].rstrip() == '매수전': #매수전이면 send_order 매쏘드 실행
                self.kiwoom.send_order("send_order_req", "0101", account, 1, code, num, price,
                                       hoga_lookup[hoga], "")



        # buy list
        for i, row_data in enumerate(buy_list): #주문 완료 후 매수전을 주문완료로 상태 변경
            buy_list[i] = buy_list[i].replace("매수전", "주문완료")

        # file update
        f = open("buy_list.txt", 'wt') #변경된 내용 buy_list 파일에도 반영
        for row_data in buy_list:
            f.write(row_data)
        f.close()

        hog = self.current_price()
        print(hog)


    def current_price(self): #현재가 출력을 위한 함수
        ret = self.kiwoom._opt10081("048530","주식기본정보")

    def hoga_price(self):
        ret = self.kiwoom.GetCommRealData("048530", 27)
        return ret







    def timeout(self): #이 함수는 pytrader를 실행 했을 때 ui를 종료할때까지 반복하여 실행된다.
        market_start_time = QTime(9, 0, 0) #장 시작 시간 저장 >> 이 형식으로 수정하여 실제 거래가 실행 될 시간 설정 가능
        current_time = QTime.currentTime() #현재 시간 저장 >> 반복문이기 때문에 지속적으로 수정되어 저장된다.
        cur_date = QDate.currentDate() #현재 날짜 저장>> 반복문이기 때문에 지속적으로 수정되어 저장된다.


        #if  self.start_date < cur_date and current_time > market_start_time and self.trade_stocks_done is False :
        if  current_time > market_start_time and self.trade_stocks_done is False:
            #처음 실행했을때 저장된 날짜와 현재 날짜를 비교, 시간도 마찬가지 조건을 설정하여 send_order 매쏘드를 실행한다.
            self.send_order()
            self.trade_stocks_done = True #매매가 실행 되었을 때 더이상 send_order가 실행 되지 않게하는 flag역할
            self.current_price()


        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time

        state = self.kiwoom.get_connect_state()
        if state == 1:
            state_msg = "서버 연결 중"
        else:
            state_msg = "서버 미 연결 중"

        self.statusbar.showMessage(state_msg + " | " + time_msg)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()