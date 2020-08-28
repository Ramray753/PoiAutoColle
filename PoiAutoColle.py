# @Time    : 2020/8/22
# @Author  : Ramray
# @Desc    : 通过图像识别和鼠标模拟在舰队Collection上进行脚本操作
# @File    : KanAutoColle.py
# @Software: PyCharm

import pyautogui
import random
import time
import cv2
import numpy as np
from PoiConfig import *
from PoiScreenConfig import *
import math
from skimage.metrics import structural_similarity as ssim
from datetime import datetime
from playsound import playsound


def relocate():
    print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("此方法用于重新定位游戏界面，请按照以下指示移动鼠标:")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
    input("STEP 1/3: 请将鼠标移至「左上角」并按回车键")
    topLeftX, topLeftY = pyautogui.position()
    print("「左上角」定位成功!")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
    input("STEP 2/3: 请将鼠标移至「右上角」并按回车键")
    topRightX = pyautogui.position()[0]
    print("「右上角」定位成功!")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
    input("STEP 3/3: 请将鼠标移至「左下角」并按回车键")
    botLeftY = pyautogui.position()[1]
    print("「左下角」定位成功!")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("参数已写入「KanScreenConfig.py」!")
    file = open("KanScreenConfig.py", "w")
    now = datetime.now()
    today = now.strftime("%Y/%m/%d")
    file.write("# @Time    : " + today + "\n")
    file.write("# @Author  : Ramray\n")
    file.write("# @Desc    : 为KanAutoColle提供初始化游戏屏幕坐标参数\n")
    file.write("# @File    : KanScreenConfig.py\n")
    file.write("# @Software: PyCharm\n\n")
    file.write('"""以下三个参数确定游戏边界，如果更换界面排序，平台或者设备，请进行重新初始化。"""\n')
    file.write("\n# 当前游戏边界\n")
    file.write("DEFAULT_TOP_LEFT = ({}, {})\n".format(topLeftX, topLeftY))
    file.write("DEFAULT_LENGTH = {}\n".format(topRightX - topLeftX))
    file.write("DEFAULT_WIDTH = {}\n".format(botLeftY - topLeftY))
    file.close()


class PoiAutoColle:
    def __init__(self):
        self.TOP_LEFT = DEFAULT_TOP_LEFT
        self.WIDTH = DEFAULT_WIDTH
        self.LENGTH = DEFAULT_LENGTH
        self.IMG_HOME = cv2.imread("image/HOME.png")
        self.IMG_MOVE_ON = cv2.imread("image/MOVE_ON.png")
        self.IMG_NOT_NIGHT = cv2.imread("image/NOT_NIGHT.png")
        self.IMG_COMPASS = cv2.imread("image/COMPASS.png")
        self.IMG_COL_FORMAT = cv2.imread("image/COL_FORMAT.png")
        self.IMG_NEXT_PAGE_S = cv2.imread("image/NEXT_PAGE_S.png")
        self.IMG_NEXT_PAGE_A = cv2.imread("image/NEXT_PAGE_A.png")
        self.IMG_EXE_COL = cv2.imread("image/EXE_COL.png")
        self.IMG_NEW_SHIP = cv2.imread("image/NEW_SHIP.png")
        self.IMG_ROW_FORMAT = cv2.imread("image/ROW_FORMAT.png")
        self.IMG_END_SAIL = cv2.imread("image/END_SAIL.png")

    @staticmethod
    def __printTime__(text, nextLine=True):
        now = datetime.now()
        dtString = now.strftime("%H:%M:%S")
        if nextLine:
            print(dtString, text)
        else:
            print(dtString, text, end="")

    def __click__(self, centralPer, errorPer, delay, rand):
        time.sleep(random.uniform(delay, delay + rand))
        central = (self.TOP_LEFT[0] + centralPer[0] * self.LENGTH,
                   self.TOP_LEFT[1] + centralPer[1] * self.WIDTH)
        xError = errorPer[0] * self.LENGTH
        yError = errorPer[1] * self.WIDTH
        outCordX = central[0] + random.uniform(-xError, xError)
        outCordY = central[1] + random.uniform(-yError, yError)
        pyautogui.moveTo(outCordX, outCordY,
                         random.uniform(0, 0.5),
                         pyautogui.easeInOutQuad)
        pyautogui.leftClick()
        outCordX = self.TOP_LEFT[0] + 0.5 * self.LENGTH
        outCordY = self.TOP_LEFT[1] + 1.1 * self.WIDTH
        pyautogui.moveTo(outCordX, outCordY,
                         random.uniform(0, 0.5),
                         pyautogui.easeInOutQuad)

    def __screenshot__(self, centralPer, errorPer):
        left = (self.TOP_LEFT[0] + (centralPer[0] - errorPer[0]) * self.LENGTH) * ZOOM_MODIFIER
        top = (self.TOP_LEFT[1] + (centralPer[1] - errorPer[1]) * self.WIDTH) * ZOOM_MODIFIER
        width = 2 * errorPer[0] * self.LENGTH * ZOOM_MODIFIER
        height = 2 * errorPer[1] * self.WIDTH * ZOOM_MODIFIER
        temImage = pyautogui.screenshot(region=(left, top, width, height))
        cvImage = np.array(temImage.convert('RGB'))
        return cvImage

    def __moveToGame__(self):
        self.__click__((0.5, 0.5), (0.4, 0.4), 0, 0)
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        print("              PoiAutoColle助手已启用，愿提督武运昌隆！")

    def __attackStart__(self):
        # 点击主页的出击按钮
        self.__click__(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, 2, 2)
        # 点击出击选择中的出击按钮
        self.__click__(NEXT_ATTACK_CENTRAL, NEXT_ERROR, 2, 1)

    def __attackEnd__(self):
        # 点击决定
        self.__click__(DECIDE_CENTRAL, DECIDE_ERROR, 0, 1)
        # 点击出击开始
        self.__click__(FINAL_ATTACK_CENTRAL, FINAL_ATTACK_ERROR, 0, 1)

    def __sailStart__(self):
        # 点击主页的出击按钮
        self.__click__(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, 0, 0)
        # 点击远征
        self.__click__(NEXT_SAIL_CENTRAL, NEXT_ERROR, 2, 1)

    def __sailEnd__(self, fleet):
        # 点击决定
        self.__click__(DECIDE_CENTRAL, DECIDE_ERROR, 0, 0.5)
        if fleet == 3:
            self.__click__(DECIDE_FLEET3_CENTRAL, DECIDE_FLEET_ERROR, 0, 0.5)
        # 点击出击开始
        self.__click__(FINAL_ATTACK_CENTRAL, FINAL_ATTACK_ERROR, 0, 0.5)

    def __supply__(self, head, num):
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__validate__(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, self.IMG_HOME, "母港")
        self.__click__(SUPPLY_CENTRAL, SUPPLY_ERROR, 0, 1)
        if num == 3:
            self.__click__(SUPPLY_FLEET3_CENTRAL, SUPPLY_FLEET_ERROR, 2, 2)
        if head:
            self.__click__(SUPPLY_HEAD_CENTRAL, SUPPLY_HEAD_ERROR, 2, 2)
            self.__click__(BOTH_SUPPLY_CENTRAL, BOTH_SUPPLY_ERROR, 0, 1)
        else:
            self.__click__(ALL_SUPPLY_CENTRAL, ALL_SUPPLY_ERROR, 2, 2)
        self.__printTime__("已完成补给")

    @staticmethod
    def __compare__(img1, img2):
        grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        H1 = cv2.calcHist([img1], [1], None, [256], [0, 256])
        H1 = cv2.normalize(H1, H1, 0, 1, cv2.NORM_MINMAX, -1)
        H2 = cv2.calcHist([img2], [1], None, [256], [0, 256])
        H2 = cv2.normalize(H2, H2, 0, 1, cv2.NORM_MINMAX, -1)
        similarity1 = cv2.compareHist(H1, H2, 0)
        similarity2 = ssim(grayA, grayB, multichannel=True)
        if similarity1 > similarity2:
            return similarity1
        return similarity2

    def __validate__(self, centralPer, errorPer, baseImg, text):
        self.__printTime__("正在识别图像...", nextLine=False)
        while True:
            temImage = self.__screenshot__(centralPer, errorPer)
            print(".", end="")
            if self.__compare__(temImage, baseImg) > 0.85:
                print("已成功识别: {}".format(text))
                break
            time.sleep(1)

    def __combat__(self, sec1, sec2, formation):
        time.sleep(sec1)
        if formation != "none":
            if formation == "col":
                self.__validate__(COL_FORMAT_CENTRAL, FORMAT_ERROR, self.IMG_COL_FORMAT, "单纵阵")
                self.__click__(COL_FORMAT_CENTRAL, FORMAT_ERROR, 0, 1)
                self.__printTime__("已选择单纵阵型")
            elif formation == "row":
                self.__validate__(ROW_FORMAT_CENTRAL, FORMAT_ERROR, self.IMG_ROW_FORMAT, "单横阵")
                self.__click__(ROW_FORMAT_CENTRAL, FORMAT_ERROR, 0, 1)
                self.__printTime__("已选择单横阵型")
        time.sleep(sec2)
        clickNotNight = False
        self.__printTime__("正在识别图像...", nextLine=False)
        while True:
            temImage = self.__screenshot__(NOT_NIGHT_CENTRAL, NOT_NIGHT_ERROR)
            print(".", end="")
            if self.__compare__(temImage, self.IMG_NOT_NIGHT) > 0.85:
                print("已成功识别: {}".format("回避夜战"))
                clickNotNight = True
                break
            temImage = self.__screenshot__(NEXT_PAGE_CENTRAL, NEXT_PAGE_ERROR)
            print(".", end="")
            if self.__compare__(temImage, self.IMG_NEXT_PAGE_S) > 0.85 or \
                    self.__compare__(temImage, self.IMG_NEXT_PAGE_A) > 0.85:
                print("已成功识别: {}".format("下一页"))
                break
            time.sleep(1)
        if clickNotNight:
            self.__click__(NOT_NIGHT_CENTRAL, NOT_NIGHT_ERROR, 0, 1)
            self.__printTime__("已选择回避夜战")
            time.sleep(10)
            self.__printTime__("正在识别图像...", nextLine=False)
            while True:
                temImage = self.__screenshot__(NEXT_PAGE_CENTRAL, NEXT_PAGE_ERROR)
                print(".", end="")
                if self.__compare__(temImage, self.IMG_NEXT_PAGE_S) > 0.85 or \
                        self.__compare__(temImage, self.IMG_NEXT_PAGE_A) > 0.85:
                    print("已成功识别: {}".format("下一页"))
                    break
                time.sleep(1)
        self.__click__((0.5, 0.5), (0.4, 0.4), 0, 1)
        self.__printTime__("已点击屏幕")
        self.__click__((0.5, 0.5), (0.4, 0.4), 5, 1)
        self.__printTime__("已点击屏幕")
        time.sleep(3)
        clickMoveOn = False
        clickReturn = False
        self.__printTime__("正在识别图像...", nextLine=False)
        while True:
            temImage = self.__screenshot__(NEW_SHIP_CENTRAL, NEW_SHIP_ERROR)
            print(".", end="")
            if self.__compare__(temImage, self.IMG_NEW_SHIP) > 0.85:
                print("已成功识别: {}".format("获得新船"))
                playsound("audio/new_ship.mp3")
                clickReturn = True
                break
            temImage = self.__screenshot__(MOVE_ON_CENTRAL, MOVE_ON_ERROR)
            print(".", end="")
            if self.__compare__(temImage, self.IMG_MOVE_ON) > 0.85:
                print("已成功识别: {}".format("进击"))
                clickMoveOn = True
                break
            temImage = self.__screenshot__(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR)
            print(".", end="")
            if self.__compare__(temImage, self.IMG_HOME) > 0.85:
                print("已成功识别: {}".format("母港"))
                break
            time.sleep(1)
        if clickReturn:
            self.__click__((0.5, 0.5), (0.4, 0.4), 0, 1)
            self.__printTime__("已点击屏幕")
            time.sleep(3)
            self.__printTime__("正在识别图像...", nextLine=False)
            while True:
                temImage = self.__screenshot__(MOVE_ON_CENTRAL, MOVE_ON_ERROR)
                print(".", end="")
                if self.__compare__(temImage, self.IMG_MOVE_ON) > 0.85:
                    print("已成功识别: {}".format("进击"))
                    clickMoveOn = True
                    break
                temImage = self.__screenshot__(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR)
                print(".", end="")
                if self.__compare__(temImage, self.IMG_HOME) > 0.85:
                    print("已成功识别: {}".format("母港"))
                    break
                time.sleep(1)
        if clickMoveOn:
            self.__click__(MOVE_ON_CENTRAL, MOVE_ON_ERROR, 0, 1)

    def __attack1_1__(self):
        # 点击出击
        self.__attackStart__()
        # 点击图1-1
        self.__click__(FIRST_MAP_CENTRAL, MAP_ERROR, 2, 1)
        # 确定出击
        self.__attackEnd__()
        # 以下为战斗部分
        # 战斗1
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗1:")
        self.__combat__(0, 30, "none")
        self.__printTime__("战斗1结束，进击到下一区域")
        # 战斗2
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗2:")
        time.sleep(2)
        self.__validate__(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.__click__(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        self.__printTime__("已点击罗盘")
        self.__combat__(0, 40, "none")
        self.__printTime__("战斗2结束，返回母港")
        # 补给
        time.sleep(3)
        self.__supply__(head=True, num=1)

    def __attack1_5__(self):
        # 点击出击
        self.__attackStart__()
        # 点击扩张海域
        self.__click__(EXTRA_ATTACK_CENTRAL, EXTRA_ATTACK_ERROR, 2, 1)
        # 点击图1-5
        self.__click__(EXTRA_5_CENTRAL, EXTRA_5_ERROR, 0, 0.5)
        # 确定出击
        self.__attackEnd__()
        # 以下为战斗部分
        # 战斗1
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗1:")
        self.__combat__(10, 30, "row")
        self.__printTime__("战斗1结束，进击到下一区域")
        # 战斗2
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗2:")
        self.__combat__(10, 30, "row")
        self.__printTime__("战斗2结束，进击到下一区域")
        # 战斗3
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗3:")
        time.sleep(3)
        self.__validate__(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.__click__(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        self.__printTime__("已点击罗盘")
        self.__combat__(10, 35, "row")
        self.__printTime__("战斗3结束，进击到下一区域")
        # 战斗4
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗4:")
        time.sleep(3)
        self.__validate__(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.__click__(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        self.__printTime__("已点击罗盘")
        time.sleep(10)
        self.__validate__(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.__click__(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        self.__printTime__("已点击罗盘")
        self.__combat__(10, 35, "row")
        self.__printTime__("战斗4结束，返回母港")
        # 补给
        time.sleep(3)
        self.__supply__(head=False, num=1)

    def __attack2_2__(self):
        # 点击出击
        self.__attackStart__()
        # 点击图2
        self.__click__(SECOND_SUB_CENTRAL, SECOND_SUB_ERROR, 2, 1)
        # 点击图2-2
        self.__click__(SECOND_MAP_CENTRAL, MAP_ERROR, 0, 0.5)
        # 确定出击
        self.__attackEnd__()
        # 以下为战斗部分
        # 战斗1
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗1:")
        time.sleep(10)
        self.__validate__(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.__click__(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        self.__printTime__("已点击罗盘")
        self.__combat__(7, 55, "col")
        self.__printTime__("战斗1结束，进击到下一区域")
        # 战斗2
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.__printTime__("战斗2:")
        self.__click__((0.5, 0.5), (0.4, 0.4), 12, 1)
        self.__printTime__("已点击屏幕")
        self.__printTime__("战斗2结束，返回母港")
        # 补给
        time.sleep(3)
        self.__supply__(head=False, num=1)

    def __expedition03__(self, fleet):
        # 点击远征
        self.__sailStart__()
        # 点击远征任务
        self.__click__(SAIL_03_CENTRAL, SELECT_SAIL_ERROR, 2, 1)
        # 确定出击第三舰队
        self.__sailEnd__(fleet=fleet)

    def pointLocate(self, calError=False):
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("此方法用于显示定位点坐标，请照照以下指示移动鼠标:")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        if calError:
            input("STEP 1/3: 请将鼠标移至定位点并按回车键")
        else:
            input("STEP 1/1: 请将鼠标移至定位点并按回车键")
        X, Y = pyautogui.position()
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        if calError:
            input("STEP 2/3: 请将鼠标移至X轴最大误差点并按回车键")
            XError = pyautogui.position()[0]
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            input("STEP 3/3: 请将鼠标移至Y轴最大误差点并按回车键")
            YError = pyautogui.position()[1]
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("当前定位点绝对坐标为: ({}, {})".format(X, Y))
            print(f"当前定位点百分比坐标为: (%.3f, %.3f)" %
                  ((X - self.TOP_LEFT[0]) / self.LENGTH,
                   (Y - self.TOP_LEFT[1]) / self.WIDTH))
            print(f"百分比误差为: (%.3f, %.3f)" %
                  (math.fabs(XError - X) / self.LENGTH,
                   math.fabs(YError - Y) / self.WIDTH))
        else:
            print("当前定位点绝对坐标为: ({}, {})".format(X, Y))
            print(f"当前定位点百分比坐标为: (%.3f, %.3f)" %
                  ((X - self.TOP_LEFT[0]) / self.LENGTH,
                   (Y - self.TOP_LEFT[1]) / self.WIDTH))

    def screenshot(self, centralPer, errorPer):
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("STEP 1/1: 请点击游戏画面，并将鼠标移至画面外，3秒后开始截屏")
        time.sleep(3)
        left = (self.TOP_LEFT[0] + (centralPer[0] - errorPer[0]) * self.LENGTH) * ZOOM_MODIFIER
        top = (self.TOP_LEFT[1] + (centralPer[1] - errorPer[1]) * self.WIDTH) * ZOOM_MODIFIER
        width = 2 * errorPer[0] * self.LENGTH * ZOOM_MODIFIER
        height = 2 * errorPer[1] * self.WIDTH * ZOOM_MODIFIER
        temImage = pyautogui.screenshot(region=(left, top, width, height))
        temImage.save(r"image/new_screen_shot.png")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("已截取游戏屏幕，并保存于「image」文件夹")

    def sortie(self, sortieMap, num):
        self.__moveToGame__()
        playsound("audio/begin.mp3")
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        self.__printTime__("开始进行{}练级(共{}回)".format(sortieMap, num))
        sumTime = 0
        for i in range(1, num + 1):
            if i != 1:
                self.__click__(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 0, 0)
            startTime = time.time()
            print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
            self.__printTime__("第{}回{}练级开始(共{}回)".format(i, sortieMap, num))
            if sortieMap == '1-1':
                self.__attack1_1__()
            elif sortieMap == '1-5':
                self.__attack1_5__()
            elif sortieMap == '2-2':
                self.__attack2_2__()
            if i == num:
                self.__click__(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 2, 2)
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            endTime = time.time()
            diffTime = endTime - startTime
            sumTime = sumTime + diffTime
            self.__printTime__(
                "第{}回{}练级结束(共{}回)，耗时{}分{}秒".format(i, sortieMap, num, int(diffTime) // 60, round(diffTime % 60)))
            if i != num:
                delay = random.uniform(0, 30)
                sumTime = sumTime + delay
                print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
                self.__printTime__("延迟{}秒后开始下一轮出击".format(round(delay)))
                time.sleep(delay)
        playsound("audio/end.mp3")
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        self.__printTime__("{}练级结束，共{}回，共耗时{}分{}秒".format(sortieMap, num, int(sumTime) // 60, round(sumTime % 60)))

    def expedition(self, sailMap, fleet, num):
        self.__moveToGame__()
        playsound("audio/begin.mp3")
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        self.__printTime__("第{}舰队开始进行{}号远征(共{}回)".format(fleet, sailMap, num))
        for i in range(1, num + 1):
            duration = None
            if sailMap == "3":
                duration = 20
                self.__expedition03__(fleet)
            print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
            self.__printTime__("第{}舰队开始第{}回{}号远征(共{}回)".format(fleet, i, sailMap, num))
            times = duration // 5
            for j in range(1, times):
                time.sleep(200)
                self.__printTime__("距离远征结束还有{}分钟".format(duration - j * 5))
            mod = duration % 5
            time.sleep(60 * 5)
            if mod != 0:
                self.__printTime__("距离远征结束还有{}分钟".format(mod))
                time.sleep(60 * mod)
            delay = random.uniform(0, 60)
            self.__printTime__("远征已结束，延迟{}秒后返回母港".format(round(delay)))
            time.sleep(delay)
            self.__click__(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 0, 0.5)
            time.sleep(3)
            self.__validate__(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, self.IMG_HOME, "母港")
            self.__click__((0.5, 0.5), (0.4, 0.4), 0.5, 0.5)
            time.sleep(10)
            self.__validate__(END_SAIL_CENTER, END_SAIL_ERROR, self.IMG_END_SAIL, "下一页")
            self.__click__((0.5, 0.5), (0.4, 0.4), 1, 0.5)
            self.__click__((0.5, 0.5), (0.4, 0.4), 1, 0.5)
            self.__printTime__("已返回主港")
            time.sleep(3)
            self.__supply__(head=False, num=fleet)
            self.__click__(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 2, 2)
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            self.__printTime__("第{}舰队第{}回{}号远征结束(共{}回)".format(fleet, i, sailMap, num))
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        self.__printTime__("第{}舰队{}号远征结束(共{}回)".format(fleet, sailMap, num))
        playsound("audio/end.mp3")
