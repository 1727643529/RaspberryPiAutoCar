import RPi.GPIO as GPIO     #引入RPi.GPIO库函数命名为GPIO
import time
import cv2
import numpy as np

GPIO.setwarnings(False)

# 设置GPIO口为BCM编号规范
GPIO.setmode(GPIO.BCM)      #将GPIO编程方式设置为BCM模式，基于插座引脚编号

# 定义引脚
INT2 = 18                   #将L298 INT2口连接到树莓派Pin18
INT1 = 23                   #将L298 INT1口连接到树莓派Pin23
INT4 = 24                   #将L298 INT4口连接到树莓派Pin24
INT3 = 25                   #将L298 INT3口连接到树莓派Pin25

# 设置GPIO口为输出
GPIO.setup(INT1, GPIO.OUT)
GPIO.setup(INT2, GPIO.OUT)
GPIO.setup(INT3, GPIO.OUT)
GPIO.setup(INT4, GPIO.OUT)

# 设置PWM波,频率为500Hz
motor_l1 = GPIO.PWM(INT1, 500)   #PWM initialization:500HZ
motor_l2 = GPIO.PWM(INT2, 500)   #PWM initialization:500HZ
motor_r1 = GPIO.PWM(INT3, 500)   #PWM initialization:500HZ
motor_r2 = GPIO.PWM(INT4, 500)   #PWM initialization:500HZ

# pwm波控制初始化
motor_l1.start(0)   #motor start
motor_l2.start(0)   #motor start
motor_r1.start(0)   #motor start
motor_r2.start(0)   #motor start


def left(speed):
    motor_l1.ChangeDutyCycle(0)  # speed set range:0~100
    motor_l2.ChangeDutyCycle(0)
    motor_r1.ChangeDutyCycle(0)
    motor_r2.ChangeDutyCycle(speed)


def right(speed):
    motor_l1.ChangeDutyCycle(0)  # speed set range:0~100
    motor_l2.ChangeDutyCycle(speed)
    motor_r1.ChangeDutyCycle(0)
    motor_r2.ChangeDutyCycle(0)


def forward(speed):
    motor_l1.ChangeDutyCycle(0)  # speed set range:0~100
    motor_l2.ChangeDutyCycle(speed)
    motor_r1.ChangeDutyCycle(0)
    motor_r2.ChangeDutyCycle(speed)