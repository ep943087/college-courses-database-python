from tkinter import *

class Class(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.text = "Class"
        Label(self,text=self.text).pack()