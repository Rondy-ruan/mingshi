# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# ============================================================
# @Date    : 2022/12/29
# @Author  : rondy
# @File    : doBodyFatCheck.py
# @IDE     : 
# @Func    : 通过串口接受身高体重体脂数据，并写入文件
# ============================================================
"""
import time
import serial.tools.list_ports
import os,sys

PATHPACKAGE = '\\newpackage\\'

def SaveUserData(save_result):
    fileName = '体脂结果.txt'
    fpathDir = os.path.abspath('.')+PATHPACKAGE
    fpath = os.path.abspath('.')+PATHPACKAGE+fileName
    ###判断文件夹是否存在
    if os.path.exists(fpathDir):
        pass
    else:
        os.mkdir(fpathDir) #创建文件夹
    ####
    print(fpath)
    fileData = open(fpath, 'w')


    userData = save_result 
    fileData.writelines(userData)
    
    print(userData)
    fileData.close()   


def GetPort():

    fileName = 'config.ini'
    fpath = os.path.abspath('.')+'\\'+fileName
    print(fpath)
    if os.path.isfile(fpath) :#判断文件是否存在
        fileData = open(fpath, 'r', encoding='utf-8')  
        strData = fileData.read()
        print (strData)
        
        for line in strData.split('\n'):
            print(line)
            if 'BodyFatPort' in line:
                bodyFatPort =   line[14:18]           #BodyFatPort = COM6
                fileData.close()
                return bodyFatPort      #COM6
    return 0  #没有配置好的串口

def StartDoBodyFat():

        port_num = GetPort()

        if port_num == 0:
            # 读取串口列表
            ports_list = list(serial.tools.list_ports.comports())
            if len(ports_list) <= 0:
                print("无串口设备")
                return 0
            else:
                print("可用的串口设备如下: ")
                print("%-10s %-30s %-10s" % ("num", "name", "number"))
                for i in range(len(ports_list)):
                    comport = list(ports_list[i])
                    comport_number, comport_name = comport[0], comport[1]
                    print("%-10s %-30s %-10s" % (i, comport_name, comport_number))
            port_num = ports_list[0][0]


    
        print("默认选择串口: %s" % port_num)
        # 串口号: port_num, 波特率: 115200, 数据位: 8, 停止位: 1, 超时时间: 1秒

        ser = serial.Serial(port=port_num, baudrate=9600, bytesize=8, timeout=1, stopbits=1)
        if ser.isOpen():
            print("打开串口成功, 串口号: %s" % ser.name)
        else:
            print("打开串口失败")
 


        # 等待串口返回信息并输出

        while True:
            time.sleep(1)

            com_output =str(ser.readline()) 

            if len(com_output) > 10 :
                
                #print("output:\n%s" % com_output)       #b'\x1c&\x02@6045167550000000000000000000001850000A\x0c\x03'
                Data =str(com_output[2:-1]).split('@')[1]

                #print("Data: %s" % Data)       #604517550000000000000000000001850000A\x0c\x03
                
                heightData = Data[4:7] +"." +Data[8] +" CM"
                weightData = Data[0:2] +"." +Data[2:4] +" KG"
                bodyfatData = Data[29:31] +"." +Data[31:33]+ "%"
                print("身高：%s" % heightData)
                print("体重：%s" % weightData)
                print("体脂：%s" % bodyfatData)
                save_result = "身高：\t\t" +heightData +"\n" +"体重：\t\t" +weightData+"\n"+"体脂：\t\t"+bodyfatData                
                SaveUserData(save_result)   #保存数据到文件
                break

        ser.close()
        
        if ser.isOpen():
            print("串口未关闭")
        else:
            print("串口已关闭")



if __name__ == '__main__':
    StartDoBodyFat()

