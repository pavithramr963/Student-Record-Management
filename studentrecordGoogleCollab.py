

# STUDENT RECORD MANAGEMENT SYSTEM
# GOOGLE COLAB VERSION
# Using ipywidgets + SQLite


import sqlite3
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from html import escape


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


# INPUT FIELDS


id_entry = widgets.Text(
    description="Student ID:",
    placeholder="Enter student ID",
    layout=widgets.Layout(width="350px")
)

name_entry = widgets.Text(
    description="Name:",
    placeholder="Enter student name",
    layout=widgets.Layout(width="350px")
)

mark_entry = widgets.Text(
    description="Mark:",
    placeholder="Enter mark (0-100)",
    layout=widgets.Layout(width="350px")
)

confirm_delete = widgets.Checkbox(
    value=False,
    description="I confirm that I want to delete this student"
)

# Output areas
status_output = widgets.Output()
table_output = widgets.Output()


# MESSAGE FUNCTION


def show_message(message, color="#2463A5"):
    with status_output:
        clear_output(wait=True)
        display(HTML(
            f'<div style="padding:10px; color:white; '
            f'background:{color}; border-radius:5px;">'
            f'{escape(message)}</div>'
        ))


# CLEAR FIELDS


def clear_fields():
    id_entry.value = ""
    name_entry.value = ""
    mark_entry.value = ""
    confirm_delete.value = False
    show_message("Fields cleared successfully!", "#2463A5")


# DISPLAY STUDENTS


def display_students(records=None):

    if records is None:
        cur.execute("SELECT * FROM students ORDER BY id")
        records = cur.fetchall()

    with table_output:
        clear_output(wait=True)

        if not records:
            display(HTML("<h4>No student records found.</h4>"))
            return

        html = """
        <table style="width:100%; border-collapse:collapse;
                      text-align:center;">
        <tr style="background:#1F4E79; color:white;">
            <th style="padding:12px;">Student ID</th>
            <th style="padding:12px;">Student Name</th>
            <th style="padding:12px;">Mark</th>
        </tr>
        """

        for row in records:
            html += f"""
            <tr style="background:#EAF2F8;">
                <td style="padding:10px; border:1px solid #ccc;">
                    {row[0]}
                </td>
                <td style="padding:10px; border:1px solid #ccc;">
                    {escape(str(row[1]))}
                </td>
                <td style="padding:10px; border:1px solid #ccc;">
                    {row[2]}
                </td>
            </tr>
            """

        html += "</table>"

        display(HTML(html))


# ADD STUDENT


def add_student(button):

    try:
        sid = int(id_entry.value)
        name = name_entry.value.strip()
        mark = int(mark_entry.value)

        if not name:
            show_message("Enter student name!", "#B33B3B")
            return

        if mark < 0 or mark > 100:
            show_message("Mark must be between 0 and 100!", "#B33B3B")
            return

        cur.execute(
            "INSERT INTO students VALUES (?, ?, ?)",
            (sid, name, mark)
        )
        con.commit()

        show_message("Student added successfully!", "#27864A")
        display_students()
        clear_input_values()

    except ValueError:
        show_message("Enter valid numbers for ID and Mark!", "#B33B3B")

    except sqlite3.IntegrityError:
        show_message("Student ID already exists!", "#B33B3B")


# SEARCH STUDENT


def search_student(button):

    try:
        sid = int(id_entry.value)

        cur.execute(
            "SELECT * FROM students WHERE id = ?",
            (sid,)
        )

        record = cur.fetchone()

        if record:
            name_entry.value = record[1]
            mark_entry.value = str(record[2])

            display_students([record])
            show_message("Student found successfully!", "#27864A")

        else:
            show_message("Student not found!", "#B33B3B")

    except ValueError:
        show_message("Enter a valid Student ID!", "#B33B3B")


# UPDATE STUDENT MARK

def update_student(button):

    try:
        sid = int(id_entry.value)
        mark = int(mark_entry.value)

        if mark < 0 or mark > 100:
            show_message("Mark must be between 0 and 100!", "#B33B3B")
            return

        cur.execute(
            "UPDATE students SET mark = ? WHERE id = ?",
            (mark, sid)
        )

        if cur.rowcount > 0:
            con.commit()
            show_message("Student mark updated successfully!", "#27864A")
            display_students()
            clear_input_values()

        else:
            show_message("Student not found!", "#B33B3B")

    except ValueError:
        show_message("Enter valid Student ID and Mark!", "#B33B3B")


# DELETE STUDENT


def delete_student(button):

    try:
        sid = int(id_entry.value)

        if not confirm_delete.value:
            show_message(
                "Please tick the confirmation checkbox before deleting!",
                "#B33B3B"
            )
            return

        cur.execute(
            "DELETE FROM students WHERE id = ?",
            (sid,)
        )

        if cur.rowcount > 0:
            con.commit()
            show_message("Student deleted successfully!", "#27864A")
            display_students()
            clear_input_values()

        else:
            show_message("Student not found!", "#B33B3B")

    except ValueError:
        show_message("Enter a valid Student ID!", "#B33B3B")

# CLEAR INPUT VALUES (INTERNAL)


def clear_input_values():
    id_entry.value = ""
    name_entry.value = ""
    mark_entry.value = ""
    confirm_delete.value = False


# BUTTONS


add_btn = widgets.Button(
    description="Add Student",
    button_style="success",
    icon="plus",
    layout=widgets.Layout(width="150px")
)

view_btn = widgets.Button(
    description="View Students",
    button_style="primary",
    icon="list",
    layout=widgets.Layout(width="150px")
)

search_btn = widgets.Button(
    description="Search Student",
    button_style="info",
    icon="search",
    layout=widgets.Layout(width="150px")
)

update_btn = widgets.Button(
    description="Update Mark",
    button_style="warning",
    icon="edit",
    layout=widgets.Layout(width="150px")
)

delete_btn = widgets.Button(
    description="Delete Student",
    button_style="danger",
    icon="trash",
    layout=widgets.Layout(width="150px")
)

clear_btn = widgets.Button(
    description="Clear",
    button_style="",
    icon="refresh",
    layout=widgets.Layout(width="150px")
)

# Connect buttons to functions

add_btn.on_click(add_student)
view_btn.on_click(lambda b: (
    display_students(),
    show_message("Student records displayed!", "#2463A5")
))
search_btn.on_click(search_student)
update_btn.on_click(update_student)
delete_btn.on_click(delete_student)
clear_btn.on_click(lambda b: clear_fields())


# MAIN INTERFACE


title = widgets.HTML("""
<div style="
    background:#1F4E79;
    color:white;
    text-align:center;
    padding:20px;
    border-radius:8px;
    font-size:23px;
    font-weight:bold;">
    STUDENT RECORD MANAGEMENT SYSTEM
</div>
""")

form = widgets.VBox([
    id_entry,
    name_entry,
    mark_entry,
    confirm_delete
], layout=widgets.Layout(
    align_items="center",
    padding="15px"
))

button_row1 = widgets.HBox(
    [add_btn, view_btn, search_btn],
    layout=widgets.Layout(
        justify_content="center",
        flex_flow="row wrap"
    )
)

button_row2 = widgets.HBox(
    [update_btn, delete_btn, clear_btn],
    layout=widgets.Layout(
        justify_content="center",
        flex_flow="row wrap"
    )
)

interface = widgets.VBox([
    title,
    form,
    button_row1,
    button_row2,
    status_output,
    widgets.HTML("<h3>STUDENT RECORDS</h3>"),
    table_output
], layout=widgets.Layout(
    width="100%",
    padding="15px"
))

display(interface)

# Display existing records
display_students()

show_message("Student Management System is ready!", "#27864A")


