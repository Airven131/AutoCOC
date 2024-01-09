import os
import cv2
import time
# from math import sqrt
# from math import pow
# from random import randint
from PIL import Image
import numpy as np

TCN = 10

class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    #图片裁切，只选取左上角1265*772的有效区域        
def image_cut(image_full):
    image = image_full[0:772, 0:1265].copy()
    return image

    #图片裁切，只选取左上角1265*772的有效区域        
def image_cut_ma(image_full):
    image = image_full[0:950, 0:1520].copy()
    return image

def get_icon_position(icon_name, randtap = True, conf = 0.9):
    # time_now = time.strftime('%H:%M:%S', time.localtime())

    # 读取图片和图标的灰度图
    icon = cv2.imread('icon/' + icon_name + '.png', cv2.IMREAD_GRAYSCALE)
    image = cv2.imread('/home/airven/.zhuoyi/common/移动数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)

    #图片裁切，只选取左上角1265*772的有效区域
    image = image_cut(image)

    # 匹配图片和图标
    resule = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)
    _, _, min_loc, max_loc = cv2.minMaxLoc(resule)

    # 丢弃掉匹配值较低的pisition
    if _ < conf:
        return Position(-1, -1)
    
    # 获取图标左上角的坐标
    x, y = max_loc

    return Position(x, y)

def get_icon_position_ma(icon_name, randtap = True, conf = 0.9):
    time_now = time.strftime('%H:%M:%S', time.localtime())

    # 读取图片和图标的灰度图
    icon = cv2.imread('icon/' + icon_name + '.png', cv2.IMREAD_GRAYSCALE)
    image = cv2.imread('/home/airven/.zhuoyi/common-{6c0bd68b-7b82-44c0-bf59-d0f2eb43e5be}-12/移动x数据/存储卡/screen.png', cv2.IMREAD_GRAYSCALE)

    #图片裁切，只选取左上角1265*772的有效区域
    image = image_cut(image)

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
    
def exist_ma(icon_file, conf_exist = 0.9):
    time_now = time.strftime('%H:%M:%S', time.localtime())
    x = get_icon_position_ma(icon_file, conf = conf_exist).x
    y = get_icon_position_ma(icon_file, conf = conf_exist).y
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
    
def notexist_ma(icon_file, conf_exist = 0.9):
    time_now = time.strftime('%H:%M:%S', time.localtime())
    x = get_icon_position_ma(icon_file, conf = conf_exist).x
    y = get_icon_position_ma(icon_file, conf = conf_exist).y
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