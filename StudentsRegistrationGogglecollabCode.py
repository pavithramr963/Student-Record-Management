import sqlite3
import ipywidgets as widgets
from IPython.display import display, clear_output

# 1. Create database
con = sqlite3.connect("student.db")
cur = con.cursor()

# 2. Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    age INTEGER,
    course TEXT
)
""")

con.commit()

# 3. Create input fields
name = widgets.Text(description="Name:")
age = widgets.IntText(description="Age:")
course = widgets.Text(description="Course:")

# 4. Create buttons
save_button = widgets.Button(
    description="Save Student",
    button_style="success"
)

display_button = widgets.Button(
    description="Display Records",
    button_style="info"
)

# Output area
output = widgets.Output()

# 5. Save student details
def save_data(b):

    with output:
        clear_output()

        if name.value == "" or course.value == "" or age.value <= 0:
            print("Please enter valid student details!")

        else:
            cur.execute(
                "INSERT INTO students VALUES (?, ?, ?)",
                (name.value, age.value, course.value)
            )

            con.commit()

            print("Student Registered Successfully!")

            name.value = ""
            age.value = 0
            course.value = ""

# 6. Display student records
def display_data(b):

    with output:
        clear_output()

        cur.execute("SELECT * FROM students")
        records = cur.fetchall()

        if records:
            print("STUDENT RECORDS")
            print("-------------------------")

            for row in records:
                print("Name:", row[0])
                print("Age:", row[1])
                print("Course:", row[2])
                print("-------------------------")

        else:
            print("No student records found!")

# 7. Connect buttons to functions
save_button.on_click(save_data)
display_button.on_click(display_data)

# 8. Display application
print("STUDENT REGISTRATION SYSTEM")
display(name, age, course)
display(save_button, display_button)
display(output)
