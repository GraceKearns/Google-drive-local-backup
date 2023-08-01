import io
import tkinter as tk
import customtkinter
from PIL import Image
from googleDrive import googleDrive 
import threading
import urllib.request
class Application:
    def __init__(self):
        self.drive = googleDrive()
        self.labelCollection = []
        self.imageCollection = []
        self.buttonCollection = []
        self.windowCollection = []
        self.frameCollection = []
        customtkinter.set_appearance_mode('dark')
        self.root = customtkinter.CTk()
        self.createWindow("Google Drive Backup",300,400,False)
        self.createLabel(window=self.windowCollection[0],font=('Arial',25),wraplength=150,text="Google Drive Local Backup",side=tk.TOP,padx=10,pady=50,anchor=tk.CENTER)
        self.createLabel(window=self.windowCollection[0],wraplength=200,text="This application is not affiliated with Google in any way",side=tk.BOTTOM,padx=10,pady=10,anchor=tk.CENTER)
        self.createImage('../images/google.png')
        self.createButton(window=self.windowCollection[0],fg_color="white",text_color="black",hover_color="#F5ECEB",text="Sign in with Google",image=self.imageCollection[0], command=self.authenticate,relx=0.5,rely=0.7,anchor=tk.CENTER)
        self.windowCollection[0].mainloop();
    def scaleFactor(self,window,twidth,theight):
        wSF = window.winfo_screenwidth()/twidth
        hSF = window.winfo_screenheight()/theight
        return (wSF,hSF)
    def createLabel(self,window,font=('TkDefaultFont',12),wraplength=200,text="",side=tk.CENTER,padx=0,pady=0,anchor=tk.CENTER):
        label = customtkinter.CTkLabel(master=window,font=font, wraplength=wraplength, text=text)
        label.pack(side=side,pady=pady, padx=padx, anchor=anchor)
        self.labelCollection.append(label)
    def createImageLabel(self,window,font=('TkDefaultFont',12),wraplength=200,img="",side=tk.CENTER,padx=0,pady=0,anchor=tk.CENTER):
        label = customtkinter.CTkLabel(master=window,font=font,wraplength=wraplength,text="",image=img)
        label.pack(side=side,pady=pady, padx=padx, anchor=anchor)
        self.labelCollection.append(label)
    def createImageUrl(self,url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        imageProd = customtkinter.CTkImage(image,size=(150,150))
        self.imageCollection.append(imageProd)
        return imageProd
    def createImage(self,imagePath):
        photo = customtkinter.CTkImage(Image.open(imagePath))
        self.imageCollection.append(photo)
    def createButton(self,window,fg_color,text_color,hover_color,text="",image="",relx=0.5,rely=0.5,anchor=tk.CENTER,command=None):
        button = customtkinter.CTkButton(master=window, fg_color=fg_color, text_color=text_color, hover_color=hover_color, text=text,image = image,command=command)
        button.place(relx=relx,rely=rely,anchor=anchor)
        self.buttonCollection.append(button)
    def createWindow(self,title,twidth,theight,resizable):
        window = customtkinter.CTkToplevel(self.root)
        window.title(title)
        self.sF = self.scaleFactor(window,twidth,theight)
        windowHeight = int(window.winfo_screenheight()/self.sF[1])
        windowWidth = int(window.winfo_screenwidth()/self.sF[0])
        window.geometry(f"{windowWidth}x{windowHeight}")
        window.resizable(resizable,resizable)
        self.windowCollection.append(window)
    def on_authentication_completed(self):
        self.progressbar.destroy()
        self.createLabel(window=self.windowCollection[0], font=('TkDefaultFont', 16),
                         wraplength=200, text="Authentication Successful", side=tk.BOTTOM,padx=10,pady=10,anchor=tk.CENTER)
        for value in self.labelCollection:
            value.destroy()
        for value in self.buttonCollection:
            value.destroy()
        self.labelCollection.clear()
        self.buttonCollection.clear()
        self.windowCollection[0].destroy()
        self.windowCollection.pop()
        self.driveInfo = self.drive.get_about_info()
        self.createWindow("Google Drive Backup",self.root.winfo_screenwidth(),self.root.winfo_screenheight(),True)
        self.populateWindow("mainmenu")
        print(self.windowCollection)
        self.createFrame(window=self.windowCollection[0],fill=tk.BOTH,border_width=2,side=tk.TOP,padx=0,pady=10,anchor=tk.N)
        self.createImageLabel(self.frameCollection[0],font=('TkDefaultFont',26),img=self.createImageUrl(self.driveInfo["user"]["photoLink"]),side=tk.RIGHT,padx=0,pady=0,anchor=tk.E)
        self.createLabel(self.frameCollection[0],font=('TkDefaultFont',26),wraplength=1000,text=f"Hello {self.driveInfo['user']['displayName']}",side=tk.TOP,padx=10,pady=10,anchor=tk.NW)
        self.createLabel(self.frameCollection[0],font=('TkDefaultFont',20),wraplength=1000,text=f"You're currently signed in with {self.driveInfo['user']['emailAddress']}",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)
        self.createFrame(window=self.windowCollection[0],fill=tk.BOTH,border_width=2,side=tk.TOP,padx=0,pady=10,anchor=tk.N)
        self.createLabel(self.frameCollection[1],font=('TkDefaultFont',18),wraplength=1000,text=f"Choose Files or folders to backup",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)
        self.createFrame(window=self.frameCollection[1],fill=tk.BOTH,border_width=2,side=tk.TOP,padx=0,pady=10,anchor=tk.N)
        self.createLabel(self.frameCollection[2],font=('TkDefaultFont',18),wraplength=1000,text=f"Choose Files or folders to backup",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)
        print(self.drive.get_files())
    def populateWindow(self,windowName):
        if windowName=="mainmenu":
            print("E")

    def createFrame(self,window=None,fill=tk.BOTH,width=0,height=0,border_width=0,fg_color=None,border_color=None,side=tk.TOP,padx=0,pady=0,anchor=tk.CENTER):
        frame = customtkinter.CTkFrame(master=window, width=width, height=height,border_width=border_width,fg_color=fg_color,border_color=border_color)
        self.frameCollection.append(frame)
        frame.pack(fill=fill,side=side,pady=pady, padx=padx, anchor=anchor)
    def check_authentication_status(self):
        if self.authentication_thread.is_alive():
            # The authentication thread is still running, check again after 100 milliseconds.
            self.windowCollection[0].after(100, self.check_authentication_status)
        else:
            self.on_authentication_completed()
    def authenticate(self):
        self.buttonCollection[0].destroy()
        self.createLabel(window=self.windowCollection[0],font=('TkDefaultFont',16),wraplength=200,text="Awaiting Authentication",side=tk.TOP,padx=10,pady=30,anchor=tk.CENTER)
        self.progressbar = customtkinter.CTkProgressBar(master=self.windowCollection[0])
        self.progressbar.start()
        self.progressbar.place(relx=0.175, rely=0.7)
        self.authentication_thread = threading.Thread(target=self.drive.authentication)
        self.authentication_thread.start()
        self.check_authentication_status()         
        

       

   

app = Application()
