# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# ============================================================
# @Date    : 2022/12/24
# @Author  : rondy
# @File    : doBloodPressure.py
# @IDE     : 
# @Func    : 通过串口命令启动血压仪，并接收对应的结果，然后写入文件中
# ============================================================
"""
import time
import binascii
import serial.tools.list_ports
import os,sys


g_save_result = ""      #fffe0a932155007900504a00
PATHPACKAGE = '\\newpackage\\'



def GetPort():

    fileName = 'config.ini'
    fpath = os.path.abspath('.')+'\\'+fileName
    print(fpath)
    if os.path.isfile(fpath) :
        fileData = open(fpath, 'r', encoding='utf-8')  
        strData = fileData.read()
        print (strData)
        
        for line in strData.split('\n'):
            #print(line)
            if 'BloodPressurePort ' in line:
                bloodPressurePort =   line[20:24]           #BloodPressurePort = COM6
                fileData.close()
                return bloodPressurePort      #COM6
    return 0  #没有配置好的串口

def SaveUserData(save_result):
    fileName = '血压结果.txt'
    fpath = os.path.abspath('.')+PATHPACKAGE+fileName

    
    ###判断文件夹是否存在
    fpathDir = os.path.abspath('.')+PATHPACKAGE
    if os.path.exists(fpathDir):
        pass
    else:
        os.mkdir(fpathDir) #创建文件夹
    ####

    print(fpath)
    fileData = open(fpath, 'w')

    high_pressure = "收缩压：\t"+str(int(save_result[14:16], base=16))+' mmHg'
        
    low_pressure =  "扩张压：\t"+str(int(save_result[18:20], base=16))+' mmHg'               

    pulse ="心率：\t"+ str(int(save_result[20:22], base=16))+' 次/分'

    userData = high_pressure+'\n'+low_pressure+'\n'+pulse
    fileData.writelines(userData)
    
    print(high_pressure)
    print(low_pressure)
    print(pulse)
    print(userData)
    fileData.close()    

def ShowResult(save_result): #fffe0a932155007900504a00 ,
    
    if save_result == "":
        return 0
    #高压
    high_pressure = int(save_result[14:16], base=16)
    print("高压:%d mmHg" % high_pressure)
    #低压
    low_pressure = int(save_result[18:20], base=16)
    print("低压:%d mmHg" % low_pressure)
    #脉搏
    pulse = int(save_result[20:22], base=16)
    print("脉搏:%d 次/分" % pulse)
    SaveUserData(save_result)

def StartDoBloodPressure():
    global g_save_result
    
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
 
        # 打开串口
        
        port_num = GetPort()
        print("get:%s" % port_num)
        if port_num == 0:
            port_num = ports_list[0][0]
        print("默认选择:%s" % port_num)
        print("默认选择串口: %s" % port_num)
        # 串口号: port_num, 波特率: 115200, 数据位: 7, 停止位: 2, 超时时间: 0.5秒
##        ser = serial.Serial(port=port_num, baudrate=9600, bytesize=serial.SEVENBITS, stopbits=serial.STOPBITS_TWO,
##                            timeout=0.5)

        ser = serial.Serial(port=port_num, baudrate=9600, bytesize=8, timeout=50, stopbits=1)
        if ser.isOpen():
            print("打开串口成功, 串口号: %s" % ser.name)
        else:
            print("打开串口失败")
 
        # 串口发送数据
        data_a = 'FF FE 04 A5 01 A0'
        print("发送数据: ")
        print(data_a)
        # 简单的发送16进制字符
        # ser.write(b'\xFE\xFE\xFE')
        data_d=bytes.fromhex(data_a)
        write_len = ser.write(data_d)
        print("串口发出{}个字节".format(write_len))

        show_size = 6 # the first line
        # 等待串口返回信息并输出
        t0 = time.time()
        while True:
            com_input = ser.read(show_size)
            t1 = time.time()
            t = t1 - t0
            #print("\r等待串口接收数据, %.2f 秒" % t, end="")
            if com_input or t >= 3:
##            if com_input:
                print("receive",str(binascii.b2a_hex(com_input))[2:-1])
                if len(str(binascii.b2a_hex(com_input))[2:-1]) == 4:
                    g_save_result = g_save_result[20:40] + str(binascii.b2a_hex(com_input))[2:-1]
                else:
                    g_save_result = str(binascii.b2a_hex(com_input))[2:-1]
                show_size = 20
                if len(g_save_result) == 24:
                    print("已经接受完数据了")
                    break
                #print("\n%s" % com_input)
            else:
                print("\n%s" % "没有接收到任何数据")
                
#        com_input = ser.read_all()
        # 关闭串口
        ser.close()
        if ser.isOpen():
            print("串口未关闭")
        else:
            print("串口已关闭")
        
        ShowResult(g_save_result)


if __name__ == '__main__':
    StartDoBloodPressure()
    #SaveUserData(g_save_result)
