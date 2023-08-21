import io
import json
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
        self.scrollFrameCollection = []
        self.googleItemCollection = []
        self.selectedFrames= []
        self.folderStack = []
        self.folderContents= []
        customtkinter.set_appearance_mode('dark')
        self.root = customtkinter.CTk()
        self.createWindow("Google Drive Backup",300,400,False)
        self.createImage('../images/google.png') #0
        self.createImage('../images/folder.png') #1
        self.createImage('../images/file.png')#2
        self.createImage('../images/form.png')#3
        self.createImage('../images/sheet.png')#4
        self.createImage('../images/word.png')#5
        self.createImage('../images/slide.png')#6
        self.createImage('../images/return.png')#7
        self.populateWindow("signin")
        self.windowCollection[0].mainloop();
    def scaleFactor(self,window,twidth,theight):
        wSF = window.winfo_screenwidth()/twidth
        hSF = window.winfo_screenheight()/theight
        return (wSF,hSF)
    def createLabel(self,window,font=('TkDefaultFont',12),wraplength=200,text="",side=tk.CENTER,padx=0,pady=0,anchor=tk.CENTER):
        label = customtkinter.CTkLabel(master=window,font=font, wraplength=wraplength, text=text)
        label.pack(side=side,pady=pady, padx=padx, anchor=anchor)
        self.labelCollection.append(label)
        return label
    def createImageLabel(self,window,font=('TkDefaultFont',12),wraplength=200,img="",side=tk.CENTER,padx=0,pady=0,anchor=tk.CENTER):
        label = customtkinter.CTkLabel(master=window,font=font,wraplength=wraplength,text="",image=img)
        label.pack(side=side,pady=pady, padx=padx, anchor=anchor)
        self.labelCollection.append(label)
        return label
    def createImageUrl(self,url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        #self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        imageProd = customtkinter.CTkImage(image,size=(100,100))
        self.imageCollection.append(imageProd)
        return imageProd
    def createImage(self,imagePath):
        photo = customtkinter.CTkImage(Image.open(imagePath))
        self.imageCollection.append(photo)
    def createButton(self,window,fg_color,text_color,hover_color,text="",image=None,side=tk.TOP,padx=0,pady=0,anchor=tk.CENTER,command=None,width=0,height=0,corner_radius=0):
        button = customtkinter.CTkButton(master=window, width=width,height=height,fg_color=fg_color, text_color=text_color, hover_color=hover_color, text=text,image = image,command=command,corner_radius=corner_radius)
        button.pack(side=side,padx=padx,pady=pady,anchor=anchor)
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
        self.clearAll()
        self.windowCollection[0].destroy()
        self.windowCollection.pop()
        self.driveInfo = self.drive.get_about_info()
        self.createWindow("Google Drive Backup",self.root.winfo_screenwidth(),self.root.winfo_screenheight(),True)
        self.populateWindow("mainmenu")

    def populateWindow(self,windowName):
        if windowName=="signin":
            self.createLabel(window=self.windowCollection[0],font=('Arial',25),wraplength=150,text="Google Drive Local Backup",side=tk.TOP,padx=10,pady=50,anchor=tk.CENTER)
            self.createLabel(window=self.windowCollection[0],wraplength=200,text="This application is not affiliated with Google in any way",side=tk.BOTTOM,padx=10,pady=10,anchor=tk.CENTER)
            self.createButton(window=self.windowCollection[0],fg_color="white",text_color="black",hover_color="#F5ECEB",text="Sign in with Google",image=self.imageCollection[0],side=tk.BOTTOM,padx=0,pady=30,command=lambda:self.populateWindow("authenticating"),anchor=tk.CENTER)
        if windowName=="authenticating":
            self.buttonCollection[0].destroy()
            self.createLabel(window=self.windowCollection[0],font=('TkDefaultFont',16),wraplength=200,text="Awaiting Authentication",side=tk.TOP,padx=10,pady=30,anchor=tk.CENTER)
            self.progressbar = customtkinter.CTkProgressBar(master=self.windowCollection[0])
            self.progressbar.start()
            self.progressbar.place(relx=0.175, rely=0.7)
            self.authentication_thread = threading.Thread(target=self.drive.authentication)
            self.authentication_thread.start()
            self.check_authentication_status()     
        if windowName=="mainmenu":
            self.clearAll()
            self.selectedFrames.clear()
            self.createFrame(window=self.windowCollection[0],fill=tk.BOTH,border_width=2,side=tk.TOP,padx=10,pady=10,anchor=tk.N)
            self.createImageLabel(self.frameCollection[0],font=('TkDefaultFont',26),img=self.createImageUrl(self.driveInfo["user"]["photoLink"]),side=tk.RIGHT,padx=0,pady=0,anchor=tk.E)
            self.createLabel(self.frameCollection[0],font=('TkDefaultFont',26),wraplength=1000,text=f"Hello {self.driveInfo['user']['displayName']}",side=tk.TOP,padx=10,pady=10,anchor=tk.NW)
            self.createLabel(self.frameCollection[0],font=('TkDefaultFont',20),wraplength=1000,text=f"You're currently signed in with {self.driveInfo['user']['emailAddress']}",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)
            self.createFrame(window=self.windowCollection[0],expand=True,fill=tk.BOTH,border_width=2,side=tk.TOP,padx=10,pady=10,anchor=tk.N)
            self.createScrollFrame(window=self.frameCollection[1],expand=True,fill=tk.BOTH,border_width=2,side=tk.BOTTOM,padx=10,pady=5,anchor=tk.N)
            self.driveItems = self.drive.get_files()
            self.createItemFrame(window=self.scrollFrameCollection[0])
            self.createFrame(window=self.windowCollection[0],fill=tk.BOTH,border_width=2,side=tk.TOP,padx=10,pady=10,anchor=tk.S)
            self.createButton(window=self.frameCollection[3],fg_color="white",text_color="black",hover_color="#F5ECEB",text="Sign Out",side=tk.LEFT,padx=10,pady=10,anchor=tk.W,corner_radius=30)
            self.createButton(window=self.frameCollection[3],fg_color="white",text_color="black",hover_color="#F5ECEB",text="Next",side=tk.RIGHT,padx=10,pady=10,anchor=tk.E,command=lambda:self.populateWindow(windowName="confirmation"),corner_radius=30)
        if windowName=="confirmation":
            self.clearAll()
            self.createFrame(window=self.windowCollection[0],fill=tk.BOTH,border_width=2,side=tk.TOP,padx=10,pady=10,anchor=tk.N)
            self.createImageLabel(self.frameCollection[0],font=('TkDefaultFont',26),img=self.createImageUrl(self.driveInfo["user"]["photoLink"]),side=tk.RIGHT,padx=0,pady=0,anchor=tk.E)
            self.createLabel(self.frameCollection[0],font=('TkDefaultFont',26),wraplength=1000,text=f"Hello {self.driveInfo['user']['displayName']}",side=tk.TOP,padx=10,pady=10,anchor=tk.NW)
            self.createLabel(self.frameCollection[0],font=('TkDefaultFont',20),wraplength=1000,text=f"You're currently signed in with {self.driveInfo['user']['emailAddress']}",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)
            self.createFrame(window=self.windowCollection[0],expand=True,fill=tk.BOTH,border_width=2,side=tk.TOP,padx=10,pady=10,anchor=tk.N)
            self.createLabel(self.frameCollection[1],font=('TkDefaultFont',18),wraplength=1000,text=f"Confirm items to backup",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)
            self.createScrollFrame(window=self.frameCollection[1],expand=True,fill=tk.BOTH,border_width=2,side=tk.LEFT,padx=10,pady=5,anchor=tk.W)
            for x in self.selectedFrames:
                self.createLabel(self.scrollFrameCollection[0],font=('TkDefaultFont',18),wraplength=1000,text=f"{x['name']}",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)

            self.createFrame(window=self.windowCollection[0],fill=tk.BOTH,border_width=2,side=tk.BOTTOM,padx=10,pady=10,anchor=tk.S)
            self.createButton(window=self.frameCollection[2],fg_color="white",text_color="black",hover_color="#F5ECEB",text="Back",side=tk.LEFT,padx=10,pady=10,anchor=tk.W,command=lambda:self.populateWindow(windowName="mainmenu"),corner_radius=30)
            self.createButton(window=self.frameCollection[2],fg_color="white",text_color="black",hover_color="#F5ECEB",text="Create Script",side=tk.RIGHT,padx=10,pady=10,anchor=tk.E,command=self.createScript,corner_radius=30)
            
    def clearAll(self):
        self.labelCollection.clear()
        self.buttonCollection.clear()
        for x in self.scrollFrameCollection:
            x.destroy()
        for x in self.frameCollection:
            x.destroy()
        self.frameCollection.clear()
        self.scrollFrameCollection.clear()
       
    def createItemFrame(self, window=None,init=True):
        if init:
            self.createLabel(self.frameCollection[1],font=('TkDefaultFont',18),wraplength=1000,text=f"Choose Files or folders to backup",side=tk.TOP,padx=10,pady=0,anchor=tk.NW)
            value = self.createImageLabel(self.frameCollection[1],font=('TkDefaultFont',26),img=self.imageCollection[7],side=tk.LEFT,padx=20,pady=0,anchor=tk.E)
            value.bind("<Button-1>", self.click_return)
        self.frame = customtkinter.CTkFrame(master=self.scrollFrameCollection[0], border_width=2)
        self.frameCollection.append(self.frame)
        self.frame.pack(side=tk.TOP, expand=True,fill=tk.BOTH, padx=0, pady=0, anchor=tk.W)
        row_frame = customtkinter.CTkFrame(master=self.frame, height=100,border_width=0)
        row_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0, anchor=tk.W)
        frame_data_mapping = {}
        frame_dataName_mapping = {}
            
        for i, item in enumerate(self.driveItems):
            if item['id'] in self.selectedFrames:
                item_frame = customtkinter.CTkFrame(master=row_frame, width=200, fg_color="green",border_width=0)
            else:
                item_frame = customtkinter.CTkFrame(master=row_frame, width=200 ,border_width=0)
            item_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0, anchor=tk.W)
            label = customtkinter.CTkLabel(
                master=item_frame, font=("TkDefaultFont", 12), width=105, height=50, wraplength=100, text=item['name']
            )
            label.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=20, pady=20, anchor=tk.CENTER)
          
            framedata = {
                "id":item["id"],
                "name":item["name"]
            }
            frame_data_mapping[item_frame] = framedata 
            img = None
            if(item["mimeType"] == "application/vnd.google-apps.spreadsheet"):
                item_frame.bind("<Button-1>", self.click_frame)
                img = self.imageCollection[4]
            elif(item["mimeType"] == "application/vnd.google-apps.document"):
                item_frame.bind("<Button-1>", self.click_frame)
                img = self.imageCollection[5]
            elif(item["mimeType"] == "application/vnd.google-apps.folder"):
                item_frame.bind("<Button-1>", self.click_folder)
                img = self.imageCollection[1]
                
            else:
                item_frame.bind("<Button-1>", self.click_frame)
                img = self.imageCollection[2]
         
            imglabel = customtkinter.CTkLabel(master=item_frame,text="",image=img)
            imglabel.pack(side=tk.BOTTOM,fill=tk.BOTH, padx=20, pady=20, anchor=tk.CENTER)

            if (i + 1) % 10 == 0:  # Change '3' to the desired number of labels per row
                row_frame = customtkinter.CTkFrame(master=self.frame, border_width=0)
                row_frame.pack(side=tk.TOP, fill=tk.BOTH,padx=0, pady=0, anchor=tk.W)
        self.frame_data_mapping = frame_data_mapping
        self.frame_dataName_mapping = frame_dataName_mapping
        self.googleItemCollection.append(self.frame)
        
    def click_frame(self,event):
        clicked_frame = event.widget.master
        str_value = self.frame_data_mapping.get(clicked_frame) 
        print(str_value)
        if event.widget.master.cget("fg_color") == "green":
            new_color = "#2B2B2B"  # Change the color back to black
            self.selectedFrames.remove(str_value)
        else:
            new_color = "green"  # Change the color to green
            self.selectedFrames.append(str_value)
        event.widget.master.configure(fg_color=new_color)
    def click_folder(self,event):
        self.frame.destroy()
        clicked_frame = event.widget.master
        str_value = self.frame_data_mapping.get(clicked_frame) 
        print(str_value["id"])
        self.folderStack.append(str_value["id"])
        self.driveItems= self.drive.get_folder(str_value["id"])
        self.createItemFrame(window=self.scrollFrameCollection[0],init=False)
    def createScript(self):
        print(self.selectedFrames)
        dictionary = {
            "items": self.selectedFrames,
            "scriptPath": ["./backup/output.json"],
            "path": ["./backup/"],
            "nameExten": "backup",
            "backupPeriod": "2400"
        }
        print(dictionary['items'])
        json_object = json.dumps(dictionary, indent=4)
        with open("scripts/sample.json", "w") as outfile:
            outfile.write(json_object)
        self.drive.document_automation(DOCUMENT_ID=dictionary['items'],FILE_PATH=dictionary['path'])
    def click_return(self,event):
        if self.folderStack:
          
           self.frame.destroy()
           self.folderStack.pop()
           if self.folderStack:
            self.driveItems= self.drive.get_folder(self.folderStack[len(self.folderStack-1)])
           else:
            self.driveItems=self.drive.get_files()
           self.createItemFrame(window=self.scrollFrameCollection[0],init=False)
        else:
            print("space")
        
    def createScrollFrame(self,window=None,fill=tk.NONE,width=0,expand=False,height=0,border_width=0,fg_color=None,border_color=None,side=tk.TOP,padx=0,pady=0,anchor=tk.CENTER):
        frame = customtkinter.CTkScrollableFrame(master=window, width=width, height=height,border_width=border_width,fg_color=fg_color,border_color=border_color)
        self.scrollFrameCollection.append(frame)
        frame.pack(fill=fill,expand=expand,side=side,pady=pady, padx=padx, anchor=anchor)
    def createFrame(self,window=None,expand=False,fill=tk.BOTH,width=0,height=0,border_width=0,fg_color=None,border_color=None,side=tk.TOP,padx=0,pady=0,anchor=tk.CENTER):
        frame = customtkinter.CTkFrame(master=window, width=width, height=height,border_width=border_width,fg_color=fg_color,border_color=border_color)
        self.frameCollection.append(frame)
        frame.pack(fill=fill,expand=expand,side=side,pady=pady, padx=padx, anchor=anchor)
        return frame
    def check_authentication_status(self):
        if self.authentication_thread.is_alive():
            # The authentication thread is still running, check again after 100 milliseconds.
            self.windowCollection[0].after(100, self.check_authentication_status)
        else:
            self.on_authentication_completed()
        

       

   

app = Application()
