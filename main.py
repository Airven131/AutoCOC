# from Core import *
import os
import cv2
import time
# import numpy as np
# from threading import Thread
# from PIL import Image



class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class Core():
    def __init__(self, times = 0, icon_name = None, image_name = None, conf = 0.9):
        self.times = times
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


    def GetScreen(self):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        os.system(f'adb shell screencap /sdcard/screen.png')
        out = '[%d][%s]:已截图' %(self.times, time_now)
        time.sleep(1)
        return out

    def Exist(self, icon_name = None, conf = 0.9):
        if icon_name is None:
            icon_name = self._icon_name
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.GetIconPosition(icon_name, conf).x
        y = self.GetIconPosition(icon_name, conf).y
        if x == -1 :
            out = False, '[%d][%s]:未发现%s图标' %(self.times, time_now, icon_name)
            return out
        else:
            out = True, '[%d][%s]:成功在%d %d发现图标%s' %(self.times, time_now, x, y, icon_name)
            return out
        
    def NotExist(self, icon_name = None, conf = 0.9):
        if icon_name is None:
            icon_name = self._icon_name
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.GetIconPosition(icon_name, conf).x
        y = self.GetIconPosition(icon_name, conf).y
        if x == -1 :
            print('[%d][%s]:%s图标不存在' %(self.times, time_now, icon_name))
            return True
        else:
            print('[%d][%s]:成功在%d %d发现%s' %(self.times, time_now, x, y, icon_name))
            return False

    def PyTap(self, x, y, before_time = 2.0, after_time = 2.0):
        time.sleep(before_time)
        time_now = time.strftime('%H:%M:%S', time.localtime())
        os.system('adb shell input tap %d %d' %(x, y))
        out = '[%d][%s]:已点击坐标 %d %d' %(self.times, time_now, x, y)
        time.sleep(after_time)
        return out

    def PySwipe(self, from_x, from_y, to_x, to_y, way_time):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        # if time is None:
        #     length = sqrt(pow(from_x - to_x), 2) + pow((from_y - to_y),2)
        #     speed = randint(1500, 2000)
        #     time = length/speed*1000
        os.system('adb shell input swipe %d %d %d %d %d' %(from_x, from_y, to_x, to_y, int(way_time)))
        out = '[%d][%s]:成功从%d %d 滑动至 %d %d' %(self.times, time_now, from_x, from_y, to_x, to_y)
        return out

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
    def __init__(self, times = 0):
        self.times = times

    def xiabin(self):
        print(Core(times = self.times).PyTap(180, 705, 0.05, 0.05))                                         # 点击第1个单位
        print(Core(times = self.times).PyTap(21, 366, 0.05, 0.05), end = '\r')
        print(Core(times = self.times).PyTap(290, 705, 0.05, 0.05), end = '\r')                                      # 点击第2个单位
        print(Core(times = self.times).PyTap(109, 275, 0.05, 0.05), end = '\r')
        print(Core(times = self.times).PyTap(370, 705, 0.05, 0.05), end = '\r')                                         # 点击第3个单位
        print(Core(times = self.times).PyTap(365, 87, 0.05, 0.05), end = '\r')
        print(Core(times = self.times).PyTap(460, 705, 0.05, 0.05), end = '\r')                                         # 点击第4个单位
        print(Core(times = self.times).PyTap(843, 56, 0.05, 0.05), end = '\r')
        print(Core(times = self.times).PyTap(550, 705, 0.05, 0.05), end = '\r')                                         # 点击第5个单位
        print(Core(times = self.times).PyTap(1110, 250, 0.05, 0.05), end = '\r')
        print(Core(times = self.times).PyTap(640, 705, 0.05, 0.05), end = '\r')                                         # 点击第6个单位
        print(Core(times = self.times).PyTap(1173, 450, 0.05, 0.05), end = '\r')
        print(Core(times = self.times).PyTap(730, 705, 0.05, 0.05), end = '\r')                                         # 点击第7个单位
        print(Core(times = self.times).PyTap(1000, 610, 0.05, 0.05), end = '\r')
        print(Core(times = self.times).PyTap(820, 705, 0.05, 0.05), end = '\r')                                         # 点击第8个单位
        print(Core(times = self.times).PyTap(310, 610, 0.05, 0.05), end = '\r')
        # Core.PyTap(910, 705)                                       # 点击第9个单位
        # Core.PyTap(263, 573)
        # Core.PyTap(1000, 705)                                      # 点击第10个单位
        # Core.PyTap(21, 366)

    def Fight(self):
        print(Core(times = self.times).GetScreen())
        Core(times = self.times).PyTap(70, 700, 0.5, 0.5)
        print('[%d][%s]:成功在 70 700 点击进攻图标' %(self.times, time.strftime('%H:%M:%S', time.localtime())))                                  # 点击进攻 
        Core(times = self.times).PyTap(976, 500, 0.5, 0.5)                                 # 点击立即寻找
        print('[%d][%s]:成功在 976 500 点击立即寻找图标' %(self.times, time.strftime('%H:%M:%S', time.localtime()))) 
        while Core(times = self.times).Exist(icon_name = '开战倒计时', conf = 0.6)[0] is not True:                     # 判断是否寻敌完成
            Core(times = self.times).GetScreen()
        self.xiabin()
        nhnw2 = True
        while Core(times = self.times).Exist(icon_name = '距离战斗结束还有', conf = 0.6):  #下兵完成，循环判断是否进入结束战斗
            Core(times = self.times).GetScreen()
        while Core(times = self.times).NotExist(icon_name = '回营'):
            Core(times = self.times).GetScreen()         #结束战斗，循环判断是否进入二阶段还是战斗
            if nhnw2:
                if Core(times = self.times).Exist(icon_name = '开战倒计时', conf = 0.6):  #判断是否存在来判断是否进入二阶段
                    self.xiabin()
                    nhnw2 = False
        Core(times = self.times).PyTap(645, 645) #点击回营
        while Core(times = self.times).NotExist(icon_name = '移动', conf = 0.8):
            Core(times = self.times).GetScreen()
            if Core(times = self.times).Exist(icon_name = '确定', conf = 0.7):   # 用于判断是否有胜利之星奖励
                Core(times = self.times).PyTap(600, 600, 2, 3)                                  # 判断是否回城完成
        Core(times = self.times).PySwipe(976, 500, 976, 700, 500)
        Core(times = self.times).PyTap(926, 108, 0.2, 0.2) #点击圣水车
        Core(times = self.times).PyTap(965, 655, 0.1, 0.1) 
        Core(times = self.times).PyTap(1110, 75, 0.1, 0.1)


# class AutoHomeTown():
#     def xiabin():
#         Core.PySwipe(0, 0, 0.5, 0.5)

#     def fight(self):
#         while Core.notexist('移动'):
#             Core.GetScreen()
#         Core.PyTap(70, 700, 0.5, 0.5)
#         Core.PyTap(917, 493, 0.5, 0.5)
#         while Core.exist('结束战斗'):
#             Core.GetScreen()

if __name__ == '__main__':
    n = 1
    N = 100
    choise = input('1.自动家乡作战\n2.自动夜世界作战\n3.退出\n')
    N = input('请输入循环次数(default = 100)\n')
    if N == '':
        N = 100
    N = int(N)

    # get_screen_thread = Thread(target=Core.LoopGetScreen,args=(),daemon=True)
    # get_screen_thread.start()

    if choise == '1':
        while n <= N:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            # AutoHomeTown(n).fight()
            exit()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
    elif choise == '2':
        while n <= N:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            AutoNightWorld(n).Fight()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
    elif choise == '3':
        print('已退出\n')
        exit()
    else:
        print(type(n))
