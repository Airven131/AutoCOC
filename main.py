# from Core import *
import os
import cv2
import time
import numpy as np
from threading import Thread
from PIL import Image



class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class Core():
    def __init__(self,icon_name = None, image_name = None, conf = 0.9):
        self._icon_name = icon_name
        self._image_name = image_name
        self._conf = conf
        pass

    def ImageCut(self, image_full):
        image = image_full[0:772, 0:1265].copy()
        return image

        #图片裁切，只选取左上角1265*772的有效区域        
    def ImageCut_ma(self, image_full):
        image = image_full[0:950, 0:1520].copy()
        return image

    def GetIconPosition(self, icon_name = None, conf = 0.9):
        # time_now = time.strftime('%H:%M:%S', time.localtime())
        # if icon_name is None:
        #     icon_name = self._icon_name
        # 读取图片和图标的灰度图
        icon = cv2.imread('/home/airven/Code/AutoCOC/icon/' + icon_name + '.png', cv2.IMREAD_GRAYSCALE)
        image = cv2.imread('/home/airven/.zhuoyi/common/移动数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)

        #图片裁切，只选取左上角1265*772的有效区域
        image = image[0:772, 0:1265]

        # 匹配图片和图标
        resule = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)
        _, _, min_loc, max_loc = cv2.minMaxLoc(resule)

        # 丢弃掉匹配值较低的pisition
        if _ < conf:
            return Position(-1, -1)
        
        # 获取图标左上角的坐标
        x, y = max_loc

        return Position(x, y)


    def GetScreen():
        time_now = time.strftime('%H:%M:%S', time.localtime())
        os.system(f'adb shell screencap /sdcard/screen.png')
        print('[%s]:get the screen' %(time_now))
        time.sleep(1)

    def LoopGetScreen():
        while True:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            os.system(f'adb shell screencap /sdcard/screen.png')
            print('[%s]:get the screen' %(time_now))
            time.sleep(1)

    def Exist(self, icon_name = None, conf = 0.9):
        if icon_name is None:
            icon_name = self._icon_name
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.GetIconPosition(icon_name, conf).x
        y = self.GetIconPosition(icon_name, conf).y
        if x == -1 :
            print('[%s]:The icon %s is not exist' %(time_now, icon_name))
            return False
        else:
            print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_name, x, y))
            return True
        
    def NotExist(self, icon_name = None, conf = 0.9):
        if icon_name is None:
            icon_name = self._icon_name
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.GetIconPosition(icon_name, conf).x
        y = self.GetIconPosition(icon_name, conf).y
        if x == -1 :
            print('[%s]:The icon %s is not exist' %(time_now, icon_name))
            return True
        else:
            print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_name, x, y))
            return False

    def PyTap(self, x, y, before_time = 2.0, after_time = 2.0):
        time.sleep(before_time)
        time_now = time.strftime('%H:%M:%S', time.localtime())
        os.system('adb shell input tap %d %d' %(x, y))
        print('[%s]:Successful tap %d %d' %(time_now, x, y))
        time.sleep(after_time)

    def PySwipe(self, from_x, from_y, to_x, to_y, way_time):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        # if time is None:
        #     length = sqrt(pow(from_x - to_x), 2) + pow((from_y - to_y),2)
        #     speed = randint(1500, 2000)
        #     time = length/speed*1000
        os.system('adb shell input swipe %d %d %d %d %d' %(from_x, from_y, to_x, to_y, int(way_time)))
        print('[%s]:Successful swip from %d %d to %d %d' %(time_now, from_x, from_y, to_x, to_y))

    # def icontap(icon_file):
    #     icon_position = GetIconPosition(icon_name = icon_file)
    #     h, w =  cv2.imread('icon/' + icon_file + '.png', cv2.IMREAD_GRAYSCALE)
    #     x = icon_position.x
    #     y = icon_position.y
    #     os.system('adb shell input tap %d %d' %(x, y))

    #色彩转换
    # def trans_color(image_rgb, r, g, b):
    #     i = 0
    #     j = 0
    #     image = [[[]]]
    #     while i <= 1265:
    #         while j <= 772:
    #             image[i][j][0] = image_rgb[i][j][0] * r
    #             image[i][j][1] = image_rgb[i][j][1] * g
    #             image[i][j][2] = image_rgb[i][j][2] * b
    #     return image
        
    # def GetResource(self):
    #     path = '/home/airven/.zhuoyi/common/移动数据/存储卡/screen.png'

    #     result = []
    #     reader = easyocr.Reader(['en'])
    #     resule_all = reader.readtext(path, paragraph="False")
    #     n = 0
    #     for n in resule_all:
    #         if 0 < resule_all[n][0][0][0] < 1 and 0 < resule_all[n][0][0][1] < 1:
    #             result[0] = resule_all[n][1]
    #         if 0 < resule_all[n][0][0][0] < 1 and 0 < resule_all[n][0][0][1] < 1:
    #             result[1] = resule_all[n][1]
    #         if 0 < resule_all[n][0][0][0] < 1 and 0 < resule_all[n][0][0][1] < 1:
    #             result[2] = resule_all[n][1]


class AutoNightWorld():
    def xiabin(self):
        Core().PyTap(180, 705, 0.05, 0.05)                                         # 点击第1个单位
        Core().PyTap(21, 366, 0.05, 0.05)
        Core().PyTap(290, 705, 0.05, 0.05)                                         # 点击第2个单位
        Core().PyTap(109, 275, 0.05, 0.05)
        Core().PyTap(370, 705, 0.05, 0.05)                                         # 点击第3个单位
        Core().PyTap(365, 87, 0.05, 0.05)
        Core().PyTap(460, 705, 0.05, 0.05)                                         # 点击第4个单位
        Core().PyTap(843, 56, 0.05, 0.05)
        Core().PyTap(550, 705, 0.05, 0.05)                                         # 点击第5个单位
        Core().PyTap(1110, 250, 0.05, 0.05)
        Core().PyTap(640, 705, 0.05, 0.05)                                         # 点击第6个单位
        Core().PyTap(1173, 450, 0.05, 0.05)
        Core().PyTap(730, 705, 0.05, 0.05)                                         # 点击第7个单位
        Core().PyTap(1000, 610, 0.05, 0.05)
        Core().PyTap(820, 705, 0.05, 0.05)                                         # 点击第8个单位
        Core().PyTap(310, 610, 0.05, 0.05)
        # Core.PyTap(910, 705)                                       # 点击第9个单位
        # Core.PyTap(263, 573)
        # Core.PyTap(1000, 705)                                      # 点击第10个单位
        # Core.PyTap(21, 366)

    def xiabin_ma(self):
        Core().PyTap(200, 880, 0.2, 0.2)                                         # 点击第1个单位
        Core().PyTap(124, 293, 0.2, 0.2)
        Core().PyTap(320, 880, 0.2, 0.2)                                         # 点击第2个单位
        Core().PyTap(511, 14, 0.2, 0.2)
        Core().PyTap(430, 880, 0.2, 0.2)                                         # 点击第3个单位
        Core().PyTap(1055, 22, 0.2, 0.2)
        Core().PyTap(540, 705, 0.2, 0.2)                                         # 点击第4个单位
        Core().PyTap(1344, 239, 0.2, 0.2)
        Core().PyTap(650, 705, 0.2, 0.2)                                         # 点击第5个单位
        Core().PyTap(1110, 250, 0.2, 0.2)
        Core().PyTap(760, 705, 0.2, 0.2)                                         # 点击第6个单位
        Core().PyTap(1411, 546, 0.2, 0.2)
        Core().PyTap(870, 705, 0.2, 0.2)                                         # 点击第7个单位
        Core().PyTap(1061, 781, 0.2, 0.2)
        Core().PyTap(980, 705, 0.2, 0.2)                                         # 点击第8个单位
        Core().PyTap(403, 754, 0.2, 0.2)
        # Core.PyTap(1090, 705, 0.2, 0.2)                                                  # 点击第9个单位
        # Core.PyTap(263, 573, 0.2, 0.2)
        # Core.PyTap(1200, 705, 0.2, 0.2)                                                  # 点击第10个单位
        # Core.PyTap(21, 366, 0.2, 0.2)

    def Fight(self):
        Core.GetScreen()
        Core().PyTap(70, 700, 0.5, 0.5)                                  # 点击进攻 
        Core().PyTap(976, 500, 0.5, 0.5)                                 # 点击立即寻找
        while Core().NotExist(icon_name = '开战倒计时', conf = 0.6):                     # 判断是否寻敌完成
            Core.GetScreen()
        self.xiabin()
        nhnw2 = True
        while Core().Exist(icon_name = '距离战斗结束还有', conf = 0.6):  #下兵完成，循环判断是否进入结束战斗
            Core.GetScreen()
        while Core().NotExist(icon_name = '回营'):
            Core.GetScreen()         #结束战斗，循环判断是否进入二阶段还是战斗
            if nhnw2:
                if Core().Exist(icon_name = '开战倒计时', conf = 0.6):  #判断是否存在来判断是否进入二阶段
                    self.xiabin()
                    nhnw2 = False
        Core().PyTap(645, 645) #点击回营
        while Core().NotExist(icon_name = '移动', conf = 0.8):
            Core.GetScreen()
            if Core().Exist(icon_name = '确定', conf = 0.7):   # 用于判断是否有胜利之星奖励
                Core().PyTap(600, 600, 2, 3)                                  # 判断是否回城完成
        Core().PySwipe(976, 500, 976, 700, 500)
        Core().PyTap(875, 209, 0.2, 0.2) #点击圣水车
        Core().PyTap(965, 655, 0.1, 0.1) 
        Core().PyTap(1110, 75, 0.1, 0.1)

    def fight_ma(self):
        Core.PyTap(90, 865, 0.5, 0.5)                                  # 点击进攻 
        Core.PyTap(1150, 620, 0.5, 0.5)                                 # 点击立即寻找
        while Core.notexist('开战倒计时_马', conf_exist = 0.6):                     # 判断是否寻敌完成
            Core.GetScreen()
            img = cv2.imread('/home/airven/.zhuoyi/common-{6c0bd68b-7b82-44c0-bf59-d0f2eb43e5be}-12/移动x数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)
            image = Core.ImageCut_ma(img)
            cv2.imshow('screen', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        self.xiabin_ma()
        not_defeat_night_world_2 = True
        while Core.exist('距离战斗结束还有_马', conf_exist= 0.8):  #下兵完成，循环判断是否进入结束战斗
            Core.GetScreen()
        while Core.notexist('回营_马'):
            Core.GetScreen()         #结束战斗，循环判断是否进入二阶段还是战斗
            if not_defeat_night_world_2:
                if Core.exist('开战倒计时_马', conf_exist = 0.6):  #通过判断奥仔岗哨按钮是否存在来判断是否进入二阶段
                    self.xiabin_ma()
                    not_defeat_night_world_2 = False
        Core.PyTap(766, 800)
        while Core.notexist('进攻_马', conf_exist = 0.6):
            Core.GetScreen()
            if Core.exist('确定'):   # 用于判断是否有胜利之星奖励
                Core.PyTap(600, 600)                                  # 判断是否回城完成
        time.sleep(3)
        Core.PySwipe(976, 500, 976, 750, 500)
        Core.PyTap(875, 209, 0.2, 0.2) #点击圣水车
        Core.PyTap(965, 655, 0.2, 0.2) 
        Core.PyTap(1110, 75, 0.2, 0.2)

class AutoHomeTown():
    def xiabin():
        Core.PySwipe(0, 0, 0.5, 0.5)

    def fight(self):
        while Core.notexist('移动'):
            Core.GetScreen()
        Core.PyTap(70, 700, 0.5, 0.5)
        Core.PyTap(917, 493, 0.5, 0.5)
        while Core.exist('结束战斗'):
            Core.GetScreen()

if __name__ == '__main__':
    n = 1
    N = 100
    choise = input('1.自动家乡作战\n2.自动夜世界作战\n3.退出\n')
    N = input('请输入循环次数(default = 100)')
    N = int(N)

    # get_screen_thread = Thread(target=Core.LoopGetScreen,args=(),daemon=True)
    # get_screen_thread.start()

    if choise == '1':
        while n <= N:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            AutoHomeTown.fight()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
    elif choise == '2':
        while n <= N:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            AutoNightWorld().Fight()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
    elif choise == '3':
        print('已退出\n')
        exit()
    else:
        print(type(n))
