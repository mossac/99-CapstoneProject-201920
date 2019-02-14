"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Aidan Moss, James Kelley, Guang Yang.
  Winter term, 2018-2019.
"""

import time


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

    def go_straight_for_seconds(self, time_entry, speed_entry):
        self.robot.drive_system.go_straight_for_seconds(int(time_entry), float(speed_entry))

    def go_straight_for_inches_using_time(self, time_entry, speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_time(int(time_entry), float(speed_entry))

    def go_straight_for_inches_using_encoder(self, time_entry, speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_encoder(int(time_entry), float(speed_entry))

    def beep(self, n):
        for k in range(n):
            self.robot.sound_system.beeper.beep().wait()

    def tone(self, frequency, duration):
        self.robot.sound_system.tone_maker.play_tone(frequency, duration)

    def speak(self, text):
        self.robot.sound_system.speech_maker.speak(text)

    def find_object_clockwise(self,speed):
        print("Finding object using camera")
        self.robot.drive_system.spin_clockwise_until_sees_object(speed,)

    def find_object_counterclockwise(self,speed):
        print("Finding object using camera")
        self.robot.drive_system.spin_counterclockwise_until_sees_object(speed,)

    def pick_up(self):
        print('Picking up object')




    def m3_pick_up(self, initial_rate, increase_rate, speed):
        starting_distance = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
        self.robot.drive_system.go_until_distance_is_within(0.1, 1, speed)
        rate = 1 / initial_rate
        self.robot.led_system.left_led.turn_on()
        state = 0
        while True:
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() < 1.2:
                break
            if state == 0:
                self.robot.led_system.left_led.turn_on()
            elif state == 1:
                self.robot.led_system.left_led.turn_off()
                self.robot.led_system.right_led.turn_on()
            elif state == 2:
                self.robot.led_system.left_led.turn_on()
            elif state == 3:
                self.robot.led_system.left_led.turn_off()
                self.robot.led_system.right_led.turn_off()
            state = state % 4
            time.sleep(rate)
            rate = (self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()) / starting_distance
            rate += 1 / ((1 / rate) + increase_rate)
        self.robot.arm_and_claw.raise_arm()
        self.robot.led_system.left_led.turn_off()
        self.robot.led_system.right_led.turn_off()
