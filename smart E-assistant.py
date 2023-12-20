import sqlite3
import tkinter
import tkinter.messagebox as tk
from tkinter.font import Font
from easygui import *
from tkinter import *
from turtle import *
import random

conn = sqlite3.connect('Assistant1.db')
cur = conn.cursor()


#conn.execute("CREATE TABLE learningstatus (domain_id int,student_id text,coursename text,knowledge text,typeofassistant text,description text,status text)")
#conn.execute("CREATE TABLE status (project_id int,student_id text,projectname text,teamcount text,typeofassistant text,description text,status text)")
#conn.execute("CREATE TABLE student (student_id text,Name text,designation text,skills text,ContactNumber text,Password text)")

def GuideLogin():
    message = "Enter Student ID and Password"
    title = "Login"
    fieldnames = ["Student ID", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)

    for row in conn.execute('SELECT * FROM student'):
        if field[0] == row[0] and field[1] == row[5]:
            global login
            login = field[0]
            f = 1
            print("Success")
            tkinter.messagebox.showinfo("Student Login", "Login Successfully")
            guidewindow()
            break
    else:
        print("Invalid")
        tk.showerror("Error info", "Incorrect student id or password")


def StudentLogin():
    message = "Enter Student ID and Password"
    title = "Student Login"
    fieldnames = ["Student ID", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)

    for row in conn.execute('SELECT * FROM student'):
        if field[0] == row[0] and field[1] == row[5]:
            global login
            login = field[0]
            f = 1
            print("Success")
            tkinter.messagebox.showinfo("Student Login", "Login Successfully")
            StudentLoginWindow()
            break
    else:
        print("Invalid")
        tk.showerror("Error info", "Incorrect student id or password")


def Studentlogout():
    global login
    login = -1
    LoginWindow.destroy()


def StudentProjectStatus():
    global projectStatus
    ProjectStatus = []
    for i in conn.execute('SELECT * FROM status where student_id=?', [login]):
        projectStatus = i

    WindowStatus()


def StudentAllStatus():
    allStatus = Toplevel()
    txt = Text(allStatus)
    for i in conn.execute('SELECT * FROM status where student_id=?', [login]):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def StudentInformationWindow():
    studentInformation = Toplevel()
    txt = Text(studentInformation)
    for i in conn.execute('SELECT student_id,Name,designation,skills,ContactNumber FROM student where student_id=?',
                          [login]):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def StudentAllInformationWindow():
    allStudentInformation = Toplevel()
    txt = Text(allStudentInformation)
    for i in conn.execute('SELECT student_id,Name,designation,skills,ContactNumber FROM student'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def WindowStatus():
    StatusWindow = Toplevel()
    label_1 = Label(StatusWindow, text="Student ID:", fg="blue", justify=LEFT, font=("Calibri", 16))
    label_2 = Label(StatusWindow, text=projectStatus[1], font=("Calibri", 16))
    label_3 = Label(StatusWindow, text="Domain", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_4 = Label(StatusWindow, text=projectStatus[2], font=("Calibri", 16))
    label_5 = Label(StatusWindow, text="Title", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_6 = Label(StatusWindow, text=projectStatus[3], font=("Calibri", 16))
    label_7 = Label(StatusWindow, text="Team Count", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_8 = Label(StatusWindow, text=projectStatus[4], font=("Calibri", 16))
    label_9 = Label(StatusWindow, text="Status:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_10 = Label(StatusWindow, text=projectStatus[6], font=("Calibri", 16))
    label_11 = Label(StatusWindow, text="Project ID:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_12 = Label(StatusWindow, text=projectStatus[0], font=("Calibri", 16))
    label_11.grid(row=0, column=0)
    label_12.grid(row=0, column=1)
    label_1.grid(row=1, column=0)
    label_2.grid(row=1, column=1)
    label_3.grid(row=2, column=0)
    label_4.grid(row=2, column=1)
    label_5.grid(row=3, column=0)
    label_6.grid(row=3, column=1)
    label_7.grid(row=4, column=0)
    label_8.grid(row=4, column=1)
    label_9.grid(row=5, column=0)
    label_10.grid(row=5, column=1)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Project<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def apply():
    message = "Enter the following details "
    title = "Project Registration"
    fieldNames = ["Student ID", "Project Name", "Team Count", "Assistant Type", "Description"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Project Domain"
    title1 = "Select Domain"
    choices = ["UI/UX", "Machine Learning", "AI", "Software Engineering", "Big Data", "Data Mining", "other"]
    choice = choicebox(message1, title1, choices)
    projectid = random.randint(1, 1000)

    conn.execute(
        "INSERT INTO status(Project_id,student_id,projectname,teamcount,typeofassistant,description,status) VALUES (?,?,?,?,?,?,?)",
        (projectid, fieldValues[0], choice, fieldValues[1], fieldValues[2], fieldValues[3], "Pending"))
    conn.commit()


def ProjectApproval():
    message = "Enter Project_id"
    title = "Assistance approval"
    fieldNames = ["Project_id"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Approve/Deny"
    title1 = "Approve"
    choices = ["approve", "deny"]
    choice = choicebox(message1, title1, choices)

    conn.execute("UPDATE status SET status = ? WHERE project_id= ?", (choice, fieldValues[0]))
    conn.commit()


def StudentallStatus():
    allStatus = Toplevel()
    txt = Text(allStatus)
    for i in conn.execute('SELECT * FROM status where student_id=?', [login]):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def Projectlist():
    projectlistwindow = Toplevel()
    txt = Text(projectlistwindow)
    for i in conn.execute('SELECT * FROM status'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Learning<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def courseApproval():
    message = "Enter Domain_id"
    title = "Assistance approval"
    fieldNames = ["Domain_id"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Approve/Deny"
    title1 = "Approve"
    choices = ["approve", "deny"]
    choice = choicebox(message1, title1, choices)

    conn.execute("UPDATE learningstatus SET status = ? WHERE domain_id= ?", (choice, fieldValues[0]))
    conn.commit()


def courselist():
    courselistwindow = Toplevel()
    txt = Text(courselistwindow)
    for i in conn.execute('SELECT * FROM learningstatus'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def WindowDomainStatus():
    StatusWindow = Toplevel()
    label_1 = Label(StatusWindow, text="Student ID:", fg="blue", justify=LEFT, font=("Calibri", 16))
    label_2 = Label(StatusWindow, text=projectStatus[1], font=("Calibri", 16))
    label_3 = Label(StatusWindow, text="Domain", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_4 = Label(StatusWindow, text=projectStatus[2], font=("Calibri", 16))
    label_5 = Label(StatusWindow, text="Topic", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_6 = Label(StatusWindow, text=projectStatus[3], font=("Calibri", 16))
    label_7 = Label(StatusWindow, text="Knowledge", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_8 = Label(StatusWindow, text=projectStatus[4], font=("Calibri", 16))
    label_9 = Label(StatusWindow, text="Status:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_10 = Label(StatusWindow, text=projectStatus[6], font=("Calibri", 16))
    label_11 = Label(StatusWindow, text="Course ID:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_12 = Label(StatusWindow, text=projectStatus[0], font=("Calibri", 16))
    label_11.grid(row=0, column=0)
    label_12.grid(row=0, column=1)
    label_1.grid(row=1, column=0)
    label_2.grid(row=1, column=1)
    label_3.grid(row=2, column=0)
    label_4.grid(row=2, column=1)
    label_5.grid(row=3, column=0)
    label_6.grid(row=3, column=1)
    label_7.grid(row=4, column=0)
    label_8.grid(row=4, column=1)
    label_9.grid(row=5, column=0)
    label_10.grid(row=5, column=1)


def StudentCourseStatus():
    global projectStatus
    ProjectStatus = []
    for i in conn.execute('SELECT * FROM learningstatus where student_id=?', [login]):
        projectStatus = i

    WindowDomainStatus()


def StudentAllStatus():
    allStatus = Toplevel()
    txt = Text(allStatus)
    for i in conn.execute('SELECT * FROM learningstatus where student_id=?', [login]):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def applyd():
    message = "Enter the following details "
    title = "Registration"
    fieldNames = ["Student ID", "Domain", "Knowledge level", "Assistant Type", "Description"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Domain"
    title1 = "Select general Domain(if present) "
    choices = ["UI/UX", "Machine Learning", "AI", "Software Engineering", "Big Data", "Data Mining", "other"]
    choice = choicebox(message1, title1, choices)
    domainid = random.randint(1, 1000)

    conn.execute(
        "INSERT INTO learningstatus(domain_id,student_id,coursename,knowledge,typeofassistant,description,status) VALUES (?,?,?,?,?,?,?)",
        (domainid, fieldValues[0], choice, fieldValues[1], fieldValues[2], fieldValues[3], "Pending"))
    conn.commit()


def CourseApproval():
    message = "Enter Domain_id"
    title = "Assistance approval"
    fieldNames = ["Domain_id"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Approve/Deny"
    title1 = "Approve"
    choices = ["approve", "deny"]
    choice = choicebox(message1, title1, choices)

    conn.execute("UPDATE status SET learningstatus = ? WHERE domain_id= ?", (choice, fieldValues[0]))
    conn.commit()


def Courselist():
    courselistwindow = Toplevel()
    txt = Text(courselistwindow)
    for i in conn.execute('SELECT * FROM learningstatus'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


########################################################################################################################################################################

def registration():
    message = "Enter Details of Student"
    title = "Registration"
    fieldNames = ["Student ID", "Name", "Designation", "Skills", "Contact Number", "Password"]
    fieldValues = []
    fieldValues = multpasswordbox(message, title, fieldNames)
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        if errmsg == "": break

        fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
    conn.execute("INSERT INTO student(student_id,Name,designation,skills,ContactNumber,Password) VALUES (?,?,?,?,?,?)",
                 (fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4], fieldValues[5]))

    conn.commit()


def StudentLoginWindow():
    global LoginWindow
    LoginWindow = Toplevel()
    LoginWindow.wm_attributes('-fullscreen', '1')
    Background_Label = Label(LoginWindow, image=filename)
    Background_Label.place(x=0, y=0, relwidth=1, relheight=1)

    informationStudent = Button(LoginWindow, text='User Information', command=StudentInformationWindow, bd=12,
                                relief=GROOVE, fg="black", bg="#36f575",
                                font=("Calibri", 36, "bold"), pady=3)
    informationStudent['font'] = BtnFont
    informationStudent.pack(fill=X)

    submit = Button(LoginWindow, text='Submit Project', command=apply, bd=12, relief=GROOVE, fg="black", bg="#ffce44",
                    font=("Calibri", 36, "bold"), pady=3)
    submit['font'] = BtnFont
    submit.pack(fill=X)

    ProjectApplicationStatus = Button(LoginWindow, text='Latest Project status', command=StudentProjectStatus, bd=12,
                                      relief=GROOVE, fg="white", bg="#357ec7",
                                      font=("Calibri", 36, "bold"), pady=3)
    ProjectApplicationStatus['font'] = BtnFont
    ProjectApplicationStatus.pack(fill=X)

    AllProjectStatus = Button(LoginWindow, text='All Projects status', command=StudentallStatus, bd=12, relief=GROOVE,
                              fg="black", bg="#b5eaaa",
                              font=("Calibri", 36, "bold"), pady=3)
    AllProjectStatus['font'] = BtnFont
    AllProjectStatus.pack(fill=X)

    Submit = Button(LoginWindow, text='Submit Domain(course)', command=applyd, bd=12, relief=GROOVE, fg="black",
                    bg="#ffce44",
                    font=("Calibri", 36, "bold"), pady=3)
    Submit['font'] = BtnFont
    Submit.pack(fill=X)

    CourseApplicationStatus = Button(LoginWindow, text='Latest course status', command=StudentCourseStatus, bd=12,
                                     relief=GROOVE, fg="white", bg="#357ec7",
                                     font=("Calibri", 36, "bold"), pady=3)
    CourseApplicationStatus['font'] = BtnFont
    CourseApplicationStatus.pack(fill=X)

    AllCourseStatus = Button(LoginWindow, text='All courses status', command=StudentAllStatus, bd=12, relief=GROOVE,
                             fg="black", bg="#b5eaaa",
                             font=("Calibri", 36, "bold"), pady=3)
    AllCourseStatus['font'] = BtnFont
    AllCourseStatus.pack(fill=X)

    LogoutBtn = Button(LoginWindow, text='Logout', bd=12, relief=GROOVE, fg="white", bg="#eb5406",
                       font=("Calibri", 36, "bold"), pady=3, command=Studentlogout)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationStudent.pack()
    submit.pack()
    ProjectApplicationStatus.pack()
    AllProjectStatus.pack()

    Submit.pack()
    CourseApplicationStatus.pack()
    AllCourseStatus.pack()

    LogoutBtn.pack()
    ExitBtn.pack()


def guidewindow():
    guidemainwindow = Toplevel()
    guidemainwindow.wm_attributes('-fullscreen', '1')
    Background_Label = Label(guidemainwindow, image=filename)

    Background_Label.place(x=0, y=0, relwidth=1, relheight=1)
    informationStudent = Button(guidemainwindow, text='User Information', command=StudentAllInformationWindow, bd=12,
                                relief=GROOVE, fg="black", bg="#36f575",
                                font=("Calibri", 36, "bold"), pady=3)
    informationStudent['font'] = BtnFont
    informationStudent.pack(fill=X)

    ProjectListButton = Button(guidemainwindow, text='Projects List', command=Projectlist, bd=12, relief=GROOVE,
                               fg="white", bg="#357ec7",
                               font=("Calibri", 36, "bold"), pady=3)
    ProjectListButton['font'] = BtnFont
    ProjectListButton.pack(fill=X)

    ApprovalButton = Button(guidemainwindow, text='Approve Project', command=ProjectApproval, bd=12, relief=GROOVE,
                            fg="black", bg="#ffce44",
                            font=("Calibri", 36, "bold"), pady=3)
    ApprovalButton['font'] = BtnFont
    ApprovalButton.pack(fill=X)

    CourseListButton = Button(guidemainwindow, text='Course List', command=courselist, bd=12, relief=GROOVE, fg="white",
                              bg="#357ec7",
                              font=("Calibri", 36, "bold"), pady=3)
    CourseListButton['font'] = BtnFont
    CourseListButton.pack(fill=X)

    CourseApprovalButton = Button(guidemainwindow, text='Approve Course', command=courseApproval, bd=12, relief=GROOVE,
                                  fg="black", bg="#ffce44",
                                  font=("Calibri", 36, "bold"), pady=3)
    CourseApprovalButton['font'] = BtnFont
    CourseApprovalButton.pack(fill=X)

    LogoutBtn = Button(guidemainwindow, text='Logout', command=guidemainwindow.destroy, bd=12, relief=GROOVE,
                       fg="white",
                       bg="#eb5406",
                       font=("Calibri", 36, "bold"), pady=3)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationStudent.pack()
    ProjectListButton.pack()
    ApprovalButton.pack()
    CourseListButton.pack()
    CourseApprovalButton.pack()
    ExitBtn.pack()


root = Tk()
root.wm_attributes('-fullscreen', '1')
root.title("E-Smart Assistant")
root.iconbitmap(default='logo.ico')
filename = PhotoImage(file="background.GIF")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
BtnFont = Font(family='Calibri(Body)', size=20)
MainLabel = Label(root, text="E-Smart Assistant", bd=12, relief=GROOVE, fg="white", bg="blue",
                  font=("Calibri", 36, "bold"), pady=3)
MainLabel.pack(fill=X)
im = PhotoImage(file='login.gif')

GuideLgnBtn = Button(root, text='Guide your mentee', bd=12, relief=GROOVE, fg="black", bg="#adf802",
                     font=("Calibri", 36, "bold"), pady=3, command=GuideLogin)
GuideLgnBtn['font'] = BtnFont
GuideLgnBtn.pack(fill=X)

LoginBtn = Button(root, text='Explore assistant ', bd=12, relief=GROOVE, fg="Black", bg="#9acd32",
                  font=("Calibri", 36, "bold"), pady=3, command=StudentLogin)
LoginBtn['font'] = BtnFont
LoginBtn.pack(fill=X)

StudentRegistration = Button(root, text='User Registration', command=registration, bd=12, relief=GROOVE, fg="black",
                             bg="#ffce44",
                             font=("Calibri", 36, "bold"), pady=3)
StudentRegistration['font'] = BtnFont
StudentRegistration.pack(fill=X)

ExitBtn = Button(root, text='Exit', command=root.destroy, bd=12, relief=GROOVE, fg="White", bg="#eb5406",
                 font=("Calibri", 36, "bold"), pady=3)
ExitBtn['font'] = BtnFont
ExitBtn.pack(fill=X)
MainLabel.pack()
GuideLgnBtn.pack()
LoginBtn.pack()
StudentRegistration.pack()
ExitBtn.pack()

root.mainloop()
