#!/usr/bin/env python3

import rospy
import time
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL
from mavros_msgs.msg import State, PositionTarget
from sensor_msgs.msg import LaserScan

LOOP_RATE = 2      
LOOP_RATE_FASTER = 10      

def set_arm():
    arm_client = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
    arm_res = arm_client(True)
    rospy.loginfo("Waiting for arm..")

def set_disarm():
    arm_client = rospy.ServiceProxy("/mavros/cmd/arming",CommandBool)
    arm_res = arm_client(False)
    rospy.loginfo("Waiting for disarm..")

def set_land():
    mode_client = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    mode_res = mode_client(0,'LAND')
    rospy.loginfo("Waiting for Land..")

def set_auto():
    mode_client = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    mode_res = mode_client(0,'AUTO')
    rospy.loginfo("Waiting for Auto..")

def set_guided():
    mode_client = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    mode_res = mode_client(0,'GUIDED')
    rospy.loginfo("Waiting for Guided..")

def set_guided_nogps():
    mode_client = rospy.ServiceProxy("/mavros/set_mode",SetMode)
    mode_res = mode_client(0,'GUIDED_NOGPS')
    rospy.loginfo("Waiting for Guided No GPS..")
    
def guided_and_arm():

    while(fcu_state.mode!='GUIDED'):
       set_guided()
       rate.sleep()

    rospy.sleep(1)

    rospy.loginfo("Arming...")
    while(not fcu_state.armed):
        set_arm()
        rate.sleep()

    time.sleep(1)
    
def set_takeoff(alt_target):
    takeoff_client = rospy.ServiceProxy("/mavros/cmd/takeoff",CommandTOL)
    takeoff_res = takeoff_client(0,0,0,0,alt_target)
    rospy.loginfo("Waiting for Takeoff..")      

# publisher, tambahin sendiri beberapa yang diperlukan

speedy_pub = rospy.Publisher("/mavros/setpoint_raw/local", PositionTarget, queue_size=1)

def moveAtVelocity(lin_x = 0, lin_y = 0, lin_z = 0):
    speed_data = PositionTarget()
    speed_data.coordinate_frame = 8
    speed_data.type_mask = 1991

    speed_data.velocity.x = lin_y
    speed_data.velocity.y = -lin_x
    speed_data.velocity.z = lin_z

    speedy_pub.publish(speed_data)
    
# kalo mau bikin fungsi, tambah di bawah ini

def main():
    guided_and_arm()
    set_takeoff(3)
    rospy.loginfo("Taking off to 3 meters")
    rospy.sleep(10)
    rospy.loginfo("Kiri")
    moveAtVelocity(-1,0,0)
    rospy.sleep(5)
    rospy.loginfo("Stopping")
    print(alt)
    moveAtVelocity(0,0,0)
    rospy.sleep(2)
    rospy.loginfo("Landing")
    set_land()
    rospy.sleep(10)

if __name__=="__main__":
    rospy.init_node("control",anonymous=True)
    rospy.loginfo("Initialize control node")
    
    rate = rospy.Rate(LOOP_RATE)
    rate_fast = rospy.Rate(LOOP_RATE_FASTER)
    
    # Subscribers, tambahin sendiri beberapa info yang diperlukan

    fcu_state = State()
    def fcu_state_cb(data):
        global fcu_state
        fcu_state = data
    rospy.Subscriber("/mavros/state",State,fcu_state_cb)

    alt = 0
    def alt_cb(data):
        global alt
        alt = data.ranges[0]
    rospy.Subscriber('/laser/bawah', LaserScan, alt_cb)
    
    # code kalian di sini
    
    main()