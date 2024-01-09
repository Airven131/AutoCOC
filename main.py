import os
import cv2
import time
from math import sqrt
from math import pow
from random import randint
from PIL import Image

TCN = 10

class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

# class Army:
#     def __init__(self) -> None:
#         pass

def get_icon_position(icon_name, randtap = True, conf = 0.9):
    time_now = time.strftime('%H:%M:%S', time.localtime())

    # 读取图片和图标
    icon = cv2.imread('icon/' + icon_name + '.png')
    image = cv2.imread('/home/airven/.zhuoyi/common/移动数据/存储卡/screen.png')

    # 匹配图片和图标
    resule = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)
    _, _, s, max_loc = cv2.minMaxLoc(resule)

    # 丢弃掉匹配值较低的pisition
    if _ < conf:
        # print('[%s]:Fail to find the icon: %s' %(time_now, icon_name))
        return Position(-1, -1)
    
    # 获取图标左上角的坐标
    x, y = max_loc
    # print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_name, x, y))

    # 给点击坐标一些随机偏差
    # if randtap == 1:
    #     x = x + randint(icon.width//3, 2*icon.width//3)
    #     y = y + randint(icon.height//3, 2*icon.height//3)

    return Position(x, y)

def get_screen():
    time_now = time.strftime('%H:%M:%S', time.localtime())

    os.system(f'adb shell screencap /sdcard/screen.png')
    # time.sleep(3)
    # os.system(f'adb pull /sdcard/screen.png screen.png')

    print('[%s]:get the screen' %(time_now))
    time.sleep(1)

def exist(icon_file, conf_exist = 0.9):
    time_now = time.strftime('%H:%M:%S', time.localtime())
    x = get_icon_position(icon_file, conf = conf_exist).x
    y = get_icon_position(icon_file, conf = conf_exist).y
    if x == -1 :
        print('[%s]:The icon %s is not exist' %(time_now, icon_file))
        return False
    else:
        print('[%s]:Successful to find the icon at %s %d %d' %(time_now, icon_file, x, y))
        return True
    
def notexist(icon_file, conf_exist = 0.9):
    time_now = time.strftime('%H:%M:%S', time.localtime())
    x = get_icon_position(icon_file, conf = conf_exist).x
    y = get_icon_position(icon_file, conf = conf_exist).y
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

def pyswipe(from_x, from_y, to_x, to_y, time):
    # if time is None:
    #     length = sqrt(pow(from_x - to_x), 2) + pow((from_y - to_y),2)
    #     speed = randint(1500, 2000)
    #     time = length/speed*1000
    os.system('adb shell input swipe %d %d %d %d %d' %(from_x, from_y, to_x, to_y, int(time)))

def icontap(icon_file):
    icon_position = get_icon_position(icon_name = icon_file)
    x = icon_position.x
    y = icon_position.y
    os.system('adb shell input tap %d %d' %(x, y))

def night_world_xiabin():
    pytap(180, 705, 0.2, 0.2)                                         # 点击第1个单位
    pytap(21, 366, 0.2, 0.2)
    pytap(290, 705, 0.2, 0.2)                                         # 点击第2个单位
    pytap(109, 275, 0.2, 0.2)
    pytap(370, 705, 0.2, 0.2)                                         # 点击第3个单位
    pytap(365, 87, 0.2, 0.2)
    pytap(460, 705, 0.2, 0.2)                                         # 点击第4个单位
    pytap(843, 56, 0.2, 0.2)
    pytap(550, 705, 0.2, 0.2)                                         # 点击第5个单位
    pytap(1110, 250, 0.2, 0.2)
    pytap(640, 705, 0.2, 0.2)                                         # 点击第6个单位
    pytap(1173, 450, 0.2, 0.2)
    pytap(730, 705, 0.2, 0.2)                                         # 点击第7个单位
    pytap(833, 699, 0.2, 0.2)
    # pytap(820, 705)                                       # 点击第8个单位
    # pytap(482, 704)
    # pytap(910, 705)                                       # 点击第9个单位
    # pytap(263, 573)
    # pytap(1000, 705)                                      # 点击第10个单位
    # pytap(21, 366)

def auto_night_world():
    get_screen()
    pytap(70, 700, 0.5, 0.5)                                  # 点击进攻 
    pytap(976, 500, 0.5, 0.5)                                 # 点击立即寻找
    while notexist('开战倒计时', conf_exist = 0.6):                     # 判断是否寻敌完成
        get_screen()
    night_world_xiabin()
    not_defeat_night_world_2 = True
    while notexist ('回营'):  #下兵完成，循环判断是否进入二阶段或者结束战斗
        get_screen()
        time.sleep(3)
        if not_defeat_night_world_2:
            if exist('开战倒计时', conf_exist = 0.6):  #通过判断奥仔岗哨按钮是否存在来判断是否进入二阶段
                night_world_xiabin()
                not_defeat_night_world_2 = False
    pytap(645, 645)
    while notexist('进攻'):
        get_screen()
        if exist('确定'):
            pytap(600, 600)                                  # 判断是否回城完成
    pyswipe(976, 500, 976, 700, 500)
    pytap(875, 209, 0.2, 0.2) #点击圣水车
    pytap(965, 655, 0.2, 0.2) 
    pytap(1110, 75, 0.2, 0.2)
   
   
if __name__ == '__main__':
    n = 1
    while n <= 100:
        time_now = time.strftime('%H:%M:%S', time.localtime())
        print('开始第 %d 轮战斗' %(n))
        auto_night_world()
        time_now = time.strftime('%H:%M:%S', time.localtime())
        print('第 %d 轮战斗结束' %(n))
        n += 1
    # pytap(875, 209) #点击圣水车
    # pytap(965, 655) 
    # pytap(1110, 75)
    # pyswipe(976, 500, 976, 700, 500)