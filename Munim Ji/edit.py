import sqlite3
import tkinter as tk
from tkinter.constants import X
from tkinter.font import BOLD
from tkinter.messagebox import askyesno, askquestion
from tkinter import StringVar, messagebox
class edit():

    title_var = ""
    amount_var = ""
    remark_var = ""
    type_var = ""
    username = ""

    def get_data(title,amount,remark,type,user):
        global title_var,amount_var,remark_var,type_var,username
        title_var = title
        amount_var = amount
        remark_var = remark
        type_var = type
        username = user

    def __init__(self,root):
        self.root = root
        self.root.title("Edit Record - Munim Ji")
        self.root.geometry("270x335")
        self.root.resizable(False,False)
        self.root.iconbitmap("images/favicon.ico")
        self.root.focus_force()

        #variables
        self.title_val = StringVar()
        self.amount_val = StringVar()
        self.remark_val = StringVar()

        #Edit frame
        Frame_edit = tk.Frame(self.root,bg="#2C394B")
        Frame_edit.place(x=0,y=0,height=335,width=270)

        tk.Label(Frame_edit,text="Update the record here...",font=("Helvetica",12,BOLD),fg="white",bg="#FF4C29",height=2).pack(fill=X)

        title = tk.Label(Frame_edit,text="Title*",font=("Helvetica",10,BOLD),bg="#2C394B",fg="white").place(x=10,y=50)
        self.title_txt = tk.Entry(Frame_edit,font=("Helvetica",10),bg="#334756",fg="white",insertbackground='white',textvariable=self.title_val)
        self.title_txt.place(x=10,y=80,width=250,height=30)
        self.title_txt.focus()

        amount = tk.Label(Frame_edit,text="Amount (INR)*",font=("Helvetica",10,BOLD),bg="#2C394B",fg="white").place(x=10,y=120)
        self.amount_txt = tk.Entry(Frame_edit,font=("Helvetica",10),bg="#334756",fg="white",insertbackground='white',textvariable=self.amount_val)
        self.amount_txt.place(x=10,y=150,width=250,height=30)

        remarks = tk.Label(Frame_edit,text="Remarks (If any)",font=("Helvetica",10,BOLD),bg="#2C394B",fg="white").place(x=10,y=190)
        self.remarks_txt = tk.Entry(Frame_edit,font=("Helvetica",10),bg="#334756",fg="white",insertbackground='white',textvariable=self.remark_val)
        self.remarks_txt.place(x=10,y=220,width=250,height=50)

        update_btn = tk.Button(Frame_edit,command=self.update_edit,text="Update",font=("Helvetica",10,BOLD),bg="lime green",fg="white",cursor="hand2").place(x=10,y=290,width=120,height=30)
        cancel_btn = tk.Button(Frame_edit,command=self.cancel_edit,text="Cancel",font=("Helvetica",10,BOLD),bg="tomato",fg="white",cursor="hand2").place(x=140,y=290,width=120,height=30)

        self.set_data()

    def set_data(self):
        global title_var,amount_var,remark_var
        self.title_val.set(title_var)
        self.amount_val.set(amount_var)
        self.remark_val.set(remark_var)

    def update_edit(self):
        global title_var,amount_var,remark_var,type_var,username
        if(self.title_txt.get()=="" or self.amount_txt.get()==""):
            messagebox.showerror("Edit Entry - Munim Ji","Title and Amount are mandatory fields, cannot be left empty.",parent=self.root)
            self.root.focus_force()
        elif(self.amount_txt.get().isnumeric()==False):
            messagebox.showerror("Edit Entry - Munim Ji","Amount says - Invalid Input.",parent=self.root)
            self.root.focus_force()
        else:
            answer = askyesno(title="Edit Entry - Munim Ji",message="Are you sure you want to update the record?",parent=self.root)
            if(answer):
                con = sqlite3.connect("munimji.db")
                cur = con.cursor()
                cur.execute("update records set title=? , amount=? , remark=? where title=? and amount=? and remark=? and username=?",(self.title_val.get(),self.amount_val.get(),self.remark_val.get(),title_var,amount_var,remark_var,username))
                con.commit()
                con.close()
                if(type_var=="Cash-In"):
                    con = sqlite3.connect("munimji.db")
                    cur = con.cursor()
                    cur.execute("Select bal from users where username=?",(username,))
                    row = cur.fetchone()
                    cur.execute("update users set bal=? where username=?",(str(int(row[0])-int(amount_var)),username))
                    con.commit()
                    cur.execute("Select bal from users where username=?",(username,))
                    row = cur.fetchone()
                    cur.execute("update users set bal=? where username=?",(str(int(row[0])+int(self.amount_val.get())),username))
                    con.commit()
                    con.close()
                elif(type_var=="Cash-Out"):
                    con = sqlite3.connect("munimji.db")
                    cur = con.cursor()
                    cur.execute("Select bal from users where username=?",(username,))
                    row = cur.fetchone()
                    cur.execute("update users set bal=? where username=?",(str(int(row[0])+int(amount_var)),username))
                    con.commit()
                    cur.execute("Select bal from users where username=?",(username,))
                    row = cur.fetchone()
                    cur.execute("update users set bal=? where username=?",(str(int(row[0])-int(self.amount_val.get())),username))
                    con.commit()
                    con.close()
                messagebox.showinfo("Edit Entry - Munim Ji","The record has been updated sucessfully.",parent=self.root)
                self.root.destroy()

    def cancel_edit(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    obj = edit(root)
    root.mainloop()
