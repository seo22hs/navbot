#!/usr/bin/env python3

import os
import select
import sys

import rospy
from geometry_msgs.msg import Twist

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


BURGER_MAX_LIN_VEL = 0.16
BURGER_MAX_ANG_VEL = 1.20

WAFFLE_MAX_LIN_VEL = 0.18
WAFFLE_MAX_ANG_VEL = 0.90

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.05

MSG = """
Exhibition Mapping Teleop
---------------------------
Moving around:
        w
   a    s    d
        x

w/x : increase/decrease linear velocity
a/d : increase/decrease angular velocity
space key, s : force stop

This teleop is tuned for slower and smoother mapping.
CTRL-C to quit
"""


def get_key():
    if os.name == "nt":
        if sys.version_info[0] >= 3:
            return msvcrt.getch().decode()
        return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1) if rlist else ""
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, SETTINGS)
    return key


def vels(target_linear_vel, target_angular_vel):
    return f"currently:\tlinear vel {target_linear_vel}\t angular vel {target_angular_vel}"


def make_simple_profile(output, input_value, slop):
    if input_value > output:
        output = min(input_value, output + slop)
    elif input_value < output:
        output = max(input_value, output - slop)
    else:
        output = input_value
    return output


def constrain(input_value, low, high):
    return min(max(input_value, low), high)


def check_linear_limit_velocity(vel):
    if TURTLEBOT3_MODEL == "burger":
        return constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    if TURTLEBOT3_MODEL in ("waffle", "waffle_pi"):
        return constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    return constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)


def check_angular_limit_velocity(vel):
    if TURTLEBOT3_MODEL == "burger":
        return constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    if TURTLEBOT3_MODEL in ("waffle", "waffle_pi"):
        return constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    return constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)


if __name__ == "__main__":
    if os.name != "nt":
        SETTINGS = termios.tcgetattr(sys.stdin)

    rospy.init_node("exhibition_teleop_key")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)

    TURTLEBOT3_MODEL = rospy.get_param("model", "burger")

    status = 0
    target_linear_vel = 0.0
    target_angular_vel = 0.0
    control_linear_vel = 0.0
    control_angular_vel = 0.0

    try:
        print(MSG)
        while True:
            key = get_key()
            if key == "w":
                target_linear_vel = check_linear_limit_velocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                status += 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == "x":
                target_linear_vel = check_linear_limit_velocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                status += 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == "a":
                target_angular_vel = check_angular_limit_velocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                status += 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key == "d":
                target_angular_vel = check_angular_limit_velocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                status += 1
                print(vels(target_linear_vel, target_angular_vel))
            elif key in (" ", "s"):
                target_linear_vel = 0.0
                control_linear_vel = 0.0
                target_angular_vel = 0.0
                control_angular_vel = 0.0
                print(vels(target_linear_vel, target_angular_vel))
            else:
                if key == "\x03":
                    break

            if status == 20:
                print(MSG)
                status = 0

            twist = Twist()
            control_linear_vel = make_simple_profile(
                control_linear_vel, target_linear_vel, LIN_VEL_STEP_SIZE / 2.0
            )
            control_angular_vel = make_simple_profile(
                control_angular_vel, target_angular_vel, ANG_VEL_STEP_SIZE / 2.0
            )

            twist.linear.x = control_linear_vel
            twist.angular.z = control_angular_vel
            pub.publish(twist)
    except Exception:
        pass
    finally:
        twist = Twist()
        pub.publish(twist)
        if os.name != "nt":
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, SETTINGS)
