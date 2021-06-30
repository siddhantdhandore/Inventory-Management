from tkinter import *


FONT="Times 14"
class RegisterFrame(Frame):
    def __init__(self,root,controller,delete):
        super().__init__()
        self.root=root
        self['width']=900
        self['height']=600
        self['bg']= "#ff9F7F"
        
        #=====REGISTER FIELD FRAME==========================================
        #==1)lframe= container; 2)labels=fname,lnamepassword,confirm password,email,mobile,secQ,roll;  
        #==3)entry =entries for respective labels,
        #==4) buttons= login, register, forgot password
        '''Frame'''
        rFrame=Frame(self,width=605,height=500,bd=8,relief="ridge",bg="#6F8F8f")
        rFrame.place(x=100,y=50)
        
        '''Labels'''
        heading=Label(rFrame,text="REGISTRATION",width=20,font="Verdana 28 bold",padx=33).place(x=0,y=0)
        
        firstl=Label(rFrame,text="First Name",font=FONT).place(x=10,y=60)
        lastl=Label(rFrame,text="Last Name",font=FONT).place(x=300,y=60)
        
        passwordl=Label(rFrame,text="Password",font=FONT).place(x=10,y=140)
        cpasswordl=Label(rFrame,text="Confirm Password",font=FONT).place(x=300,y=140)
        
        mobilel=Label(rFrame,text="Mobile Number",font=FONT).place(x=10,y=220)
        emaill=Label(rFrame,text="Email id",font=FONT).place(x=300,y=220)
        
        secql=Label(rFrame,text="Security Question",font=FONT).place(x=10,y=300)
        answerl=Label(rFrame,text="Answer",font=FONT).place(x=300,y=300)
        
        '''Entries'''
        firste=Entry(rFrame,width=30,font=FONT)
        laste=Entry(rFrame,width=30,font=FONT)
        passworde=Entry(rFrame,width=30,font=FONT)
        cpassworde=Entry(rFrame,width=30,font=FONT)
        mobilee=Entry(rFrame,width=30,font=FONT)
        emaile=Entry(rFrame,width=30,font=FONT)
        secqe=Entry(rFrame,width=30,font=FONT)
        answere=Entry(rFrame,width=30,font=FONT)
        
        firste.place(x=10,y=90)
        firste.focus()
        laste.place(x=300,y=90)
        passworde.place(x=10,y=170)
        cpassworde.place(x=300,y=170)
        mobilee.place(x=10,y=250)
        emaile.place(x=300,y=250)
        secqe.place(x=10,y=330)
        answere.place(x=300,y=330)
        
        
        '''Buttons'''
        resetb=Button(rFrame,text="RESET",font=FONT,width=14)
        resetb.place(x=40,y=380)
        
        registerb=Button(rFrame,text="REGISTER",font=FONT,width=14)
        registerb.place(x=200,y=380)
        
        backb=Button(rFrame,text="BACK",font=FONT,width=14,
        command=lambda:controller.showFrame('log',self))
        backb.place(x=360,y=380)
        
        
        #********************LOGIN FIELD FRAME*********************************
