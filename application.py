from tkinter import *
#==IMPORT ALL FRAME CLASSES======
from login import LoginFrame
from register import RegisterFrame
#==****************=================

#creating Tk class '''root=Tk()'''
class Application(Tk):
    def __init__(self):
        super().__init__()
        #======main window configuration=========================
        self.width  = self.winfo_screenwidth()//2
        self.height = self.winfo_screenheight()//2
        self.geometry(f"900x600+{self.width-450}+{self.height-300}")
        self.title('Inventory Management System v0.0.1')
        #=====******************===============================================
        
        self.frames={'log':LoginFrame,'reg':RegisterFrame}
        
        #=====CONTAINER FRAME================================
        #contains other frames
        self.container=Frame(self,width=900,height=600,bg="#3F4F5F")
        self.container.place(x=0,y=0)
        
        loginob=LoginFrame(self.container,self,'log')
        loginob.place(x=0,y=0)
        self.toDestroy=[loginob]
        
    def showFrame(self,controller,delete):
        self.toDestroy[0]=delete
        self.toDestroy[0].destroy()
        
        frame=self.frames[controller]
        frameob=frame(self.container,self,self)
        frameob.place(x=0,y=0)
        

        
                
app=Application()
app.mainloop()        
        