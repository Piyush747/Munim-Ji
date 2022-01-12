import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import BOTH, RIGHT, VERTICAL, X, Y
from tkinter.font import BOLD
from PIL import ImageTk
from tkinter import StringVar, ttk

class search():

    username = ""
    
    def set_user(arg):
        global username 
        username = arg

    def __init__(self,root):
        self.root = root
        root.title("Search Record - Munim Ji")
        self.root.geometry("600x540")
        self.root.resizable(False,False)
        self.root.iconbitmap("images/favicon.ico")
        self.root.focus_force()

        self.title_var = StringVar()
        self.user_var = username

        #control frame
        tk.Label(root,bg="#2C394B").place(x=0,y=0,width=600,height=80)

        tk.Label(self.root,text="Search by Title: ",font=("Helvetica",12,BOLD),bg="#2C394B",fg="white").place(x=10,y=10)
        self.search_txt = tk.Entry(self.root,bg="#334756",fg="white",insertbackground='white',textvariable=self.title_var)
        self.search_txt.place(x=10,y=40,width=250,height=30)
        self.search_txt.focus()

        tk.Button(self.root,text="Search",background="deep sky blue",fg="white",font=("Helvetica",12,BOLD),cursor="hand2",command=self.show_searched).place(x=270,y=40,width=100,height=30)
        tk.Button(self.root,text="Clear",background="coral1",fg="white",font=("Helvetica",12,BOLD),cursor="hand2",command=self.clear).place(x=380,y=40,width=100,height=30)
        tk.Button(self.root,text="Show All",background="yellow green",fg="white",font=("Helvetica",12,BOLD),cursor="hand2",command=self.show_all_data).place(x=490,y=40,width=100,height=30)
        
        scroll_y = tk.Scrollbar(self.root,orient=VERTICAL)

        self.table = ttk.Treeview(self.root,column=("Title","Description","Type","Amount"),yscrollcommand=scroll_y.set)
        scroll_y.place(x=580,y=80,width=20,height=460)

        scroll_y.config(command=self.table.yview)

        self.table.heading("Title",text="Title")
        self.table.heading("Description",text="Description")
        self.table.heading("Type",text="Type")
        self.table.heading("Amount",text="Amount")

        self.table['show']='headings'
        self.table.column("Title",width=60)
        self.table.column("Description",width=200)
        self.table.column("Type",width=40)
        self.table.column("Amount",width=40)

        self.table.place(x=0,y=80,width=580,height=460)

        self.show_all_data()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="lemon chiffon",foreground="tomato",rowheight=50,fieldbackground="ghost white")
        style.map('Treeview',background=[('selected','seagreen')])

    def clear(self):
        self.search_txt.delete(0, 'end')

    def show_all_data(self):
        try:
            con = sqlite3.connect(database="munimji.db")
            cur = con.cursor()
            cur.execute("select title, remark, type, amount from records where username = ?",(self.user_var,))
            rows = cur.fetchall()
            self.table.delete(*self.table.get_children())
            for row in rows:
                self.table.insert('','end',values=row)
        except Exception as e:
            messagebox.showerror("Error","Oops some error occured. Please try again.",parent=self.root)

    def show_searched(self):
        try:
            if self.title_var.get()=="":
                messagebox.showerror("Error","Please enter the title to search.",parent=self.root)
                self.root.focus_force()
            else:
                con = sqlite3.connect(database="munimji.db")
                cur = con.cursor()
                cur.execute("select title, remark, type, amount from records where title = ? and username= ?",(self.title_var.get(),self.user_var))
                rows = cur.fetchall()
                self.table.delete(*self.table.get_children())
                for row in rows:
                    self.table.insert('','end',values=row)
        except Exception as e:
            messagebox.showerror("Error","Oops some error occured. Please try again.",parent=self.root)


if __name__ == '__main__':
    root = tk.Tk()
    obj = search(root)
    root.mainloop()