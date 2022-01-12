from tkinter.constants import X
from tkinter.font import BOLD
from PIL import ImageTk
from tkinter import *
from tkinter import ttk,messagebox
import sqlite3

class signup():

    def __init__(self,root):
        self.root = root
        self.root.title("New User - Munim Ji")
        self.root.geometry("600x500")
        self.root.resizable(False,False)
        self.root.iconbitmap("images/favicon.ico")
        self.root.focus_force()

        #variables
        self.name_var = StringVar()
        self.username_var = StringVar()
        self.phone_var = StringVar()
        self.password_var = StringVar()
        self.cpassword_var = StringVar()

        #Background
        self.bg = ImageTk.PhotoImage(file="images/bg2.jpg")
        self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        #signup frame
        self.signup = Label(self.root,bg="white").place(x=0,y=50,height=400,width=600)

        #textboxes and labels
        Label(self.root,text="Register here, Its 100% free!!",font=("Impact",16),bg="tomato",fg="white").place(x=50,y=30,height=40,width=500)
        Label(self.root,text="Note: All fields are mandatory",font=("Helvetica",10),bg="white",fg="tomato").place(x=0,y=80,width=600,height=25)

        Label(self.root,text="Enter your Name:",font=("Helvetica",10),bg="white").place(x=10,y=120,width=250,height=30)
        name_txt = Entry(self.root,bg="light gray",textvariable=self.name_var)
        name_txt.place(x=280,y=120,width=250,height=30)
        name_txt.focus()
        
        Label(self.root,text="Enter your Username:",font=("Helvetica",10),bg="white").place(x=10,y=180,width=250,height=30)
        username_txt = Entry(self.root,bg="light gray",textvariable=self.username_var).place(x=280,y=180,width=250,height=30)
        
        Label(self.root,text="Enter your Phone Number:",font=("Helvetica",10),bg="white").place(x=10,y=240,width=250,height=30)
        phone_txt = Entry(self.root,bg="light gray",textvariable=self.phone_var).place(x=280,y=240,width=250,height=30)

        Label(self.root,text="Enter your Password:",font=("Helvetica",10),bg="white").place(x=10,y=300,width=250,height=30)
        pass_txt = Entry(self.root,bg="light gray",textvariable=self.password_var).place(x=280,y=300,width=250,height=30)

        Label(self.root,text="Confirm your Password:",font=("Helvetica",10),bg="white").place(x=10,y=360,width=250,height=30)
        cpass_txt = Entry(self.root,bg="light gray",textvariable=self.cpassword_var).place(x=280,y=360,width=250,height=30)
        
        #buttons
        register_btn = Button(self.root,text="Register",font=("Helvetica",12,BOLD),bg="sea green",fg="white",activebackground="white",activeforeground="sea green",command=self.register,cursor="hand2")
        register_btn.place(x=140,y=430,height=40,width=150)
        cancel_btn = Button(self.root,text="Cancel",font=("Helvetica",12,BOLD),bg="tomato",fg="white",activeforeground="tomato",activebackground="white",command=self.cancel_signup,cursor="hand2").place(x=310,y=430,height=40,width=150)

    def register(self):
        con = sqlite3.connect(database="munimji.db")
        cur = con.cursor()
        try:
            if self.name_var.get()=="" or self.phone_var.get()=="" or self.password_var.get()=="" or self.cpassword_var.get()=="":
                messagebox.showerror("Error","Mandatory fields cannot be left empty.",parent=self.root)
                self.root.focus_force()
            elif (len(self.phone_var.get())<10 or self.phone_var.get().isnumeric()==False):
                messagebox.showerror("Error","Invalid Phone Number",parent=self.root)
                self.root.focus_force()
            elif(self.password_var.get()!=self.cpassword_var.get()):
                messagebox.showerror("Error","Password does not match",parent=self.root)
                self.root.focus_force()
            elif self.username_var.get()=="":
                messagebox.showerror("Error","Mandatory fields cannot be left empty.",parent=self.root)
                self.root.focus_force()
            elif len(self.password_var.get())<6:
                messagebox.showwarning("Warning","Password is too weak.",parent=self.root)
                self.root.focus_force()
            else:
                cur.execute("select * from users where username=?",(self.username_var.get(),))
                row = cur.fetchone()
                print(row)
                if(row!=None):
                    messagebox.showinfo("Error","This username is already taken. Please use another one.",parent=self.root)
                    self.root.focus_force()
                else:
                    cur.execute("INSERT INTO users (name,username,phonenumber,password) VALUES (?,?,?,?)",(self.name_var.get(),self.username_var.get(),self.phone_var.get(),self.password_var.get()))
                    con.commit()
                    messagebox.showinfo("Registered Succesfully","Welcome {}, Your username is {} and your password is {}".format(self.name_var.get(),self.username_var.get(),self.password_var.get(),parent=self.root),parent=self.root)
                    self.root.destroy()
                
        except Exception as e:
            messagebox.showerror("Error","Oops, Some error occured. Please try again",parent=self.root)
            
    def cancel_signup(self):
        self.root.destroy()

if __name__ == '__main__':
    root = Tk()
    obj = signup(root)
    root.mainloop()
    