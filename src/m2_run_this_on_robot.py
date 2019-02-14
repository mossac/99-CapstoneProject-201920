"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Guang Yang.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    real_thing()


def real_thing():
    robot = rosebot.RoseBot()
    delegate_receiving = shared_gui_delegate_on_robot.DelegateReceiving(robot)
    mqtt_receiver = com.MqttClient(delegate_receiving)
    mqtt_receiver.connect_to_pc()

    while True:
        time.sleep(0.01)


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

def run_test_move_with_increasing_tone():
    robot=rosebot.RoseBot()





# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()