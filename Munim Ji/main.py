from edit import edit
from search import search
import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, RIGHT, TOP, VERTICAL, W, Y
from tkinter.font import BOLD
from PIL import ImageTk
from tkinter import StringVar, messagebox
from tkinter import ttk
from tkinter.messagebox import askyesno
from signup import signup
from forgetpass import forgetpass
from cashin import cashin
from cashout import cashout
import sqlite3
import random

class Login():

    def __init__(self,root):
        self.root = root
        self.root.title("Munim Ji")
        self.root.geometry("800x600+100+50")
        self.root.resizable(False,False)
        self.root.iconbitmap("images/favicon.ico")

        #All variables
        self.name_var = ""
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.selected_or_not = False
        self.selected_title = StringVar()
        self.selected_remark = StringVar()
        self.selected_amount = StringVar()
        self.bal = StringVar()
        
        #Background
        self.bg = ImageTk.PhotoImage(file="images/bg.jpg")
        self.bg_image = tk.Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        #Login frame
        Frame_login = tk.Frame(self.root,bg="white")
        Frame_login.place(x=200,y=140,height=360,width=400)

        self.munim_ji = ImageTk.PhotoImage(file="images/man.png")
        self.munim_ji_label = tk.Label(Frame_login,image=self.munim_ji,bg="white").place(x=40,y=5)

        name = tk.Label(Frame_login,text="Munim Ji",font="Impact 35",fg="springgreen4",bg="white").place(x=110)
        moto = tk.Label(Frame_login,text="Your Expense Tracker...",font=("Helvetica",10),fg="seagreen",bg="white").place(x=190,y=55)
        desc = tk.Label(Frame_login,text="Please enter your username and password to login.",font=("Helvetica",10,BOLD),fg="seagreen",bg="white").place(x=35,y=90)

        username = tk.Label(Frame_login,text="Username:",font=("Helvetica",10),bg="white").place(x=35,y=120)
        self.username_txt = tk.Entry(Frame_login,font=("Helvetica",10),bg="light gray",textvariable=self.username_var)
        self.username_txt.place(x=35,y=150,width=335,height=30)
        self.username_txt.focus()

        password = tk.Label(Frame_login,text="Password:",font=("Helvetica",10),bg="white").place(x=35,y=190)
        self.password_txt = tk.Entry(Frame_login,font=("Helvetica",10),bg="light gray",textvariable=self.password_var,show="*")
        self.password_txt.place(x=35,y=220,width=290,height=30)
        self.eye_img = ImageTk.PhotoImage(file="images/eye.png")
        self.eye_btn = tk.Button(Frame_login,image=self.eye_img,background="white",bd=0,command=self.show_pass,cursor="hand2",activebackground="white")
        self.eye_btn.place(x=335,y=220)

        forget_btn = tk.Button(Frame_login,command=self.forget_passowrd,text="Forget Password?",cursor="hand2",font=("Helvetica",10),bg="white",fg="steel blue",bd=0).place(x=30,y=260)
        login_btn = tk.Button(Frame_login,command=self.login_function,cursor="hand2",text="Login",font=("Helvetica",16,BOLD),bg="tomato",fg="white").place(x=35,y=295,width=330,height=40)

        signup_btn = tk.Button(root,command=self.sign_up,cursor="hand2",text="New User? Register Here",font=("Helvetica",12,BOLD),bg="seagreen",fg="white").place(x=200,y=520,width=400,height=40)

    def show_pass(self):
        self.password_txt.config(show="")

    def main(self,root):
        self.root.title(self.name_var+" - Munim Ji")

        #Background
        self.bg2 = ImageTk.PhotoImage(file="images/bg2.jpg")
        self.bg2_image = tk.Label(self.root,image=self.bg2).place(x=0,y=0,relwidth=1,relheight=1)

        #header frame
        Frame_header = self.Frame_main = tk.Frame(self.root,bg="salmon")
        self.Frame_main.place(x=50,y=50,height=70,width=700) 

        self.munim_ji = ImageTk.PhotoImage(file="images/man.png")
        munim_ji_label = tk.Label(Frame_header,image=self.munim_ji,bg="salmon").place(x=10,y=5)
        text = tk.Label(Frame_header,text="Your Income/Expenses",font="Impact 28",fg="white",bg="salmon").place(x=80,y=10)

        self.reset_img = ImageTk.PhotoImage(file="images/reset.png")
        self.reset_btn = tk.Button(Frame_header,command=self.reset_function,cursor="hand2",image=self.reset_img,bg="salmon",bd=0,activebackground="salmon")
        self.reset_btn.place(x=630,y=2)
        self.reset_btn.bind("<Enter>",self.entry_reset)
        self.reset_btn.bind("<Leave>",self.leave_btn)

        self.search_img = ImageTk.PhotoImage(file="images/search.png")
        self.search_btn = tk.Button(Frame_header,cursor="hand2",image=self.search_img,command=self.search_function,bg="salmon",bd=0,activebackground="salmon")
        self.search_btn.place(x=559,y=2)
        self.search_btn.bind("<Enter>",self.entry_search)
        self.search_btn.bind("<Leave>",self.leave_btn)
        
        #main frame
        self.Frame_main = tk.Frame(self.root,bg="white")
        self.Frame_main.place(x=50,y=120,height=350,width=700)

        self.scroll_y = tk.Scrollbar(self.Frame_main,orient=VERTICAL)

        self.table = ttk.Treeview(self.Frame_main,column=("Title","Description","Type","Amount"),yscrollcommand=self.scroll_y.set)
        self.scroll_y.pack(side=RIGHT,fill=Y)

        self.scroll_y.config(command=self.table.yview)

        self.table.heading("Title",text="Title")
        self.table.heading("Description",text="Description")
        self.table.heading("Type",text="Type")
        self.table.heading("Amount",text="Amount")

        self.table["show"]='headings'
        self.table.column("Title",width=60)
        self.table.column("Description",width=200)
        self.table.column("Type",width=40)
        self.table.column("Amount",width=40)
        self.table.pack(fill=BOTH,expand=1)
        self.table.bind("<ButtonRelease-1>",self.selected)
        self.show_data(self.table)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",background="lemon chiffon",fg="tomato",rowheight=50,fieldbackground="ghost white",font=("Helvetica",12))
        style.map('Treeview',background=[('selected','seagreen')])

        #buttons frame
        self.Frame_Buttons = tk.Frame(self.root,bg="white")
        self.Frame_Buttons.place(x=50,y=470,height=80,width=700)

        bal_label = tk.Label(self.Frame_Buttons,text="Net Balance: ",fg="seagreen",bg="white",font="Helvetica 12").place(x=5,y=5)

        self.get_bal()

        self.balance = tk.Label(self.Frame_Buttons,text="Rs. {}/-".format(self.bal.get()),fg="indian red1",bg="white",font=("Impact",24, BOLD))
        self.balance.place(x=5,y=30)

        self.add_img = ImageTk.PhotoImage(file="images/add.png")
        self.add_btn = tk.Button(self.Frame_Buttons,cursor="hand2",command=self.cashin_function,image=self.add_img,bg="white",bd=0,activebackground="white")
        self.add_btn.place(x=398,y=7)
        self.icon_label = tk.Label(self.root,text="()",bd=0,bg="slate gray",fg="white",font=("Helvetica",10))
        self.icon_label.place(x=740,y=580,width=60,height=20)
        self.add_btn.bind("<Enter>",self.entry_add)
        self.add_btn.bind("<Leave>",self.leave_btn)

        self.minus_img = ImageTk.PhotoImage(file="images/negative.png")
        self.minus_btn = tk.Button(self.Frame_Buttons,cursor="hand2",image=self.minus_img,command=self.cashout_function,bg="white",bd=0,activebackground="white")
        self.minus_btn.place(x=474,y=7)
        self.minus_btn.bind("<Enter>",self.entry_minus)
        self.minus_btn.bind("<Leave>",self.leave_btn)

        self.edit_img = ImageTk.PhotoImage(file="images/edit.png")
        self.edit_btn = tk.Button(self.Frame_Buttons,image=self.edit_img,cursor="hand2",bg="white",bd=0,activebackground="white",command=self.edit_function)
        self.edit_btn.place(x=550,y=7)
        self.edit_btn.bind("<Enter>",self.entry_edit)
        self.edit_btn.bind("<Leave>",self.leave_btn)

        self.delete_img = ImageTk.PhotoImage(file="images/delete.png")
        self.delete_btn = tk.Button(self.Frame_Buttons,cursor="hand2",image=self.delete_img,bg="white",bd=0,activebackground="white",command=self.delete_function)
        self.delete_btn.place(x=626,y=7)
        self.delete_btn.bind("<Enter>",self.entry_delete)
        self.delete_btn.bind("<Leave>",self.leave_btn)

        logout_btn = tk.Button(root,text="Logout",command=self.logout_function,background="tomato",fg="white",font=("Helvetica",10,BOLD),cursor="hand2",bd=0,activebackground="white",activeforeground="tomato").place(x=740,y=10)

    def selected(self,ev):
        r = self.table.focus()
        content = self.table.item(r)
        row = content["values"]
        self.selected_title.set(row[0])
        self.selected_amount.set(row[3])
        self.selected_remark.set(row[1])
        edit.get_data(row[0],row[3],row[1],row[2],self.username_var.get())
        self.selected_or_not= True

    def entry_add(self,e):
        self.icon_label.config(text="Cash-In")

    def entry_minus(self,e):
        self.icon_label.config(text="Cash-Out")

    def entry_edit(self,e):
        self.icon_label.config(text="Edit")

    def entry_delete(self,e):
        self.icon_label.config(text="Delete")

    def entry_search(self,e):
        self.icon_label.config(text="Search")

    def entry_reset(self,e):
        self.icon_label.config(text="Reset")

    def leave_btn(self,e):
        self.icon_label.config(text="()")

    def login_function(self):
        con = sqlite3.connect(database="munimji.db")
        cur = con.cursor()
        try:
            if self.username_txt.get()=="" or self.password_txt.get()=="":
                messagebox.showerror("Error","All fields are required.",parent=self.root)
            else:
                cur.execute("Select * from users where username=?",(self.username_var.get(),))
                cashin.set_user(self.username_var.get())
                cashout.set_user(self.username_var.get())
                search.set_user(self.username_var.get())
                row = cur.fetchone()
                if(row==None):
                    messagebox.showerror("Error","Invalid Username / User doesn't exist",parent=self.root)
                else:
                    cur.execute("Select password from users where username=?",(self.username_var.get(),))
                    passw = cur.fetchone()[0]
                    cur.execute("Select name from users where username=?",(self.username_var.get(),))
                    self.name_var = cur.fetchone()[0]
                    if(self.password_var.get()==passw):
                        messagebox.showinfo("Login Sucessful","Welcome {}".format(self.name_var),parent=self.root)
                        self.main(root)
                    else:
                        messagebox.showerror("Error","Username and Password doesn't match.",parent=self.root)
        except Exception as e:
            print(str(e))
            messagebox.showerror("Error","Oops some error occured. Please try again.",parent=self.root)

    def show_data(self,table):
        con = sqlite3.connect(database="munimji.db")
        cur = con.cursor()
        cur.execute("select title, remark, type, amount from records where username = ?",(self.username_var.get(),))
        rows = cur.fetchall()
        table.delete(*table.get_children())
        for row in rows:
            table.insert('','end',values=row)

    def get_bal(self):
        con = sqlite3.connect("munimji.db")
        cur = con.cursor()
        cur.execute("Select bal from users where username=?",(self.username_var.get(),))
        row = cur.fetchone()
        self.bal.set(row[0])

    def cashin_function(self):
        global bal
        self.cashin_win = tk.Toplevel(self.root)
        self.cashin_obj = cashin(self.cashin_win)
        self.root.wait_window(self.cashin_win)
        self.show_data(self.table)
        self.get_bal()
        self.balance.configure(text="Rs. {}/-".format(self.bal.get()))

    def cashout_function(self):
        self.cashout_win = tk.Toplevel(self.root)
        self.cashout_obj = cashout(self.cashout_win)
        self.root.wait_window(self.cashout_win)
        self.show_data(self.table)
        self.get_bal()
        self.balance.configure(text="Rs. {}/-".format(self.bal.get()))

    def edit_function(self):
        try:
            if(self.selected_or_not):
                self.edit_win = tk.Toplevel(self.root)
                self.edit_obj = edit(self.edit_win)
                self.root.wait_window(self.edit_win)
                self.show_data(self.table)
                self.get_bal()
                self.balance.configure(text="Rs. {}/-".format(self.bal.get()))
                self.selected_or_not=False
                edit.get_data("","","","",self.username_var.get())
            else:
                messagebox.showerror("Error","Please select the record you want to edit.",parent=self.root)    
        except Exception as e:
            print(str(e))
            messagebox.showerror("Error","Oops some error occured. Please try again.",parent=self.root)

    def delete_function(self):
        try:
            if(self.selected_or_not):
                answer = messagebox.askyesno("Confirm Delete","Are you sure you want to delete the selected record?",parent=self.root)
                if(answer):
                    con = sqlite3.connect("munimji.db")
                    cur = con.cursor()
                    cur.execute("select type from records where title=? and amount=? and remark=?",(self.selected_title.get(),self.selected_amount.get(),self.selected_remark.get()))
                    row = cur.fetchone()
                    if(row[0]=="Cash-In"):
                        cur.execute("select bal from users where username=?",(self.username_var.get(),))
                        data = cur.fetchone()
                        cur.execute("update users set bal=? where username=?",(str(int(data[0])-int(self.selected_amount.get())),self.username_var.get()))
                        con.commit()
                        self.get_bal()
                        self.balance.configure(text="Rs. {}/-".format(self.bal.get()))
                    elif(row[0]=="Cash-Out"):
                        cur.execute("select bal from users where username=?",(self.username_var.get(),))
                        data = cur.fetchone()
                        cur.execute("update users set bal=? where username=?",(str(int(data[0])+int(self.selected_amount.get())),self.username_var.get()))
                        con.commit()
                        self.get_bal()
                        self.balance.configure(text="Rs. {}/-".format(self.bal.get()))
                    cur.execute("Delete from records where title=? and amount=? and remark=?",(self.selected_title.get(),self.selected_amount.get(),self.selected_remark.get()))
                    self.selected_amount.set(StringVar())
                    self.selected_title.set(StringVar())
                    self.selected_remark.set(StringVar())
                    con.commit()
                    self.selected_or_not=False
                    edit.get_data("","","","",self.username_var.get())
                    self.show_data(self.table)
                    messagebox.showinfo("Deleted","Record Deleted Successfully.",parent=self.root)
            else:
                messagebox.showerror("Error","Please select the record you want to delete.",parent=self.root)
        except Exception as e:
            print(e)
            messagebox.showerror("Error","Oops some error occured. Please try again.",parent=self.root)

    def search_function(self):
        self.search_win = tk.Toplevel(self.root)
        self.search_obj = search(self.search_win)

    def logout_function(self):
        logoutq = askyesno(title="Logout - Munim Ji",message="Are you sure you want to logout?",parent=self.root)
        if(logoutq):
            Login(root)
            messagebox.showinfo("Logout - Munim Ji","Logged out sucessfully.",parent=self.root)

    def reset_function(self):
        resetq = askyesno(title="Reset Record - Munim Ji",message="All the entries will be erased. This action cannot be undone. Are you sure you want to reset?",parent=self.root)
        if(resetq):
            con = sqlite3.connect(database="munimji.db")
            cur = con.cursor()
            cur.execute("delete from records where username = ?",(self.username_var.get(),))
            con.commit()
            self.selected_or_not=False
            edit.get_data("","","","",self.username_var.get())
            self.show_data(self.table)
            self.bal.set('0')
            cur.execute("update users set bal='0' where username=?",(self.username_var.get(),))
            con.commit()
            con.close()
            self.balance.configure(text="Rs. {}/-".format(self.bal.get()))
            messagebox.showinfo("Reset Record - Munim Ji","The record has been reset sucessfully.",parent=self.root)
         
    def forget_passowrd(self):
        messagebox.showinfo("Information","Sorry, This feature is still under development.",parent=self.root)
        # self.forgetpass_win = tk.Toplevel(self.root)
        # self.forgetpass_obj = forgetpass(self.forgetpass_win)

    def sign_up(self):
        self.sign_up_win = tk.Toplevel(self.root)
        self.sign_up_obj = signup(self.sign_up_win)

if __name__ == '__main__':
    root = tk.Tk()
    obj = Login(root)
    root.mainloop()
