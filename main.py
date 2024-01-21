# from core import *
import os
import cv2
import time
import easyocr
import numpy as np
from threading import Thread
from PIL import Image



class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

class core():
    def image_cut(image_full):
        image = image_full[0:772, 0:1265].copy()
        return image

        #图片裁切，只选取左上角1265*772的有效区域        
    def image_cut_ma(image_full):
        image = image_full[0:950, 0:1520].copy()
        return image

    def get_icon_position(self, icon_name, randtap = True, conf = 0.9):
        # time_now = time.strftime('%H:%M:%S', time.localtime())

        # 读取图片和图标的灰度图
        icon = cv2.imread('icon/' + icon_name + '.png', cv2.IMREAD_GRAYSCALE)
        image = cv2.imread('/home/airven/.zhuoyi/common/移动数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)

        #图片裁切，只选取左上角1265*772的有效区域
        image = self.image_cut(image)

        # 匹配图片和图标
        resule = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)
        _, _, min_loc, max_loc = cv2.minMaxLoc(resule)

        # 丢弃掉匹配值较低的pisition
        if _ < conf:
            return Position(-1, -1)
        
        # 获取图标左上角的坐标
        x, y = max_loc

        return Position(x, y)

    def get_icon_position_ma(self, icon_name, randtap = True, conf = 0.9):
        time_now = time.strftime('%H:%M:%S', time.localtime())

        # 读取图片和图标的灰度图
        icon = cv2.imread('icon/' + icon_name + '.png', cv2.IMREAD_GRAYSCALE)
        image = cv2.imread('/home/airven/.zhuoyi/common-{6c0bd68b-7b82-44c0-bf59-d0f2eb43e5be}-12/移动x数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)

        #图片裁切，只选取左上角1265*772的有效区域
        image = self.image_cut(image)

        # 匹配图片和图标
        resule = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)
        _, _, min_loc, max_loc = cv2.minMaxLoc(resule)

        # 丢弃掉匹配值较低的pisition
        if _ < conf:
            return Position(-1, -1)
        
        # 获取图标左上角的坐标
        x, y = max_loc

        return Position(x, y)

    def get_screen():
        time_now = time.strftime('%H:%M:%S', time.localtime())
        os.system(f'adb shell screencap /sdcard/screen.png')
        print('[%s]:get the screen' %(time_now))
        time.sleep(1)

    def loop_get_screen(self):
        while True:
            self.get_screen()

    def exist(self, icon_file, conf_exist = 0.9):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.get_icon_position(icon_file, conf = conf_exist).x
        y = self.get_icon_position(icon_file, conf = conf_exist).y
        if x == -1 :
            print('[%s]:The icon %s is not exist' %(time_now, icon_file))
            return False
        else:
            print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_file, x, y))
            return True
        
    def exist_ma(self, icon_file, conf_exist = 0.9):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.get_icon_position_ma(icon_file, conf = conf_exist).x
        y = self.get_icon_position_ma(icon_file, conf = conf_exist).y
        if x == -1 :
            print('[%s]:The icon %s is not exist' %(time_now, icon_file))
            return False
        else:
            print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_file, x, y))
            return True
        
    def notexist(self, icon_file, conf_exist = 0.9):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.get_icon_position(icon_file, conf = conf_exist).x
        y = self.get_icon_position(icon_file, conf = conf_exist).y
        if x == -1 :
            print('[%s]:The icon %s is not exist' %(time_now, icon_file))
            return True
        else:
            print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_file, x, y))
            return False
        
    def notexist_ma(self, icon_file, conf_exist = 0.9):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        x = self.get_icon_position_ma(icon_file, conf = conf_exist).x
        y = self.get_icon_position_ma(icon_file, conf = conf_exist).y
        if x == -1 :
            print('[%s]:The icon %s is not exist' %(time_now, icon_file))
            return True
        else:
            print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_file, x, y))
            return False

    def pytap(x, y, before_time = 2.0, after_time = 2.0):
        time.sleep(before_time)
        time_now = time.strftime('%H:%M:%S', time.localtime())
        os.system('adb shell input tap %d %d' %(x, y))
        print('[%s]:Successful tap %d %d' %(time_now, x, y))
        time.sleep(after_time)

    def pyswipe(from_x, from_y, to_x, to_y, way_time):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        # if time is None:
        #     length = sqrt(pow(from_x - to_x), 2) + pow((from_y - to_y),2)
        #     speed = randint(1500, 2000)
        #     time = length/speed*1000
        os.system('adb shell input swipe %d %d %d %d %d' %(from_x, from_y, to_x, to_y, int(way_time)))
        print('[%s]:Successful swip from %d %d to %d %d' %(time_now, from_x, from_y, to_x, to_y))

    # def icontap(icon_file):
    #     icon_position = get_icon_position(icon_name = icon_file)
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
        
    def get_resource(self):
        path = '/home/airven/.zhuoyi/common/移动数据/存储卡/screen.png'

        result = []
        reader = easyocr.Reader(['en'])
        resule_all = reader.readtext(path, paragraph="False")
        n = 0
        for n in resule_all:
            if 0 < resule_all[n][0][0][0] < 1 and 0 < resule_all[n][0][0][1] < 1:
                result[0] = resule_all[n][1]
            if 0 < resule_all[n][0][0][0] < 1 and 0 < resule_all[n][0][0][1] < 1:
                result[1] = resule_all[n][1]
            if 0 < resule_all[n][0][0][0] < 1 and 0 < resule_all[n][0][0][1] < 1:
                result[2] = resule_all[n][1]


class AutoNightWorld():
    def xiabin(self):
        core.pytap(180, 705, 0.05, 0.05)                                         # 点击第1个单位
        core.pytap(21, 366, 0.05, 0.05)
        core.pytap(290, 705, 0.05, 0.05)                                         # 点击第2个单位
        core.pytap(109, 275, 0.05, 0.05)
        core.pytap(370, 705, 0.05, 0.05)                                         # 点击第3个单位
        core.pytap(365, 87, 0.05, 0.05)
        core.pytap(460, 705, 0.05, 0.05)                                         # 点击第4个单位
        core.pytap(843, 56, 0.05, 0.05)
        core.pytap(550, 705, 0.05, 0.05)                                         # 点击第5个单位
        core.pytap(1110, 250, 0.05, 0.05)
        core.pytap(640, 705, 0.05, 0.05)                                         # 点击第6个单位
        core.pytap(1173, 450, 0.05, 0.05)
        core.pytap(730, 705, 0.05, 0.05)                                         # 点击第7个单位
        core.pytap(1000, 610, 0.05, 0.05)
        core.pytap(820, 705, 0.05, 0.05)                                         # 点击第8个单位
        core.pytap(310, 610, 0.05, 0.05)
        # core.pytap(910, 705)                                       # 点击第9个单位
        # core.pytap(263, 573)
        # core.pytap(1000, 705)                                      # 点击第10个单位
        # core.pytap(21, 366)

    def xiabin_ma(self):
        core.pytap(200, 880, 0.2, 0.2)                                         # 点击第1个单位
        core.pytap(124, 293, 0.2, 0.2)
        core.pytap(320, 880, 0.2, 0.2)                                         # 点击第2个单位
        core.pytap(511, 14, 0.2, 0.2)
        core.pytap(430, 880, 0.2, 0.2)                                         # 点击第3个单位
        core.pytap(1055, 22, 0.2, 0.2)
        core.pytap(540, 705, 0.2, 0.2)                                         # 点击第4个单位
        core.pytap(1344, 239, 0.2, 0.2)
        core.pytap(650, 705, 0.2, 0.2)                                         # 点击第5个单位
        core.pytap(1110, 250, 0.2, 0.2)
        core.pytap(760, 705, 0.2, 0.2)                                         # 点击第6个单位
        core.pytap(1411, 546, 0.2, 0.2)
        core.pytap(870, 705, 0.2, 0.2)                                         # 点击第7个单位
        core.pytap(1061, 781, 0.2, 0.2)
        core.pytap(980, 705, 0.2, 0.2)                                         # 点击第8个单位
        core.pytap(403, 754, 0.2, 0.2)
        # core.pytap(1090, 705, 0.2, 0.2)                                                  # 点击第9个单位
        # core.pytap(263, 573, 0.2, 0.2)
        # core.pytap(1200, 705, 0.2, 0.2)                                                  # 点击第10个单位
        # core.pytap(21, 366, 0.2, 0.2)

    def fight(self):
        core.pytap(70, 700, 0.5, 0.5)                                  # 点击进攻 
        core.pytap(976, 500, 0.5, 0.5)                                 # 点击立即寻找
        while core.notexist('开战倒计时', conf_exist = 0.6):                     # 判断是否寻敌完成
            time.sleep(1)
        self.xiabin()
        not_defeat_night_world_2 = True
        while core.exist('距离战斗结束还有', conf_exist = 0.6):  #下兵完成，循环判断是否进入结束战斗
            time.sleep(1)
        while core.notexist('回营'):
            time.sleep(1)         #结束战斗，循环判断是否进入二阶段还是战斗
            if not_defeat_night_world_2:
                if core.exist('开战倒计时', conf_exist = 0.6):  #判断是否存在来判断是否进入二阶段
                    self.xiabin()
                    not_defeat_night_world_2 = False
        core.pytap(645, 645) #点击回营
        while core.notexist('移动', conf_exist = 0.8):
            time.sleep(1)
            if core.exist('确定', conf_exist = 0.7):   # 用于判断是否有胜利之星奖励
                core.pytap(600, 600, 2, 3)                                  # 判断是否回城完成
        core.pyswipe(976, 500, 976, 700, 500)
        core.pytap(875, 209, 0.2, 0.2) #点击圣水车
        core.pytap(965, 655, 0.1, 0.1) 
        core.pytap(1110, 75, 0.1, 0.1)

    def fight_ma(self):
        core.pytap(90, 865, 0.5, 0.5)                                  # 点击进攻 
        core.pytap(1150, 620, 0.5, 0.5)                                 # 点击立即寻找
        while core.notexist('开战倒计时_马', conf_exist = 0.6):                     # 判断是否寻敌完成
            core.get_screen()
            img = cv2.imread('/home/airven/.zhuoyi/common-{6c0bd68b-7b82-44c0-bf59-d0f2eb43e5be}-12/移动x数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)
            image = core.image_cut_ma(img)
            cv2.imshow('screen', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        self.xiabin_ma()
        not_defeat_night_world_2 = True
        while core.exist('距离战斗结束还有_马', conf_exist= 0.8):  #下兵完成，循环判断是否进入结束战斗
            core.get_screen()
        while core.notexist('回营_马'):
            core.get_screen()         #结束战斗，循环判断是否进入二阶段还是战斗
            if not_defeat_night_world_2:
                if core.exist('开战倒计时_马', conf_exist = 0.6):  #通过判断奥仔岗哨按钮是否存在来判断是否进入二阶段
                    self.xiabin_ma()
                    not_defeat_night_world_2 = False
        core.pytap(766, 800)
        while core.notexist('进攻_马', conf_exist = 0.6):
            core.get_screen()
            if core.exist('确定'):   # 用于判断是否有胜利之星奖励
                core.pytap(600, 600)                                  # 判断是否回城完成
        time.sleep(3)
        core.pyswipe(976, 500, 976, 750, 500)
        core.pytap(875, 209, 0.2, 0.2) #点击圣水车
        core.pytap(965, 655, 0.2, 0.2) 
        core.pytap(1110, 75, 0.2, 0.2)

class AutoHomeTown():
    def xiabin():
        core.pyswipe(0, 0, 0.5, 0.5)

    def fight(self):
        while core.notexist('移动'):
            core.get_screen()
        core.pytap(70, 700, 0.5, 0.5)
        core.pytap(917, 493, 0.5, 0.5)
        while core.exist('结束战斗'):
            core.get_screen()

if __name__ == '__main__':
    n = 1
    choise = input('1.自动家乡作战\n2.自动夜世界作战\n3.退出\n')

    get_screen_thread = Thread(target=core.loop_get_screen,
                               args=(),
                               daemon=True)
    get_screen_thread.start

    if choise == 1:
        while n <= 100:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            AutoNightWorld.fight()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
        get_screen_thread.a
    elif choise == 2:
        while n <= 100:
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:开始第 %d 轮战斗\033[0m" %(time_now,n))
            AutoHomeTown.fight()
            time_now = time.strftime('%H:%M:%S', time.localtime())
            print("\033[0;30;47m[%s]:第 %d 轮战斗结束\033[0m" %(time_now, n))
            n += 1
    elif choise == 3:
        print('已退出\n')
        exit()
