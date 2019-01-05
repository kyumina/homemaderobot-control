# -*- coding:utf-8 -*-

#ROS LIB
import rospy
from imgaxis.srv import GetSpeedReq

#depend import 
import time
import serial

ARDUINO0 = "/dev/ttyUSB0"
# ser = serial.Serial(ARDUINO0, 57600)
ser = serial.Serial(ARDUINO0, 57600, timeout=1)


# -------- Main Program Loop -----------

print ser.portstr

def motor(left_v,right_v):
    print left_v
    print right_v
    ser.write(str(int(-left_v)))
    time.sleep(0.01)
    ser.write(str(int(right_v)))
    time.sleep(0.01)

def main():
    rospy.init_node("bluetank",anonymous=True, disable_signals=True)
    #blue=Blue()
    setspeed()
    try:
        rospy.spin()
        #blue.motor(0,0)
        print("see you")
    except:
        pass

def setspeed():
    start=time.time()
    flag=True
    while True:
        test=ser.readline()
        if flag:
            motor(200,200)
        else:
            motor(200,200)
        if time.time()-start>7:
            flag=False
        #    start=time.time()
        time.sleep(1)
        print(time.time()-start)


if __name__=='__main__':
    motor(0,0)
    try:
        main()
    except KeyboardInterrupt:
        motor(0,0)
