import tkinter
import threading
import os,sys
import datetime
from tkinter import *
from PIL import Image, ImageTk
import time
import cv2

menber = 1
cameraUrl = ""
volumeValue = 22


def DoBodyFatCheck():
    pass
def DoShowOther():
    global menber
    if menber < 5:
        menber = menber + 1
    else:
        menber = 1
    textMenber = '学憩仓-' + str(menber)
    word_2=Label(window, text=textMenber, width=72, bg="yellow",height=2, font="宋体 20 bold")
    word_2.place(x=0, y=1000)


def SetVolume(value):
    global volumeValue
    if volumeValue > 0 and volumeValue < 100:
        volumeValue = volumeValue + int(value)
    elif volumeValue == 0 and int(value)>0:
        volumeValue = volumeValue + int(value)
    elif volumeValue == 100 and int(value)<0:   
        volumeValue = volumeValue + int(value)

    textVolume = str(volumeValue)
    word_1=Label(window, text=textVolume, width=8, height=3, anchor="center",bg="deepskyblue", fg="white", relief ="ridge", font="宋体 24 bold")
    word_1.place(x=450, y=1750)
################################################################################################################################################################

window=Tk()

##窗口位于屏幕中间
width = 1080
height = 1920
g_screenwidth = window.winfo_screenwidth()
g_screenheight = window.winfo_screenheight()
alignstr = '%dx%d+%d+0' % (width, height, g_screenwidth,)
window.geometry(alignstr)

#window.geometry("760x1360")    #窗口大小

window.title("学憩仓操作界面")   #窗口标题
window.config(bg="skyblue")       #窗口背景颜色


######################################################################################################################################################################################################################################################################
#监控区
canvas = Canvas(window, width=1080, height=1000, bg='black')
canvas.pack() 

cap = cv2.VideoCapture("VID.mp4")
def photo_image(img):
    h, w = img.shape[:2]
    data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
    return PhotoImage(width=w, height=h, data=data, format='PPM')

def update():
    ret, img = cap.read()
    if ret:
        photo = photo_image(img)
        canvas.create_image(0, 0, image=photo, anchor=NW)
        canvas.image = photo
    window.after(1, update)

####################################################################################################################
#操作区
userOperationFrame = Frame(window, bg='white', width=600, height=1080) 
userOperationFrame.place(x=1300, y=10)

word_2=Label(window, text='学憩仓-1', width=72, bg="yellow",height=2, font="宋体 20 bold")
word_2.place(x=0, y=1000)

body_fat_Button= Button(window, text="切换学憩仓", width=38, height=3, font="宋体 20 bold", command=DoShowOther) 
body_fat_Button.place(x=230, y=1150)

blood_fat_Button= Button(window, text="播放视频", width=38, height=3, font="宋体 20 bold", command=DoBodyFatCheck) 
blood_fat_Button.place(x=230, y=1300)

blood_fat_Button= Button(window, text="视频-1", width=8, height=3, font="宋体 20 bold", command=DoBodyFatCheck) 
blood_fat_Button.place(x=230, y=1450)

blood_fat_Button= Button(window, text="视频-2", width=8, height=3, font="宋体 20 bold", command=DoBodyFatCheck) 
blood_fat_Button.place(x=380, y=1450)

blood_fat_Button= Button(window, text="视频-3", width=8, height=3, font="宋体 20 bold", command=DoBodyFatCheck) 
blood_fat_Button.place(x=530, y=1450)

blood_fat_Button= Button(window, text="视频-4", width=8, height=3, font="宋体 20 bold", command=DoBodyFatCheck) 
blood_fat_Button.place(x=680, y=1450)


take_photo_Button= Button(window, text="启动对话", width=38, height=3, font="宋体 20 bold", command=DoBodyFatCheck) 
take_photo_Button.place(x=230, y=1600)

blood_pressure_Button= Button(window, text="音量 + ", width=8, height=3, font="宋体 20 bold", command=lambda: SetVolume("+1")) 
blood_pressure_Button.place(x=230, y=1750)

skin_Button= Button(window, text="音量 - ", width=8, height=3, font="宋体 20 bold", command=lambda: SetVolume("-1")) 
skin_Button.place(x=680, y=1750)

word_1=Label(window, text='22', width=8, height=3, anchor="center",bg="deepskyblue", fg="white", relief ="ridge", font="宋体 24 bold")
word_1.place(x=450, y=1750)

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
#窗口尺寸处理函数
update()
window.mainloop()
cap.release()
