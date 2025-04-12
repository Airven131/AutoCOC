import cv2
import time
import uiautomator2 as u2

device = u2.connect("127.0.0.1:5555")

class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


class Core():
    def __init__(
            self,
            times : int | None = 0):
        self.times = times
        pass

    def GetScreen(self):
        time_now = time.strftime('%H:%M:%S', time.localtime())

        # result = device_ppadb.screencap()
        # resule_trans = np.frombuffer(result, np.uint8)
        # image = cv2.imdecode(resule_trans, cv2.IMREAD_COLOR)
        image = device.screenshot(format='opencv')

        print('[%d][%s]:get the screen' %(self.times, time_now))
        time.sleep(1)
        return image

    def GetIconPosition(self,
                        icon_name : str,
                        conf : float | None = 0.9):
        if icon_name is None:
            raise NameError
        icon = cv2.imread('./icon/' + icon_name + '.png', cv2.IMREAD_COLOR)
        image = self.GetScreen()
        icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 匹配图片和图标
        resule = cv2.matchTemplate(image_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resule)

        # 丢弃掉匹配值较低的position
        if max_val < conf:
            return Position(-1, -1)
        
        # 获取图标左上角的坐标
        x, y = max_loc

        return Position(x, y)

    def Exist(self,
              icon_name : str | None,
              conf : float | None = 0.9):
        if icon_name is None:
            icon_name = self._icon_name
        time_now = time.strftime('%H:%M:%S', time.localtime())
        pos = self.GetIconPosition(icon_name, conf)
        x = pos.x
        y = pos.y
        if x == -1 :
            print('[%d][%s]:The icon %s is not exist' %(self.times, time_now, icon_name))
            return False
        else:
            print('[%d][%s]:Successful to find the icon at %s %d %d' %(self.times, time_now, icon_name, x, y))
            return True
        
    def NotExist(self,
                 icon_name = None,
                 conf : float | None = ''):
        if icon_name is None:
            icon_name = self._icon_name
        time_now = time.strftime('%H:%M:%S', time.localtime())
        pos = self.GetIconPosition(icon_name, conf)
        x = pos.x
        y = pos.y
        if x == -1 :
            print('[%d][%s]:The icon %s is not exist' %(self.times, time_now, icon_name))
            return True
        else:
            print('[%d][%s]:Successful to find the icon at %s %d %d' %(self.times, time_now, icon_name, x, y))
            return False

    def PyTap(self,
              x : int,
              y : int,
              before_time : float | None = 2.0,
              after_time :float | None = 2.0):
        time.sleep(before_time)
        time_now = time.strftime('%H:%M:%S', time.localtime())
        device.click(x, y)
        # device_ppadb.shell('input tap %d %d' %(x, y))
        print('[%d][%s]:Successful tap %d %d' %(self.times, time_now, x, y))
        time.sleep(after_time)

    def PySwipe(self,
                from_x : int,
                from_y : int,
                to_x : int,
                to_y : int,
                way_time : float | None = 0.5):
        time_now = time.strftime('%H:%M:%S', time.localtime())
        device.swipe(from_x, from_y, to_x, to_y, way_time)
        # device_ppadb.shell('input swipe %d %d %d %d %d' %(from_x, from_y, to_x, to_y, int(way_time)))
        print('[%d][%s]:Successful swip from %d %d to %d %d' %(self.times, time_now, from_x, from_y, to_x, to_y))


class AutoNightWorld():
    def __init__(self, times = 0):
        self.times = times

    def xiabin(self):
        Core(times = self.times).PyTap(197, 980, 0.05, 0.10)       # 点击第0个单位
        Core(times = self.times).PyTap(280, 560, 0.05, 0.10)
        Core(times = self.times).PyTap(363, 980, 0.05, 0.05)       # 点击第1个单位
        Core(times = self.times).PyTap(955, 65, 0.05, 0.05)
        Core(times = self.times).PyTap(519, 970, 0.05, 0.05)       # 点击第2个单位
        Core(times = self.times).PyTap(1625, 560, 0.05, 0.05)
        Core(times = self.times).PyTap(665, 965, 0.05, 0.05)       # 点击第3个单位
        Core(times = self.times).PyTap(600, 800, 0.05, 0.05)
        Core(times = self.times).PyTap(824, 971, 0.05, 0.05)       # 点击第4个单位
        Core(times = self.times).PyTap(400, 900, 0.05, 0.05)
        Core(times = self.times).PyTap(979, 963, 0.05, 0.05)       # 点击第5个单位
        Core(times = self.times).PyTap(660, 280, 0.05, 0.05)
        Core(times = self.times).PyTap(1127, 962, 0.05, 0.05)      # 点击第6个单位
        Core(times = self.times).PyTap(1300, 300, 0.05, 0.05)
        Core(times = self.times).PyTap(1282, 964, 0.05, 0.05)      # 点击第7个单位
        Core(times = self.times).PyTap(1305, 800, 0.05, 0.05)
        Core(times = self.times).PyTap(1432, 969, 0.05, 0.05)      # 点击第8个单位
        Core(times = self.times).PyTap(610, 805, 0.05, 0.05)
        Core(times = self.times).PyTap(280, 560, 0.05, 0.10)
        Core(times = self.times).PyTap(955, 65, 0.05, 0.05)
        Core(times = self.times).PyTap(1625, 560, 0.05, 0.05)

    def Fight(self):
        Core(times = self.times).GetScreen()
        Core(times = self.times).PyTap(125, 1000, 0.5, 0.5)                                                     # 点击进攻 
        Core(times = self.times).PyTap(1450, 720, 0.5, 0.5)                                                     # 点击立即寻找
        while Core(times = self.times).NotExist(icon_name = 'time_left_before_attack', conf = 0.6):             # 判断是否寻敌完成
            pass
        self.xiabin()
        #下兵完成
        is_attack_part_2 = False
        while Core(times = self.times).Exist(icon_name = 'time_left_before_finish_attack', conf = 0.6):         #循环判断是否进入结束战斗
            pass
        #第一阶段战斗结束
        while Core(times = self.times).NotExist(icon_name = 'back_home', conf = 0.9):                           #如果只有一个阶段则直接推出
            #循环判断是否进入二阶段还是战斗
            if not is_attack_part_2:
                if Core(times = self.times).Exist(icon_name = 'time_left_before_finish_attack_2', conf = 0.6):  #判断是否存在来判断是否进入二阶段
                    self.xiabin()
                    is_attack_part_2 = True
        Core(times = self.times).PyTap(972, 918)                                    #点击回营
        while Core(times = self.times).NotExist(icon_name = 'move', conf = 0.8):
            Core(times = self.times).GetScreen()
            if Core(times = self.times).Exist(icon_name = 'night_world_daily_reward', conf = 0.7):   # 用于判断是否有胜利之星奖励
                Core(times = self.times).PyTap(966, 846, 2, 3)                      # 判断是否回城完成
        Core(times = self.times).PySwipe(976, 500, 976, 700, 0.5)
        Core(times = self.times).PyTap(1376, 91, 0.2, 0.2)                          #点击圣水车
        Core(times = self.times).PyTap(1420, 927, 0.1, 0.1) 
        Core(times = self.times).PyTap(1610, 105, 0.1, 0.1)


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
    try:
        N = int(input('请输入循环次数(default = 100)\n'))
    except ValueError:
        pass
    # print('n的类型是%', type(N), '值是', N)

    if choise == '1':
        print(time.strftime('[%H:%M:%S]:'), '暂时无法使用，按任意键推出')
        input()
        exit()
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
    elif choise == '4':
        while not Core().Exist('attack'):
            pass
    else:
        print(type(n))
