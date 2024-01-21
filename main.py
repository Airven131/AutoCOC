from core import *
TCN = 10

class AutoNightWorld():
    def xiabin(self):
        pytap(180, 705, 0.05, 0.05)                                         # 点击第1个单位
        pytap(21, 366, 0.05, 0.05)
        pytap(290, 705, 0.05, 0.05)                                         # 点击第2个单位
        pytap(109, 275, 0.05, 0.05)
        pytap(370, 705, 0.05, 0.05)                                         # 点击第3个单位
        pytap(365, 87, 0.05, 0.05)
        pytap(460, 705, 0.05, 0.05)                                         # 点击第4个单位
        pytap(843, 56, 0.05, 0.05)
        pytap(550, 705, 0.05, 0.05)                                         # 点击第5个单位
        pytap(1110, 250, 0.05, 0.05)
        pytap(640, 705, 0.05, 0.05)                                         # 点击第6个单位
        pytap(1173, 450, 0.05, 0.05)
        pytap(730, 705, 0.05, 0.05)                                         # 点击第7个单位
        pytap(1000, 610, 0.05, 0.05)
        pytap(820, 705, 0.05, 0.05)                                         # 点击第8个单位
        pytap(310, 610, 0.05, 0.05)
        # pytap(910, 705)                                       # 点击第9个单位
        # pytap(263, 573)
        # pytap(1000, 705)                                      # 点击第10个单位
        # pytap(21, 366)

    def xiabin_ma(self):
        pytap(200, 880, 0.2, 0.2)                                         # 点击第1个单位
        pytap(124, 293, 0.2, 0.2)
        pytap(320, 880, 0.2, 0.2)                                         # 点击第2个单位
        pytap(511, 14, 0.2, 0.2)
        pytap(430, 880, 0.2, 0.2)                                         # 点击第3个单位
        pytap(1055, 22, 0.2, 0.2)
        pytap(540, 705, 0.2, 0.2)                                         # 点击第4个单位
        pytap(1344, 239, 0.2, 0.2)
        pytap(650, 705, 0.2, 0.2)                                         # 点击第5个单位
        pytap(1110, 250, 0.2, 0.2)
        pytap(760, 705, 0.2, 0.2)                                         # 点击第6个单位
        pytap(1411, 546, 0.2, 0.2)
        pytap(870, 705, 0.2, 0.2)                                         # 点击第7个单位
        pytap(1061, 781, 0.2, 0.2)
        pytap(980, 705, 0.2, 0.2)                                         # 点击第8个单位
        pytap(403, 754, 0.2, 0.2)
        # pytap(1090, 705, 0.2, 0.2)                                                  # 点击第9个单位
        # pytap(263, 573, 0.2, 0.2)
        # pytap(1200, 705, 0.2, 0.2)                                                  # 点击第10个单位
        # pytap(21, 366, 0.2, 0.2)

    def fight(self):
        get_screen()
        pytap(70, 700, 0.5, 0.5)                                  # 点击进攻 
        pytap(976, 500, 0.5, 0.5)                                 # 点击立即寻找
        while notexist('开战倒计时', conf_exist = 0.6):                     # 判断是否寻敌完成
            get_screen()
        self.xiabin()
        not_defeat_night_world_2 = True
        while exist('距离战斗结束还有', conf_exist = 0.6):  #下兵完成，循环判断是否进入结束战斗
            get_screen()
        while notexist('回营'):
            get_screen()         #结束战斗，循环判断是否进入二阶段还是战斗
            if not_defeat_night_world_2:
                if exist('开战倒计时', conf_exist = 0.6):  #通过判断奥仔岗哨按钮是否存在来判断是否进入二阶段
                    self.xiabin()
                    not_defeat_night_world_2 = False
        pytap(645, 645) #点击回营
        while notexist('移动', conf_exist = 0.8):
            get_screen()
            if exist('确定', conf_exist = 0.7):   # 用于判断是否有胜利之星奖励
                pytap(600, 600, 2, 3)                                  # 判断是否回城完成
        pyswipe(976, 500, 976, 700, 500)
        pytap(875, 209, 0.2, 0.2) #点击圣水车
        pytap(965, 655, 0.1, 0.1) 
        pytap(1110, 75, 0.1, 0.1)

    def fight_ma(self):
        pytap(90, 865, 0.5, 0.5)                                  # 点击进攻 
        pytap(1150, 620, 0.5, 0.5)                                 # 点击立即寻找
        while notexist('开战倒计时_马', conf_exist = 0.6):                     # 判断是否寻敌完成
            get_screen()
            img = cv2.imread('/home/airven/.zhuoyi/common-{6c0bd68b-7b82-44c0-bf59-d0f2eb43e5be}-12/移动x数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)
            image = image_cut_ma(img)
            cv2.imshow('screen', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        self.xiabin_ma()
        not_defeat_night_world_2 = True
        while exist('距离战斗结束还有_马', conf_exist= 0.8):  #下兵完成，循环判断是否进入结束战斗
            get_screen()
        while notexist('回营_马'):
            get_screen()         #结束战斗，循环判断是否进入二阶段还是战斗
            if not_defeat_night_world_2:
                if exist('开战倒计时_马', conf_exist = 0.6):  #通过判断奥仔岗哨按钮是否存在来判断是否进入二阶段
                    self.xiabin_ma()
                    not_defeat_night_world_2 = False
        pytap(766, 800)
        while notexist('进攻_马', conf_exist = 0.6):
            get_screen()
            if exist('确定'):   # 用于判断是否有胜利之星奖励
                pytap(600, 600)                                  # 判断是否回城完成
        time.sleep(3)
        pyswipe(976, 500, 976, 750, 500)
        pytap(875, 209, 0.2, 0.2) #点击圣水车
        pytap(965, 655, 0.2, 0.2) 
        pytap(1110, 75, 0.2, 0.2)

class AutoHomeTown():
    def xiabin():
        pyswipe(0, 0, 0.5, 0.5)

    def auto_home_town(self):
        get_screen()
        while notexist('移动'):
            get_screen()
        pytap(70, 700, 0.5, 0.5)
        pytap(917, 493, 0.5, 0.5)
        while notexist('结束战斗'):
            get_screen()


if __name__ == '__main__':
    n = 1
    choise = input('1.自动家乡作战\n2.自动夜世界作战\n')
    if choise == 1:
        while n <= 100:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            AutoNightWorld.fight()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
    elif choise == 2:
        while n <= 100:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            AutoHomeTown.auto_home_town()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
            