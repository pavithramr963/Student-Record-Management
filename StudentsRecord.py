
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# DATABASE CONNECTION
con = sqlite3.connect("student.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    mark INTEGER NOT NULL
)
""")
con.commit()


# FUNCTIONS

def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    mark_entry.delete(0, tk.END)


def display_students(records=None):
    for item in table.get_children():
        table.delete(item)

    if records is None:
        cur.execute("SELECT * FROM students")
        records = cur.fetchall()

    for row in records:
        table.insert("", tk.END, values=row)


def add_student():
    try:
        sid = int(id_entry.get())
        name = name_entry.get().strip()
        mark = int(mark_entry.get())

        if not name:
            messagebox.showerror("Error", "Enter student name")
            return

        if mark < 0 or mark > 100:
            messagebox.showerror("Error", "Mark must be 0 to 100")
            return

        cur.execute(
            "INSERT INTO students VALUES (?, ?, ?)",
            (sid, name, mark)
        )
        con.commit()

        messagebox.showinfo("Success", "Student added successfully!")
        display_students()
        clear_fields()

    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers for ID and Mark")

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists!")


def search_student():
    try:
        sid = int(id_entry.get())

        cur.execute(
            "SELECT * FROM students WHERE id = ?", (sid,)
        )
        record = cur.fetchone()

        if record:
            display_students([record])

            clear_fields()
            id_entry.insert(0, record[0])
            name_entry.insert(0, record[1])
            mark_entry.insert(0, record[2])

        else:
            messagebox.showinfo("Result", "Student not found!")

    except ValueError:
        messagebox.showerror("Error", "Enter a valid Student ID")


def update_student():
    try:
        sid = int(id_entry.get())
        mark = int(mark_entry.get())

        if mark < 0 or mark > 100:
            messagebox.showerror("Error", "Mark must be 0 to 100")
            return

        cur.execute(
            "UPDATE students SET mark = ? WHERE id = ?",
            (mark, sid)
        )
        con.commit()

        if cur.rowcount > 0:
            messagebox.showinfo("Success", "Mark updated!")
            display_students()
            clear_fields()
        else:
            messagebox.showinfo("Result", "Student not found!")

    except ValueError:
        messagebox.showerror("Error", "Enter valid ID and Mark")


def delete_student():
    try:
        sid = int(id_entry.get())

        answer = messagebox.askyesno(
            "Confirm", "Do you want to delete this student?"
        )

        if answer:
            cur.execute(
                "DELETE FROM students WHERE id = ?", (sid,)
            )
            con.commit()

            if cur.rowcount > 0:
                messagebox.showinfo("Success", "Student deleted!")
                display_students()
                clear_fields()
            else:
                messagebox.showinfo("Result", "Student not found!")

    except ValueError:
        messagebox.showerror("Error", "Enter a valid Student ID")


def select_student(event):
    selected = table.selection()

    if selected:
        values = table.item(selected[0], "values")

        clear_fields()
        id_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        mark_entry.insert(0, values[2])


# MAIN WINDOW

root = tk.Tk()
root.title("Student Record Management System")
root.geometry("700x550")
root.configure(bg="#EAF2F8")

title = tk.Label(
    root,
    text="STUDENT RECORD MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#1F4E79",
    fg="white",
    pady=15
)
title.pack(fill="x")


# INPUT FORM

form = tk.Frame(root, bg="#EAF2F8", pady=15)
form.pack()

tk.Label(form, text="Student ID:", bg="#EAF2F8",
         font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=8)

id_entry = tk.Entry(form, font=("Arial", 12))
id_entry.grid(row=0, column=1, padx=10, pady=8)

tk.Label(form, text="Student Name:", bg="#EAF2F8",
         font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=8)

name_entry = tk.Entry(form, font=("Arial", 12))
name_entry.grid(row=1, column=1, padx=10, pady=8)

tk.Label(form, text="Mark:", bg="#EAF2F8",
         font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=8)

mark_entry = tk.Entry(form, font=("Arial", 12))
mark_entry.grid(row=2, column=1, padx=10, pady=8)


# BUTTONS

buttons = tk.Frame(root, bg="#EAF2F8", pady=10)
buttons.pack()

tk.Button(buttons, text="Add Student", width=15,
          bg="#27864A", fg="white",
          command=add_student).grid(row=0, column=0, padx=5, pady=5)

tk.Button(buttons, text="View Students", width=15,
          bg="#2463A5", fg="white",
          command=display_students).grid(row=0, column=1, padx=5, pady=5)

tk.Button(buttons, text="Search Student", width=15,
          bg="#7952A0", fg="white",
          command=search_student).grid(row=0, column=2, padx=5, pady=5)

tk.Button(buttons, text="Update Mark", width=15,
          bg="#C17B20", fg="white",
          command=update_student).grid(row=1, column=0, padx=5, pady=5)

tk.Button(buttons, text="Delete Student", width=15,
          bg="#B33B3B", fg="white",
          command=delete_student).grid(row=1, column=1, padx=5, pady=5)

tk.Button(buttons, text="Clear", width=15,
          command=clear_fields).grid(row=1, column=2, padx=5, pady=5)


# STUDENT TABLE

table_frame = tk.Frame(root)
table_frame.pack(padx=15, pady=15, fill="both", expand=True)

columns = ("ID", "Name", "Mark")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

table.heading("ID", text="Student ID")
table.heading("Name", text="Student Name")
table.heading("Mark", text="Mark")

table.column("ID", width=100, anchor="center")
table.column("Name", width=250, anchor="center")
table.column("Mark", width=100, anchor="center")

table.pack(fill="both", expand=True)

table.bind("<<TreeviewSelect>>", select_student)

# RUN APPLICATION

display_students()
root.mainloop()

con.close()
