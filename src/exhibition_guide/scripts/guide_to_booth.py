#!/usr/bin/env python3

import math
import sys

import actionlib
import rospy
import rospkg
import yaml
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


def yaw_to_quaternion(yaw):
    half_yaw = yaw * 0.5
    return math.sin(half_yaw), math.cos(half_yaw)


def make_goal(location):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = float(location["x"])
    goal.target_pose.pose.position.y = float(location["y"])
    goal.target_pose.pose.position.z = 0.0

    z, w = yaw_to_quaternion(float(location.get("yaw", 0.0)))
    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = w
    return goal


class BoothGuide:
    def __init__(self):
        config_file = rospy.get_param("~booth_file", "")
        if not config_file:
            pkg_path = rospkg.RosPack().get_path("exhibition_guide")
            config_file = pkg_path + "/config/booth_locations.yaml"

        with open(config_file, "r") as stream:
            config = yaml.safe_load(stream)

        self.entrance = config["entrance"]
        self.booths = config["booths"]
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)

    def wait_for_server(self):
        rospy.loginfo("Waiting for move_base...")
        if not self.client.wait_for_server(rospy.Duration(30.0)):
            rospy.logerr("move_base is not available.")
            return False
        return True

    def send_location(self, label, location):
        rospy.loginfo("Going to %s: x=%.2f, y=%.2f", label, location["x"], location["y"])
        self.client.send_goal(make_goal(location))
        self.client.wait_for_result()
        state = self.client.get_state()

        if state == actionlib.GoalStatus.SUCCEEDED:
            rospy.loginfo("Arrived at %s.", label)
            return True

        rospy.logwarn("Failed to reach %s. move_base state: %s", label, state)
        return False

    def run(self):
        labels = sorted(self.booths.keys())
        print("Available booths: " + ", ".join(labels))
        print("Type a booth label, 'home' to return, or 'q' to quit.")

        while not rospy.is_shutdown():
            selected = input("booth> ").strip().upper()
            if selected in ("Q", "QUIT", "EXIT"):
                break
            if selected in ("HOME", "ENTRANCE", "RETURN"):
                self.send_location("Entrance", self.entrance)
                continue
            if selected not in self.booths:
                print("Unknown booth. Choose one of: " + ", ".join(labels))
                continue

            reached = self.send_location(selected, self.booths[selected])
            if reached:
                answer = input("Return to entrance? [y/N] ").strip().lower()
                if answer == "y":
                    self.send_location("Entrance", self.entrance)


def main():
    rospy.init_node("guide_to_booth")
    guide = BoothGuide()
    if not guide.wait_for_server():
        sys.exit(1)
    guide.run()


if __name__ == "__main__":
    main()
