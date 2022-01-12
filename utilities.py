import random
import sqlite3
from tkinter import messagebox
import tkinter as tk
from tkinter import StringVar

class util():

    def create_connection(db):
        con = sqlite3.connect(db)
        cur = con.cursor()
        return cur

    def set_value(val,val2):
        val.set(val2)

    def get_value(val):
        return val.get()

    def display_errorbox(title,message,root):
        messagebox.showerror(title,message,parent=root)

    def display_infobox(title,message,root):
        messagebox.showinfo(title,message,parent=root)

    def display_warningbox(title,message,root):
        messagebox.showwarning(title,message,parent=root)

    def display_askbox(title,message,root):
        answer = messagebox.askyesno(title,message,parent=root)
        return answer

    def open_toplevel(parent,child):
        new_win = tk.Toplevel(child)
        parent_obj = parent(new_win)

    def get_otp():
        return random.randrange(100000,999999)

    def close_win(root):
        root.destroy()

    def clear_table(table):
        table.delete(*table.get_children())

    def is_phone_number(val):
        if len(val)<10 and val.isnumeric():
            return True
        else:
            return False

    def is_number(val):
        return val.isnumeric()

    def is_empty(entry):
        return entry.get()==""

    def to_integer(val):
        return int(val)
    
    def to_string(val):
        return str(val)

    def clear_entry_box(entry):
        entry.delete(0,'end')



    