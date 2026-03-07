# 5a. Connecting Tkinter with SQL code for writing data into tables and reading contents of tables.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# database connection

db_file = "example_ship.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

table_name = "passengers"
create_table_sql = """
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        nationality TEXT
    );"""

#helper functions

def connect_to_database(db_file):
    con = sqlite3.connect(db_file)
    print (con)
    return con
    
db_base = connect_to_database(db_file)
cursor = db_base.cursor()
cursor.execute(create_table_sql)
conn.commit()

# function to read data and display in treeview

def read_data_from_database_to_form(cursor, table_name):
    """
    Executes a SELECT query on the specified table
    and displays the results in the Tkinter Treeview.
    """
    try:
        cursor.execute(f"SELECT * FROM  {table_name}")   
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        for item in tree.get_children():
            tree.delete(item)
        tree["columns"] = columns
        tree["show"] = "headings"
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
            
        for row in rows:
            tree.insert("", tk.END, values=row)
    except Exception as e:
        print("Error:", e)

# function to insert data

def insert_data():
    try:
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        age = entry_age.get()
        nationality = entry_nationality.get()

        if not first_name or not last_name:
            messagebox.showerror("Error", "First and Last name are required.")
            return
        if not(age.isdigit()):
            messagebox.showerror("Error", "Age must be an integer value")
            return
            
        cursor.execute("""
            INSERT INTO passengers 
            (first_name, last_name, age, nationality)
            VALUES (?, ?, ?, ?)
        """, (first_name, last_name, age, nationality))

        conn.commit()

        read_data_from_database_to_form(cursor, table_name)

        entry_first_name.delete(0, tk.END) # clear fields
        entry_last_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_nationality.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# making a custom class for rounded box corners

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, border_radius=30, padding=20, bg_color="white", **kwargs):
        super().__init__(parent, highlightthickness=0, bg=parent["bg"], **kwargs)
        self.border_radius = border_radius
        self.padding = padding
        self.bg_color = bg_color
        
        self.container = tk.Frame(self, bg=bg_color)
        self.container_window = self.create_window(0, 0, window=self.container, anchor="nw")
        
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.delete("round_bg")
        w, h = event.width, event.height
        r = self.border_radius
        
        points = [r, 0, w-r, 0, w, 0, w, r, w, h-r, w, h, w-r, h, r, h, 0, h, 0, h-r, 0, r, 0, 0]
        self.create_polygon(points, fill=self.bg_color, smooth=True, tags="round_bg")
        
        self.itemconfig(self.container_window, width=w-(self.padding*2), height=h-(self.padding*2))
        self.coords(self.container_window, self.padding, self.padding)

# GUI setup

root = tk.Tk()
root.title("Passenger Entry Form")
root.geometry("1100x650") 

navy_blue = "#001f3f"
root.configure(bg=navy_blue)

courier = ("Courier", 11, "bold")

root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

form_frame = RoundedFrame(root, border_radius=40, padding=35, width=380)
form_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
form_area = form_frame.container

tk.Label(form_area, text="> FIRST NAME", bg='white', fg='black', font=courier).pack(anchor="w")
entry_first_name = tk.Entry(form_area, bg="white", fg="black", font=courier, insertbackground="black")
entry_first_name.pack(pady=(0,20), fill='x', ipady=8)

tk.Label(form_area, text="> LAST NAME", bg='white', fg='black', font=courier).pack(anchor="w")
entry_last_name = tk.Entry(form_area, bg="white", fg="black", font=courier, insertbackground="black")
entry_last_name.pack(pady=(0,20), fill='x', ipady=8)

tk.Label(form_area, text="> AGE", bg='white', fg='black', font=courier).pack(anchor="w")
entry_age = tk.Entry(form_area, bg="white", fg="black", font=courier, insertbackground="black")
entry_age.pack(pady=(0,20), fill='x', ipady=8)

tk.Label(form_area, text="> NATIONALITY", bg='white', fg='black', font=courier).pack(anchor="w")
entry_nationality = tk.Entry(form_area, bg="white", fg="black", font=courier, insertbackground="black")
entry_nationality.pack(pady=(0,20), fill='x', ipady=8)

btn_submit = tk.Button(form_area, text="EXECUTE INSERT", font=courier, bg='white', fg='black', command=insert_data)
btn_submit.pack(pady=(0,20), fill='x', ipady=8)

db_frame = RoundedFrame(root, border_radius=40, padding=25)
db_frame.grid(row=0, column=1, padx=(0, 30), pady=30, sticky="nsew")
table_area = db_frame.container

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", fieldbackground="white", foreground="black", font=courier)
style.configure("Treeview.Heading", font=courier)

scroll_y = ttk.Scrollbar(table_area, orient="vertical")
tree = ttk.Treeview(table_area, yscrollcommand=scroll_y.set)
scroll_y.config(command=tree.yview)
scroll_y.pack(side="right", fill="y")
tree.pack(fill="both", expand=True)

read_data_from_database_to_form(cursor, table_name)

root.mainloop()
conn.close()
