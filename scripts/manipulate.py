#!/usr/bin/env python

#ROSlib import 
import rospy
from manipulate_motors.msg import Speed

#depend import
import smbus
import struct
import time

class AStar:
  def __init__(self):
    self.bus = smbus.SMBus(1)
    self.speed_sub=rospy.Subscriber('speed', Speed, self.callback)
    self.motors(0,0)
  
  def callback(self,data):
    print(data.left_speed)
    print(data.right_speed)
    #data.left_speed=0
    #data.right_speed=0
    self.motors(data.left_speed,data.right_speed)
  
  def write_pack(self, address, format, *data):
    data_array = [ord(s) for s in list(struct.pack(format, *data))]
    self.bus.write_i2c_block_data(20, address, data_array)
    time.sleep(0.0001)
  def motors(self, left, right):
    print("receive: %d,%d" %(left,right))
    self.write_pack(6, 'hh', int(left), int(right))

def main():
  rospy.init_node('manipulate_motors',anonymous=True, disable_signals = True)
  aster = AStar() #manipulate_loop
  try:
    rospy.spin()
    aster.motors(0,0)
    print("Shutting down")
  except e:
    print(e)

if __name__=='__main__':
  main()
