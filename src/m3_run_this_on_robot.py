"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and James Kelley.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import math
import shared_gui_delegate_on_robot


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    # run_arm_and_claw_tests()
    # run_drive_system_tests()

    # run_turn_test()

    real_thing()


def real_thing():
    """ Includes the structure for Sprint 3 delegate. """
    robot = rosebot.RoseBot()
    delegate_receiving = DelegateReceiving(robot)
    mqtt_client = com.MqttClient(delegate_receiving)
    mqtt_client.connect_to_pc()

    while True:
        time.sleep(0.01)
        if delegate_receiving.is_time_to_stop:
            break
        if delegate_receiving.stage == 1:
            mqtt_client.send_message('change_distance_forward', [str(delegate_receiving.distance_away)])
            delegate_receiving.return_to_sender_stage_2(delegate_receiving.speed)
        elif delegate_receiving.stage == 2:
            mqtt_client.send_message('change_distance_out', [str(delegate_receiving.distance_left)])
            delegate_receiving.return_to_sender_stage_3(delegate_receiving.speed)


class DelegateReceiving(object):

    def __init__(self, robot):
        ''' :type robot:  rosebot.RoseBot '''
        self.robot = robot
        self.is_time_to_stop = False
        self.stage = 0
        self.distance_away = 0
        self.distance_left = 0
        self.speed = 0

    def return_to_sender_stage_1(self, speed):
        """ Proceeds forward until finding a wall. Records the distance. """
        self.robot.arm_and_claw.calibrate_arm()
        self.robot.drive_system.left_motor.reset_position()
        self.robot.drive_system.go_forward_until_distance_is_less_than(3, speed)
        self.distance_away = self.robot.drive_system.left_motor.WheelCircumference * self.robot.drive_system.left_motor.get_position() / 360
        self.speed = speed
        self.stage = 1

    def return_to_sender_stage_2(self, speed):
        """ Turns 90 degrees left. Proceeds until sees block. Picks up block. Records Distance. """
        self.robot.drive_system.left_motor.reset_position()
        turn_left(self.robot, 90, speed)
        self.robot.drive_system.left_motor.reset_position()
        go_until_block(self.robot, speed)
        self.robot.arm_and_claw.raise_arm()
        self.distance_left = self.robot.drive_system.left_motor.WheelCircumference * self.robot.drive_system.left_motor.get_position() / 360
        self.stage = 2

    def return_to_sender_stage_3(self, speed):
        """ Returns to the starting location. """
        self.robot.arm_and_claw.lower_arm()
        print(self.distance_away, self.distance_left)
        needed_degrees = 180 - (180 * math.atan(self.distance_away / self.distance_left) / math.pi)
        print("Needed degrees:", needed_degrees)
        turn_left(self.robot, needed_degrees, speed)
        self.robot.drive_system.left_motor.reset_position()
        distance = math.sqrt((self.distance_away ** 2) + (self.distance_left ** 2))
        print("Distance:", distance)
        self.robot.drive_system.go_straight_for_inches_using_encoder(distance, speed)
        self.stage = 99

    def quit(self):
        """ Establishes that the robot should stop. """
        self.is_time_to_stop = True


def go_until_block(delegate, speed):
    """ Proceeds until camera senses the block. """
    delegate.drive_system.go(speed, speed)
    while True:
        b = delegate.sensor_system.camera.get_biggest_blob()
        time.sleep(.01)
        print(b.get_area())
        if b.get_area() >= 1500:
            break
    delegate.drive_system.stop()


def turn_left(robot, degrees, speed):
    """ Turns the robot the desired number of degrees left. """
    robot.drive_system.left_motor.reset_position()
    robot.drive_system.go(-speed, speed)

    while True:
        if robot.drive_system.left_motor.get_position() <= -(4.10 * degrees):
            break

    robot.drive_system.stop()


def run_arm_and_claw_tests():
    run_test_raise_arm()
    run_test_calibrate_arm()
    run_test_move_arm_to_position()
    run_test_lower_arm()


def run_drive_system_tests():
    run_test_go()
    run_test_stop()
    run_test_go_straight_for_seconds()
    run_test_go_straight_for_inches_using_time()
    run_test_go_straight_for_inches_using_encoder()


def run_test_raise_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.raise_arm()


def run_test_calibrate_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.calibrate_arm()


def run_test_move_arm_to_position():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    time.sleep(6)
    robot.arm_and_claw.move_arm_to_position(2500)
    time.sleep(6)
    robot.arm_and_claw.move_arm_to_position(1500)
    time.sleep(6)


def run_test_lower_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    robot.arm_and_claw.raise_arm()
    robot.arm_and_claw.lower_arm()


def run_test_go():
    robot = rosebot.RoseBot()
    robot.drive_system.go(100, 100)
    time.sleep(3)
    robot.drive_system.go(50, 50)
    time.sleep(3)


def run_test_stop():
    robot = rosebot.RoseBot()
    robot.drive_system.stop()


def run_test_go_straight_for_seconds():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_seconds(4, 74)
    time.sleep(5)
    robot.drive_system.go_straight_for_seconds(1, 100)
    time.sleep(2)


def run_test_go_straight_for_inches_using_time():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_inches_using_time(48, 100)
    time.sleep(7)
    robot.drive_system.go_straight_for_inches_using_time(24, 50)
    time.sleep(8)


def run_test_go_straight_for_inches_using_encoder():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_inches_using_encoder(12, 20)
    time.sleep(8)
    robot.drive_system.go_straight_for_inches_using_encoder(40, 100)
    time.sleep(4)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
