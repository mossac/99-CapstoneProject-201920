"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and James Kelley.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    # run_test_raise_arm()
    # run_test_calibrate_arm()
    run_test_move_arm_to_position()
    # run_test_lower_arm()


def run_test_raise_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.raise_arm()


def run_test_calibrate_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.calibrate_arm()


def run_test_move_arm_to_position():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    robot.arm_and_claw.move_arm_to_position(0)
    robot.arm_and_claw.move_arm_to_position(2500)
    robot.arm_and_claw.move_arm_to_position(1500)


def run_test_lower_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.lower_arm()


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()