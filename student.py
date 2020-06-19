from tkinter import *
import sqlite3

class Student(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.text = "Students"
        Label(self,text=self.text).pack()
        self.content = Frame(self)
        btn = Button(self,text="Add Student",fg="blue",command=self.create_add_window)
        btn.pack()
        self.content.pack()
        self.init_content()
        self.add_window = None
    def init_content(self):
        for child in self.content.winfo_children():
            child.destroy()
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("Select * From Student ORDER BY StudentLastName")
        students = c.fetchall()
        conn.commit()
        conn.close()
        for index,student in enumerate(students):
            Label(self.content,text=student[1],fg="black",relief="groove",borderwidth=1,width=7).grid(row=index,column=0)
            Label(self.content,text=student[2],fg="black",relief="groove",borderwidth=1,width=7).grid(row=index,column=1)
            Button(self.content,text="Schedule",fg="blue",relief="groove",borderwidth=1,width=7).grid(row=index,column=2)
            btn = Button(self.content,text="Delete",fg="red",width=7,command=lambda i=student[0]:self.delete_student(i))
            btn.grid(row=index,column=3)
    def reset_add_window(self):
        self.add_window.destroy()
        self.add_window = None
    def delete_student(self,id):
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("""
            DELETE FROM Student
            WHERE StudentID = :id
        """,{"id":id})
        conn.commit()
        conn.close()
        self.init_content()
    def create_add_window(self):       
        if(self.add_window!=None):
            self.reset_add_window()
        self.add_window = Toplevel(self)
        self.add_window.title("Add Student")
        self.add_window.protocol("WM_DELETE_WINDOW", self.reset_add_window)
        self.first_name = Entry(self.add_window)
        self.last_name = Entry(self.add_window)
        
        Label(self.add_window,text="First Name: ").grid(row=0,column=0)
        Label(self.add_window,text="Last Name: ").grid(row=1,column=0)
        self.first_name.grid(row=0,column=1)
        self.last_name.grid(row=1,column=1)

        btn = Button(self.add_window,text="Add Student",command=lambda: self.create_student(None))
        btn.grid(row=2,column=0,columnspan=2)

        self.first_name.focus()
        self.last_name.bind("<Return>",self.create_student)

    def create_student(self,e):
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO STUDENT(StudentFirstName,StudentLastName)
            VALUES(:first,:last)
        """,{
            "first" : self.first_name.get(),
            "last" : self.last_name.get()
        })
        conn.commit()
        conn.close()

        self.reset_add_window()
        self.init_content()
        