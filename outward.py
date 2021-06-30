from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import filedialog
from pdftable import OutPdf
from datetime import datetime
import sqlite3

#=================================database===============================
conn=sqlite3.connect('newdatabase.db')
cur=conn.cursor()
'''
cur.execute("create table outward(date varchar(10),time varchar(8),category \
        varchar(30),product varchar(30),brand varchar(30),\
        quantity real,gatepass varchar(10),reciever varchar(30),\
        reciever varchar(30));")
'''

#========********************************************======================


class OutwardFrame(Frame):
    
    def __init__(self,root):
        super().__init__()
        '''background image'''
        self.bgimg=Image.open('bg3.jpg')
        self.bgimg=self.bgimg.resize((970,600))
        self.bgimg=ImageTk.PhotoImage(self.bgimg)
        bglabel=Label(self,image=self.bgimg).place(x=0,y=0)
        oheading=Label(self,text='OUTWARD MANAGEMENT',font='Helvetica 20 bold').place(x=5,y=5)

                



        ocategoryl=Label(self,text="SELECT CATEGORY",font='Cambria 12 italic').place(x=5,y=50)
        oproductl=Label(self,text="SELECT PRODUCT",font='Cambria 12 italic').place(x=5,y=100)
        obrandl=Label(self,text="SELECT BRAND",font='Cambria 12 italic').place(x=5,y=150)
        oquantityl=Label(self,text="QUANTITY",font='Cambria 12 italic').place(x=5,y=200)
        orecipientl=Label(self,text="RECIPIENT",font='Cambria 12 italic').place(x=5,y=250)
        oremarksl=Label(self,text="REMARKS",font='Cambria 12 italic').place(x=5,y=300)
        

        def populateqty(e):
            bra=obrandc.get()
            cat=ocategoryc.get()
            pro=oproductc.get()
            materials1=cur.execute(f"select quantity from stock where category='{cat}' and brand='{bra}' \
                                                and product='{pro}';")
            materials1=materials1.fetchall()
            
            if materials1 != []:
                oquantity.delete('0','end')
                oquantity.insert('0',materials1)
            else:
                oquantity['values']=''
                oquantity.delete('0','end')
                oquantity.insert('0',materials1)
                messagebox.showinfo('alert','no entries found..!!')
            '''
            bra=obrandc.get()
            
##            populate materials''
            materials1=cur.execute(f"select distinct quantity from stock where brand='{bra}';")
            materials1=materials1.fetchall()

            if materials1 != []:
                oquantity.delete('0','end')
                oquantity.insert('0',materials1)
            else:
                oquantity['values']=''
                oquantity.delete('0','end')
                oquantity.insert('0',materials1)
                messagebox.showinfo('alert','no entries found..!!')
                '''

        def populatebrand(e):
            pro=oproductc.get()
            oquantity.delete('0','end')
            '''populate materials'''
            materials1=cur.execute(f"select distinct brand from stock where product='{pro}';")
            materials1=materials1.fetchall()

            if materials1 != []:
                materials1=sum(materials1,())
                obrandc['values']=materials1
                obrandc.current(0)
            else:
                obrandc['values']=''
                obrandc.set('')
                messagebox.showinfo('alert','no entries found..!!')
            

                
        def populateproduct4(e):
            cat=ocategoryc.get()
            
            '''populate materials'''
            materials=cur.execute(f"select distinct product from stock where category='{cat}';")
            materials=materials.fetchall()
            obrandc['values']=''
            obrandc.set('')
            oquantity.delete('0','end')


            if materials != []:
                materials=sum(materials,())
                oproductc['values']=materials
                oproductc.current(0)
            else:
                oproductc['values']=''
                oproductc.set('')
                messagebox.showinfo('alert','no entries found..!!')
                
        def addtotree():
            if ocategoryc.get() =='' or obrandc.get()=='' or \
               oproductc.get()=='' or oquantity.get()=='':
                messagebox.showinfo('alert','all fields are required..!!!!')
            else:
                cat=ocategoryc.get()
                bra=obrandc.get()
                pro=oproductc.get()
                qty=oquantity.get()

                #check if qty is valid input
                try:
                    qty=float(qty)
                    values_from_db=cur.execute(f"select * from stock where category='{cat}' and brand='{bra}' \
                                                and product='{pro}';")
                    values_from_db=values_from_db.fetchall()[0]
 
                    #if given quantity is larger than available
                    if qty > values_from_db[4] or qty < 0 :
                        messagebox.showinfo('alert',f'Invalid Quantity, available : {values_from_db[4]}\
    {values_from_db[5]}')
                    else:
                        #enterd quantity is in stock
                        #1)first check if it is already in tree\
                        #2)if tree does not contain then only add
                        length_of_otree=len(otree.get_children())

                        #tree has no items
                        if length_of_otree == 0:
                            otree.insert('','end',iid=0,
                                         values=(*values_from_db[:4],qty,*values_from_db[5:]))
                            
                        #tree has some items
                        #check if it contains entered item 
                        else:
                            for j in range(length_of_otree):
                                #if item already in tree
                                
                                if values_from_db[0] in otree.item(j,'values'):
                                    messagebox.showinfo('alert','item already added. delete iteme')
                                    break
                            #loop ended
                            else:
                                otree.insert('','end',iid=len(otree.get_children()),
                                             values=(*values_from_db[:4],qty,*values_from_db[5:]))
                                
                                    
                            
                            
                        
                except Exception as e:
                    print(e)
                    #messagebox invalid quantity
                    messagebox.showinfo('alert','invalid quantity')
                    
        def deletefromtree():
            x1=otree.selection()
            for i in range(len(x1)):
                otree.delete(x1[i])

        def confirmtodata():
            if len(otree.get_children())>0:
                orecipient['state']=NORMAL
                oremarks['state']=NORMAL
                
                oaddb['state']=DISABLED
                odelb['state']=DISABLED
                ocategoryc['state']=DISABLED
                oproductc['state']=DISABLED
                obrandc['state']=DISABLED
                oquantity['state']=DISABLED
                osubmitb['state']=NORMAL
                oconfirmb['state']=DISABLED
        def resetdata():
            otree.delete(*otree.get_children())
            
            oaddb['state']=NORMAL
            odelb['state']=NORMAL
            ocategoryc['state']='readonly'
            oproductc['state']='readonly'
            oproductc['values']=''
            oproductc.set('')
            obrandc['state']='readonly'
            obrandc['values']=''
            obrandc.set('')
            oquantity['state']=NORMAL
            oquantity.delete(0,'end')

            orecipient.delete(0,'end')
            oremarks.delete(0,'end')
            orecipient['state']=DISABLED
            oremarks['state']=DISABLED
            osubmitb['state']=DISABLED
            oconfirmb['state']=NORMAL
        def finalsubmit():
            if orecipient.get() == '' or oremarks.get() == '':
                messagebox.showinfo('alert','all fields required...!!!!')
            else:
                #filedialog
                answer=messagebox.askquestion('Confirm',"Are You Sure?")
                if answer=='yes':
                    
                    currentdate=datetime.now()
                    cdateo=currentdate.strftime("%d-%m-%Y")
                    currenttime=datetime.now()
                    ctimeo=currenttime.strftime("%H:%M:%S")
                    fctimeo=currenttime.strftime("%H-%M-%S")
                    filepath=filedialog.asksaveasfilename(initialfile=f'{fctimeo}-{cdateo}',initialdir='D:\\outward',filetypes=[('pdf','*.pdf')])
                    if filepath != '':
                        
                        #creating empty list for storing treeview data and
                        #recipient and remarks to transfer it toward the CLASS
                        #SEND DATA TO '''OUTPDF CLASS'''
                        #===================================================================================
                        outward_data=[filepath]

                        for i in otree.get_children():
                            
                            
                            VALUE=otree.item(i)['values']
                            outward_data.append(VALUE)
                            print('pid',VALUE[0],VALUE[4])
                            '''
                            SUBTRACT FROM STOCK
                            '''
                            x=cur.execute(f"select quantity from stock where pid='{VALUE[0]}';")
                            x=x.fetchone()

                            #if selected quantity is equal to available quantity
                            #then delete that entry from stock
                            #else subtract that quantity from stock
                            if x[0] == float(VALUE[4]):
                                #delete from entry
                                print(f'{x[0]} = {float(VALUE[4])}')
                                cur.execute(f"delete from stock where pid='{VALUE[0]}';")
                            else:
                                #subtract
                                cur.execute(f"update stock set quantity={x[0]-float(VALUE[4])} where pid='{VALUE[0]}';")
                                print(f'{x[0]-float(VALUE[4])},DIFFRENCE')
                            conn.commit()
                            

                        outward_data.append(cdateo)
                        

                        outward_data.append(ctimeo)

                        
                        outward_data.append(orecipient.get())
                        outward_data.append(oremarks.get())
                        
                        #=====SUBTRACT FROM STOCK D.B.===============================================================
                        
                        #=======================================================================================
                        print(outward_data)
                        ob=OutPdf(outward_data)
                    
                #=======================================================================================

                




        ocategoryc=ttk.Combobox(self,width=25,state="readonly")
        ocategoryc['values'] = ['Raw Material','Plumbing Material','Electric Material','Indoor Fittings','Floorings']
        ocategoryc.current(0)
        ocategoryc.place(x=150,y=50)
        ocategoryc.bind("<<ComboboxSelected>>",populateproduct4)
        
        
        oproductc=ttk.Combobox(self,width=25,state="readonly")
        oproductc.place(x=150,y=100)
        oproductc.bind("<<ComboboxSelected>>",populatebrand)

        obrandc=ttk.Combobox(self,width=25,state="readonly")
        obrandc.place(x=150,y=150)
        obrandc.bind("<<ComboboxSelected>>",populateqty)

        oquantity=Entry(self,width=30,bg='lightblue')
        oquantity.place(x=150,y=200)

        #==========prohibit RECIPIENT FOR MORE THAN 25 CHARS
        recipient_text = StringVar()
        orecipient=Entry(self,width=30,bg='lightblue',state=DISABLED,textvariable = recipient_text)
        orecipient.place(x=150,y=250)
        def character_limit(recipient_text):
            if len(recipient_text.get()) > 0:
                recipient_text.set(recipient_text.get()[:25])
        recipient_text.trace("w", lambda *args: character_limit(recipient_text))
        #==========prohibit RECIPIENT FOR MORE THAN 25 CHARS


        #==========prohibit REMARKS FOR MORE THAN 25 CHARS
        remarks_text = StringVar()
        oremarks=Entry(self,width=30,bg='lightblue',state=DISABLED,textvariable = remarks_text)
        oremarks.place(x=150,y=300)
        
        def character_limit(remarks_text):
            if len(remarks_text.get()) > 0:
                remarks_text.set(remarks_text.get()[:35])
        remarks_text.trace("w", lambda *args: character_limit(remarks_text))
        #==========prohibit REMARKS FOR MORE THAN 25 CHARS

        

        oaddb=Button(self,text='Add',font='calibri 12 bold',width=10,command=addtotree)
        oaddb.place(x=5,y=350)
        odelb=Button(self,text='Delete',font='calibri 12 bold',width=10,command=deletefromtree)
        odelb.place(x=105,y=350)
        oconfirmb=Button(self,text='Save',font='calibri 12 bold',width=10,command=confirmtodata)
        oconfirmb.place(x=205,y=350)
        oresetb=Button(self,text='Reset',font='calibri 12 bold',width=10,command=resetdata)
        oresetb.place(x=5,y=400)
        
        osubmitb=Button(self,text='Submit',font='calibri 12 bold',state=DISABLED,width=10,command=finalsubmit)
        osubmitb.place(x=105,y=400)
        

  
    







        #OUTWARD TABLE
        oscroll=Scrollbar(self)  
        otree=ttk.Treeview(self,height=15,column=("id","category","product",'brand',"quantity","unit"),
                               yscrollcommand=oscroll.set)
        otree.place(x=350,y=50)

        
        ttk.Style().map('Treeview',background=[('selected','#00009f')])
        otree.tag_configure('oddrow',background="white")
        otree.tag_configure('evenrow',background="lightblue")
        
        otree.column("#0",minwidth=0,width=0,stretch=NO)

        otree.column("id",minwidth=70,width=70,stretch=NO,)
        otree.column("category",minwidth=90,width=90,stretch=NO,)
        otree.column("product",minwidth=70,width=70,stretch=NO,)
        otree.column("brand",minwidth=100,width=100,stretch=NO,)
        otree.column("quantity",minwidth=50,width=50,stretch=NO,)
        otree.column("unit",minwidth=60,width=60,stretch=NO,)

        
        

        otree.heading("id",text="ID")
        otree.heading("category",text="Category")
        otree.heading("product",text="Product")
        otree.heading("brand",text="Brand")
        otree.heading("quantity",text="Qty")
        otree.heading("unit",text="Unit")

        oscroll.place(x=842,y=50,height=325)
        oscroll.config(command=otree.yview)








        
