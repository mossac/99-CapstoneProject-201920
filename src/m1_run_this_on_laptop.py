"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Aidan Moss.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui
import m1_delegate
import time


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    root1 = tkinter.Tk()

    LaptopHandler = m1_delegate.LaptopHandler(root1)
    mqtt_sender = com.MqttClient(LaptopHandler)
    mqtt_sender.connect_to_ev3()

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Toplevel()
    root.title("Capstone Project")

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief="groove")
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    #teleop_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # DONE: Implement and call get_my_frames(...)
    line_frame , teleop_frame = get_personal_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleop_frame, line_frame)
    LaptopHandler.window(root1)
    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    #real_thing(LaptopHandler)

    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
   # arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
   # control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
   # drive_frame = shared_gui.get_drive_frame(main_frame, mqtt_sender)

    return teleop_frame


def get_personal_frames(main_frame,mqtt_sender):
   line_frame = get_line_follow(main_frame, mqtt_sender)
   teleop_frame = get_teleoperation_frame(main_frame, mqtt_sender)

   return  line_frame, teleop_frame


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

    direction_label = ttk.Label(frame, text='Direction:')
    direction_entry = ttk.Entry(frame, width = 8)

    speed_label = ttk.Label(frame, text="Speed:")
    speed_entry = ttk.Entry(frame, width=8)

    area_label = ttk.Label(frame, text="Area:")
    area_entry = ttk.Entry(frame, width=8)

    scale = ttk.Scale(frame, from_= 0,to=100)

    pick_up_button = ttk.Button(frame, text="Pick up")
    m1_cam_pick_up =ttk.Button(frame, text='Camera pick up')

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    scale.grid(row=0,column=0)

    initial_rate_label.grid(row=1, column=0)
    initial_rate_entry.grid(row=1, column=1)

    increase_rate_label.grid(row=2, column=0)
    increase_rate_entry.grid(row=2, column=1)

    speed_label.grid(row=3, column=0)
    speed_entry.grid(row=3, column=1)

    pick_up_button.grid(row=6, column=1)
    m1_cam_pick_up.grid(row=6,column=0)

    direction_label.grid(row=5,column=0)
    direction_entry.grid(row=5,column=1)

    area_label.grid(row=4, column=0)
    area_entry.grid(row=4, column=1)

    # Set the Button callbacks:
    pick_up_button["command"] = lambda: handle_pick_up(mqtt_sender, initial_rate_entry, increase_rate_entry, speed_entry)
    m1_cam_pick_up['command']= lambda: handle_m1_cam_pick_up(mqtt_sender,direction_entry,initial_rate_entry,increase_rate_entry,speed_entry,area_entry)

    return frame


def get_line_follow(window, mqtt_sender):

    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    title = ttk.Label(frame,width = 16, text ='Line Follow')
    scale_title = ttk.Label(frame, text = 'Speed')

    scale = ttk.Scale(frame, from_=25, to=75)

    Sub_Point = ttk.Button(frame ,text = 'Subtract Point')

    lets_go_button = ttk.Button(frame, text = 'Lets Go!')
    pick_up_button = ttk.Button(frame, text = 'Pick up')
    Add_Point = ttk.Button(frame, text = "Add Point")

    title.grid(row=0, column=0)

    scale.grid(row=1,column=1)
    scale_title.grid(row=1,column=0)
    lets_go_button.grid(row=2,column=0)
    pick_up_button.grid(row=2, column=1)

    Sub_Point.grid(row=3, column=1)
    Add_Point.grid(row=3,column = 0)

    lets_go_button['command']= lambda : handle_lets_go(mqtt_sender,scale)
    pick_up_button['command'] = lambda: handle_pick_up(mqtt_sender, 5, 5, scale)
    Sub_Point['command']= lambda: handle_sub_point(mqtt_sender)
    Add_Point['command']= lambda: handle_add_point(mqtt_sender)






    return frame

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
    left_speed_label = ttk.Label(frame, text="Left wheel speed ")
    right_speed_label = ttk.Label(frame, text="Right wheel speed ")

    left_speed_entry = ttk.Scale(frame, from_=0, to=100 )
    right_speed_entry = ttk.Scale(frame, from_=0, to=100 )

    forward_button = ttk.Button(frame, text="Forward")
    backward_button = ttk.Button(frame, text="Backward")
    left_button = ttk.Button(frame, text="Left")
    right_button = ttk.Button(frame, text="Right")
    stop_button = ttk.Button(frame, text="Stop")
    grab_button = ttk.Button(frame, text ='Grab')
    drop_button = ttk.Button(frame, text='Drop')

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
    grab_button.grid(row= 5, column =0)
    backward_button.grid(row=5, column=1)
    drop_button.grid(row=5, column=2)

    forward_button["command"] = lambda: handle_forward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    backward_button["command"] = lambda: handle_backward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    left_button["command"] = lambda: handle_left(
        left_speed_entry, right_speed_entry, mqtt_sender)
    right_button["command"] = lambda: handle_right(
        left_speed_entry, right_speed_entry, mqtt_sender)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)
    drop_button['command'] = lambda: handle_lower_arm(mqtt_sender)
    grab_button["command"]=lambda: handle_raise_arm(mqtt_sender)

    return frame



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



def handle_pick_up(mqtt_sender, initial_rate_entry, increase_rate_entry, speed_entry,):
    print("Proximity pick up")
    mqtt_sender.send_message("m3_pick_up", [float(initial_rate_entry),
                                            float(increase_rate_entry),
                                            float(speed_entry.get())])


def handle_m1_cam_pick_up(mqtt_sender,direction_entry,initial_rate_entry,increase_rate_entry,speed_entry,area_entry):
    print('Picking up using camera')
    mqtt_sender.send_message("m1_camera_pick_up", [float(initial_rate_entry.get()),
                                                    float(increase_rate_entry.get()),
                                                    float(speed_entry.get()),
                                                    direction_entry.get(),
                                                    float(area_entry.get())])

def handle_forward(left_entry_box, right_entry_box, mqtt_sender):


    print("forward", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("forward", [int(left_entry_box.get()), int(right_entry_box.get())])


def handle_backward(left_entry_box, right_entry_box, mqtt_sender):


    print("backward", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("backward", [-int(left_entry_box.get()), -int(right_entry_box.get())])


def handle_left(left_entry_box, right_entry_box, mqtt_sender):

    print("left", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("left", [-int(left_entry_box.get()), int(right_entry_box.get())])


def handle_right(left_entry_box, right_entry_box, mqtt_sender):

    print("right", left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message("right", [int(left_entry_box.get()), -int(right_entry_box.get())])


def handle_stop(mqtt_sender):


    print("stop")
    mqtt_sender.send_message("stop")


def handle_lets_go(mqtt_sender,scale):
    print('Line Following')
    mqtt_sender.send_message("m1_line_follow",[float(scale.get())])

def handle_add_point(mqtt_sender):
    mqtt_sender.send_message('Add_Point')


def handle_sub_point(mqtt_sender):
    mqtt_sender.send_message('Sub_Point')




def real_thing(LaptopHandler):
    mqtt_reciever = com.MqttClient(LaptopHandler)
    mqtt_reciever.connect_to_ev3()



def grid_frames(teleop_frame, line_frame):
    teleop_frame.grid(row=0, column=0)
    line_frame.grid(row=0,column=2)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()


