from tkinter import *
import sqlite3

class Subject(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.text = "Subjects"
        Label(self,text=self.text).pack()
        btn = Button(self,text="Add Subject",fg="blue",command=self.create_add_window)
        btn.pack()
        self.content = Frame(self)
        self.content.pack()
        self.init_content()
        self.add_window = None

    def reset_add_window(self):
        self.add_window.destroy()
        self.add_window = None

    def create_add_window(self):
        if(self.add_window!=None):
            self.reset_add_window()
        self.add_window = Toplevel(self)
        self.add_window.title("Add Subject")
        self.add_window.protocol("WM_DELETE_WINDOW", self.reset_add_window) 

        Label(self.add_window,text="Subject Name: ").grid(row=0,column=0)

        self.subject_name = Entry(self.add_window)
        self.subject_name.grid(row=0,column=1)
        self.subject_name.focus()
        self.subject_name.bind("<Return>",lambda e: self.create_subject())

        btn = Button(self.add_window,text="Add Subject",command=self.create_subject)
        btn.grid(row=1,column=0,columnspan=2)

    def create_subject(self):
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO Subject(SubjectName)
            VALUES(:name)
        """,{
            "name":self.subject_name.get()
        })
        conn.commit()
        conn.close()
        self.reset_add_window()
        self.init_content()

    def delete_subject(self,id):
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("""
            DELETE FROM Subject
            WHERE SubjectID = :id
        """,{"id":id})
        conn.commit()
        conn.close()
        self.init_content()

    def init_content(self):
        for child in self.content.winfo_children():
            child.destroy()
        conn = sqlite3.connect('college_courses.db')
        c = conn.cursor()
        c.execute("""
            SELECT * FROM SUBJECT ORDER BY SubjectName
        """)
        subjects = c.fetchall()
        conn.commit()
        conn.close()
        for index,subject in enumerate(subjects):
            Label(self.content,text=subject[1],borderwidth=1,width=7,relief="groove").grid(row=index,column=0)
            btn = Button(self.content,text="Delete",fg="red",width=7,command=lambda i=subject[0]:self.delete_subject(i))
            btn.grid(row=index,column=1)
        