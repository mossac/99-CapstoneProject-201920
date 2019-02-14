"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and James Kelley.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("Capstone Project")

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief="groove")
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    teleop_frame, arm_frame, control_frame, drive_frame, sound_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    proximity_frame, camera_frame = get_my_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame, arm_frame, control_frame, drive_frame, sound_frame, proximity_frame, camera_frame)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    drive_frame = shared_gui.get_drive_frame(main_frame, mqtt_sender)
    sound_frame = shared_gui.get_sound_system_frame(main_frame, mqtt_sender)

    return teleop_frame, arm_frame, control_frame, drive_frame, sound_frame


def get_my_frames(main_frame, mqtt_sender):
    proximity_frame = get_proximity_sensor_frame(main_frame, mqtt_sender)
    camera_frame = get_camera_frame(main_frame, mqtt_sender)

    return proximity_frame, camera_frame


def get_proximity_sensor_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Proximity Sensor")
    initial_rate_label = ttk.Label(frame, text="Initial Rate:")
    initial_rate_entry = ttk.Entry(frame, width=8)

    increase_rate_label = ttk.Label(frame, text="Increase Rate:")
    increase_rate_entry = ttk.Entry(frame, width=8)

    speed_label = ttk.Label(frame, text="Speed:")
    speed_entry = ttk.Entry(frame, width=8)

    pick_up_button = ttk.Button(frame, text="Pick up")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)

    initial_rate_label.grid(row=1, column=0)
    initial_rate_entry.grid(row=1, column=1)

    increase_rate_label.grid(row=2, column=0)
    increase_rate_entry.grid(row=2, column=1)

    speed_label.grid(row=3, column=0)
    speed_entry.grid(row=3, column=1)

    pick_up_button.grid(row=4, column=1)

    # Set the Button callbacks:
    pick_up_button["command"] = lambda: handle_pick_up(mqtt_sender, initial_rate_entry, increase_rate_entry, speed_entry)

    return frame


def get_camera_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Proximity Sensor")
    direction_label = ttk.Label(frame, text="Direction:")
    direction_entry = ttk.Entry(frame, width=8)

    initial_rate_label = ttk.Label(frame, text="Initial Rate:")
    initial_rate_entry = ttk.Entry(frame, width=8)

    increase_rate_label = ttk.Label(frame, text="Increase Rate:")
    increase_rate_entry = ttk.Entry(frame, width=8)

    area_label = ttk.Label(frame, text="Area:")
    area_entry = ttk.Entry(frame, width=8)

    speed_label = ttk.Label(frame, text="Speed:")
    speed_entry = ttk.Entry(frame, width=8)

    camera_pick_up_button = ttk.Button(frame, text="Pick up")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)

    direction_label.grid(row=1, column=0)
    direction_entry.grid(row=1, column=1)

    initial_rate_label.grid(row=2, column=0)
    initial_rate_entry.grid(row=2, column=1)

    increase_rate_label.grid(row=3, column=0)
    increase_rate_entry.grid(row=3, column=1)

    area_label.grid(row=4, column=0)
    area_entry.grid(row=4, column=1)

    speed_label.grid(row=5, column=0)
    speed_entry.grid(row=5, column=1)

    camera_pick_up_button.grid(row=6, column=1)

    # Set the Button callbacks:
    camera_pick_up_button["command"] = lambda: handle_camera_pick_up(mqtt_sender, direction_entry, initial_rate_entry, increase_rate_entry, area_entry, speed_entry)

    return frame


def handle_pick_up(mqtt_sender, initial_rate_entry, increase_rate_entry, speed_entry):
    print("I will pick up object using the proximity sensor.")
    mqtt_sender.send_message("m3_pick_up", [float(initial_rate_entry.get()),
                                            float(increase_rate_entry.get()),
                                            float(speed_entry.get())])


def handle_camera_pick_up(mqtt_sender, direction_entry, initial_rate_entry, increase_rate_entry, area_entry, speed_entry):
    print("I will pick up object using the camera then proximity.")
    mqtt_sender.send_message("m3_pick_up", [str(direction_entry.get()), float(initial_rate_entry.get()),
                                            float(increase_rate_entry.get()), int(area_entry.get()),
                                            float(speed_entry.get())])


def grid_frames(teleop_frame, arm_frame, control_frame, drive_frame, sound_frame, proximity_frame, camera_frame):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    control_frame.grid(row=2, column=0)
    drive_frame.grid(row=0, column=1)
    sound_frame.grid(row=1, column=1)
    proximity_frame.grid(row=2, column=1)
    camera_frame.grid(row=3, column=1)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
