import tkinter as tk
from tkinter import messagebox
from database import connectDatabase
from functions import *
from functions.methods import *

DARK_BG = "#2b2b2b"
TEXT_COLOR = "#e6e6e6"
BUTTON_BG = "#3c3f41"
ENTRY_BG = "#3c3f41"
TEXTBOX_BG = "#1e1e1e"
TEXTBOX_FG = "#00ffcc"
FONT = ('Segoe UI', 11)

class GymApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Management System")
        self.geometry("1000x800")
        self.configure(bg=DARK_BG)
        self.resizable(True, True)

        self.db_connection = None
        self.frames = {}

        container = tk.Frame(self, bg=DARK_BG)
        container.pack(fill="both", expand=True)

        for F in (StartPage, MainMenu, MembersMenu, ClassesMenu, EquipmentMenu):
            frame = F(container, self)
            frame.configure(bg=DARK_BG)
            self.frames[F] = frame
            frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def connect_to_db(self, db_name):
        self.db_connection = connectDatabase()
        return self.db_connection is not None


class CenteredFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=DARK_BG)
        self.pack(fill="both", expand=True)
        self.inner = tk.Frame(self, bg=DARK_BG)
        self.inner.place(relx=0.5, rely=0.5, anchor="center")


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=DARK_BG)
        wrapper = CenteredFrame(self)
        wrapper.pack(fill="both", expand=True)
        inner = wrapper.inner

        tk.Label(inner, text="Enter database name (e.g. XYZGym.sqlite):", font=FONT, fg=TEXT_COLOR, bg=DARK_BG).pack(pady=20)
        self.db_entry = tk.Entry(inner, width=40, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
        self.db_entry.pack(pady=10)

        self.status_label = tk.Label(inner, text="", fg="red", bg=DARK_BG, font=FONT)
        self.status_label.pack()

        connect_btn = tk.Button(inner, text="Connect", font=FONT, bg=BUTTON_BG, fg=TEXT_COLOR, width=20,
                                command=lambda: self.connect(controller))
        connect_btn.pack(pady=10)

    def connect(self, controller):
        db_name = self.db_entry.get().strip()
        if not db_name:
            self.status_label.config(text="❌ Database name cannot be empty.", fg="red")
            return

        self.status_label.config(text="Connecting...", fg="blue")
        self.update_idletasks()

        if controller.connect_to_db(db_name):
            self.status_label.config(text="✅ Connected successfully!", fg="green")
            messagebox.showinfo("Connection", "Successfully connected to the database!")
            self.after(1000, lambda: controller.show_frame(MainMenu))
        else:
            self.status_label.config(text="❌ Failed to connect to database.", fg="red")
            messagebox.showerror("Connection Failed", "Could not connect to the database.")


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=DARK_BG)
        wrapper = CenteredFrame(self)
        wrapper.pack(fill="both", expand=True)
        inner = wrapper.inner

        tk.Label(inner, text="Main Menu", font=('Segoe UI', 18), bg=DARK_BG, fg=TEXT_COLOR).pack(pady=30)
        tk.Button(inner, text="Members Menu", width=30, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=lambda: controller.show_frame(MembersMenu)).pack(pady=5)
        tk.Button(inner, text="Classes Menu", width=30, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=lambda: controller.show_frame(ClassesMenu)).pack(pady=5)
        tk.Button(inner, text="Equipment Menu", width=30, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=lambda: controller.show_frame(EquipmentMenu)).pack(pady=5)
        tk.Button(inner, text="Logout and Exit", width=30, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=controller.destroy).pack(pady=30)


class MembersMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=DARK_BG)
        wrapper = CenteredFrame(self)
        wrapper.pack(fill="both", expand=True)
        inner = wrapper.inner

        tk.Label(inner, text="Members Menu", font=('Segoe UI', 16), bg=DARK_BG, fg=TEXT_COLOR).pack(pady=10)
        self.output = tk.Text(inner, height=20, width=100, wrap="word", bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self.output.pack(pady=10)
        self.output.config(state='disabled')

        tk.Button(inner, text="View All Members", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_all_members).pack(pady=2)
        tk.Button(inner, text="Expired Memberships", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_expired_memberships).pack(pady=2)
        tk.Button(inner, text="Average Member Age", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_average_age).pack(pady=2)
        tk.Button(inner, text="View All Membership Plans", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_membership_options).pack(pady=2)
        tk.Button(inner, text="Back to Main Menu", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=lambda: controller.show_frame(MainMenu)).pack(pady=10)

        # Implementing CRUD commands. ------------------------------------------------------------------------------------------------
        tk.Button(inner, text="Add New Member", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.add_member).pack(pady=2)
        tk.Button(inner, text="Edit Existing Member", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.edit_member).pack(pady=2)
        tk.Button(inner, text="Delete Existing Member", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.delete_member).pack(pady=2)

    def show_all_members(self):
        result = getAllMembers(return_output=True)
        self.display(result)

    def show_expired_memberships(self):
        result = getExpiredMemberships(return_output=True)
        self.display(result)

    def show_average_age(self):
        result = calculateAverageAge(return_output=True)
        self.display(result)

    def show_membership_options(self):
        result = getAllMemberships(return_output=True)
        self.display(result)

    # ----------------------------------------------------------------------------------------------------------------------------
    def add_member(self):
        def submit():
            try:
                args = [entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(), entries[4].get(),
                        entries[5].get(), entries[6].get(), entriesB[0].get(), entriesB[1].get()]
                top.destroy()
                newMember(args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Member Table Editing")
        top.configure(bg=DARK_BG)
        
        entry_frameA = tk.Frame(top, bg=DARK_BG)
        entry_frameA.pack(side="top", fill="x")
        tk.Label(entry_frameA, text="Enter, respectively: Name, Email, Phone Number, Address, Age, Membership Start Date, Membership End Date", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        entries = [tk.Entry(entry_frameA, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(7)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5, pady=30)

        entry_frameB = tk.Frame(top, bg=DARK_BG)
        entry_frameB.pack(side="top", fill="x")
        tk.Label(entry_frameB, text="(Optional) - Enter: Plan ID, Payment Date, ", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        entriesB = [tk.Entry(entry_frameB, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(2)]
        for entry in entriesB:
            entry.pack(side=tk.TOP, padx=5, pady=5)

        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def edit_member(self):
        def submit():
            try:
                memberId = idEntry.get()
                args = [entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(), entries[4].get(),
                        entries[5].get(), entries[6].get(), entries[7].get()]
                top.destroy()
                updateMember(memberId, args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Member Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter the ID of the member to be updated.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        idEntry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        idEntry.pack(pady=5)

        #("Name,\t"+"Email,\t"+"Phone,\t"+"Address,\t"+"Age,\t"+"Membership Start,\t"+"Membership End").expandtabs(10)
        tk.Label(top, text="Enter, respectively: Name, Email, Phone Number, Address, Age, Membership Start Date, Membership End Date, Plan ID (optional)", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        tk.Label(top, text="Entries left empty will not update their respective attribute - they will stay the same.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(8)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def delete_member(self):
        def submit():
            try:
                memberId = idEntry.get()
                top.destroy()
                delMember(memberId)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Member Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter the ID of the member to be deleted.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        idEntry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        idEntry.pack(pady=5)

        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
    # ----------------------------------------------------------------------------------------------------------------------------

    def display(self, text):
        self.output.config(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state='disabled')

class ClassesMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=DARK_BG)
        wrapper = CenteredFrame(self)
        wrapper.pack(fill="both", expand=True)
        inner = wrapper.inner

        tk.Label(inner, text="Classes Menu", font=('Segoe UI', 16), bg=DARK_BG, fg=TEXT_COLOR).pack(pady=10)
        self.output = tk.Text(inner, height=20, width=100, wrap="word", bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self.output.pack(pady=10)
        self.output.config(state='disabled')

        button_frameA = tk.Frame(inner, bg=DARK_BG)
        button_frameA.pack(side=tk.LEFT, fill="x")
        tk.Button(button_frameA, text="Show All Classes", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_classes).pack(pady=2)
        tk.Button(button_frameA, text="Top Instructors", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.top_instructors).pack(pady=2)
        tk.Button(button_frameA, text="Classes by Instructor", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.classes_by_instructor).pack(pady=2)
        tk.Button(button_frameA, text="Find Members by Class ID", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.members_by_class).pack(pady=2)
        tk.Button(button_frameA, text="Members Attending All Yoga Classes", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.members_by_type).pack(pady=2)
        
        tk.Button(button_frameA, text="Show All Attendance", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_attendance).pack(pady=20)
        tk.Button(button_frameA, text="Recent Class Attendance", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.recent_attendance).pack(pady=2)
        
        # Implementing CRUD commands. ------------------------------------------------------------------------------------------------
        button_frameB = tk.Frame(inner, bg=DARK_BG)
        button_frameB.pack(side=tk.RIGHT, fill="x")
        tk.Button(button_frameB, text="Add New Class", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.add_class).pack(pady=2)
        tk.Button(button_frameB, text="Edit Existing Class", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.edit_class).pack(pady=2)
        tk.Button(button_frameB, text="Delete Existing Class", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.delete_class).pack(pady=2)
        
        tk.Button(button_frameB, text="Add Class Attendance", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.add_class_attendance).pack(pady=2)
        tk.Button(button_frameB, text="Update Class Attendance", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.update_class_attendance).pack(pady=2)
        tk.Button(button_frameB, text="Delete Class Attendance", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.delete_class_attendance).pack(pady=2)
        # ----------------------------------------------------------------------------------------------------------------------------
        
        tk.Button(button_frameB, text="Back to Main Menu", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=lambda: controller.show_frame(MainMenu)).pack(pady=20)

    def display(self, text):
        self.output.config(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state='disabled')

    def show_classes(self):
        self.display(showClasses(return_output=True))

    def top_instructors(self):
        self.display(topInstructors(return_output=True))

    def classes_by_instructor(self):
        def submit():
            try:
                instructor_id = int(entry.get())
                top.destroy()
                self.display(getClassesByInstructor(instructor_id, return_output=True))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid instructor ID.")

        top = tk.Toplevel(self)
        top.title("Enter Instructor ID")
        top.configure(bg=DARK_BG)
        tk.Label(top, text="Instructor ID:", bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        entry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        entry.pack(pady=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def members_by_class(self):
        def submit():
            try:
                class_id = int(entry.get())
                top.destroy()
                self.display(getMembersByClass(class_id, return_output=True))
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid class ID.")

        top = tk.Toplevel(self)
        top.title("Enter Class ID")
        top.configure(bg=DARK_BG)
        tk.Label(top, text="Class ID:", bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        entry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        entry.pack(pady=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def members_by_type(self):
        self.display(findMembersByClassType("Yoga", return_output=True))

    def show_attendance(self):
        self.display(showClassAttendance(return_output=True))

    def recent_attendance(self):
        self.display(recentClassAttendance(return_output=True))

    # ----------------------------------------------------------------------------------------------------------------------------
    def add_class(self):
        def submit():
            try:
                args = [entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(), entries[4].get(),
                        entries[5].get()]
                top.destroy()
                newClass(args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Class Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter, respectively: Class Name, Class Type, Duration, Class Capacity, The Instructor's ID, The Gym's ID", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(6)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def edit_class(self):
        def submit():
            classId = idEntry.get()
            args = [entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get(), entries[4].get(),
                    entries[5].get()]
            top.destroy()
            updateClass(classId, args)

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Class Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter the ID of the class to be updated.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        idEntry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        idEntry.pack(pady=5)

        tk.Label(top, text="Enter, respectively: Class Name, Class Type, Duration, Class Capacity, The Instructor's ID, The Gym's ID", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        tk.Label(top, text="Entries left empty will not update their respective attribute - they will stay the same.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(6)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def delete_class(self):
        def move_class_members(classId):
            def submitMove():
                try:
                    newId = newIdEntry.get()
                    top.destroy()
                    moveMembersOfClass(classId, newId)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid class.")

            top = tk.Toplevel(self, height=500, width=500)
            top.title("Move Class Members")
            top.configure(bg=DARK_BG)

            tk.Label(top, text="Registered members must attend a class. Enter a class ID to move this class' members to.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
            newIdEntry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
            newIdEntry.pack(pady=5)

            tk.Button(top, text="Submit", command=submitMove, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        def submit():
            try:
                classId = idEntry.get()
                top.destroy()

                if checkClassEnrollment(classId) == True:
                    move_class_members(classId)

                delClass(classId)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Class Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter the ID of the class to be deleted.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        idEntry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        idEntry.pack(pady=5)

        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    # ----------------------------------------------------------------------------------------------------------------------------
    def add_class_attendance(self):
        def submit():
            try:
                args = [entries[0].get(), entries[1].get(), entries[2].get()]
                top.destroy()
                addClassAttendee(args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Attendance Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter, respectively: The Member's ID, The Class ID, Attendance Date", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(3)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def update_class_attendance(self):
        def submit():
            try:
                args = [entries[0].get(), entries[1].get()]
                top.destroy()
                updateClassAttendee(args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Attendance Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter, respectively: The Member's ID, The New Class' ID", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(2)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def delete_class_attendance(self):
        def submit():
            try:
                args = [entries[0].get(), entries[1].get()]
                top.destroy()
                deleteClassAttendee(args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Attendance Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter, respectively: The Member's ID, The Class' ID", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(2)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
    # ----------------------------------------------------------------------------------------------------------------------------


class EquipmentMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=DARK_BG)
        wrapper = CenteredFrame(self)
        wrapper.pack(fill="both", expand=True)
        inner = wrapper.inner

        tk.Label(inner, text="Equipment Menu", font=('Segoe UI', 16), bg=DARK_BG, fg=TEXT_COLOR).pack(pady=10)
        self.output = tk.Text(inner, height=20, width=100, wrap="word", bg=TEXTBOX_BG, fg=TEXTBOX_FG)
        self.output.pack(pady=10)
        self.output.config(state='disabled')

        tk.Button(inner, text="Show Cardio Equipment", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_cardio).pack(pady=2)
        tk.Button(inner, text="Show Strength Equipment", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_strength).pack(pady=2)
        tk.Button(inner, text="Show All Equipment", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.show_equipment).pack(pady=2)
        tk.Button(inner, text="Back to Main Menu", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=lambda: controller.show_frame(MainMenu)).pack(pady=10)
        
        # Implementing CRUD commands. ------------------------------------------------------------------------------------------------
        tk.Button(inner, text="Add New Equipment", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.add_equipment).pack(side=tk.RIGHT, padx=2)
        tk.Button(inner, text="Edit Existing Equipment", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.edit_equipment).pack(side=tk.RIGHT, padx=2)
        tk.Button(inner, text="Delete Existing Equipment", width=40, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT,
                  command=self.delete_equipment).pack(side=tk.RIGHT, padx=2)

    def display(self, text):
        self.output.config(state='normal')
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state='disabled')

    def show_cardio(self):
        self.display(listEquipmentByType("Cardio", return_output=True))

    def show_strength(self):
        self.display(listEquipmentByType("Strength", return_output=True))

    def show_equipment(self):
        self.display(showEquipment(return_output=True))

    # ----------------------------------------------------------------------------------------------------------------------------
    def add_equipment(self):
        def submit():
            try:
                args = [entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get()]
                top.destroy()
                newEquipment(args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Eqipment Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter, respectively: Equipment Name, Equipment Type, Quantity of Equipment, The Gym's ID", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(4)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def edit_equipment(self):
        def submit():
            try:
                equipmentId = idEntry.get()
                args = [entries[0].get(), entries[1].get(), entries[2].get(), entries[3].get()]
                top.destroy()
                updateEquipment(equipmentId, args)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Equipment Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter the ID of the equipment to be updated.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        idEntry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        idEntry.pack(pady=5)

        tk.Label(top, text="Enter, respectively: Equipment Name, Equipment Type, Quantity of Equipment, The Gym's ID", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        tk.Label(top, text="Entries left empty will not update their respective attribute - they will stay the same.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

        entries = [tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR) for _ in range(4)]
        for entry in entries:
            entry.pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)

    def delete_equipment(self):
        def submit():
            try:
                equipmentId = idEntry.get()
                top.destroy()
                delEquipment(equipmentId)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid attributes.")

        top = tk.Toplevel(self, height=500, width=500)
        top.title("Equipment Table Editing")
        top.configure(bg=DARK_BG)

        tk.Label(top, text="Enter the ID of the equipment to be deleted.", 
                 bg=DARK_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
        idEntry = tk.Entry(top, bg=ENTRY_BG, fg=TEXT_COLOR, font=FONT, insertbackground=TEXT_COLOR)
        idEntry.pack(pady=5)

        tk.Button(top, text="Submit", command=submit, bg=BUTTON_BG, fg=TEXT_COLOR, font=FONT).pack(pady=5)
    # ----------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app = GymApp()
    app.mainloop()