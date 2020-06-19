from tkinter import *
import sqlite3

class Course(Frame):
    def __init__(self,root):
        super().__init__(root)
        self.text = "Courses"
        Label(self,text=self.text).pack()
        btn = Button(self,text="Add Course",fg="blue",command=self.create_add_window)
        btn.pack()
        self.content = Frame(self)
        self.content.pack()
        self.init_content()
        self.add_window = None
    def reset_add_window(self):
        self.add_window.destroy()
        self.add_window = None

    def init_content(self):
        for child in self.content.winfo_children():
            child.destroy()
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("""
            SELECT *,Subject.SubjectName as SubjectName
            FROM Course
            INNER JOIN Subject ON Subject.SubjectID=Course.SubjectID
            ORDER BY SubjectName, CourseName
        """)
        courses = c.fetchall()
        conn.commit()
        conn.close()
        print(courses)
        for index,course in enumerate(courses):
            Label(self.content,text=course[4],borderwidth=1,width=7,relief="groove").grid(row=index,column=0)
            Label(self.content,text=course[1],borderwidth=1,width=17,relief="groove").grid(row=index,column=1)
            btn = Button(self.content,text="Delete",fg="red",command=lambda i=course[0]: self.delete_course(i))
            btn.grid(row=index,column=2)
            
    def init_subjects_menu(self):
        conn = sqlite3.connect('college_courses.db')
        c = conn.cursor()
        c.execute("""
            SELECT * FROM Subject ORDER BY SubjectName
        """)
        subjects = c.fetchall()
        conn.commit()
        conn.close()
        self.subjects_dict = {}
        for subject in subjects:
            self.subjects_dict[subject[1]] = subject[0]
        self.subject_chosen = StringVar(self.add_window)
        self.subject_chosen.set(subjects[0][1])
        self.subjects_menu = OptionMenu(self.add_window,self.subject_chosen,*self.subjects_dict.keys())
        print(subjects)
        print(self.subjects_dict)
    def create_course(self):
        name = self.course_name.get()
        id = self.subjects_dict[self.subject_chosen.get()]
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO course(CourseName,SubjectID)
            VALUES(:name,:id)
        """,{
            "name": name,
            "id": id
        })
        print(name,id)
        conn.commit()
        conn.close()
        self.reset_add_window()
        self.init_content()
    def delete_course(self,id):
        conn = sqlite3.connect("college_courses.db")
        c = conn.cursor()
        c.execute("""
            DELETE FROM Course
            WHERE CourseID = :id
        """,{"id":id})
        conn.commit()
        conn.close()
        self.init_content()
    def create_add_window(self):
        if(self.add_window!=None):
            self.reset_add_window()
        self.add_window = Toplevel(self)
        self.add_window.protocol("WM_DELETE_WINDOW",self.reset_add_window)
        self.add_window.title("Add Course")
        self.init_subjects_menu()

        Label(self.add_window,text="Course Name: ").grid(row=0,column=0)
        self.subjects_menu.grid(row=0,column=2)
        self.course_name = Entry(self.add_window)
        self.course_name.grid(row=0,column=1)
        self.course_name.focus()
        self.course_name.bind("<Return>",lambda e: self.create_course())

        btn = Button(self.add_window,text="Add Course",command=self.create_course)
        btn.grid(row=1,column=0,columnspan=3)
        