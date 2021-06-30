from tkinter import *
from PIL import Image,ImageTk


LARGE_FONT= "Times 16 bold"
SMALL_FONT="Mistral 14 "
class LoginFrame(Frame):
    def __init__(self,root,controller,delete):
        super().__init__()
        self.root =root
        self['width']=900
        self['height']=600
        self['bg']= "#3F4F5F"
        
        #===LOGO OF COMPANY=======================================
        self.logoimage=Image.open('logo.jpg')
        self.logoimage=self.logoimage.resize((600,100))
        self.logoimage=ImageTk.PhotoImage(self.logoimage)
        self.label=Label(self,image=self.logoimage).place(x=100,y=0)
        #******************END LOGO OF COMPANY==***************************
        
        #=====LOGIN FIELD FRAME==========================================
        #=1)lframe= container; 2)labels=user,password;  3)entry =user,password,
        #=4) buttons= login, register, forgot password
        '''Frame'''
        lFrame=Frame(self,width=605,height=400,bd=8,relief="ridge",bg="#6F8F8f")
        lFrame.place(x=100,y=110)
        
        '''Labels'''
        userl=Label(lFrame,text="USER ID ",width =10,font=LARGE_FONT,anchor=W).place(x=40,y=20)
        passwordl=Label(lFrame,text="PASSWORD ",width =10,font=LARGE_FONT,anchor=W).place(x=40,y=80)
        
        '''Entrys'''
        usere=Entry(lFrame,width=25,font='Times 16')
        usere.place(x=250,y=20)
        
        passworde=Entry(lFrame,width=25,font='Times 16',show="*")
        passworde.place(x=250,y=80)
        
        
        '''Buttons'''
        loginb=Button(lFrame,text="LOGIN",font=SMALL_FONT,width=15)
        loginb.place(x=40,y=150)
        
        registerb=Button(lFrame,text="REGISTER",font=SMALL_FONT,width=15,
        command=lambda:controller.showFrame('reg',self))
        registerb.place(x=200,y=150)
        
        forgotb=Button(lFrame,text="FORGOT PASSWORD",font=SMALL_FONT,width=20)
        forgotb.place(x=360,y=150)
        
        
        #********************LOGIN FIELD FRAME*********************************
