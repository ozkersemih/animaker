#######################################
## This basic program developed by huseyinozker
## It may has bugs and any other problems. It has been developed to learn tkinter.
#######################################
from PIL import Image as pilimg
from PIL import ImageSequence,ImageTk,ImageFile
from PIL import GifImagePlugin
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path
import numpy as np
import imageio
import time

#<a target="_blank" href="https://icons8.com/icons/set/back">Back icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self,width=800,bg="gray",height=150)
        scrollbar = Scrollbar(self, orient=HORIZONTAL, command=canvas.xview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 10), window=self.scrollable_frame, anchor="nw")

        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.grid(row=0,column=0)
        scrollbar.grid(row=1, column=0, sticky=E+W)

class frameButton(Button):
    def __init__(self,master,frame_img,frame_index):
        Button.__init__(self,master)
        self.master=master
        self.frame_index=frame_index
        self.configure(command=lambda arg1=frame_index :app.showFrame(arg1),image=frame_img)
class App():
    def __init__(self,master):
        self.play_count=1
        self.playing=False
        self.master=master
        self.window_width=master.winfo_screenwidth()/4*3
        self.window_height=master.winfo_screenheight()/4*3
        master.geometry("%dx%d+0+0" % (self.window_width,self.window_height))
        self.baseFrame=Frame(master,width=600,height=400,bg="gray")
        self.baseFrame.place(x=150,y=40)
        self.gif=pilimg.open("idle2.gif")
        self.my_frames = []
        self.gif_frames=[]
        self.frameLabels=[]
        self.anim_len=IntVar
        self.last_index=0
        self.original_size=Variable #it hold original size of gif or image
        self.fpsValue=100
        self.baseLabel=Label(self.baseFrame,bg="gray")
        self.baseLabel.place(x=0,y=0)
        self.btn = ttk.Button(master,image=playImg, command=lambda  arg2=0 ,arg3=self.gif,arg4=1: self.play_anim(arg2,arg3,arg4))
        self.btn.place(x=15, y=20)
        self.fileButton=Button(text="Select a gif\nfrom directory",bg="gray",command=self.selectGif)
        self.fileButton.place(x=15,y=140)
        self.frameSaveButton=ttk.Button(text="Save this frame as image",command=self.saveFrame)
        self.frameSaveButton.place(x=770,y=120)
        self.animatonSaveButton=ttk.Button(text="Save this animation \nwith all frames",command=self.saveAnimation)
        self.animatonSaveButton.place(x=770,y=150)
        self.fpsEntry=Entry()
        self.fpsEntry.place(x=770,y=40)
        self.fpsButton=ttk.Button(text="FPS!",command=self.set_fps)
        self.fpsButton.place(x=770,y=65)
        ##creating menu
        self.menuBar=Menu(master)
        self.fileMenu=Menu(self.menuBar,tearoff=0)
        self.saveMenu=Menu(self.menuBar,tearoff=0)
        self.helpMenu=Menu(self.menuBar,tearoff=0)
        self.fileMenu.add_command(label="Open animation(gif)",command=self.selectGif)
        self.saveMenu.add_command(label="Save current frame as image")
        self.saveMenu.add_command(label="Save all frames as animation(gif)")
        self.helpMenu.add_command(label="About")
        self.menuBar.add_cascade(label="File",menu=self.fileMenu)
        self.menuBar.add_cascade(label="Save",menu=self.saveMenu)
        self.menuBar.add_cascade(label="Help",menu=self.helpMenu)
        self.master.config(menu=self.menuBar)
        ##animation frames in Frame Component and other settings widget
        self.framePanel=ScrollableFrame(self.master,width=100,height=150)
        self.framePanel.place(x=80,y=465)
        self.frameCounterLabel=Label(text=("Current Frame: %d" %(self.last_index)),bg="green")
        self.frameCounterLabel.place(x=800,y=365)
        self.backFrameButton=Button(image=backImg,command=self.backFrame)
        self.backFrameButton.place(x=800,y=325)
        self.nextFrameButton = Button(image=nextImg,command=self.nextFrame)
        self.nextFrameButton.place(x=840,y=325)
        ##add frame
        self.addFrameButton=Button(self.master,text=" Add new \n frame(s) ",image=addImg,compound=LEFT,command=self.addFrame)
        self.addFrameButton.place(x=930,y=325)
        ##remove frame
        self.addFrameButton = Button(self.master, text=" Remove  \n frame  ", image=removeImg, compound=LEFT,command=self.removeFrame)
        self.addFrameButton.place(x=930, y=275)




    def play_anim(self, ind, anim,counter):
        if len(self.my_frames)>0:
            self.btn.configure(image=pauseImg)
            self.play_count=counter
            self.btn.configure(command=self.stop_anim,text="Stop\nAnimation")
            self.playing=True
            if self.play_count==1:
                #print(ind)
                frame = self.my_frames[ind]
                ind += 1
                self.baseLabel.configure(image=frame)
                if ind > len(self.my_frames)-1:
                    ind = 0
                self.last_index=ind
                self.frameCounterLabel.configure(text="Current Frame: %d" %(self.last_index))
                self.loop=self.master.after(self.fpsValue, self.play_anim, ind, anim,1)
            else:
                return
        else:
            self.showWarning("You have not loaded animation")
    def stop_anim(self):
        self.master.after_cancel(self.loop)
        self.btn.configure(command=lambda  arg2=self.last_index,arg3=self.gif,arg4=1: self.play_anim(arg2,arg3,arg4),image=playImg)


    def selectGif(self):
        self.my_frames.clear()
        self.last_index=0
        if(self.playing==True):
            self.stop_anim()
        #print(self.last_index)
        under = Tk()
        under.withdraw()
        self.gifFilePath=askopenfilename(initialdir = "C:/Users/Hüseyin/Desktop/animation gifs", title = "Dosya Seç", filetypes = (("gif files","*.gif"),("all files","*.*")))
        if len(self.gifFilePath)!=0:
            newGif=pilimg.open(self.gifFilePath)
            under.destroy()
            print(newGif.info['duration'])
            self.original_size=newGif.size
            self.gif_extract(newGif)
            self.createFrameLabels()

    def gif_extract(self,gif):
        frames=[]
        len_count=0
        self.gif_frames.clear()#important!
        for f in ImageSequence.Iterator(gif):
            f=f.resize(self.calculateSize(f))
            fi=ImageTk.PhotoImage(f)
            frames.append(fi)
            self.gif_frames.append(f)
            len_count=len_count+1
        self.my_frames=frames
        self.anim_len=len_count


    def set_fps(self):
        self.fpsValue=int(1000/int(self.fpsEntry.get()))
    def calculateSize(self,image_):
        newWidth=(600/image_.width)*image_.width
        newHeight=(400/image_.height)*image_.height
        return (int(newWidth),int(newHeight))
    def createFrameLabels(self):

        if(len(self.frameLabels)>0):
            for i in np.arange(0,len(self.frameLabels)):
                print("x")
                self.frameLabels[i].destroy()
        index=0
        for i in self.gif_frames:
            i=i.resize((110,110))
            newImg=ImageTk.PhotoImage(i)
            newButton=frameButton(self.framePanel.scrollable_frame,newImg,index)
            newButton.photo=newImg
            newButton.pack(side=LEFT)#place(x=(index*120)+10,y=15)
            self.frameLabels.append(newButton)
            index=index+1

    def showFrame(self,frameIndex):
        self.last_index = frameIndex
        print(self.last_index)
        if self.playing==True:
            self.stop_anim()
            self.baseLabel.configure(image=self.my_frames[frameIndex])
        else:
            self.baseLabel.configure(image=self.my_frames[frameIndex])

        print(self.last_index)
        self.frameCounterLabel.configure(text="Current Frame: %d" % (self.last_index))
    def backFrame(self):
        if self.last_index>0:
            self.last_index=self.last_index-1
            if self.playing==True:
                self.stop_anim()
                self.baseLabel.configure(image=self.my_frames[self.last_index])
            else:
                self.baseLabel.configure(image=self.my_frames[self.last_index])
            self.frameCounterLabel.configure(text="Current Frame: %d" % (self.last_index))
    def nextFrame(self):
        if self.last_index<(len(self.my_frames)-1):
            self.last_index=self.last_index+1
            if self.playing==True:
                self.stop_anim()
                self.baseLabel.configure(image=self.my_frames[self.last_index])
            else:
                self.baseLabel.configure(image=self.my_frames[self.last_index])
            self.frameCounterLabel.configure(text="Current Frame: %d" % (self.last_index))
    def addFrame(self):
        if self.playing:
            self.stop_anim()
        under=Tk()
        under.withdraw()
        newImgPaths=askopenfilenames(parent=under,initialdir = imgpath,title = "Select image for frame",filetypes = (("png files","*.png"),("jpg files","*.jpg"),("all files","*.*")))
        under.update()
        under.destroy()
        root.tk.splitlist(newImgPaths)
        for i in newImgPaths:
            newImg=pilimg.open(i)
            self.original_size=newImg.size
            newImg=newImg.resize(self.calculateSize(newImg))
            ni=ImageTk.PhotoImage(newImg)
            self.my_frames.insert(self.last_index,ni)
            self.anim_len=len(self.my_frames)
            self.gif_frames.insert(self.last_index+1,newImg)
            self.last_index = self.last_index + 1
        self.createFrameLabels()
    def removeFrame(self):
        if self.playing:
            self.stop_anim()
        self.my_frames.pop(self.last_index)
        self.gif_frames.pop(self.last_index)
        if self.last_index>0:
            self.last_index=self.last_index-1
        elif self.last_index<len(self.my_frames)-1:
            self.last_index=self.last_index+1
        self.createFrameLabels()


    def showWarning(self,message):
        messagebox.showinfo("Warning",message)
    def saveAnimation(self):
        saveFrames=[]
        a = self.fpsValue/1000
        save_path=asksaveasfilename(initialdir='/',filetypes = (("gif files","*.gif"),("all files","*.*")), defaultextension=".gif")
        for i in self.gif_frames:
            j=i.resize(self.original_size)
            saveFrames.append(j)
        imageio.mimsave(save_path,saveFrames,format='GIF',duration=a)
        #d=[1,1,1,1,1,1,1,1,1,1,1,1]
        #saveFrames[0].save('C:/Users/Hüseyin/Desktop/animation gifs/created anims/new.gif', format='GIF', save_all=True, append_images=saveFrames[1:], loop=0, duration=30)
    def saveFrame(self):
        save_path = asksaveasfilename(initialdir='/', filetypes=(("png file", "*.png"),("jpg file", "*.jpg"), ("all files", "*.*")),
                                      defaultextension=".png")
        ext=Path(save_path).suffix
        if(ext=='.png'):
            self.gif_frames[self.last_index].save(save_path)
        elif(ext=='.jpg'):
            self.gif_frames[self.last_index].convert('RGB').save(save_path,"JPEG")
root=Tk()
imgpath="C:/Users/Hüseyin/Desktop/animation gifs/frames"
backIcon= pilimg.open(r"back_icon.png")
backIcon=backIcon.resize((25,25))
backImg=ImageTk.PhotoImage(backIcon)
nextIcon= pilimg.open(r"next_icon.png")
nextIcon=nextIcon.resize((25,25))
nextImg=ImageTk.PhotoImage(nextIcon)
addIcon=pilimg.open(r"add_icon.png")
addImg=ImageTk.PhotoImage(addIcon)
removeIcon=pilimg.open(r"remove_icon.png")
removeImg=ImageTk.PhotoImage(removeIcon)
playIcon=pilimg.open(r"play_icon.png")
playIcon=playIcon.resize((48,48))
playImg=ImageTk.PhotoImage(playIcon)
pauseIcon=pilimg.open(r"pause_icon.png")
pauseIcon=pauseIcon.resize((48,48))
pauseImg=ImageTk.PhotoImage(pauseIcon)

app=App(root)
root.mainloop()