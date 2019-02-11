"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Aidan Moss, James Kelley, Guang Yang.
  Winter term, 2018-2019.
"""


class DelegateReceiving(object):

    def __init__(self, robot):
        ''' :type robot:  rosebot.RoseBot '''
        self.robot = robot
        self.is_time_to_stop = False

    def forward(self, left_wheel_speed, right_wheel_speed):
        self.robot.drive_system.go(int(left_wheel_speed), int(right_wheel_speed))
    
    def backward(self, left_wheel_speed, right_wheel_speed):
        self.robot.drive_system.go(int(left_wheel_speed), int(right_wheel_speed))
    
    def left(self, left_wheel_speed, right_wheel_speed):
        self.robot.drive_system.go(int(left_wheel_speed), int(right_wheel_speed))
    
    def right(self, left_wheel_speed, right_wheel_speed):
        self.robot.drive_system.go(int(left_wheel_speed), int(right_wheel_speed))
    
    def stop(self):
        self.robot.drive_system.stop()

    def raise_arm(self):
        self.robot.arm_and_claw.raise_arm()

    def lower_arm(self):
        self.robot.arm_and_claw.lower_arm()

    def calibrate_arm(self):
        self.robot.arm_and_claw.calibrate_arm()

    def move_arm_to_position(self, position):
        self.robot.arm_and_claw.move_arm_to_position(position)

    def quit(self):
        self.is_time_to_stop = True

    def go_straight_for_seconds(self,time_entry,speed_entry):
        self.robot.drive_system.go_straight_for_seconds(int(time_entry), float(speed_entry))

    def go_straight_for_inches_using_time(self,time_entry,speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_time(int(time_entry),float(speed_entry))

    def go_straight_for_inches_using_encoder(self, time_entry,speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_encoder(int(time_entry), float(speed_entry))

    def beep(self, n):
        print('got beep')

        for k in range(n):
            self.robot.sound_system.beeper.beep().wait()
