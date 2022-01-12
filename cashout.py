from abc import ABCMeta
import tkinter as tk
from tkinter.constants import X
from tkinter.font import BOLD
from tkinter import StringVar, messagebox
import sqlite3
class cashout():

    username = ""
    
    def set_user(arg):
        global username 
        username = arg
    
    def __init__(self,root):
        self.root = root
        self.root.title("Cash Out - Munim Ji")
        self.root.geometry("270x335")
        self.root.resizable(False,False)
        self.root.iconbitmap("images/favicon.ico")
        self.root.focus_force()

        #variables
        self.title_var = StringVar()
        self.amount_var = StringVar()
        self.remark_var = StringVar()
        self.type_var = "Cash-Out"
        self.user_var = username
        self.curr_bal = StringVar()

        tk.Label(self.root,bg="#2C394B").place(x=0,y=0,height=335,width=270)

        tk.Label(self.root,text="Enter your expenses here...",font=("Helvetica",12,BOLD),fg="white",bg="#FF4C29",height=2).pack(fill=X)

        title = tk.Label(self.root,text="Title*",font=("Helvetica",10,BOLD),bg="#2C394B",fg="white").place(x=10,y=50)
        self.title_txt = tk.Entry(self.root,font=("Helvetica",10),bg="#334756",fg="white",insertbackground='white',textvariable=self.title_var)
        self.title_txt.place(x=10,y=80,width=250,height=30)
        self.title_txt.focus()

        amount = tk.Label(self.root,text="Amount (INR)*",font=("Helvetica",10,BOLD),bg="#2C394B",fg="white").place(x=10,y=120)
        self.amount_txt = tk.Entry(self.root,font=("Helvetica",10),bg="#334756",fg="white",insertbackground='white',textvariable=self.amount_var)
        self.amount_txt.place(x=10,y=150,width=250,height=30)

        remarks = tk.Label(self.root,text="Remarks (If any)",font=("Helvetica",10,BOLD),bg="#2C394B",fg="white").place(x=10,y=190)
        self.remarks_txt = tk.Entry(self.root,font=("Helvetica",10),bg="#334756",fg="white",insertbackground='white',textvariable=self.remark_var)
        self.remarks_txt.place(x=10,y=220,width=250,height=50)

        add_btn = tk.Button(self.root,command=self.add_cashout,text="Add",font=("Helvetica",10,BOLD),bg="lime green",fg="white",cursor="hand2").place(x=10,y=290,width=120,height=30)
        cancel_btn = tk.Button(self.root,command=self.cancel_cashout,text="Cancel",font=("Helvetica",10,BOLD),bg="tomato",fg="white",cursor="hand2").place(x=140,y=290,width=120,height=30)

    def add_cashout(self):
        con = sqlite3.connect(database="munimji.db")
        cur = con.cursor()
        if(self.title_txt.get()=="" or self.amount_txt.get()==""):
            messagebox.showerror("Cash Out - Munim Ji","Title and Amount are mandatory fields, cannot be left empty.",parent=self.root)
            self.root.focus_force()
        elif(self.amount_txt.get().isnumeric()==False):
            messagebox.showerror("Cash Out - Munim Ji","Amount says - Invalid Input.",parent=self.root)
            self.root.focus_force()
        else:
            cur.execute("INSERT INTO records(title,amount,remark,type,username) VALUES(?,?,?,?,?)",(self.title_var.get(),self.amount_var.get(),self.remark_var.get(),self.type_var,self.user_var))
            con.commit()
            cur.execute("select bal from users where username=?",(self.user_var,))
            row = cur.fetchone()
            self.curr_bal.set(row[0])
            cur.execute("update users set bal=? where username=?",(str(int(self.curr_bal.get())-int(self.amount_var.get())),self.user_var))
            con.commit()
            con.close()
            messagebox.showinfo("Cash Out Successful - Munim Ji","The record has been added sucessfully.",parent=self.root)
            self.root.destroy()

    def cancel_cashout(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    obj = cashout(root)
    root.mainloop()