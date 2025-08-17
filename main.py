import cv2
import time
import uiautomator2 as u2
import yaml
import logging
import re
from typing import Optional
from inputimeout import inputimeout, TimeoutOccurred
from paddleocr import PaddleOCR
from windows_toasts import Toast, WindowsToaster
from multiprocessing import Process, Queue



with open('config.yml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

dev_addr = config['device']['host'] + ':' + config['device']['port']
device = u2.connect(dev_addr)

logging.disable(logging.DEBUG)
ocr : PaddleOCR = None
config = None



class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)



class Resource:
    def __init__(self,
                 gold : int | None = 0,
                 elixir: int | None = 0,
                 darkelixir: int | None = 0):
        self.gold = gold
        self.elixir = elixir
        self.darkelixir = darkelixir

        try:
            goldweight = config['gameconfig']['godlweight']
        except:
            goldweight = 1

        try:
            elixirweight = config['gameconfig']['elixirweight']
        except:
            elixirweight = 1
        
        try:
            darkelixirweight = config['gameconfig']['darkelixirweight']
        except:
            darkelixirweight = 150

        self.totle = gold * goldweight + elixir * elixirweight + darkelixir * darkelixirweight



class Core():
    def __init__(self,
            times : int | None = 0,
            printLogFormat : int | None = 0,
            log_queue: Optional[Queue] = None):
        self.times = times
        self._printLogFormat = printLogFormat
        self.log_queue = log_queue
        pass

    def stdout(self, 
            message : str,
            printLogFormat : int,
            log_queue : Optional[Queue] | None = None):
        if printLogFormat is None:
            printLogFormat = self._printLogFormat
        if printLogFormat == 0:
            pass
        elif printLogFormat == 1:
            print(message)
        elif printLogFormat == 2 and log_queue:
            log_queue.put(message)
        pass

    def OcrLoad(self):
        global ocr
        ocr = PaddleOCR(use_angle_cls=True, lang='en', ppocrdebug=False)
        

    def GetScreen(self, printLogFormat : int | None = 0):

        image = device.screenshot(format='opencv')
        message = '[%d][%s]:get the screen' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
        self.stdout(message, printLogFormat, self.log_queue)
        time.sleep(1)
        return image


    def GetIconPosition(self,
                        iconName : str,
                        conf : float | None = 0.9,
                        printLogFormat : int | None = 0):
        if iconName is None:
            raise NameError
        icon = cv2.imread('./icon/' + iconName + '.png', cv2.IMREAD_COLOR)
        image = device.screenshot(format='opencv')
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


    def GetRes(self,
               printLogFormat : int | None = 0) -> Resource:
        message = '[%d][%s]:start get resource' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
        self.stdout(message, printLogFormat, self.log_queue)
        image = device.screenshot(format='opencv')

        goldImg = image[150:190, 90:300]
        elixirImg = image[206:246, 90:300]
        darkelixirImg = image[262:302, 90:300]
        
        # cv2.imshow('screen', image)
        # cv2.imshow('gold', goldImg)
        # cv2.imshow('elixir', elixirImg)
        # cv2.imshow('dark', darkelixirImg)
        # time.sleep(3)
        # cv2.destroyAllWindows()
        try:
            gold = ocr.ocr(goldImg, cls=True)[0][0][-1][0]
            elixir = ocr.ocr(elixirImg, cls=True)[0][0][-1][0]
            darkelixir = ocr.ocr(darkelixirImg, cls=True)[0][0][-1][0]
        except TypeError:
            return Resource(0, 0, 0)

        # print('ggold', gold)
        # print('elixirr', elixir)
        # print('darkelixirr', darkelixir)
        try:
            gold_num = int(gold)
        except ValueError:
            digital_match = r'\d+'
            digital = re.findall(digital_match, gold)
            gold_num = ''
            for d in digital:
                gold_num += d
            gold_num = int(gold_num)

        try:
            elixir_num = int(elixir)
        except ValueError:
            digital_match = r'\d+'
            digital = re.findall(digital_match, elixir)
            elixir_num = ''
            for d in digital:
                elixir_num += d
            elixir_num = int(elixir_num)

        try:
            darkelixir_num = int(darkelixir)
        except ValueError:
            digital_match = r'\d+'
            digital = re.findall(digital_match, darkelixir)
            darkelixir_num = ''
            for d in digital:
                darkelixir_num += d
            darkelixir_num = int(darkelixir_num)

        # message = '[%d][%s]:success find gold [%d], elixir [%d], darkelixir [%d]' %(self.times, time.strftime('%H:%M:%S', time.localtime()), gold, elixir, darkelixir)
        # self.stdout(message, printLogFormat)
        return Resource(gold_num, elixir_num, darkelixir_num)


    def Exist(self,
              iconName : str,
              conf : float | None = 0.9,
              printLogFormat : int | None = 0) -> bool:
        pos = self.GetIconPosition(iconName, conf, printLogFormat)
        x = pos.x
        y = pos.y
        if x == -1 :
            message = '[%d][%s]:The icon %s is not exist' %(self.times, time.strftime('%H:%M:%S', time.localtime()), iconName)
            self.stdout(message, printLogFormat, self.log_queue)
            return False
        else:
            message = '[%d][%s]:Successful to find the icon at %s %d %d' %(self.times, time.strftime('%H:%M:%S', time.localtime()), iconName, x, y)
            self.stdout(message, printLogFormat, self.log_queue)
            return True
        

    def NotExist(self,
                 iconName : str,
                 conf : float | None = 0.9,
                 printLogFormat : int | None = 0) -> bool:
        pos = self.GetIconPosition(iconName, conf, printLogFormat)
        x = pos.x
        y = pos.y
        if x == -1 :
            message = '[%d][%s]:The icon %s is not exist' %(self.times, time.strftime('%H:%M:%S', time.localtime()), iconName)
            self.stdout(message, printLogFormat, self.log_queue)
            return True
        else:
            message = '[%d][%s]:Successful to find the icon at %s %d %d' %(self.times, time.strftime('%H:%M:%S', time.localtime()), iconName, x, y)
            self.stdout(message, printLogFormat, self.log_queue)
            return False


    def PyTap(self,
              x : int,
              y : int,
              before_time : float | None = 2.0,
              after_time :float | None = 2.0,
              printLogFormat : int | None = 0):
        time.sleep(before_time)
        device.click(x, y)
        message = '[%d][%s]:Successful tap %d %d' %(self.times, time.strftime('%H:%M:%S', time.localtime()), x, y)
        self.stdout(message, printLogFormat, self.log_queue)
        time.sleep(after_time)


    def PySwipe(self,
                from_x : int,
                from_y : int,
                to_x : int,
                to_y : int,
                way_time : float | None = 0.5,
                printLogFormat : int | None = 0):
        device.swipe(from_x, from_y, to_x, to_y, way_time)
        message = '[%d][%s]:Successful swip from %d %d to %d %d' %(self.times, time.strftime('%H:%M:%S', time.localtime()), from_x, from_y, to_x, to_y)
        self.stdout(message, printLogFormat, self.log_queue)


    def Launch(self,
               printLogFormat : int | None = 0):
        cur = device.app_current()
        app = cur['package']
        
        if app != 'com.supercell.clashofclans':
            device.app_start("com.supercell.clashofclans")

        while self.NotExist(iconName = 'message', printLogFormat = 0):
            pass
        message = "\033[0;30;47m[%s]:游戏启动完成\033[0m" %(time.strftime('%H:%M:%S', time.localtime()))
        self.stdout(message, printLogFormat, self.log_queue)



class AutoNightWorld():
    def __init__(self, times : int | None = 0):
        self.times = times


    def xiabin(self):
        Core(times = self.times).PyTap(197, 980, 0.05, 0.10)       # 点击第0个单位
        Core(times = self.times).PyTap(280, 560, 0.05, 0.10)
        Core(times = self.times).PyTap(363, 980, 0.05, 0.05)       # 点击第1个单位
        Core(times = self.times).PyTap(955, 65, 0.05, 0.05)
        Core(times = self.times).PyTap(519, 970, 0.05, 0.05)       # 点击第2个单位
        Core(times = self.times).PyTap(1625, 560, 0.05, 0.05)
        # Core(times = self.times).PyTap(665, 965, 0.05, 0.05)       # 点击第3个单位
        # Core(times = self.times).PyTap(600, 800, 0.05, 0.05)
        # Core(times = self.times).PyTap(824, 971, 0.05, 0.05)       # 点击第4个单位
        # Core(times = self.times).PyTap(400, 800, 0.05, 0.05)
        # Core(times = self.times).PyTap(979, 963, 0.05, 0.05)       # 点击第5个单位
        # Core(times = self.times).PyTap(660, 280, 0.05, 0.05)
        # Core(times = self.times).PyTap(1127, 962, 0.05, 0.05)      # 点击第6个单位
        # Core(times = self.times).PyTap(1300, 300, 0.05, 0.05)
        # Core(times = self.times).PyTap(1282, 964, 0.05, 0.05)      # 点击第7个单位
        # Core(times = self.times).PyTap(1305, 800, 0.05, 0.05)
        # Core(times = self.times).PyTap(1432, 969, 0.05, 0.05)      # 点击第8个单位
        # Core(times = self.times).PyTap(610, 805, 0.05, 0.05)
        Core(times = self.times).PyTap(280, 560, 0.05, 0.10)
        Core(times = self.times).PyTap(955, 65, 0.05, 0.05)
        Core(times = self.times).PyTap(1625, 560, 0.05, 0.05)


    def Fight(self) -> None:
        Core(times = self.times).GetScreen()
        Core(times = self.times).PyTap(125, 1000, 0.5, 0.5)                                                     # 点击进攻
        isAttackCrash = False
        isShowLastAttackInfo = False
        while Core(times = self.times).Exist(iconName = 'time_left_before_last_attck_finished'):               # 判断上一场战斗是否完成
            if not isShowLastAttackInfo:
                print('[%d][%s]:等待上一场战斗结束' %(self.times, time.strftime('%H:%M:%S', time.localtime())))
                isShowLastAttackInfo = True
        Core(times = self.times).PyTap(1450, 720, 0.5, 0.5)                                                     # 点击立即寻找

        print('[%d][%s]:开始寻敌' %(self.times, time.strftime('%H:%M:%S', time.localtime())))
        while Core(times = self.times).NotExist(iconName = 'time_left_before_attack', conf = 0.6):             # 判断是否寻敌完成
            pass
        print('[%d][%s]:寻敌完成' %(self.times, time.strftime('%H:%M:%S', time.localtime())))

        self.xiabin()
        print('[%d][%s]:等待战斗结束' %(self.times, time.strftime('%H:%M:%S', time.localtime())))
        isAttackPart2 = False
        while Core(times = self.times).Exist(iconName = 'time_left_before_finish_attack', conf = 0.6):         #循环判断是否进入结束战斗
            pass
        print('[%d][%s]:第一阶段战斗结束' %(self.times, time.strftime('%H:%M:%S', time.localtime())))

        while Core(times = self.times).NotExist(iconName = 'back_home', conf = 0.9):                           #如果只有一个阶段则直接推出
            #循环判断是否进入二阶段还是战斗
            if not isAttackPart2:
                if Core(times = self.times).Exist(iconName = 'time_left_before_finish_attack_2', conf = 0.6):  #判断是否存在来判断是否进入二阶段
                    time.sleep(1)
                    self.xiabin()
                    print('[%d][%s]:等待第二阶段战斗结束' %(self.times, time.strftime('%H:%M:%S', time.localtime())))
                    isAttackPart2 = True
        print('[%d][%s]:所有战斗结束' %(self.times, time.strftime('%H:%M:%S', time.localtime())))

        Core(times = self.times).PyTap(972, 918)                                    #点击回营
        while Core(times = self.times).NotExist(iconName = 'move', conf = 0.8):
            Core(times = self.times).GetScreen()
            if Core(times = self.times).Exist(iconName = 'night_world_daily_reward', conf = 0.7):   # 用于判断是否有胜利之星奖励
                Core(times = self.times).PyTap(966, 846, 2, 3)                      # 判断是否回城完成
        Core(times = self.times).PySwipe(976, 500, 976, 700, 0.5)
        Core(times = self.times).PyTap(1376, 91, 0.2, 0.2)                          #点击圣水车
        Core(times = self.times).PyTap(1420, 927, 0.1, 0.1) 
        Core(times = self.times).PyTap(1610, 105, 0.1, 0.1)



class AutoHomeTown():
    def __init__(self, times : int | None = 0):
        self.times = times

    def xiabin(self) -> None:
        Core(times = self.times).PyTap(210, 950, 0.5, 0.5, 0)
        for i in range(14):
            Core(times = self.times).PyTap(530-35*i, 30+26*i, 0.05, 0.05, 0)

        Core(times = self.times).PyTap(370, 950, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(470, 130, 0.05, 0.05, 0)
        
        Core(times = self.times).PyTap(530, 950, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(470, 130, 0.05, 0.05, 0)

        Core(times = self.times).PyTap(670, 950, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(470, 130, 0.05, 0.05, 0)

        Core(times = self.times).PyTap(790, 950, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(470, 130, 0.05, 0.05, 0)

        Core(times = self.times).PyTap(910, 950, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(470, 130, 0.05, 0.05, 0)

        #选择地震法术并施放
        Core(times = self.times).PyTap(1130, 950, 0.05, 0.05, 0)

        Core(times = self.times).PyTap(720, 320, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(720, 500, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(720, 680, 0.05, 0.05, 0)

        Core(times = self.times).PyTap(1000, 200, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(1000, 350, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(1000, 500, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(1000, 650, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(1000, 800, 0.05, 0.05, 0)

        Core(times = self.times).PyTap(1280, 320, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(1280, 500, 0.05, 0.05, 0)
        Core(times = self.times).PyTap(1280, 680, 0.05, 0.05, 0)

    def Hand(self,
              pritLogFormat : int | None = 1):
        Core(times = self.times).PyTap(125, 1000, 0.5, 0.5, 0)
        Core(times = self.times).PyTap(1400, 700, 0.5, 0.5, 0)
        while True:
            message = '[%d][%s]:开始寻敌' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
            Core(times = self.times).stdout(message, printLogFormat = pritLogFormat)
            while Core(times = self.times).NotExist(iconName = 'finish_attack', printLogFormat = 0):
                pass
            message = '[%d][%s]:寻敌完成' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
            Core(times = self.times).stdout(message, printLogFormat = pritLogFormat)
            time.sleep(1)
            resource = Core(times = self.times).GetRes()
            if resource.totle < 2500000:
                message = '[%d][%s]:目标资源仅有 %d , 下一个' %(self.times, time.strftime('%H:%M:%S', time.localtime()), resource.totle)
                Core(times = self.times).stdout(message, printLogFormat = pritLogFormat)
                Core(times = self.times).PyTap(1800, 800, 0.5, 0.5, 0)
            else:
                break
        toaster = WindowsToaster('AutoCOC')
        newToasts = Toast()
        newToasts.text_fields = ['成功寻敌']
        toaster.show_toast(newToasts)
        message = '[%d][%s]:等待战斗结束' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
        Core(times = self.times).stdout(message, 1)
        while Core(times = self.times).NotExist(iconName = 'back_home', conf = 0.9, printLogFormat = 0):
            pass
        message = '[%d][%s]:战斗结束,回城' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
        Core(times = self.times).PyTap(950, 930, 0.05, 0.05, 0)
        while Core(times = self.times).NotExist(iconName = 'message', conf = 0.9, printLogFormat = 0):
            pass

    def Fight(self,
              pritLogFormat : int | None = 1):
        Core(times = self.times).PyTap(125, 1000, 0.5, 0.5, 0)
        Core(times = self.times).PyTap(1400, 700, 0.5, 0.5, 0)
        while True:
            message = '[%d][%s]:开始寻敌' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
            Core(times = self.times).stdout(message, printLogFormat = pritLogFormat)
            while Core(times = self.times).NotExist(iconName = 'finish_attack', printLogFormat = 0):
                pass
            message = '[%d][%s]:寻敌完成' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
            Core(times = self.times).stdout(message, printLogFormat = pritLogFormat)
            time.sleep(1)
            resource = Core(times = self.times).GetRes()
            if resource.totle < 2500000:
                message = '[%d][%s]:目标资源仅有 %d , 下一个' %(self.times, time.strftime('%H:%M:%S', time.localtime()), resource.totle)
                Core(times = self.times).stdout(message, printLogFormat = pritLogFormat)
                Core(times = self.times).PyTap(1800, 800, 0.5, 0.5, 0)
            else:
                break
        self.xiabin()
        # self.Hand()
        message = '[%d][%s]:等待战斗结束' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
        Core(times = self.times).stdout(message, 1)
        while Core(times = self.times).NotExist(iconName = 'back_home', conf = 0.9, printLogFormat = 0):
            pass
        message = '[%d][%s]:战斗结束,回城' %(self.times, time.strftime('%H:%M:%S', time.localtime()))
        Core(times = self.times).PyTap(950, 930, 0.05, 0.05, 0)
        while Core(times = self.times).NotExist(iconName = 'message', conf = 0.9, printLogFormat = 0):
            pass


class Run():
    def __init__(self,
                 choise : str | None = config['gameconfig']['lastgamemode'],
                 play_times : int | None = config['gameconfig']['lastgameplaytimes']):
        self.choise = choise
        self.play_times = play_times
        self._TerminalRun()
    
    def run(self,
            choise : str | None = None,
            play_times : int | None = None,
            log_queue : Optional[Queue] | None = None):
        current_times = 1
        if choise == '1':
            while current_times <= play_times:
                msg_start = "[%s]:开始第 %d/%d 轮战斗" %(time.strftime('%H:%M:%S', time.localtime()), current_times, play_times)
                if log_queue:
                    log_queue.put(msg_start)
                else:
                    print("\033[0;30;47m%s\033[0m" %(msg_start))
                AutoHomeTown(current_times).Fight()
                msg_end = "[%s]:第 %d/%d 轮战斗结束" %(time.strftime('%H:%M:%S', time.localtime()), current_times, play_times)
                if log_queue:
                    log_queue.put(msg_end)
                else:
                    print("\033[0;30;47m%s\033[0m" %(msg_end))
                current_times += 1
        elif choise == '2':
            while current_times <= play_times:
                msg_start = "[%s]:开始第 %d/%d 轮战斗" %(time.strftime('%H:%M:%S', time.localtime()), current_times, play_times)
                if log_queue:
                    log_queue.put(msg_start)
                else:
                    print("\033[0;30;47m%s\033[0m" %(msg_start))
                AutoNightWorld(current_times).Fight()
                msg_end = "[%s]:第 %d/%d 轮战斗结束" %(time.strftime('%H:%M:%S', time.localtime()), current_times, play_times)
                if log_queue:
                    log_queue.put(msg_end)
                else:
                    print("\033[0;30;47m%s\033[0m" %(msg_end))
                current_times += 1
        else:
            if log_queue:
                log_queue.put(str(choise) + ':' + choise)
                log_queue.put('已退出\n')
            else:
                print(str(choise) + ':' + choise)
                print('已退出\n')
            exit()
    

    def _TerminalRun(self):
        global config
        with open('config.yml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        launchprocess = Process(target=Core().Launch())
        launchprocess.start()
        loadprocess = Process(target=Core().OcrLoad())
        loadprocess.start()

        try:
            choise = inputimeout(prompt='1.自动家乡作战\n2.自动夜世界作战\n3.退出\n默认值: %s\n' %(config['gameconfig']['lastgamemode']), timeout=5)
            config['gameconfig']['lastgamemode'] = choise
            with open('config.yml', 'w', encoding='utf-8') as file:
                yaml.safe_dump(config, file, allow_unicode=True)
        except TimeoutOccurred:
            choise = config['gameconfig']['lastgamemode']
            message = '输入超时，已使用默认值 {}'.format(choise)
            Core().stdout(message, 1)
        except ValueError:
            choise = config['gameconfig']['lastgamemode']
            message = '输入错误，已使用默认值 {}'.format(choise)
            Core().stdout(message, 1)

        try:
            play_times : str = inputimeout(prompt='请输入战斗次数，默认值: %s\n' %(config['gameconfig']['lastgameplaytimes']), timeout=5)
            play_times : int = int(play_times)
            config['gameconfig']['lastgameplaytimes'] = int(play_times)
            with open('config.yml', 'w', encoding='utf-8') as file:
                yaml.safe_dump(config, file, allow_unicode=True)
        except TimeoutOccurred:
            play_times : int = config['gameconfig']['lastgameplaytimes']
            play_times : int = int(play_times)
            message = '输入超时，已使用默认值 {}'.format(play_times)
            Core().stdout(message, 1)
        except ValueError:
            play_times : int = config['gameconfig']['lastgameplaytimes']
            play_times : int = int(play_times)
            message = '输入错误，已使用默认值 {}'.format(play_times)
            Core().stdout(message, 1)
        launchprocess.join()
        loadprocess.join()
        self.run(choise, play_times)
        pass

    def _GUIRun(self,
                choise : str | None = None,
                play_times : int | None = None,
                log_queue : Optional[Queue] | None = None):
        launchprocess = Process(target=Core().Launch())
        launchprocess.start()
        loadprocess = Process(target=Core().OcrLoad())
        loadprocess.start()
        launchprocess.join()
        loadprocess.join()
        self.run(choise, play_times, log_queue)
        pass


if __name__ == '__main__':
    Run()._TerminalRun()
