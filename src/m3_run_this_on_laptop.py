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
    delegate_receiving = DelegateReceiving()
    mqtt_client = com.MqttClient(delegate_receiving)
    mqtt_client.connect_to_ev3()

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
    # teleop_frame, arm_frame, control_frame, drive_frame, sound_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # proximity_frame, camera_frame = get_my_frames(main_frame, mqtt_sender)
    return_to_sender_frame, distance_forward_display, distance_out_display = get_return_to_sender_frame(main_frame, mqtt_client)
    delegate_receiving.distance_forward_display, delegate_receiving.distance_out_display = distance_forward_display, distance_out_display

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    # grid_frames(teleop_frame, arm_frame, control_frame, drive_frame, sound_frame, proximity_frame, camera_frame)
    return_to_sender_frame.grid()

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------

    root.mainloop()


class DelegateReceiving(object):

    def __init__(self):
        ''' :type return_to_sender_frame:  ttk.Frame '''
        self.distance_forward_display = None
        self.distance_out_display = None

    def change_distance_forward(self, distance_forward_value):
        """ Changes the label on the tkinter to the new value. """
        print(distance_forward_value)
        new_text = '{} inches'.format(distance_forward_value)
        self.distance_forward_display['text'] = new_text

    def change_distance_out(self, distance_out_value):
        """ Changes the label on the tkinter to the new value. """
        print(distance_out_value)
        new_text = '{} inches'.format(distance_out_value)
        self.distance_out_display['text'] = new_text


def get_return_to_sender_frame(main_frame, mqtt_sender):
    """ Constructs the return_to_sender frame which is used in Sprint 3. """
    # Construct the frame to return:
    frame = ttk.Frame(main_frame, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Return to Sender")

    speed_label = ttk.Label(frame, text="Speed:")
    speed_slider = ttk.Scale(frame, from_=0, to_=100)

    distance_forward_label, distance_forward_display = make_label_and_display(frame, "Distance To Wall:")

    distance_out_label, distance_out_display = make_label_and_display(frame, "Length On Wall:")

    pick_up_button = ttk.Button(frame, text="Pick Up Package")
    quit_button = ttk.Button(frame, text="Stop Robot")

    # Grid the widgets:
    grid_widgets([frame_label, speed_label, speed_slider, distance_forward_label, distance_forward_display,
                  distance_out_label, distance_out_display, pick_up_button, quit_button])

    # Set the Button callbacks:
    pick_up_button["command"] = lambda: handle_return_to_sender(mqtt_sender, speed_slider)
    quit_button["command"] = lambda: handle_quit(mqtt_sender)

    return frame, distance_forward_display, distance_out_display


def make_label_and_display(frame, text):
    """ Constructs and returns a label and a display label corresponding to the text. """
    label = ttk.Label(frame, text=text)
    diplay_text = str("None")
    display = ttk.Label(frame, text=diplay_text)

    return label, display


def grid_widgets(sequence_of_widgets):
    """ Grids all widgets in the sequence into a nice looking frame. """
    for x in range(len(sequence_of_widgets)):
        sequence_of_widgets[x].grid(row=((x + 1) // 2), column=((x + 1) % 2))


def handle_return_to_sender(mqtt_sender, speed_slider):
    """ In response to pressing the 'Pick up package' button, this sends the appropriate MQTT message. """
    print("Picking up package.")
    mqtt_sender.send_message("return_to_sender_stage_1", [float(speed_slider.get())])


def handle_quit(mqtt_sender):
    """ In response to pressing the 'quit' button, this stops the robot's program. """
    print("Stopping Robot")
    mqtt_sender.send_message("quit")


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
    mqtt_sender.send_message("m3_camera_pick_up", [str(direction_entry.get()), float(initial_rate_entry.get()),
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
