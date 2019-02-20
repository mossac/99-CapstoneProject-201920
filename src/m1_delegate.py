import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import time


class LaptopHandler(object):

    def __init__(self,root1):
        self.main_frame = root1
        self.points = 0
        self.can_score = False
        pass

    def window(self, root1):
        root1.title("Scoreboard")
        root1.geometry("300x300")

        canvas = tkinter.Canvas(root1, width='800', height='800', bg='blue')
        canvas.grid()
        canvas.create_text(150, 150, text="Points:"+ str(self.points))

    def add_point(self):
        print('recieved')
        if self.can_score is True:
            self.points =self.points+1
            self.can_score = False

    def can_score(self):
        print('recieved')
        self.can_score = True

    def sub_point(self):
        print("Removing Point")
        self.points = self.points - 1

