"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Aidan Moss, James Kelley, Guang Yang.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import time


class DelegateReceiving(object):

    def __init__(self, robot):
        ''' :type robot:  rosebot.RoseBot '''
        self.robot = robot
        self.is_time_to_stop = False
        self.mqtt_sender = None

    ###############################################################################
    # From Teleoperation Frame
    ###############################################################################

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

    ###############################################################################
    # From Arm Frame
    ###############################################################################

    def raise_arm(self):
        print('h')
        self.robot.arm_and_claw.raise_arm()
        print('j')
        if self.robot.sensor_system.color_sensor.get_color() is 6:
            print('m')
            self.mqtt_sender.send_message('can_score')


    def lower_arm(self):
        self.robot.arm_and_claw.lower_arm()
        if self.robot.sensor_system.color_sensor.get_color() is 1:
            self.mqtt_sender.send_message('add_point')

    def calibrate_arm(self):
        self.robot.arm_and_claw.calibrate_arm()

    def move_arm_to_position(self, position):
        self.robot.arm_and_claw.move_arm_to_position(position)

    ###############################################################################
    # From Control Frame
    ###############################################################################

    def quit(self):
        self.is_time_to_stop = True

    ###############################################################################
    # From Drive Frame
    ###############################################################################

    def go_straight_for_seconds(self, time_entry, speed_entry):
        self.robot.drive_system.go_straight_for_seconds(int(time_entry), float(speed_entry))

    def go_straight_for_inches_using_time(self, time_entry, speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_time(int(time_entry), float(speed_entry))

    def go_straight_for_inches_using_encoder(self, time_entry, speed_entry):
        self.robot.drive_system.go_straight_for_inches_using_encoder(int(time_entry), float(speed_entry))

    # Color Sensor
    def go_straight_until_intensity_is_less_than(self, intensity_entry, speed_entry):
        self.robot.drive_system.go_straight_until_intensity_is_less_than(float(intensity_entry), float(speed_entry))

    def go_straight_until_intensity_is_greater_than(self, intensity_entry, speed_entry):
        self.robot.drive_system.go_straight_until_intensity_is_greater_than(float(intensity_entry), float(speed_entry))

    def go_straight_until_color_is(self,color_entry,speed_entry):
        self.robot.drive_system.go_straight_until_color_is(color_entry, float(speed_entry))

    def go_straight_until_color_is_not(self,color_entry,speed_entry):
        self.robot.drive_system.go_straight_until_color_is_not(color_entry, float(speed_entry))

    # Proximity

    def go_forward_until_distance_is_less_than(self, speed, inches):
        self.robot.drive_system.go_forward_until_distance_is_less_than(inches, speed)

    def go_forward_danger(self, speed, inches):
        self.robot.go_forward_danger(int(inches), int(speed))

    def go_backward_until_distance_is_greater_than(self, speed, inches):
        self.robot.drive_system.go_backward_until_distance_is_greater_than(inches, speed)

    def go_until_distance_is_within(self, speed, inches, delta):
        self.robot.drive_system.go_until_distance_is_within(delta, inches, speed)

    # Camera

    ###############################################################################
    # From Sound_System Frame
    ###############################################################################

    def beep(self, n):
        for k in range(n):
            self.robot.sound_system.beeper.beep().wait()

    def tone(self, frequency, duration):
        self.robot.sound_system.tone_maker.play_tone(frequency, duration)

    def speak(self, text):
        self.robot.sound_system.speech_maker.speak(text)

    def find_object_clockwise(self,speed,area):
        print("Finding object using camera")
        self.robot.drive_system.spin_clockwise_until_sees_object(speed,area)

    def find_object_counterclockwise(self,speed,area):
        print("Finding object using camera")
        self.robot.drive_system.spin_counterclockwise_until_sees_object(speed,area)
        self.m3_pick_up(10,10,speed)



##############################################
    #m2_pick_up
##############################################
    def go_and_pick(self, initial,step, speed):
        print("receive go_and_pick")
        self.robot.drive_system.go_and_pick(int(initial), int(step),int(speed))
        self.robot.arm_and_claw.raise_arm()
        self.mqtt_sender.send_message('can_score')


    def m3_pick_up(self, initial_rate, increase_rate, speed):
        total = 0
        for x in range(40):
            total += self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
        starting_distance = total / 40
        print("starting distance: ", starting_distance)
        self.go_until_distance_is_within(speed, 1, 1)
        rate = initial_rate - 1
        self.robot.led_system.left_led.turn_on()
        state = 0
        while True:
            distance = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            if distance < 1:
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
            try:
                time.sleep(1 / rate)
                rate = initial_rate - 1 + increase_rate * (starting_distance / (1 - distance))
            except ValueError or ZeroDivisionError:
                rate = initial_rate
                continue
        print("finished")
        self.robot.arm_and_claw.raise_arm()
        self.robot.led_system.left_led.turn_off()
        self.robot.led_system.right_led.turn_off()
        self.stop()

    def m2_camera_pick_up(self,direction, initial_rate, increase_rate, speed, area):
        if direction == 'left':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(speed, area)
            time.sleep(3)
            self.go_and_pick(initial_rate, increase_rate, speed)
        elif direction == 'right':
            self.robot.drive_system.spin_clockwise_until_sees_object(speed, area)
            time.sleep(3)
            self.go_and_pick(initial_rate, increase_rate, speed)

    def m3_camera_pick_up(self, direction, initial_rate, increase_rate, speed, area):
        if direction == 'left':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(speed, area)
            time.sleep(3)
            self.m3_pick_up(initial_rate, increase_rate, speed, area)
        elif direction == 'right':
            self.robot.drive_system.spin_clockwise_until_sees_object(speed, area)
            time.sleep(3)
            self.m3_pick_up(initial_rate, increase_rate, speed)

    def m1_pick_up(self, initial_rate, increase_rate,speed):
        total = 0
        for k in range(40):
            total += self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
        starting_distance = total / 40
        self.go_straight_for_inches_using_encoder(starting_distance, speed)
        frequency = initial_rate - 1
        while True:
            self.robot.sound_system.beeper.beep()
            distance = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            if distance < 1.2:
                break
            time.sleep(1 / frequency)
            frequency = initial_rate - 1 + increase_rate * (
                    starting_distance / (1 - self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()))
        self.robot.drive_system.stop()
        self.robot.arm_and_claw.raise_arm()

    def m1_camera_pick_up(self, initial_rate, increase_rate, speed, direction, area):
        if direction == 'left' or 'Left':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(speed, area)
            time.sleep(3)
            self.m1_pick_up(initial_rate, increase_rate, speed)
        elif direction == 'right' or 'Right':
            self.robot.drive_system.spin_clockwise_until_sees_object(speed, area)
            time.sleep(3)
            self.m1_pick_up(initial_rate, increase_rate, speed)


    def m1_line_follow(self,speed):
        print('test')
        start = self.robot.sensor_system.color_sensor.get_color()
        self.robot.drive_system.go(speed,speed)
        print("test 2")
        time.sleep(.5)
        while True:
            self.robot.drive_system.go(speed, speed)
            print("test 3")
            current = self.robot.sensor_system.color_sensor.get_color()
            Error = current - start
            time.sleep(.1)
            counter = 1
            if Error is 4:
                print("test 4")
                break
            while Error is not 0 or 4:
                self.robot.drive_system.go((-speed),(speed))
                time.sleep(.1*counter)
                if start or 5 is self.robot.sensor_system.color_sensor.get_color():
                    break
                self.robot.drive_system.go((speed+5), (-speed))
                time.sleep(.1*counter)
                if start or 5 is self.robot.sensor_system.color_sensor.get_color():
                    break
                counter = counter +1
            if Error is 4:
                print("test 4")
                break

        self.robot.drive_system.stop()

    def Add_Point(self):
        print('recieved')
        self.mqtt_sender.send_message('add_point')

    def Sub_Point(self):
        print('recieved')
        self.mqtt_sender.send_message('sub_point')




