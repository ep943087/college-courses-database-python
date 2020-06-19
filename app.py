from tkinter import *
from student import *
from teacher import *
from subject import *
from course import *
from Class import *
from enrollment import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("College Courses")
        self.geometry("500x500")
        self.resizable(False,False)
        self.windows = [Student(self),Teacher(self),Subject(self),Course(self),Class(self)]
        self.set_navigation()
        self.set_window(0)
    def set_window(self,index):
        for window in self.windows:
            window.forget()
        self.cur_window = self.windows[index]
        self.cur_window.pack()
    def set_navigation(self):
        nav = Frame(self)
        for i,window in enumerate(self.windows):
            btn = Button(nav,fg="blue",text=window.text,command= lambda i=i: self.set_window(i))
            btn.grid(row=0,column=i) 
        nav.pack()           

    def run(self):
        self.mainloop()