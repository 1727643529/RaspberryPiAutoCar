# coding:utf-8

# 加入摄像头模块，让小车实现自动循迹行驶
# 思路为：摄像头读取图像，进行二值化，将白色的赛道凸显出来
# 选择下方的一行像素，黑色为0，白色为255
# 找到白色值的中点
# 目标中点与标准中点（320）进行比较得出偏移量
# 根据偏移量来控制小车左右轮的转速
# 考虑了偏移过多失控->停止;偏移量在一定范围内->高速直行(这样会速度不稳定，已删)

import RPi.GPIO as GPIO     #引入RPi.GPIO库函数命名为GPIO
import time
import cv2
import numpy as np

from CleanCache import cleanCache
from Move import right, left, forward

def k_mean_two(black_index, threshold, epochs):  # k_mean algorithm
    if len(black_index) <= 2:
        return 0,0,1
    center1, center2=black_index[0],black_index[-1]
    class1, class2=[],[]
    for i in range(epochs):
        for item in black_index:
            class1.append(item) if abs(item-center1)<abs(item-center2) else class2.append(item)
        if len(class1):
            center1=np.sum(np.array(class1))/len(class1)
        #print("center1",str(center1))
        if len(class2):
            center2=np.sum(np.array(class2))/len(class2)
        #print("center2",str(center2))
        class1=[]
        class2=[]
        if abs(center1-center2)<threshold:
            return center1,center2,1
    return center1,center2,2

state=0
column_threshold = 5   
# center定义
#center = 220
# 打开摄像头，图像尺寸640*480（长*高），opencv存储值为480*640（行*列）
cap = cv2.VideoCapture(0)
while (1):
    ret, frame = cap.read()
    #cv2.imshow("capture", frame)
    #print(frame.shape)#high=480 wide=640 channel=3
    # 转化为灰度图
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # 膨胀，白区域变大
    dst = cv2.dilate(dst, None, iterations=2)
    dst = cv2.erode(dst, None, iterations=6)
    dst = cv2.dilate(dst, None, iterations=2)
    dst = cv2.erode(dst, None, iterations=6)
    dst = cv2.dilate(dst, None, iterations=2)
    dst = cv2.erode(dst, None, iterations=6)
    # # 腐蚀，白区域变小
    # dst = cv2.erode(dst, None, iterations=6)

    color = dst[420][column_threshold:641-column_threshold]  # find 450th row
    black_count = np.sum(color == 0)
    black_index = np.array([i for i,x in enumerate(color) if x==0])  # find all black position
    center1,center2,class_result=k_mean_two(black_index, 100, 3)

    if black_count != 0:
        if class_result == 1:
            if black_index[0] >= 300:
                center1 = 0
            else:
                center2 = 640
        print("center1:", center1)
        print("center2:", center2)
        center = (center1 + center2) / 2#find the center point
        print("the black center is:%d"%center)
        direction_error = center-len(color)/2#circulate the error
        #print("the error is :%d"%direction_error)
        if direction_error > 30:#the car in right,need to turn left
            print('rightrightright')
            right(65)
#            time.sleep(0.2)
            #forward(0)
            #time.sleep(0.5)
            state=1
        elif direction_error < -30:#the car in left,need to turn right
            print('leftleftleft')
            left(65)
#            time.sleep(0.2)
            #forward(0)
            #time.sleep(0.5)
            state=2
        else:
            print('sssssssssssssss')
            forward(35)
            state=3
    else:
        if state==1:
            print('rightrightright')
            right(65)
#            time.sleep(0.2)
            #forward(0)
            #time.sleep(0.5)
        elif state==2:
            print('leftleftleft')
            left(65)
#            time.sleep(0.2)
            #forward(0)
            #time.sleep(0.5)
        elif state==3:
            print('sssssssssssssss')
            forward(35)
 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放清理
cleanCache(cap)
