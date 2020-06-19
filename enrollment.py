from tkinter import *

class Enrollment(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.text = "Enrollment"
        Label(self,text=self.text).pack()