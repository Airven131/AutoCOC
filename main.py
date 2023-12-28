import os
import cv2
import time
from math import sqrt
from math import pow
from random import randint

TCN = 10

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# class Army:
#     def __init__(self) -> None:
#         pass

def get_icon_position(icon_name, randtap = 1, conf = 0.9):
    time_now = time.strftime('%H:%M:%S', time.localtime())

    # 读取图片和图标
    icon = cv2.imread('icon/' + icon_name + 'png')
    image = cv2.imread('screen.png')

    # 匹配图片和图标
    resule = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(resule)

    # 丢弃掉匹配值较低的pisition
    if _ < conf:
        print('[%s]:Fail to find the icon: %s' %(time_now, icon_name))
        return None
    
    # 获取图标左上角的坐标
    x, y = max_loc
    print('[%s]:Successful to find the icon at [%d] [%d] and tap it' %(time_now, x, y))

    # 给点击坐标一些随机偏差
    if randtap == 1:
        x = x + randint(icon.width//3, 2*icon.width//3)
        y = y + randint(icon.height//3, 2*icon.height//3)
    return Position(x, y)

def get_screen():
    time_now = time.strftime('%H:%M:%S', time.localtime())

    os.system(f'adb shell screencap /sdcard/screen.png')
    os.system(f'adh pull /sdcard/screen.png screen.png')

    print('[%s]:get the screen' %(time_now))
    # time.sleep(3)

def pytap(x, y):
    os.system('adb shell input tap %d %d' %(x, y))

def pyswipe(from_x, from_y, to_x, to_y, time):
    if time is None:
        length = sqrt(pow(from_x - to_x), 2) + pow((from_y - to_y),2)
        speed = randint(1500, 2000)
        time = length/speed*1000
    os.system('adb sehll input swipe %d %d %d %d %d' %(from_x, from_y, to_x, to_y, int(time)))

def icontap(icon_file):
    x = get_icon_position(icon_name = icon_file).x
    y = get_icon_position(icon_name = icon_file).y
    os.system('adb shell input tap %d %d' %(x, y))

def auto_night_world():
    for i in range(TCN):
        # pytap(get_icon_position('attack.png').x, get_icon_position('attack.png').y)
        icontap('attack')
        time.sleep(3)
        pytap(150, 910) # 选择机器人
        time.sleep(3)
        pytap(0, 0) # 下机器人
        time.sleep(3)

        # 下兵
        while get_icon_position('dragon_baby') is not None:
            get_screen()
            icontap('dragon_baby')
            pytap(0, 0)
            time.sleep(3)

        # 结束战斗
        while get_icon_position('back_home') is not None:
            pytap(360, 360)
            time.sleep(5)
