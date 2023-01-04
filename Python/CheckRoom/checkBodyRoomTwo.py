# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# ============================================================
# @Date    : 2022/12/23
# @Author  : rondy
# @File    : checkBodyRoomTwo.py
# @IDE     : 
# @Func    : 检测仓用户信息操作界面以及显示当前进度界面
# ============================================================
"""


import tkinter
import threading
import os,sys
import datetime

import subprocess

from tkinter import *

from PIL import Image, ImageTk
import time
from threading import Timer
from tkinter import Toplevel
import tkinter.ttk

from watchdog.observers import Observer
from watchdog.events import *

#import doBloodPressure      #ShowResult(save_result),   startDoBloodPressure()


PATHPACKAGE = '.\\package'

IMGFILE_LIFT = 'l.png'
IMGFILE_RIGHT = 'r.png'



doWindow = Tk()
showWindow = Tk()

#当这个值不变时，窗口将会暂停
global g_pause_var
g_pause_var = StringVar()   

global flag
flag = BooleanVar(doWindow)
flag.set(False)



import binascii
import serial.tools.list_ports

g_save_result = ""




##窗口位于屏幕中间
width = 1920
height = 1080
g_screenwidth = doWindow.winfo_screenwidth()
g_screenheight = doWindow.winfo_screenheight()
alignstr = '%dx%d+%d+0' % (width, height, (g_screenwidth-width)/2,)
doWindow.geometry(alignstr)

#window.geometry("760x1360")    #窗口大小

doWindow.title("触摸屏操作界面")   #窗口标题
doWindow.config(bg="skyblue")       #窗口背景颜色





 
class FileEventHandler(FileSystemEventHandler):
    print("observer5")
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):    
        if event.is_directory:
            print("observer3")
            print("directory created:{0}".format(event.src_path))
        else:
            print("observer4")#当有文件创建时
            print("file11 created:{0}".format(event.src_path))
        g_pause_var.set(1)
    def on_modified(self, event):   
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file11 modified:{0}".format(event.src_path))#当有文件被改变时
        g_pause_var.set(1)
        print("observer5")
 
def DoCheckFile():#启动监控文件变化
    
    observer=Observer()

    event_handler=FileEventHandler()
    checkPath = '.\\newpackage'#文件创建的文件夹位置

    observer.schedule(event_handler, checkPath ,True)
    print("DoCheck start 0")
    observer.start()
    print("DoCheck start 1")
    doWindow.wait_variable(g_pause_var)#让窗口进入等待状态，当这个值不变时，窗口将会暂停
    print("DoCheck end 0")
    observer.stop()



def SendDataToSerialPort(portNumber, DataStr):
    
    port_num = portNumber
    ser = serial.Serial(port=port_num, baudrate=9600, bytesize=8, timeout=50, stopbits=1)
    if ser.isOpen():
        print("打开串口成功, 串口号: %s" % ser.name)
    else:
        print("打开串口失败")
    # 串口发送数据
    write_len = ser.write(DataStr)
    print("串口she发出{}个字节".format(write_len))
    ser.close()


def GetBodyFatResult():
    fileName = '体脂结果.txt'
    fpath = os.path.abspath('.')+'\\newpackage\\'+fileName
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r')
        with fileData as f:
            strData = f.read()
        #print (strData)
        #print (fpath)
        return strData


def GetBloodPressureResult():
    fileName = '血压结果.txt'
    fpath = os.path.abspath('.')+'\\newpackage\\'+fileName
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r')
        with fileData as f:
            strData = f.read()
        #print (strData)
        #print (fpath)
        return strData



def TimeShow():


    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    #timestr = "2020-10-10 10:10:10"
    t = time.strptime(ts, "%Y-%m-%d %H:%M:%S")
    ft = time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}', t).format(y='年', m='月', d='日', h='时', f='分', s='秒')
    return ft


def PlaySound():

    soundFile =PATHPACKAGE+'\\'+'test.mp3'
    if os.path.isfile(soundFile) :
        os.startfile(soundFile)

def ProcessTime(window,showTime):#进度条，window：依赖的窗口，showTime：进度条运行的时间
    
    ##determinate：一个指针会从起点移至终点，通常当我们知道所需工作时间时，可以使用此模式，这是默认模式
    ##indeterminate：一个指针会在起点和终点间来回移动，通常当我们不知道工作所需时间时，可以使用此模式

    progressbarOne = tkinter.ttk.Progressbar(window,mode='determinate',length=1280)    
    progressbarOne.pack(side=tkinter.BOTTOM)

    progressbarOne['maximum'] = showTime
    # 进度值初始值
    progressbarOne['value'] = 0
    for i in range(showTime):
        time.sleep(1)
        progressbarOne['value'] += 1
        window.update()
def DoBodyFatCheck():
    print(flag.get())
    if flag.get() == False:
        flag.set(True)
    else:
        return 0
    print(flag.get())
    
    state['BodyFat'] = 'green'
    UpdatecCanvas(state)
    PlaySound()

    #Label(checkingWindow, text='正在检测体脂', bg='red', fg='yellow').pack(padx=0, pady=10)

    

    checkingWindow = Toplevel(userUpdateFrame,  bg='yellow')
    checkingWindow.geometry("1280x770+10+140")
    #checkingWindow.Toplevel.resizable(1280, 770)
    checkingWindow.overrideredirect(False)#去掉窗口标题=True
    #checkingWindow.attributes("-alpha", 0.1)
    checkingWindow.attributes('-topmost', 'true')

    #Label(checkingWindow, text='正在检测体脂', bg='red', fg='yellow').pack(padx=0, pady=10)
    checkingLabel = Label(checkingWindow, text="正在检测中。", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)

    def DoClose(state):
        UpdatecCanvas(state)
        checkingWindow.destroy()
        checkingWindow.update()


    
    state['BodyFat'] = 'red'
    skin_Button= Button(checkingWindow, text="关闭检测", width=38, height=3, font="宋体 20 bold", command=lambda: DoClose(state)) 
    skin_Button.place(x=300, y=600)
    
    ###启动串口接受身高体重体脂程序
    file = "体脂检测.exe"
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(file, startupinfo=startupinfo)
    ####
    DoCheckFile()
    print("observer8")

    bodyfatData = GetBodyFatResult()
    
    checkingLabel = Label(checkingWindow, text="结果如下：  ", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)
    checkingLabel = Label(checkingWindow, text=bodyfatData, width=20, height=4, anchor='w', bg='yellow', font="宋体 30 bold")
    checkingLabel.place(x=300, y=400)

    bodyfatData = bodyfatData.split('\n')
    ##体重
    userBodyData_lift = Label(userUpdateFrame, text=bodyfatData[1], anchor='w',width=20,  bg='white', height=1, font="宋体 14 bold")
    userBodyData_lift.place(x=100, y=300)
    ##身高
    userBodyData_lift = Label(userUpdateFrame, text=bodyfatData[0], anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
    userBodyData_lift.place(x=160, y=480)
    #体脂
    userBodyData_lift = Label(userUpdateFrame, text=bodyfatData[2], anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
    userBodyData_lift.place(x=160, y=500)

    ProcessTime(checkingWindow,10)#10秒进度条
    
    checkingWindow.destroy()
    state['BodyFat'] = 'red'
    UpdatecCanvas(state)
    
    flag.set(False)

def DoBloodfatCheck():
    print('DoBloodfatCheck')
    print(flag.get())
    if flag.get() == False:
        flag.set(True)
    else:
        return 0
    state['Bloodfat'] = 'green'
    UpdatecCanvas(state)

    
    checkingWindow = Toplevel(userUpdateFrame,  bg='yellow')
    checkingWindow.geometry("1280x770+10+140")
    #checkingWindow.Toplevel.resizable(1280, 770)
    checkingWindow.overrideredirect(False)#去掉窗口标题=True
    #checkingWindow.attributes("-alpha", 0.1)
    checkingWindow.attributes('-topmost', 'true')
    
    #Label(checkingWindow, text='正在检测体脂', bg='red', fg='yellow').pack(padx=0, pady=10)
    checkingLabel = Label(checkingWindow, text="1正在检测中。", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)

    state['Bloodfat'] = 'red'
    skin_Button= Button(checkingWindow, text="关闭检测", width=38, height=3, font="宋体 20 bold", command=lambda: DoClose(state)) 
    skin_Button.place(x=600, y=800)
    def DoClose(state):
        UpdatecCanvas(state)
        checkingWindow.destroy()
        checkingWindow.update()

    
def DoBloodPressureCheck():

    ###其他按键未进行活动
    if flag.get() == False:
        flag.set(True)
    else:
        return 0
    print(flag.get())
    ####

    ###更新状态窗口
    state['BloodPressure'] = 'green'
    UpdatecCanvas(state)
    ####

    checkingWindow = Toplevel(userUpdateFrame,  bg='yellow')
    checkingWindow.geometry("1280x770+10+140")
    #checkingWindow.Toplevel.resizable(1280, 770)
    checkingWindow.overrideredirect(False)#去掉窗口标题=True
    #checkingWindow.attributes("-alpha", 0.1)#透明度设置
    checkingWindow.attributes('-topmost', 'true')
    
    checkingLabel = Label(checkingWindow, text="正在检测血压中。", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)

    
    def DoClose(state):
        UpdatecCanvas(state)
        checkingWindow.destroy()
        checkingWindow.update()


    
    
    skin_Button= Button(checkingWindow, text="关闭检测", width=38, height=3, font="宋体 20 bold", command=lambda: DoClose(state)) 
    skin_Button.place(x=300, y=600)

    restart_Button= Button(checkingWindow, text="重新测试", width=38, height=3, font="宋体 16 bold", command=lambda: DoClose(state)) 
    restart_Button.place(x=300, y=450)

    state['BloodPressure'] = 'red'


    ###执行功能
    file = "血压仪.exe"
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(file, startupinfo=startupinfo)
    ####
    DoCheckFile()
    ####


 
    
    checkingLabel = Label(checkingWindow, text="结果如下：  ", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)
    checkingLabel = Label(checkingWindow, text=GetBloodPressureResult(), width=20, height=4, anchor='w', bg='yellow', font="宋体 30 bold")
    checkingLabel.place(x=300, y=400)
    userBodyData_lift = Message(userUpdateFrame, text=GetBloodPressureResult(), aspect='1500', bg='white', font="宋体 14 bold")
    userBodyData_lift.place(x=95, y=340)

    
    flag.set(False)

def DoSkinCheck():
    state['DoSkin'] = 'green'
    UpdatecCanvas(state)


    checkingWindow = Toplevel(userUpdateFrame,  bg='yellow')
    checkingWindow.geometry("1280x770+10+140")
    #checkingWindow.Toplevel.resizable(1280, 770)
    checkingWindow.overrideredirect(False)#去掉窗口标题=True
    checkingWindow.attributes("-alpha", 1)
    #Label(checkingWindow, text='正在检测体脂', bg='red', fg='yellow').pack(padx=0, pady=10)
    checkingLabel = Label(checkingWindow, text="正在检测中。", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)

    state['DoSkin'] = 'red'
    skin_Button= Button(checkingWindow, text="关闭检测", width=38, height=3, font="宋体 20 bold", command=lambda: DoClose(state)) 
    skin_Button.place(x=600, y=800)
    def DoClose(state):
        UpdatecCanvas(state)
        checkingWindow.destroy()
        checkingWindow.update()

def DoTakePhoto():
    state['TakePhoto'] = 'green'
    UpdatecCanvas(state)


    checkingWindow = Toplevel(userUpdateFrame,  bg='yellow')
    checkingWindow.geometry("1280x770+10+140")
    #checkingWindow.Toplevel.resizable(1280, 770)
    checkingWindow.overrideredirect(False)#去掉窗口标题=True

    #Label(checkingWindow, text='正在检测体脂', bg='red', fg='yellow').pack(padx=0, pady=10)
    checkingLabel = Label(checkingWindow, text="正在检测中。", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)


    state['TakePhoto'] = 'red'
    skin_Button= Button(checkingWindow, text="关闭检测", width=38, height=3, font="宋体 20 bold", command=lambda: DoClose(state)) 
    skin_Button.place(x=600, y=800)
    def DoClose(state):
        UpdatecCanvas(state)
        checkingWindow.destroy()
        checkingWindow.update()

    
def DoInfraredRay():
    state['InfraredRay'] = 'green'
    UpdatecCanvas(state)

    checkingWindow = Toplevel(userUpdateFrame,  bg='yellow')
    checkingWindow.geometry("1280x770+10+140")
    #checkingWindow.Toplevel.resizable(1280, 770)
    checkingWindow.overrideredirect(False)#去掉窗口标题=True

    #Label(checkingWindow, text='正在检测体脂', bg='red', fg='yellow').pack(padx=0, pady=10)
    checkingLabel = Label(checkingWindow, text="正在检测中。", width=20, height=1, anchor='w', bg='yellow', font="宋体 50 bold")
    checkingLabel.place(x=300, y=300)


    state['InfraredRay'] = 'red'
    skin_Button= Button(checkingWindow, text="关闭检测", width=38, height=3, font="宋体 20 bold", command=lambda: DoClose(state)) 
    skin_Button.place(x=600, y=800)
    def DoClose(state):
        UpdatecCanvas(state)
        checkingWindow.destroy()
        checkingWindow.update()

######################################################################################################################################################################################################################################################################
#获取用户基本信息   "姓名："+"\t性别："+"\t年龄："+"\t电话："
def ReadUserBasicData():
    fileName = '用户基本信息.txt'
    fpath = os.path.abspath('.')+PATHPACKAGE+'\\'+fileName
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r')
        with fileData as f:
            strData = f.read()

        strData = strData.replace("\n","\t\t\t")
        #print (strData)
        #print (fpath)
        return strData

#获取效果、医嘱信息
def ReadUserEffectData():
    fileName = '用户效果医嘱信息.txt'
    fpath = os.path.abspath('.')+PATHPACKAGE+'\\'+fileName
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r')
        with fileData as f:
            strData = f.read()
        print (strData)
        #print (fpath)
        return strData



#获取理疗技师及站点信息
def ReadNursePractitionerData():
    fileName = '技师及站点.txt'
    fpath = os.path.abspath('.')+PATHPACKAGE+'\\'+fileName
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r')
        with fileData as f:
            strData = f.read()

        strData = strData.replace("\n","\t\t\t\t\t\t\t\t\t")
        #print (strData)
        #print (fpath)
        return strData



def GetBodyData():
    fileName = '身体检测数据.txt'
    fpath = os.path.abspath('.')+PATHPACKAGE+'\\'+fileName
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r')
        with fileData as f:
            strData = f.read()+"\n"
        #print (strData)
        #print (fpath)
        return strData


def GetBodyOtherData():
    fileName = '身体检测其他数据.txt'
    fpath = os.path.abspath('.')+PATHPACKAGE+'\\'+fileName
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r')
        with fileData as f:
            strData = f.read()+"\n"
        print (strData)
        print (fpath)
        return strData





#####################################################################################################################################################################################################################################################################

#用户信息整体背景框
userDataFrame = Frame(doWindow, bg='silver', width=1280, height=1080) 
userDataFrame.place(x=10, y=10)


usedDataLabel = Label(userDataFrame, text="生理状态检查表（病历）", width=85, height=1, anchor='center', bg='white', font="宋体 20 bold")
usedDataLabel.place(x=0, y=0)

usedDataLabel = Label(userDataFrame, text="客户编号：", width=200, height=1, anchor='w', bg='white', font="宋体 10 bold")
usedDataLabel.place(x=0, y=30)
usedDataLabel = Label(userDataFrame, text="第一次", width=200, height=1, anchor='w', bg='white', font="宋体 10 bold")
usedDataLabel.place(x=1220, y=30)


usedDataBasicStr = "姓名："+"\t性别："+"\t年龄："+"\t电话："+"\n以往状态："
usedDataBasicStr = ReadUserBasicData()
usedDataLabel = Label(userDataFrame, text=usedDataBasicStr, width=180, height=1, anchor='nw', bg='white', font="宋体 12 bold")
usedDataLabel.place(x=0, y=55)
usedDataLabel = Label(userDataFrame, text="以往状态：", width=180, height=1, anchor='nw', bg='white', font="宋体 12 bold")
usedDataLabel.place(x=0, y=75)




#用户实时信息，中部框
userUpdateFrame = Frame(userDataFrame, bg='white', width=1280, height=770) 
userUpdateFrame.place(x=0, y=105)
#
usedDataLabel_lift = Label(userUpdateFrame, text="理疗前状态", width=30, height=1, anchor='center', bg='white', font="宋体 14 bold")
usedDataLabel_lift.place(x=100, y=10)

#开始时间
startTime = '时间：'+TimeShow()
usedTimeLabel_lift = Label(userUpdateFrame, text=startTime, width=36, height=1, anchor='center', bg='white', font="宋体 10 bold")
usedTimeLabel_lift.place(x=100, y=40)


usedDataLabel_right = Label(userUpdateFrame, text="理疗后状态", width=30, height=1, anchor='center', bg='white', font="宋体 14 bold")
usedDataLabel_right.place(x=700, y=10)
#结束时间
endTime = '时间：'+TimeShow()
usedTimeLabel_right = Label(userUpdateFrame, text=endTime, width=36, height=1, anchor='center', bg='white', font="宋体 10 bold")
usedTimeLabel_right.place(x=700, y=40)
#用户头像框
userImgFrame_lift = Frame(userUpdateFrame, bg='white', width=336, height=168 ,relief='groove',bd=1)  #凹槽：relief，  边框宽度bd
userImgFrame_lift.place(x=100, y=60)
userImgFrame_right = Frame(userUpdateFrame, bg='white', width=336, height=168  ,relief='groove',bd=1)
userImgFrame_right.place(x=700, y=60)

#显示用户头像-左边
imgPath_lift = PATHPACKAGE+'\\'+IMGFILE_LIFT
if os.path.isfile(imgPath_lift) :
    imgOpen_lift = Image.open(imgPath_lift)
    img_lift = ImageTk.PhotoImage(imgOpen_lift)
else:
    img_lift=''
userImgLabel_lift = Label(userImgFrame_lift, image=img_lift, anchor='center')
userImgLabel_lift.place(x=0, y=0)

#显示用户头像-右边

imgPath_righ = PATHPACKAGE+'\\'+IMGFILE_RIGHT
if os.path.isfile(imgPath_righ) :
    imgOpen_right = Image.open(imgPath_righ)
    img_right = ImageTk.PhotoImage(imgOpen_right)
else:
    img_right=''
userImgLabel_right = Label(userImgFrame_right, image=img_right, anchor='center')
userImgLabel_right.place(x=0, y=0)
#在左边显示身体检测信息
userBodyDataStr_lift = GetBodyData()
##userBodyData_lift = Message(userUpdateFrame, text=userBodyDataStr_lift, aspect='150', bg='white', font="宋体 14 bold")
##userBodyData_lift.place(x=100, y=300)

userBodyData_lift = Label(userUpdateFrame, text="体重：", anchor='w',width=20,  bg='white', height=1, font="宋体 14 bold")
userBodyData_lift.place(x=100, y=300)

userBodyData_lift = Label(userUpdateFrame, text="补充：", anchor='w',width=20,  bg='white', height=1, font="宋体 14 bold")
userBodyData_lift.place(x=100, y=320)

userBodyData_lift = Message(userUpdateFrame, text="收缩压：\n扩张压：\n心率：", aspect='1500', bg='white', font="宋体 14 bold")
userBodyData_lift.place(x=95, y=340)

userBodyData_lift = Label(userUpdateFrame, text="血糖：", anchor='w',width=20,  bg='white', height=1, font="宋体 14 bold")
userBodyData_lift.place(x=100, y=400)


userBodyData_lift = Label(userUpdateFrame, text="其他：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=100, y=460)

userBodyData_lift = Label(userUpdateFrame, text="身高：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=480)
userBodyData_lift = Label(userUpdateFrame, text="体脂：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=500)
userBodyData_lift = Label(userUpdateFrame, text="水分：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=520)
userBodyData_lift = Label(userUpdateFrame, text="肌肉值：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=540)
userBodyData_lift = Label(userUpdateFrame, text="骨骼量：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=560)
userBodyData_lift = Label(userUpdateFrame, text="卡路里：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=580)
userBodyData_lift = Label(userUpdateFrame, text="BMI值：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=600)
userBodyData_lift = Label(userUpdateFrame, text="脉搏：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=620)
userBodyData_lift = Label(userUpdateFrame, text="血氧：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyData_lift.place(x=160, y=640)

##userBodyOtherDataStr_lift = GetBodyOtherData()
##userBodyOtherData_lift = Message(userUpdateFrame, text=userBodyOtherDataStr_lift, aspect='150', bg='white', font="宋体 12 bold")
##userBodyOtherData_lift.place(x=100, y=460)




#在右边显示身体检测信息


userBodyData_right = Label(userUpdateFrame, text="体重：", anchor='w',width=20,  bg='white', height=1, font="宋体 14 bold")
userBodyData_right.place(x=700, y=300)

userBodyData_right = Label(userUpdateFrame, text="补充：", anchor='w',width=20,  bg='white', height=1, font="宋体 14 bold")
userBodyData_right.place(x=700, y=320)

userBodyData_right = Message(userUpdateFrame, text="收缩压：\n扩张压：\n心率：", aspect='1500', bg='white', font="宋体 14 bold")
userBodyData_right.place(x=695, y=340)

userBodyData_right = Label(userUpdateFrame, text="血糖：", anchor='w',width=20,  bg='white', height=1, font="宋体 14 bold")
userBodyData_right.place(x=700, y=400)



##userBodyDataStr_right = GetBodyData()
##userBodyData_right = Message(userUpdateFrame, text=userBodyDataStr_right,aspect='1500', bg='white', font="宋体 14 bold")
##userBodyData_right.place(x=700, y=300)
##
##userBodyOtherDataStr_right = GetBodyOtherData()
##userBodyOtherData_right = Message(userUpdateFrame, text=userBodyOtherDataStr_right, aspect='150', bg='white', font="宋体 12 bold")
##userBodyOtherData_right.place(x=700, y=460)

userBodyOtherData_right = Label(userUpdateFrame, text="其他：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=700, y=460)

userBodyOtherData_right = Label(userUpdateFrame, text="身高：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=480)
userBodyOtherData_right = Label(userUpdateFrame, text="体脂：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=500)
userBodyOtherData_right = Label(userUpdateFrame, text="水分：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=520)
userBodyOtherData_right = Label(userUpdateFrame, text="肌肉值：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=540)
userBodyOtherData_right = Label(userUpdateFrame, text="骨骼量：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=560)
userBodyOtherData_right = Label(userUpdateFrame, text="卡路里：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=580)
userBodyOtherData_right = Label(userUpdateFrame, text="BMI值：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=600)
userBodyOtherData_right = Label(userUpdateFrame, text="脉搏：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=620)
userBodyOtherData_right = Label(userUpdateFrame, text="血氧：", anchor='w',width=20,  bg='white', height=1, font="宋体 12 bold")
userBodyOtherData_right.place(x=760, y=640)



#显示效果医嘱
UserEffectStr = ReadUserEffectData()
usedDataLabel = Label(userDataFrame, text=UserEffectStr, width=160, height=10, anchor='nw', bg='white', font="宋体 14 bold")
usedDataLabel.place(x=0, y=883)
usedDataLabel = Message(userDataFrame, text=UserEffectStr, aspect='1500', bg='white', font="宋体 14 bold")
usedDataLabel.place(x=0, y=883)
#显示底部理疗师和站点
NursePractitionerData = ReadNursePractitionerData()
usedDataLabel = Label(userDataFrame, text=NursePractitionerData, width=160, height=1, anchor='nw', bg='white', font="宋体 12")
usedDataLabel.place(x=0, y=990)


#用户操作背景框
userOperationFrame = Frame(doWindow, bg='white', width=600, height=1080) 
userOperationFrame.place(x=1300, y=10)

word_2=Label(userOperationFrame, text='用户操作区', width=38, height=1, font="宋体 20 bold")
word_2.place(x=10, y=10)


body_fat_Button= Button(userOperationFrame, text="体脂检测", width=38, height=3, font="宋体 20 bold", command=DoBodyFatCheck) 
body_fat_Button.place(x=10, y=80)

blood_fat_Button= Button(userOperationFrame, text="血脂检测", width=38, height=3, font="宋体 20 bold", command=DoBloodfatCheck) 
blood_fat_Button.place(x=10, y=230)

blood_pressure_Button= Button(userOperationFrame, text="血压检测", width=38, height=3, font="宋体 20 bold", command=DoBloodPressureCheck) 
blood_pressure_Button.place(x=10, y=380)

skin_Button= Button(userOperationFrame, text="皮肤检测", width=38, height=3, font="宋体 20 bold", command=DoSkinCheck) 
skin_Button.place(x=10, y=530)

take_photo_Button= Button(userOperationFrame, text="照相", width=38, height=3, font="宋体 20 bold", command=DoTakePhoto) 
take_photo_Button.place(x=10, y=680)

infrared_ray_Button= Button(userOperationFrame, text="红外检测", width=38, height=3, font="宋体 20 bold", command=DoInfraredRay) 
infrared_ray_Button.place(x=10, y=830)

##show_Button= Button(userOperationFrame, text="打印结果", width=38, height=3, font="宋体 20 bold", command=DoBodyFat) 
##show_Button.place(x=10, y=980)





"""
Button      #按钮控件；在程序中显示按钮。

Checkbutton=    #多选框控件；用于在程序中提供多项选择框

Entry=      #输入控件；用于显示简单的文本内容

Frame=          #架控件；在屏幕上显示一个矩形区域，多用来作为容器


Message=            #消息控件；用来显示多行文本，与label比较类似



"""
#####################################################################################################################################################################################################################################################################
###窗口尺寸处理函数
##def WindowResize(event):
##    global save_width
##    global save_height
##
##    new_width = window.winfo_width()
##    new_height = window.winfo_height()
##
##
##    if new_width == 1 and new_height ==1:
##        return
##    
##
##


state = {'BodyFat':"red", 'Bloodfat':"red", 'BloodPressure':"red", 'DoSkin':"red", 'TakePhoto':"red", 'InfraredRay':"red"}

print (os.getcwd())
print (os.path.abspath('.'))
print (os.path.abspath(''))
print (os.path.abspath(os.curdir))



##窗口位于屏幕中间
width = 1920
height = 1080
g_screenwidth = showWindow.winfo_screenwidth()
g_screenheight = showWindow.winfo_screenheight()
alignstr = '%dx%d+%d+0' % (width, height, (g_screenwidth-width)/2,)
showWindow.geometry(alignstr)

#window.geometry("760x1360")    #窗口大小

showWindow.title("显示状态窗口")   #窗口标题
showWindow.config(bg="white")       #窗口背景颜色
#window.overrideredirect(True)      #无边框



def UpdatecCanvas(state):
    # 将画布设置为白色
    canvas_lift = Canvas(showWindow,width = 100,height = 420, bg="white", highlightthickness=0)
    # 设置基准坐标
    x0,y0,x1,y1 = 20,20,90,90
    # 绘制圆形
    oval = canvas_lift.create_oval(x0, y0, x1, y1, fill =state.get('BodyFat'), outline = '', width=2)
    oval = canvas_lift.create_oval(x0, y0+150, x1, y1+150, fill =state.get('Bloodfat'), outline = '', width=2)
    oval = canvas_lift.create_oval(x0, y0+310, x1, y1+310, fill =state.get('BloodPressure'), outline = '', width=2)
    #canvas_lift.pack()
    canvas_lift.place(x=130, y=480)

    canvas_right = Canvas(showWindow,width = 100,height = 420, bg="white", highlightthickness=0)

    oval = canvas_right.create_oval(x0, y0, x1, y1, fill =state.get('DoSkin'), outline = '', width=2)
    oval = canvas_right.create_oval(x0, y0+150, x1, y1+150, fill =state.get('TakePhoto'), outline = '', width=2)
    oval = canvas_right.create_oval(x0, y0+310, x1, y1+310, fill =state.get('InfraredRay'), outline = '', width=2)
    #create_oval(x0, y0, x1, y1, options)	1. 绘制一个圆形或椭圆形；
    #2. 参数 x0 与 y0 定义绘图区域的左上角坐标；参数 x1 与 y1 定义绘图区域的右下角坐标；
    #3. 参数 options 表示其他可选参数
    canvas_right.place(x=1135, y=480)

def UserData():
    word_1=Label(showWindow, text='病历编号：', width=10, height=3, anchor="n", font="宋体 40 bold")
    word_1.place(x=0, y=10)
    word_1=Label(showWindow, text='姓名：', width=9, height=3, anchor="n", font="宋体 40 bold")
    word_1.place(x=300, y=10)
    word_1=Label(showWindow, text='性别：', width=9, height=3, anchor="n", font="宋体 40 bold")
    word_1.place(x=570, y=10)
    word_1=Label(showWindow, text='年龄：', width=9, height=3, anchor="n", font="宋体 40 bold")
    word_1.place(x=840, y=10)
    word_1=Label(showWindow, text='电话:', width=9, height=3, anchor="n", font="宋体 40 bold")
    word_1.place(x=1110, y=10)
    word_1=Label(showWindow, text='管理员:', width=9, height=3, anchor="n", font="宋体 40 bold")
    word_1.place(x=1380, y=10)
    word_1=Label(showWindow, text=' ', width=10, height=3, anchor="n", font="宋体 40 bold")
    word_1.place(x=1650, y=10)

    infrared_ray_Button= Button(showWindow, text="翻看历史数据", width=12, height=1,font="宋体 30 bold") 
    infrared_ray_Button.place(x=1650, y=10)


'''
font参数用于设置文字字形，这个参数包含下列内容:
字形family：如Helvetica、Times等，可以进入Word内参考所有系统字形。
字号size：单位是像素
weight：例如bold、normal。
slant：例如italic、roman，如果不是italic则是roman。
underline：例如True、False。
overstrike：例如True、False。

anchor
锚点，用来指定文本或图像在label显示区的显示位置。
默认值是"center"，
可设置的值为’n’, ‘ne’, ‘e’, ‘se’, ‘s’, ‘sw’, ‘w’, ‘nw’; ‘e’、‘w’、‘s’、'n’分别表示东西南北。

'''


def UseButton():
    word_1=Label(showWindow, text='使用后数据', width=34, height=3, font="宋体 40 bold")
    word_1.place(x=0, y=200)

    word_1=Label(showWindow, text='使用前数据', width=34, height=3,  font="宋体 40 bold")
    word_1.place(x=970, y=200)

    Button_2= Button(showWindow, text="按键1", width=13, height=2,font="宋体 12 bold") 
    Button_2.place(x=0, y=230)

    Button_3= Button(showWindow, text="按键2", width=13, height=2,font="宋体 12 bold") 
    Button_3.place(x=970, y=230)


def ProjectList():
    word_2=Label(showWindow, text='第一步：体脂检测', width=15, height=1, font="宋体 40 bold")
    word_2.place(x=270, y=500)

    word_2=Label(showWindow, text='第二步：血脂检测', width=15, height=1, font="宋体 40 bold")
    word_2.place(x=270, y=655)

    word_2=Label(showWindow, text='第三步：血压检测', width=15, height=1, font="宋体 40 bold")
    word_2.place(x=270, y=820)

    word_2=Label(showWindow, text='第四步：皮肤检测', width=15, height=1, font="宋体 40 bold")
    word_2.place(x=1270, y=500)

    word_2=Label(showWindow, text='第五步：照相检测', width=15, height=1, font="宋体 40 bold")
    word_2.place(x=1270, y=655)

    word_2=Label(showWindow, text='第六步：红外检测', width=15, height=1, font="宋体 40 bold")
    word_2.place(x=1270, y=820)




"""
Button      #按钮控件；在程序中显示按钮。

Checkbutton=    #多选框控件；用于在程序中提供多项选择框

Entry=      #输入控件；用于显示简单的文本内容

Frame=          #架控件；在屏幕上显示一个矩形区域，多用来作为容器


Message=            #消息控件；用来显示多行文本，与label比较类似


"""
def UpdataFunc():
    return 0

def LoopMonitor():
    t = Timer(10, UpdataFunc)
    t.start()
    
    LoopMonitor()


def Close(): #关闭两个窗口
    doWindow.destroy()
    showWindow.destroy()
    
if __name__ == '__main__':
    #LoopMonitor()

    UpdatecCanvas(state)
    ProjectList()
    UserData()
    UseButton()


 
doWindow.protocol("WM_DELETE_WINDOW", Close)#只要其中一个窗口关闭,就同时关闭两个窗口
showWindow.protocol("WM_DELETE_WINDOW", Close)#只要其中一个窗口关闭,就同时关闭两个窗口
##
doWindow.mainloop()
showWindow.mainloop()




 


















