import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
from googleDrive import googleDrive 
from threading import Thread
class Application:
    def __init__(self):
        self.drive = googleDrive()
        self.labelCollection = []
        self.imageCollection = []
        self.buttonCollection = []
        self.windowCollection = []
        customtkinter.set_appearance_mode('dark')
        self.root = customtkinter.CTk()
        self.window = customtkinter.CTkToplevel(self.root)
        self.window.title("Google Drive Backup")
        self.sF = self.scaleFactor(self.window,300,400)
        print(self.sF)
        windowHeight = int(self.window.winfo_screenheight()/self.sF[1])
        windowWidth = int(self.window.winfo_screenwidth()/self.sF[0])
        self.window.geometry(f"{windowWidth}x{windowHeight}")
        self.window.resizable(False,False)
        # self.createWindow("Google Drive Backup",)
        self.createLabel(font=('Arial',25),wraplength=150,text="Google Drive Local Backup",relx=0.5,rely=0.3,anchor=tk.CENTER)
        self.createLabel(wraplength=200,text="This application is not affiliated with Google in any way",relx=0.5,rely=0.95,anchor=tk.CENTER)
        self.createImage('../images/google.png')
        self.createButton(fg_color="white",text_color="black",hover_color="#F5ECEB",text="Sign in with Google",image=self.imageCollection[0], command=self.authenticate,relx=0.5,rely=0.7,anchor=tk.CENTER)
        self.window.mainloop();
    def scaleFactor(self,window,twidth,theight):
        wSF = window.winfo_screenwidth()/twidth
        hSF = window.winfo_screenheight()/theight
        return (wSF,hSF)
    def createLabel(self,font=('TkDefaultFont',12),wraplength=200,text="",relx=0.5,rely=0.5,anchor=tk.CENTER):
        label = customtkinter.CTkLabel(master=self.window,font=font, wraplength=wraplength, text=text)
        label.place(relx=relx, rely=rely, anchor=anchor)
        self.labelCollection.append(label)
    def createImage(self,imagePath):
        photo = customtkinter.CTkImage(Image.open(imagePath))
        self.imageCollection.append(photo)
    def createButton(self,fg_color,text_color,hover_color,text="",image="",relx=0.5,rely=0.5,anchor=tk.CENTER,command=None):
        button = customtkinter.CTkButton(master=self.window, fg_color=fg_color, text_color=text_color, hover_color=hover_color, text=text,image = image,command=command)
        button.place(relx=relx,rely=rely,anchor=anchor)
        self.buttonCollection.append(button)
    def createWindow(self,title,wSF,hSF,resizable):
        self.window = customtkinter.CTkToplevel(self.root)
        self.window.title(title)
        self.wSF = self.window.winfo_screenwidth()/300 #Width scale factor
        self.hSF = self.window.winfo_screenheight()/400 #Height scale factor
        windowHeight = int(self.window.winfo_screenheight()/self.hSF)
        windowWidth = int(self.window.winfo_screenwidth()/self.wSF)
        self.window.geometry(f"{windowWidth}x{windowHeight}")
        self.window.resizable(False,False)
        self.windowCollection.append(self.window)
    



    def authenticate(self):
        print("clicked")
        new_thread = Thread(target=self.drive.authentication)
        self.buttonCollection[0].destroy()
        progressbar = customtkinter.CTkProgressBar(master=self.window)
        progressbar.start()
        self.createLabel(font=('TkDefaultFont',16),wraplength=200,text="Awaiting Authentication",relx=0.5,rely=0.6,anchor=tk.CENTER)
        progressbar.place(relx=0.175, rely=0.7)
        new_thread.start()
        while(new_thread.is_alive()):
            print("")
        progressbar.destroy()
        for value in self.labelCollection:
            value.destroy()
        for value in self.buttonCollection:
            value.destroy()
        self.labelCollection.clear()
        self.buttonCollection.clear()

       

   

app = Application()
