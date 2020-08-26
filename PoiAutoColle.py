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

def printTime(text, nextLine=True):
    now = datetime.now()
    dtString = now.strftime("%H:%M:%S")
    if nextLine:
        print(dtString, text)
    else:
        print(dtString, text, end="")

def compare(img1, img2):
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
        self.IMG_NEXT_PAGE = cv2.imread("image/NEXT_PAGE.png")
        self.IMG_EXE_COL = cv2.imread("image/EXE_COL.png")
        self.IMG_NEW_SHIP = cv2.imread("image/NEW_SHIP.png")
        self.IMG_ROW_FORMAT = cv2.imread("image/ROW_FORMAT.png")
        self.IMG_END_SAIL = cv2.imread("image/END_SAIL.png")

    def click(self, centralPer, errorPer, delay, rand):
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
            printTime(f"百分比误差为: (%.3f, %.3f)" %
                      (math.fabs(XError - X) / self.LENGTH,
                       math.fabs(YError - Y) / self.WIDTH))
        else:
            print("当前定位点绝对坐标为: ({}, {})".format(X, Y))
            print(f"当前定位点百分比坐标为: (%.3f, %.3f)" %
                  ((X - self.TOP_LEFT[0]) / self.LENGTH,
                   (Y - self.TOP_LEFT[1]) / self.WIDTH))

    def moveToGame(self):
        self.click((0.5, 0.5), (0.4, 0.4), 0, 0)
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        print("              PoiAutoColle助手已启用，愿提督武运昌隆！")

    def screenshot(self, centralPer, errorPer, save):
        if save:
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("STEP 1/1: 请点击游戏画面，并将鼠标移至画面外，3秒后开始截屏")
            time.sleep(3)
        left = (self.TOP_LEFT[0] + (centralPer[0] - errorPer[0]) * self.LENGTH) * ZOOM_MODIFIER
        top = (self.TOP_LEFT[1] + (centralPer[1] - errorPer[1]) * self.WIDTH) * ZOOM_MODIFIER
        width = 2 * errorPer[0] * self.LENGTH * ZOOM_MODIFIER
        height = 2 * errorPer[1] * self.WIDTH * ZOOM_MODIFIER
        temImage = pyautogui.screenshot(region=(left, top, width, height))
        if save:
            temImage.save(r"image/new_screen_shot.png")
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            print("已截取游戏屏幕，并保存于「image」文件夹")
        else:
            cvImage = np.array(temImage.convert('RGB'))
            return cvImage

    def attackStart(self):
        # 点击主页的出击按钮
        self.click(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, 2, 2)
        # 点击出击选择中的出击按钮
        self.click(NEXT_ATTACK_CENTRAL, NEXT_ERROR, 2, 1)

    def attackEnd(self):
        # 点击决定
        self.click(DECIDE_CENTRAL, DECIDE_ERROR, 0, 1)
        # 点击出击开始
        self.click(FINAL_ATTACK_CENTRAL, FINAL_ATTACK_ERROR, 0, 1)

    def sailStart(self):
        # 点击主页的出击按钮
        self.click(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, 0, 0)
        # 点击远征
        self.click(NEXT_SAIL_CENTRAL, NEXT_ERROR, 2, 1)

    def sailEnd(self, fleet):
        # 点击决定
        self.click(DECIDE_CENTRAL, DECIDE_ERROR, 0, 0.5)
        if fleet == 3:
            self.click(DECIDE_FLEET3_CENTRAL, DECIDE_FLEET_ERROR, 0, 0.5)
        # 点击出击开始
        self.click(FINAL_ATTACK_CENTRAL, FINAL_ATTACK_ERROR, 0, 0.5)

    def supply(self, head, num):
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        self.validate(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, self.IMG_HOME, "母港")
        self.click(SUPPLY_CENTRAL, SUPPLY_ERROR, 0, 1)
        if num == 3:
            self.click(SUPPLY_FLEET3_CENTRAL, SUPPLY_FLEET_ERROR, 2, 2)
        if head:
            self.click(SUPPLY_HEAD_CENTRAL, SUPPLY_HEAD_ERROR, 2, 2)
            self.click(BOTH_SUPPLY_CENTRAL, BOTH_SUPPLY_ERROR, 0, 1)
        else:
            self.click(ALL_SUPPLY_CENTRAL, ALL_SUPPLY_ERROR, 2, 2)
        printTime("已完成补给")

    def validate(self, centralPer, errorPer, baseImg, text):
        printTime("正在识别图像...", nextLine=False)
        while True:
            temImage = self.screenshot(centralPer, errorPer, save=False)
            print(".", end="")
            if compare(temImage, baseImg) > 0.85:
                print("已成功识别: {}".format(text))
                break
            time.sleep(1)

    def combat(self, sec1, sec2, formation):
        time.sleep(sec1)
        if formation != "none":
            if formation == "col":
                self.validate(COL_FORMAT_CENTRAL, FORMAT_ERROR, self.IMG_COL_FORMAT, "单纵阵")
                self.click(COL_FORMAT_CENTRAL, FORMAT_ERROR, 0, 1)
                printTime("已选择单纵阵型")
            elif formation == "row":
                self.validate(ROW_FORMAT_CENTRAL, FORMAT_ERROR, self.IMG_ROW_FORMAT, "单横阵")
                self.click(ROW_FORMAT_CENTRAL, FORMAT_ERROR, 0, 1)
                printTime("已选择单横阵型")
        time.sleep(sec2)
        clickNotNight = False
        printTime("正在识别图像...", nextLine=False)
        while True:
            temImage = self.screenshot(NOT_NIGHT_CENTRAL, NOT_NIGHT_ERROR, save=False)
            print(".", end="")
            if compare(temImage, self.IMG_NOT_NIGHT) > 0.85:
                print("已成功识别: {}".format("回避夜战"))
                clickNotNight = True
                break
            temImage = self.screenshot(NEXT_PAGE_CENTRAL, NEXT_PAGE_ERROR, save=False)
            print(".", end="")
            if compare(temImage, self.IMG_NEXT_PAGE) > 0.85:
                print("已成功识别: {}".format("下一页"))
                break
            time.sleep(1)
        if clickNotNight:
            self.click(NOT_NIGHT_CENTRAL, NOT_NIGHT_ERROR, 0, 1)
            printTime("已选择回避夜战")
            time.sleep(10)
            self.validate(NEXT_PAGE_CENTRAL, NEXT_PAGE_ERROR, self.IMG_NEXT_PAGE, "下一页")
        self.click((0.5, 0.5), (0.4, 0.4), 0, 1)
        printTime("已点击屏幕")
        self.click((0.5, 0.5), (0.4, 0.4), 5, 1)
        printTime("已点击屏幕")
        time.sleep(3)
        clickMoveOn = False
        clickReturn = False
        printTime("正在识别图像...", nextLine=False)
        while True:
            temImage = self.screenshot(NEW_SHIP_CENTRAL, NEW_SHIP_ERROR, save=False)
            print(".", end="")
            if compare(temImage, self.IMG_NEW_SHIP) > 0.85:
                print("已成功识别: {}".format("获得新船"))
                playsound("audio/new_ship.mp3")
                clickReturn = True
                break
            temImage = self.screenshot(MOVE_ON_CENTRAL, MOVE_ON_ERROR, save=False)
            print(".", end="")
            if compare(temImage, self.IMG_MOVE_ON) > 0.85:
                print("已成功识别: {}".format("进击"))
                clickMoveOn = True
                break
            temImage = self.screenshot(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, save=False)
            print(".", end="")
            if compare(temImage, self.IMG_HOME) > 0.85:
                print("已成功识别: {}".format("母港"))
                break
            time.sleep(1)
        if clickReturn:
            self.click((0.5, 0.5), (0.4, 0.4), 0, 1)
            printTime("已点击屏幕")
            time.sleep(3)
            printTime("正在识别图像...", nextLine=False)
            while True:
                temImage = self.screenshot(MOVE_ON_CENTRAL, MOVE_ON_ERROR, save=False)
                print(".", end="")
                if compare(temImage, self.IMG_MOVE_ON) > 0.85:
                    print("已成功识别: {}".format("进击"))
                    clickMoveOn = True
                    break
                temImage = self.screenshot(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, save=False)
                print(".", end="")
                if compare(temImage, self.IMG_HOME) > 0.85:
                    print("已成功识别: {}".format("母港"))
                    break
                time.sleep(1)
        if clickMoveOn:
            self.click(MOVE_ON_CENTRAL, MOVE_ON_ERROR, 0, 1)

    def attack1_1(self):
        # 点击出击
        self.attackStart()
        # 点击图1-1
        self.click(FIRST_MAP_CENTRAL, MAP_ERROR, 2, 1)
        # 确定出击
        self.attackEnd()
        # 以下为战斗部分
        # 战斗1
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗1:")
        self.combat(0, 30, "none")
        printTime("战斗1结束，进击到下一区域")
        # 战斗2
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗2:")
        time.sleep(2)
        self.validate(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.click(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        printTime("已点击罗盘")
        self.combat(0, 40, "none")
        printTime("战斗2结束，返回母港")
        # 补给
        time.sleep(3)
        self.supply(head=True, num=1)

    def attack1_5(self):
        # 点击出击
        self.attackStart()
        # 点击扩张海域
        self.click(EXTRA_ATTACK_CENTRAL, EXTRA_ATTACK_ERROR, 2, 1)
        # 点击图1-5
        self.click(EXTRA_5_CENTRAL, EXTRA_5_ERROR, 0, 0.5)
        # 确定出击
        self.attackEnd()
        # 以下为战斗部分
        # 战斗1
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗1:")
        self.combat(10, 30, "row")
        printTime("战斗1结束，进击到下一区域")
        # 战斗2
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗2:")
        self.combat(10, 30, "row")
        printTime("战斗2结束，进击到下一区域")
        # 战斗3
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗3:")
        time.sleep(3)
        self.validate(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.click(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        printTime("已点击罗盘")
        self.combat(10, 35, "row")
        printTime("战斗3结束，进击到下一区域")
        # 战斗4
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗4:")
        time.sleep(3)
        self.validate(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.click(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        printTime("已点击罗盘")
        time.sleep(10)
        self.validate(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.click(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        printTime("已点击罗盘")
        self.combat(10, 35, "row")
        printTime("战斗4结束，返回母港")
        # 补给
        time.sleep(3)
        self.supply(head=False, num=1)

    def attack2_2(self):
        # 点击出击
        self.attackStart()
        # 点击图2
        self.click(SECOND_SUB_CENTRAL, SECOND_SUB_ERROR, 2, 1)
        # 点击图2-2
        self.click(SECOND_MAP_CENTRAL, MAP_ERROR, 0, 0.5)
        # 确定出击
        self.attackEnd()
        # 以下为战斗部分
        # 战斗1
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗1:")
        time.sleep(10)
        self.validate(COMPASS_CENTRAL, COMPASS_ERROR, self.IMG_COMPASS, "罗盘")
        self.click(COMPASS_CENTRAL, COMPASS_ERROR, 0, 1)
        printTime("已点击罗盘")
        self.combat(7, 55, "col")
        printTime("战斗1结束，进击到下一区域")
        # 战斗2
        print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
        printTime("战斗2:")
        self.click((0.5, 0.5), (0.4, 0.4), 12, 1)
        printTime("已点击屏幕")
        printTime("战斗2结束，返回母港")
        # 补给
        time.sleep(3)
        self.supply(head=False, num=1)

    def sortie(self, sortieMap, num):
        self.moveToGame()
        playsound("audio/begin.mp3")
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        printTime("开始进行{}练级(共{}回)".format(sortieMap, num))
        sumTime = 0
        for i in range(1, num + 1):
            if i != 1:
                self.click(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 0, 0)
            startTime = time.time()
            print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
            printTime("第{}回{}练级开始(共{}回)".format(i, sortieMap, num))
            if sortieMap == '1-1':
                self.attack1_1()
            elif sortieMap == '1-5':
                self.attack1_5()
            elif sortieMap == '2-2':
                self.attack2_2()
            if i == num:
                self.click(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 2, 2)
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            endTime = time.time()
            diffTime = endTime - startTime
            sumTime = sumTime + diffTime
            printTime("第{}回{}练级结束(共{}回)，耗时{}分{}秒".format(i, sortieMap, num, int(diffTime) // 60, round(diffTime % 60)))
            if i != num:
                delay = random.uniform(0, 30)
                sumTime = sumTime + delay
                print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
                printTime("延迟{}秒后开始下一轮出击".format(round(delay)))
                time.sleep(delay)
        playsound("audio/end.mp3")
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        printTime("{}练级结束，共{}回，共耗时{}分{}秒".format(sortieMap, num, int(sumTime) // 60, round(sumTime % 60)))

    def expedition03(self, fleet):
        # 点击远征
        self.sailStart()
        # 点击远征任务
        self.click(SAIL_03_CENTRAL, SELECT_SAIL_ERROR, 2, 1)
        # 确定出击第三舰队
        self.sailEnd(fleet=fleet)

    def expedition(self, sailMap, fleet, num):
        self.moveToGame()
        playsound("audio/begin.mp3")
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        printTime("第{}舰队开始进行{}号远征(共{}回)".format(fleet, sailMap, num))
        for i in range(1, num + 1):
            duration = None
            if sailMap == "3":
                duration = 20
                self.expedition03(fleet)
            print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
            printTime("第{}舰队开始第{}回{}号远征(共{}回)".format(fleet, i, sailMap, num))
            times = duration // 5
            for j in range(1, times):
                time.sleep(200)
                printTime("距离远征结束还有{}分钟".format(duration - j * 5))
            mod = duration % 5
            time.sleep(60 * 5)
            if mod != 0:
                printTime("距离远征结束还有{}分钟".format(mod))
                time.sleep(60 * mod)
            delay = random.uniform(0, 60)
            printTime("远征已结束，延迟{}秒后返回母港".format(round(delay)))
            time.sleep(delay)
            self.click(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 0, 0.5)
            time.sleep(3)
            self.validate(HOME_ATTACK_CENTRAL, HOME_ATTACK_ERROR, self.IMG_HOME, "母港")
            self.click((0.5, 0.5), (0.4, 0.4), 0.5, 0.5)
            time.sleep(10)
            self.validate(END_SAIL_CENTER, END_SAIL_ERROR, self.IMG_END_SAIL, "下一页")
            self.click((0.5, 0.5), (0.4, 0.4), 1, 0.5)
            self.click((0.5, 0.5), (0.4, 0.4), 1, 0.5)
            printTime("已返回主港")
            time.sleep(3)
            self.supply(head=False, num=fleet)
            self.click(RETURN_HOME_CENTRAL, RETURN_HOME_ERROR, 2, 2)
            print("- - - - - - - - - - - - - - - - - - - - - - - - - -")
            printTime("第{}舰队第{}回{}号远征结束(共{}回)".format(fleet, i, sailMap, num))
        print("★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★")
        printTime("第{}舰队{}号远征结束(共{}回)".format(fleet, sailMap, num))
        playsound("audio/end.mp3")
