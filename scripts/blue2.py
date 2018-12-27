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

master_markers=(1,2,3,4,5,6,10,11)


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
        blue.motor(0,0)
        print("see you")
    except:
        pass

def leftsearch(getreq,removeids):
    removeids.append(-1)
    while True:
        motor(30,-30)
        time.sleep(1)
        try:
            r1=getreq(2) #req:2 単純マーカー検索リクエスト
            if not(r1.id in removeids):
                return
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

def rightsearch(getreq,removeids):
    removeids.append(-1)
    while True:
        motor(-30,30)
        time.sleep(0.05)
        try:
            r1=getreq(2) #req:1 単純マーカー検索リクエスト
            print("r1:"+str(r1.id))
            if not(r1.id in removeids):
                return
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

def setspeed():
    rospy.wait_for_service("get_speed_req")
    while True:
        test=ser.readline()
        try:
            getreq=rospy.ServiceProxy("get_speed_req", GetSpeedReq)
            r1=getreq(1) #範囲制限付きマーカー検索リクエスト
            print("receive: id:%d, l_v:%d, r_v:%d" %(r1.id,r1.leftv,r1.rightv))
            if r1.id==-1:
                motor(r1.leftv,r1.rightv)
            elif r1.id == 1:
                rightsearch(getreq,[1,3,4,5,0])
            elif r1.id == 2:
                rightsearch(getreq,[1,2,4,5,0])
            elif r1.id==3:
                leftsearch(getreq,[1,2,3,5,0])
            elif r1.id==4:
                leftsearch(getreq,[1,2,3,4,0])
            elif r1.id==5:
                rightsearch(getreq,[1,2,3,4,5])
            elif r1.id==0:
                motor(0,0)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
        #print(test)
        time.sleep(1)


if __name__=='__main__':
    main()