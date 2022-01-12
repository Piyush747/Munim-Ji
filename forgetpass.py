import tkinter as tk
from tkinter import StringVar, font
from tkinter import messagebox
from tkinter.constants import W, X
from tkinter.font import BOLD
from PIL import ImageTk
import sqlite3
from twilio.rest import Client
import random

class forgetpass():
    
    def __init__(self,root):
        self.root = root
        root.title("Reset Password - Munim Ji")
        self.root.geometry("300x320")
        self.root.resizable(False,False)
        self.root.iconbitmap("images/favicon.ico")
        self.root.focus_force()

        self.username_var = StringVar()

        main = tk.Label(root,bg="#2C394B").place(x=0,y=0,width=300,height=320)

        tk.Label(self.root,text="Forget Password? Don't worry, we got your back.",bg="#2C394B",fg="orange",font="Helvetica 10").place(x=5,y=10)
        tk.Label(self.root,text="Enter your Username:",bg="#2C394B",fg="white",font="Helvetica 10").place(x=5,y=50)
        self.user = tk.Entry(self.root,bg="#334756",fg="white",textvariable=self.username_var,insertbackground='white')
        self.user.place(x=5,y=75,width=290,height=30)
        self.user.focus()

        tk.Label(self.root,text="An otp will be sent to \nyour registered mobile number.",fg="orange",bg="#2C394B",font="Helvetica 10").place(x=5,y=120,width=300)
        tk.Button(self.root,text="Send OTP",bg="deep sky blue",fg="white",font="Helvetica 10 bold",command=self.send_otp,cursor="hand2").place(x=10,y=170,width=280,height=40)
        tk.Button(self.root,text="Resend OTP",bg="green",fg="white",font="Helvetica 10 bold",command=self.resend_otp,cursor="hand2").place(x=10,y=220,width=280,height=40)
        tk.Button(self.root,text="Cancel",bg="tomato",fg="white",font="Helvetica 10 bold",command=self.cancelresetpass,cursor="hand2").place(x=10,y=270,width=280,height=40)

    def sendotp(self):
        con = sqlite3.connect(database="munimji.db")
        cur = con.cursor()
        try:
            if(self.user.get()==""):
                messagebox.showerror("Error","Please enter username first",parent=self.root)
            else:
                cur.execute("Select * from users where username=?",(self.username_var.get(),))
                row = cur.fetchone()
                if(row==None):
                    messagebox.showerror("Error","Invalid Username / User doesn't exist",parent=self.root)
                else:
                    cur.execute("Select phonenumber from users where username=?",(self.username_var.get(),))
                    phone = cur.fetchone()[0]
                    messagebox.showinfo("OTP sent","An OTP has been sent to {}".format(phone),parent=self.root)
        except Exception as e:
            messagebox.showerror("Error","Oops some error occured. Please try again",parent=self.root)

    def cancelresetpass(self):
        self.root.destroy()

    def send_otp(self):
        pass
        # self.n = random.randint(1000,9999)
        # self.client = Client("","")
        # self.client.messages.create(to=[""],from_=[""],body=self.n)

    def resend_otp(self):
        pass
        
if __name__ == '__main__':
    root =tk.Tk()
    obj = forgetpass(root)
    root.mainloop()