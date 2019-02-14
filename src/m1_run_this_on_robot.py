"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Aidan Moss.
  Winter term, 2018-2019.
  robot:17
  lock: me430-14
  combo:6-16-2
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
    #real_thing()
    camera_test()

def real_thing():
    robot = rosebot.RoseBot()
    delegate_recieves = shared_gui_delegate_on_robot.DelegateReceiving(robot)
    mqtt_reciever = com.MqttClient(delegate_recieves)
    mqtt_reciever.connect_to_pc()
    while True:
        time.sleep(.01)
def camera_test():
    robot = rosebot.RoseBot()
    while True:
        b= robot.sensor_system.camera.get_biggest_blob()

        print(b)
        time.sleep(5)
# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()

