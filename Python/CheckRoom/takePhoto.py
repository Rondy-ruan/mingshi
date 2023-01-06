"""
# ============================================================
# @Date    : 2023/01/06
# @Author  : rondy
# @File    : takePhoto.py
# @IDE     : 
# @Func    : 调用本地摄像头拍照并保存成图片
# ============================================================
"""

import os                                  
import cv2
import time

PATHPACKAGE = '.\\newpackage\\'
g_imgFileName = 'l.jpg'

def get_photo():
    cap = cv2.VideoCapture(0)           # 开启摄像头
    f, frame = cap.read()               # 将摄像头中的一帧图片数据保存
    file = PATHPACKAGE + g_imgFileName
    cv2.imwrite(file, frame)     # 将图片保存为本地文件
    cap.release()                       # 关闭摄像头
 
if __name__ == '__main__':
    get_photo()
