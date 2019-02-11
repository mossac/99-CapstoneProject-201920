"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Constructs and returns Frame objects for the basics:
  -- teleoperation
  -- arm movement
  -- stopping the robot program

  This code is SHARED by all team members.  It contains both:
    -- High-level, general-purpose methods for a Snatch3r EV3 robot.
    -- Lower-level code to interact with the EV3 robot library.

  Author:  Your professors (for the framework and lower-level code)
    and James Kelley, Aidan Moss, and Guang Yang.
  Winter term, 2018-2019.
"""

import tkinter
from tkinter import ttk


def get_teleoperation_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Teleoperation")
    left_speed_label = ttk.Label(frame, text="Left wheel speed (0 to 100)")
    right_speed_label = ttk.Label(frame, text="Right wheel speed (0 to 100)")

    left_speed_entry = ttk.Entry(frame, width=8)
    left_speed_entry.insert(0, "100")
    right_speed_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "100")

    forward_button = ttk.Button(frame, text="Forward")
    backward_button = ttk.Button(frame, text="Backward")
    left_button = ttk.Button(frame, text="Left")
    right_button = ttk.Button(frame, text="Right")
    stop_button = ttk.Button(frame, text="Stop")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    left_speed_label.grid(row=1, column=0)
    right_speed_label.grid(row=1, column=2)
    left_speed_entry.grid(row=2, column=0)
    right_speed_entry.grid(row=2, column=2)

    forward_button.grid(row=3, column=1)
    left_button.grid(row=4, column=0)
    stop_button.grid(row=4, column=1)
    right_button.grid(row=4, column=2)
    backward_button.grid(row=5, column=1)

    # Set the button callbacks:
    forward_button["command"] = lambda: handle_forward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    backward_button["command"] = lambda: handle_backward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    left_button["command"] = lambda: handle_left(
        left_speed_entry, right_speed_entry, mqtt_sender)
    right_button["command"] = lambda: handle_right(
        left_speed_entry, right_speed_entry, mqtt_sender)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)

    return frame


def get_arm_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's Arm
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Arm and Claw")
    position_label = ttk.Label(frame, text="Desired arm position:")
    position_entry = ttk.Entry(frame, width=8)

    raise_arm_button = ttk.Button(frame, text="Raise arm")
    lower_arm_button = ttk.Button(frame, text="Lower arm")
    calibrate_arm_button = ttk.Button(frame, text="Calibrate arm")
    move_arm_button = ttk.Button(frame,
                                 text="Move arm to position (0 to 5112)")
    blank_label = ttk.Label(frame, text="")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    position_label.grid(row=1, column=0)
    position_entry.grid(row=1, column=1)
    move_arm_button.grid(row=1, column=2)

    blank_label.grid(row=2, column=1)
    raise_arm_button.grid(row=3, column=0)
    lower_arm_button.grid(row=3, column=1)
    calibrate_arm_button.grid(row=3, column=2)

    # Set the Button callbacks:
    raise_arm_button["command"] = lambda: handle_raise_arm(mqtt_sender)
    lower_arm_button["command"] = lambda: handle_lower_arm(mqtt_sender)
    calibrate_arm_button["command"] = lambda: handle_calibrate_arm(mqtt_sender)
    move_arm_button["command"] = lambda: handle_move_arm_to_position(
        position_entry, mqtt_sender)

    return frame


def get_control_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame has
    Button objects to exit this program and/or the robot's program (via MQTT).
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Control")
    quit_robot_button = ttk.Button(frame, text="Stop the robot's program")
    exit_button = ttk.Button(frame, text="Stop this and the robot's program")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    quit_robot_button.grid(row=1, column=0)
    exit_button.grid(row=1, column=2)

    # Set the Button callbacks:
    quit_robot_button["command"] = lambda: handle_quit(mqtt_sender)
    exit_button["command"] = lambda: handle_exit(mqtt_sender)

    return frame


def get_drive_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Drive System")
    position_label = ttk.Label(frame, text="Time/Inches:")
    speed_label = ttk.Label(frame, text='Speed: ')
    time_entry = ttk.Entry(frame, width=8)
    speed_entry = ttk.Entry(frame, width=8)

    forward_for_seconds_button = ttk.Button(frame, text="Forward For Seconds")
    inches_using_time_button = ttk.Button(frame, text="Inches using time")
    inches_using_encoder_button = ttk.Button(frame, text="Inches using encoder")
    blank_label = ttk.Label(frame, text="")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    position_label.grid(row=1, column=0)
    time_entry.grid(row=1, column=1)
    speed_label.grid(row=2, column=0)
    speed_entry.grid(row=2, column=1)

    blank_label.grid(row=3, column=1)
    forward_for_seconds_button.grid(row=4, column=0)
    inches_using_time_button.grid(row=4, column=1)
    inches_using_encoder_button.grid(row=4, column=2)

    # Set the Button callbacks:
    forward_for_seconds_button["command"] = lambda: handle_seconds(mqtt_sender, time_entry, speed_entry)
    inches_using_time_button["command"] = lambda: handle_using_time(mqtt_sender, time_entry, speed_entry)
    inches_using_encoder_button["command"] = lambda: handle_using_encoder(mqtt_sender, time_entry, speed_entry)

    return frame


def get_sound_system_frame(window, mqtt_sender):
    """
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Sound System")
    beep_num_label = ttk.Label(frame, text="Number of Beeps:")
    beep_num_entry = ttk.Entry(frame, width=8)

    frequency_label = ttk.Label(frame, text="Frequency:")
    frequency_entry = ttk.Entry(frame, width=8)

    duration_label = ttk.Label(frame, text="Duration:")
    duration_entry = ttk.Entry(frame, width=8)

    text_label = ttk.Label(frame, text="Text to Speak:")
    text_entry = ttk.Entry(frame, width=20)

    beep_button = ttk.Button(frame, text="Beep")
    tone_button = ttk.Button(frame, text="Tone")
    speak_button = ttk.Button(frame, text="Speak")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)

    beep_button.grid(row=1, column=0)
    beep_num_label.grid(row=1, column=1)
    beep_num_entry.grid(row=1, column=2)

    tone_button.grid(row=3, column=0)
    frequency_label.grid(row=3, column=1)
    duration_label.grid(row=3, column=2)

    frequency_entry.grid(row=4, column=1)
    duration_entry.grid(row=4, column=2)

    speak_button.grid(row=5, column=0)
    text_label.grid(row=5, column=1)
    text_entry.grid(row=5, column=2)

    # Set the Button callbacks:
    beep_button["command"] = lambda: handle_beep(mqtt_sender, beep_num_entry)
    tone_button["command"] = lambda: handle_tone(mqtt_sender, frequency_entry, duration_entry)
    speak_button["command"] = lambda: handle_speak(mqtt_sender, text_entry)

    return frame

###############################################################################
###############################################################################
# The following specifies, for each Button,
# what should happen when the Button is pressed.
###############################################################################
###############################################################################

###############################################################################
# Handlers for Buttons in the Teleoperation frame.
###############################################################################


def handle_forward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    with the speeds used as given.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """

    print("forward", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("forward", [int(left_entry_box.get()), int(right_entry_box.get())])


def handle_backward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negatives of the speeds in the entry boxes.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """

    print("backward", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("backward", [-int(left_entry_box.get()), -int(right_entry_box.get())])


def handle_left(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the left entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """

    print("left", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("left", [-int(left_entry_box.get()), int(right_entry_box.get())])


def handle_right(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the right entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """

    print("right", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("right", [int(left_entry_box.get()), -int(right_entry_box.get())])


def handle_stop(mqtt_sender):
    """
    Tells the robot to stop.
      :type  mqtt_sender:  com.MqttClient
    """

    print("stop")
    mqtt_sender.send_message("stop")


###############################################################################
# Handlers for Buttons in the ArmAndClaw frame.
###############################################################################
def handle_raise_arm(mqtt_sender):
    """
    Tells the robot to raise its Arm until its touch sensor is pressed.
      :type  mqtt_sender:  com.MqttClient
    """

    print("raise_arm")
    mqtt_sender.send_message("raise_arm")


def handle_lower_arm(mqtt_sender):
    """
    Tells the robot to lower its Arm until it is all the way down.
      :type  mqtt_sender:  com.MqttClient
    """

    print("lower_arm")
    mqtt_sender.send_message("lower_arm")


def handle_calibrate_arm(mqtt_sender):
    """
    Tells the robot to calibrate its Arm, that is, first to raise its Arm
    until its touch sensor is pressed, then to lower its Arm until it is
    all the way down, and then to mark taht position as position 0.
      :type  mqtt_sender:  com.MqttClient
    """

    print("calibrate_arm")
    mqtt_sender.send_message("calibrate_arm")


def handle_move_arm_to_position(arm_position_entry, mqtt_sender):
    """
    Tells the robot to move its Arm to the position in the given Entry box.
    The robot must have previously calibrated its Arm.
      :type  arm_position_entry  ttk.Entry
      :type  mqtt_sender:        com.MqttClient
    """

    print("move_arm_to_position", arm_position_entry.get())
    mqtt_sender.send_message("move_arm_to_position", [float(arm_position_entry.get())])


###############################################################################
# Handlers for Buttons in the Control frame.
###############################################################################
def handle_quit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
    """

    print("quit")
    mqtt_sender.send_message("quit")


def handle_exit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
    Then exit this program.
      :type mqtt_sender: com.MqttClient
    """

    print("exit")
    handle_quit(mqtt_sender)
    exit()

###############################################################################
# Handlers for Buttons in the DriveSystem frame.
###############################################################################


def handle_seconds(mqtt_sender, time_entry, speed_entry):
    print('forward for:', time_entry.get(), 'seconds')
    mqtt_sender.send_message("go_straight_for_seconds", [int(time_entry.get()), float(speed_entry.get())])


def handle_using_time(mqtt_sender, time_entry, speed_entry):
    print('Forward for', time_entry.get(), 'inches')
    mqtt_sender.send_message("go_straight_for_inches_using_time", [int(time_entry.get()), float(speed_entry.get())])


def handle_using_encoder(mqtt_sender, time_entry, speed_entry):
    print('Forward for', time_entry.get(), 'inches')
    mqtt_sender.send_message("go_straight_for_inches_using_encoder", [int(time_entry.get()), float(speed_entry.get())])

###############################################################################
# Handlers for Buttons in the SoundSystem frame.
###############################################################################


def handle_beep(mqtt_sender, beep_num_entry):
    print("I will beep ", beep_num_entry.get(), " times.")
    mqtt_sender.send_message("beep", [int(beep_num_entry.get())])


def handle_tone(mqtt_sender, frequency_entry, duration_entry):
    print("I will play a tone at frequency ", frequency_entry.get(), " for duration ", duration_entry.get(), ".")
    mqtt_sender.send_message("tone", [float(frequency_entry.get()), int(duration_entry.get())])


def handle_speak(mqtt_sender, text_entry):
    print("I will speak phrase ", text_entry.get(), ".")
    mqtt_sender.send_message("speak", [str(text_entry.get())])
