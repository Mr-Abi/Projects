from tkinter import *
from tkinter import colorchooser
import random
import psycopg2
import hashlib

s = Tk()
s.title("Login Portal")
s.geometry("700x700")
s.config(bg="black")
s.resizable(False, False)

hostname = 'localhost'
database = 'Learn'
username = 'postgres'
pwd = 'mygres'
port_id = 5432

fc = "pink"
bc = "black"


def login_page():
    global emp_id
    global list3

    def show_password():
        show_state.set(not show_state.get())
        if show_state.get():
            show_button.config(text="Hide")
            password_entry.config(show="")
        else:
            password_entry.config(show="*")
            show_button.config(text="Show")

    def db_update():
        global new_password_entry
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id,
        )
        sha256_hash = hashlib.sha256()

        # Update the hash object with the input string encoded as bytes
        sha256_hash.update(new_password_entry.get().encode('utf-8'))

        # Get the hexadecimal representation of the hashed value
        hashed_password = sha256_hash.hexdigest()

        cur = conn.cursor()
        cur.execute(f"update employee_details set password = '{hashed_password}' where emp_id={emp_id}")

        conn.commit()
        cur.close()
        conn.close()

        for k in list3:
            k.destroy()

        login_page()

    def proceed():
        global list3
        global list2
        global check_password_entry
        global emp_id
        global new_password_entry
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id,
        )

        checked_password = check_password_entry.get()
        sha256_hash = hashlib.sha256()

        # Update the hash object with the input string encoded as bytes
        sha256_hash.update(checked_password.encode('utf-8'))
        print('checked password_entry', checked_password)

        # Get the hexadecimal representation of the hashed value
        checked_hashed_password = sha256_hash.hexdigest()
        print('checked_hashed_password', checked_hashed_password)

        cur = conn.cursor()
        cur.execute(f' select password from employee_details where emp_id = {emp_id} ')
        employee_id = (cur.fetchone())

        for emp_password in employee_id:
            print(str(emp_password))

        if checked_hashed_password == emp_password:
            for j in list2:
                j.destroy()
            new_password_label = Label(s, text="New Password", fg=fc, bg=bc, font=("arial", 15))
            new_password_label.place(x=200, y=100)

            new_password_entry = Entry(s, fg=fc, bg=bc, width=30)
            new_password_entry.place(x=280, y=250)

            go_button = Button(s, text="Go", fg=fc, bg=bc, command=db_update, height=3, width=25, font=("arial", 10))
            go_button.place(x=270, y=310)
            list3 = [new_password_label, new_password_entry, go_button]
        else:
            print('Not')

    def details():
        pass

    def change_password():
        global details_button
        global change_password_button
        global change_password_entry
        global check_password_entry
        global list2

        details_button.destroy()
        change_password_button.destroy()

        notice_label = Label(s, text="Please enter existing password to change password ! ", fg=fc, bg=bc, font=("arial", 15))
        notice_label.place(x=100, y=100)

        change_password_label = Label(s, text="Enter Password ", fg=fc, bg=bc, font=("arial", 15))
        change_password_label.place(x=300, y=200)

        check_password_entry = Entry(s, show="*", fg=fc, bg=bc, width=30)
        check_password_entry.place(x=280, y=250)
        check_password_entry.focus_set()

        proceed_button = Button(s, text="--->", fg=fc, bg=bc, command=proceed, height=3, width=25, font=("arial", 10))
        proceed_button.place(x=270, y=310)

        list2 = [notice_label, change_password_label, check_password_entry, proceed_button]

    def login():
        global details_button
        global change_password_button
        global emp_id
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id,
        )

        sha256_hash = hashlib.sha256()

        # Update the hash object with the input string encoded as bytes
        sha256_hash.update(password_entry.get().encode('utf-8'))

        # Get the hexadecimal representation of the hashed value
        entered_hashed_password = sha256_hash.hexdigest()

        cur = conn.cursor()
        emp_id = employee_id_entry.get()
        cur.execute(f' select password from employee_details where emp_id = {emp_id} ')
        employee_id = (cur.fetchone())

        if employee_id == None:
            print("No such Emp_Id")
        else:
            for emp_password in employee_id:
                print(str(emp_password))
            print(password_entry.get())

            if entered_hashed_password == emp_password:
                print('Access Approved')
                for j in pack:
                    j.destroy()
                details_button = Button(s, text="Details", fg=fc, bg=bc, command=details, height=3, width=25, font=("arial", 10))
                details_button.place(x=270, y=310)

                change_password_button = Button(s, text="Change Password", fg=fc, bg=bc, command=change_password,
                                                height=3, width=25, font=("arial", 10))
                change_password_button.place(x=270, y=410)
            else:
                print('Access Denied')
                employee_id_entry.delete(0, END)
                password_entry.delete(0, END)
        conn.commit()
        cur.close()
        conn.close()

    def fontc():
        fc = colorchooser.askcolor()[1]
        title_label.config(fg=fc)
        employee_id_label.config(fg=fc)
        password_label.config(fg=fc)
        password_entry.config(fg=fc)
        portal_label.config(fg=fc)
        login_button.config(fg=fc)
        create_account_button.config(fg=fc)
        show_button.config(fg=fc)
        employee_id_entry.config(fg=fc)
        password_entry.config(fg=fc)

    def bco():
        bc = colorchooser.askcolor()[1]
        s.config(bg=bc)
        title_label.config(bg=bc)
        employee_id_label.config(bg=bc)
        password_label.config(bg=bc)
        employee_id_entry.config(bg=bc)
        password_entry.config(bg=bc)
        portal_label.config(bg=bc)
        show_button.config(bg=bc)
        login_button.config(bg=bc)
        create_account_button.config(bg=bc)

    global pack
    title_label = Label(s, text="Employee Portal", fg=fc, bg=bc, font=("arial", 30))
    title_label.place(x=220, y=10)

    employee_id_label = Label(s, text="Employee ID", fg=fc, bg=bc, font=("arial", 20))
    employee_id_label.place(x=295, y=200)

    employee_id_entry = Entry(s, fg=fc, bg=bc, width=30)
    employee_id_entry.place(x=280, y=250)
    employee_id_entry.focus_set()

    password_label = Label(s, text="Password", fg=fc, bg=bc, font=("arial", 20))
    password_label.place(x=305, y=350)

    password_variable = StringVar()
    show_state = BooleanVar(value=False)
    password_entry = Entry(s, fg=fc, bg=bc, show="*", width=30)
    password_entry.place(x=280, y=400)

    show_button = Button(s, text="Show", fg=fc, bg=bc, command=show_password, height=1, width=5)
    show_button.place(x=350, y=450)

    login_button = Button(s, text="Login", fg=fc, bg=bc, command=login, height=3, width=25, font=("arial", 10))
    login_button.place(x=270, y=510)

    create_account_button = Button(s, text="Create Account", fg=fc, bg=bc, command=create_account, height=3, width=25, font=("arial", 10))
    create_account_button.place(x=270, y=610)

    portal_label = Label(s, text="@ Employee Portal", fg=fc, bg=bc, font=("arial", 10))
    portal_label.place(x=570, y=650)

    pack = [title_label, employee_id_label, employee_id_entry, password_label, password_entry, show_button, login_button, portal_label, create_account_button]

    my_menu = Menu(s)
    s.config(menu=my_menu)
    file = Menu(my_menu)
    my_menu.add_cascade(label="Theme", menu=file)
    file.add_command(label="Font", command=fontc)
    file.add_command(label="BG", command=bco)

    s.mainloop()


def create_account():

    def show_password():
        show_state.set(not show_state.get())
        if show_state.get():
            show_button.config(text="Hide")
            create_password_entry.config(show="")
        else:
            create_password_entry.config(show="*")
            show_button.config(text="Show")

    def fontc():
        fc = colorchooser.askcolor()[1]
        title_label.config(fg=fc)
        employee_id_label.config(fg=fc)
        create_password_label.config(fg=fc)
        name_label.config(fg=fc)
        age_label.config(fg=fc)
        mail_label.config(fg=fc)
        salary_label.config(fg=fc)
        experience_label.config(fg=fc)
        department_label.config(fg=fc)
        employee_id_entry.config(fg=fc)
        create_password_entry.config(fg=fc)
        name_entry.config(fg=fc)
        age_entry.config(fg=fc)
        mail_entry.config(fg=fc)
        salary_entry.config(fg=fc)
        experience_entry.config(fg=fc)
        department_entry.config(fg=fc)
        portal_label.config(fg=fc)
        show_button.config(fg=fc)
        signup_button.config(fg=fc)

    def bco():
        bc = colorchooser.askcolor()[1]
        s.config(bg=bc)
        title_label.config(bg=bc)
        employee_id_label.config(bg=bc)
        create_password_label.config(bg=bc)
        name_label.config(bg=bc)
        age_label.config(bg=bc)
        mail_label.config(bg=bc)
        salary_label.config(bg=bc)
        experience_label.config(bg=bc)
        department_label.config(bg=bc)
        employee_id_entry.config(bg=bc)
        create_password_entry.config(bg=bc)
        name_entry.config(bg=bc)
        age_entry.config(bg=bc)
        mail_entry.config(bg=bc)
        salary_entry.config(bg=bc)
        experience_entry.config(bg=bc)
        department_entry.config(bg=bc)
        portal_label.config(bg=bc)
        show_button.config(bg=bc)
        signup_button.config(bg=bc)

    def signup():
        def show_password():
            show_state.set(not show_state.get())
            if show_state.get():
                show_button.config(text="Hide")
                password_entry.config(show="")
            else:
                password_entry.config(show="*")
                show_button.config(text="Show")

        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id,
        )
        cursor = conn.cursor()

        sha256_hash = hashlib.sha256()

        # Update the hash object with the input string encoded as bytes
        sha256_hash.update(create_password_entry.get().encode('utf-8'))

        # Get the hexadecimal representation of the hashed value
        hashed_password = sha256_hash.hexdigest()

        script = """ create table if not exists Employee_Details(S_No serial, Emp_ID int primary key, Password varchar(300), 
        Name varchar(30) not null, Age int, Mail varchar(30), Salary int, Experience int, Department varchar(30)) """
        cursor.execute(script)

        insert_script = """insert into Employee_Details(Emp_ID, Password, Name, Age, Mail, Salary, Experience, Department) 
        values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        insert_value = (employee_id_entry.get(), hashed_password, name_entry.get(), age_entry.get(), mail_entry.get(),
                        salary_entry.get(),
                        experience_entry.get(), department_entry.get())

        cursor.execute(insert_script, insert_value)
        conn.commit()
        cursor.close()
        conn.close()

        list1 = [employee_id_entry, create_password_entry, name_entry, age_entry, mail_entry, salary_entry,
                 experience_entry,
                 department_entry]
        for i in list1:
            i.delete(0, END)

        pack_list = [title_label, employee_id_label, employee_id_entry, create_password_label, create_password_entry,
                     show_button,
                     name_label, name_entry, age_label, age_entry, mail_label, mail_entry, salary_label, salary_entry,
                     experience_label, experience_entry, department_label, department_entry, signup_button,
                     portal_label]

        for i in pack_list:
            i.destroy()

        login_page()

    for i in pack:
        i.destroy()

    title_label = Label(s, text="Employee Portal", fg=fc, bg=bc, font=("arial", 30))
    title_label.place(x=200, y=10)

    employee_id_label = Label(s, text="ID", fg=fc, bg=bc, font=("arial", 20))
    employee_id_label.place(x=200, y=100)

    employee_id_entry = Entry(s, fg=fc, bg=bc, width=20)
    employee_id_entry.place(x=150, y=150)
    employee_id_entry.focus_set()
    emp_id = employee_id_entry.get()

    create_password_label = Label(s, text="Password", fg=fc, bg=bc, font=("arial", 20))
    create_password_label.place(x=460, y=100)

    password_variable = StringVar()
    show_state = BooleanVar(value=False)
    create_password_entry = Entry(s, fg=fc, bg=bc, show="*", width=30)
    create_password_entry.place(x=430, y=150)

    show_button = Button(s, text="Show", fg=fc, bg=bc, command=show_password, height=1, width=5)
    show_button.place(x=500, y=180)

    name_label = Label(s, text="Name", fg=fc, bg=bc, font=("arial", 20))
    name_label.place(x=120, y=250)

    name_entry = Entry(s, fg=fc, bg=bc, width=20)
    name_entry.place(x=100, y=300)

    age_label = Label(s, text="Age", fg=fc, bg=bc, font=("arial", 20))
    age_label.place(x=325, y=250)

    age_entry = Entry(s, fg=fc, bg=bc, width=20)
    age_entry.place(x=295, y=300)

    mail_label = Label(s, text="Mail", fg=fc, bg=bc, font=("arial", 20))
    mail_label.place(x=530, y=250)

    mail_entry = Entry(s, fg=fc, bg=bc, width=20)
    mail_entry.place(x=500, y=300)

    salary_label = Label(s, text="Salary", fg=fc, bg=bc, font=("arial", 20))
    salary_label.place(x=120, y=400)

    salary_entry = Entry(s, fg=fc, bg=bc, width=20)
    salary_entry.place(x=100, y=450)

    experience_label = Label(s, text="Experience", fg=fc, bg=bc, font=("arial", 20))
    experience_label.place(x=290, y=400)

    experience_entry = Entry(s, fg=fc, bg=bc, width=20)
    experience_entry.place(x=300, y=450)

    department_label = Label(s, text="Department", fg=fc, bg=bc, font=("arial", 20))
    department_label.place(x=500, y=400)

    department_entry = Entry(s, fg=fc, bg=bc, width=20)
    department_entry.place(x=510, y=450)

    signup_button = Button(s, text="Sign Up", fg=fc, bg=bc, command=signup, height=3, width=25, font=("arial", 10))
    signup_button.place(x=250, y=550)

    portal_label = Label(s, text="@ Employee Portal", fg=fc, bg=bc, font=("arial", 10))
    portal_label.place(x=570, y=650)

    pack_list = [title_label, employee_id_label, employee_id_entry, create_password_label, create_password_entry,
                 show_button, name_label, name_entry, age_label, age_entry, mail_label, mail_entry, salary_label,
                 salary_entry, experience_label, experience_entry, department_label, department_entry, signup_button,
                 portal_label]

    my_menu = Menu(s)
    s.config(menu=my_menu)
    file = Menu(my_menu)
    my_menu.add_cascade(label="Theme", menu=file)
    file.add_command(label="Font", command=fontc)
    file.add_command(label="BG", command=bco)


login_page()

s.mainloop()
