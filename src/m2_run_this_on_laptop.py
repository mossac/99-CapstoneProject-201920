"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Guang Yang.
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
    c_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
#    proximity_frame = get_my_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames( c_frame)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()

def c_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=15, borderwidth=10, relief="ridge")
    frame_label = ttk.Label(frame, text="Ambulance")
    frame_label.grid(row=0, column=4)



    f_lable = ttk.Label(frame, text='Forward', anchor=tkinter.W)
    f_button = ttk.Button(frame, text='W')
    f_lable.grid(row=3, column=4)
    f_button.grid(row=3, column=5)

    l_lable = ttk.Label(frame, text='Left', anchor=tkinter.W)
    l_button = ttk.Button(frame, text='A')
    l_lable.grid(row=4, column=2)
    l_button.grid(row=4, column=3)

    b_lable = ttk.Label(frame, text='Backward', anchor=tkinter.W)
    b_button = ttk.Button(frame, text='S')
    b_lable.grid(row=5, column=4)
    b_button.grid(row=5, column=5)

    r_lable = ttk.Label(frame, text='Right', anchor=tkinter.W)
    r_button = ttk.Button(frame, text='D')
    r_lable.grid(row=4, column=6)
    r_button.grid(row=4, column=7)

    stop_lable = ttk.Label(frame, text='Stop', anchor=tkinter.W)
    stop_button = ttk.Button(frame, text='space')
    stop_lable.grid(row=4, column=4)
    stop_button.grid(row=4, column=5)
    speed_label = ttk.Label(frame, text="Speed:")
    speed_entry = ttk.Entry(frame, width=8)
    speed_label.grid(row=6, column=0)
    speed_entry.grid(row=6, column=1)
    distance_label = ttk.Label(frame, text="Distance:")
    distance_entry = ttk.Entry(frame, width=8)
    distance_label.grid(row=7, column=0)
    distance_entry.grid(row=7, column=1)

    window.bind_all('<Key-w>', lambda event:sforward(mqtt_sender, speed_entry, distance_entry))
    window.bind_all('<Key-s>', lambda event:sbackward(mqtt_sender, speed_entry))
    window.bind_all('<Key-a>', lambda event:sleft(mqtt_sender, speed_entry))
    window.bind_all('<Key-d>', lambda event:sright(mqtt_sender, speed_entry))
    window.bind_all('<Key- >', lambda event: stop(mqtt_sender))

    return frame


def get_shared_frames(main_frame, mqtt_sender):
   # teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    #arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    #control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    #drive_frame = shared_gui.get_drive_frame(main_frame, mqtt_sender)
    #sound_frame = shared_gui.get_sound_system_frame(main_frame, mqtt_sender)
    c_frame1= c_frame(main_frame, mqtt_sender)


    return c_frame1


#def get_my_frames(main_frame, mqtt_sender):
#    proximity_frame = get_proximity_sensor_frame(main_frame, mqtt_sender)

  #  return proximity_frame


#def get_proximity_sensor_frame(window, mqtt_sender):
    # Construct the frame to return:
 #   frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
  #  frame.grid()

    # Construct the widgets on the frame:
   # frame_label = ttk.Label(frame, text="Proximity Sensor")
    #initial_rate_label = ttk.Label(frame, text="Initial Frequency:")
    #initial_rate_entry = ttk.Entry(frame, width=8)

    #increase_rate_label = ttk.Label(frame, text="Increase Frequency Rate:")
    #increase_rate_entry = ttk.Entry(frame, width=8)

    #speed_label = ttk.Label(frame, text="Speed:")
    #speed_entry = ttk.Entry(frame, width=8)

    #pick_up_button = ttk.Button(frame, text="Pick up")
    #camera_pick_up_button = ttk.Button(frame, text="Camera Pick up")
    #camera_pick_up_button.grid(row=6, column=1)
    #area_label = ttk.Label(frame, text="Area:")
    #area_entry = ttk.Entry(frame, width=8)
    #direction_label = ttk.Label(frame, text="Direction:")
    #direction_entry = ttk.Entry(frame, width=8)
    #camera_pick_up_button["command"] = lambda: handle_camera_pick_up(mqtt_sender, direction_entry, initial_rate_entry,
                                                           #          increase_rate_entry, area_entry, speed_entry)
    # Grid the widgets:
    #frame_label.grid(row=0, column=1)




#def handle_pick_up(mqtt_sender, initial_rate_entry, increase_rate_entry, speed_entry):
    print("I will pick up object using the proximity sensor.")
    mqtt_sender.send_message("go_and_pick", [float(initial_rate_entry.get()),
                                            float(increase_rate_entry.get()),
                                            float(speed_entry.get())])


def grid_frames(c_frame):


    c_frame.grid(row=0,column=3)

def handle_camera_pick_up(mqtt_sender, direction_entry, initial_rate_entry, increase_rate_entry, area_entry, speed_entry):
    print("I will pick up object using the camera then proximity.")
    mqtt_sender.send_message("m2_camera_pick_up", [str(direction_entry.get()), float(initial_rate_entry.get()),
                                            float(increase_rate_entry.get()), float(speed_entry.get()),
                                            int(area_entry.get())])

def sforward(mqtt_sender, speed_entry, distance_entry):
    print('f')
    mqtt_sender.send_message("go_forward_danger",[int(speed_entry.get()),int(distance_entry.get())])

def sbackward(mqtt_sender,speed_entry):
    print('b')
    mqtt_sender.send_message("backward", [-int(speed_entry.get()),- int(speed_entry.get())])

def sleft(mqtt_sender, speed_entry):
    print('l')
    mqtt_sender.send_message("left", [int(speed_entry.get()), -int(speed_entry.get())])

def sright(mqtt_sender,speed_entry):
    print('r')
    mqtt_sender.send_message("right",[-int(speed_entry.get()), int(speed_entry.get())])

def stop(mqtt_sender):
    print('stop')
    mqtt_sender.send_message("stop")
# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
