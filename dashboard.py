from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image,ImageTk
from datetime import datetime
from outward import OutwardFrame
import sqlite3
#=======================DATABASE===================
#*******************************************************
conn =sqlite3.connect('newdatabase.db')
cur = conn.cursor()

conn.commit()
#*******************************************************
#====================END===========================



root = Tk()
root.geometry('970x600')
LABEL_FONT = "Georgia 12 italic"
class DashboardFrame(Frame):
    def __init__(self,root,controller,delete):
        super().__init__()
        self.root=root
        self['width']=970
        self['height']=600
        self['bg']= "#000000"
        
        #=NOTEBOOK CONFIGURATION========================================
        ttk.Style().configure("TNotebook",tabposition="wn",background='gray21')
        ttk.Style().configure("TNotebook.Tab",width=12,font="cambria 12",padding=(5,5,5,5), highlightbackground="#ff0000")
        notebook=ttk.Notebook(self,width=860,height=480)
        notebook.place(x=0,y=110)
        
        
        productFrame=Frame(notebook,bg='WHITE')
        productFrame.pack()
        inwardFrame=Frame(notebook,bg='WHITE')
        inwardFrame.pack()
        outwardFrame=OutwardFrame(notebook)
        outwardFrame.pack()
        '''stockFrame BACKGROUND
        '''
        self.stockbg=Image.open('stockbg.jpg')
        self.stockbg=self.stockbg.resize((970,600))
        self.stockbg=ImageTk.PhotoImage(self.stockbg)
        
        stockFrame=Frame(notebook)
        stockFrame.pack()

        stockbglabel=Label(stockFrame,image=self.stockbg).place(x=0,y=0)
        notebook.add(outwardFrame,text='OUTWARD')
        notebook.add(stockFrame,text='STOCK')

        notebook.add(inwardFrame,text='INWARD')

        notebook.add(productFrame,text='PRODUCT')
        
        #=*************************************************************

        #=====notebok frame 1========
        #=1)treeview for displaying products
        #=2)scrollbar for treeview
        #=4)entries and buttons for inserting data into products
        scroll=Scrollbar(productFrame)
        
     
        tree=ttk.Treeview(productFrame,column=('pid','cat','prod','brand','unit'),yscrollcommand=scroll.set)
        tree.column('#0',width=0,minwidth=0,stretch=YES)
        
        tree.column('pid',width=50,minwidth=50,stretch=NO)
        tree.column('cat',width=100,minwidth=100,stretch=NO)
        tree.column('prod',width=100,minwidth=100,stretch=NO)
        tree.column('brand',width=100,minwidth=100,stretch=NO)
        tree.column('unit',width=70,minwidth=70,stretch=NO)
  


        tree.heading('pid',text='ID',anchor=W)
        tree.heading('cat',text='CATEGORY',anchor=W)
        tree.heading('prod',text='PRODUCT',anchor=W)
        tree.heading('brand',text='BRAND',anchor=W)
        tree.heading('unit',text='UNIT',anchor=W)

        scroll.config(command=tree.yview)
        scroll.place(x=719,y=50,height=227)
        tree.place(x=295,y=50)
        
        #=TREE EVENT
        #=WHEN CLICKED ON AN ITEM
        #=ITEM IS SELECTED ON ENTRYIES AND COMBO AND EDIT BUTTON IS ENABLED
        def showItems(e):
            itemid=tree.focus()
            
            values = tree.item(itemid,'values')
            
            pnamee.delete('0','end')
            pnamee.insert('0',values[2])

            pbrande.delete('0','end')
            pbrande.insert('0',values[3])

            pcategoryc.set(values[1])

            punitc.set(values[4])
            
            #edit button is enabled
            peditb['state'] = NORMAL
            pdeleteb['state'] = NORMAL
            
        tree.bind('<ButtonRelease>',showItems)
         
        
            
        #*******************************
        
        #==PRODUCT OPERATIONS==
        #=contains labels, entries, comboboxes 
        
        #LABELS
        productHeading = Label(productFrame,text = "Product Operations",font="Times 18 bold").place(x=0,y=50)
        
        pnamel= Label(productFrame,text="Product : ",font = LABEL_FONT).place(x=0,y=90)
        pbrandl= Label(productFrame,text="Brand : ",font = LABEL_FONT).place(x=0,y=130)
        pcategoryl= Label(productFrame,text="Category : ",font = LABEL_FONT).place(x=0,y=170)
        punitl= Label(productFrame,text="Unit : ",font = LABEL_FONT).place(x=0,y=210)
        #Entries and comboboxes
        pnamee = Entry(productFrame,width=19,bg="yellow",font='Georgia 10')
        pnamee.place(x=100,y=90)
        pnamee.focus()
        pbrande = Entry(productFrame,width=19,bg="yellow",font='Georgia 10')
        pbrande.place(x=100,y=130)
        
 
        pcategoryc=ttk.Combobox(productFrame,width=25,state="readonly")
        pcategoryc['values'] = ['Raw Material','Plumbing Material','Electric Material','Indoor Fittings','Floorings']
        pcategoryc.current(0)
        pcategoryc.place(x=100,y=170)
        
        
        punitc = ttk.Combobox(productFrame,width=25,state = "readonly")
        punitc['values'] = ['Ton','Brass','KG','No.s','Ltr','Mtr','Bag']
        punitc.current(0)
        punitc.place(x=100,y=210)

        def addb():
            if pnamee.get() == '' or pbrande.get()== '':
                messagebox.showinfo('alert','enter all fields')
            else:
                pcategory=pcategoryc.get()
                pname=pnamee.get()
                pbrand=pbrande.get()
                punit=punitc.get()
                vls=cur.execute(f"select * from deletedproducts where product = '{pcategory}';")
                vls=vls.fetchall()
                print(vls)
                if vls == []:
                    #if deleteproducts is empty then creates new id
                    x=cur.execute(f"select * from products where category='{pcategory}' order by pid desc LIMIT 1;")
                    first_row=x.fetchall()
                    if first_row == []:
                        print('products is also empty')
                        pid = pcategory[:2]+'A'+'101'
                        cur.execute(f"insert into products values(?,?,?,?,?);",(pid,pcategory,pname,pbrand,punit))
                        conn.commit()
                        tree.insert('','end',values=(pid,pcategory,pname,pbrand,punit))
                    else:
                        first_row=first_row[0]
                        print('products hace some products from that category')
                        # name collision category has same first 2 letters
                        # and this is first time for that category to enter in database
                       
                        if pcategory != first_row[1] and pcategory[:2] == first_row[1][:2]:
                            #NAME COLLISION
                            difference_code = chr(ord(first_row[0][2])+1)
                            pid = pcategory[:2]+difference_code+'101'
                            cur.execute(f"insert into products values(?,?,?,?,?);",(pid,pcategory,pname,pbrand,punit))
                            
                        else:
                            try:
                            #no name collision
                                pid = pcategory[:2] + first_row[0][2] + str(int(first_row[0][-3:])+1)
                                cur.execute(f"insert into products values(?,?,?,?,?)",(pid,pcategory,pname,pbrand,punit))
                                tree.insert('','end',values=(pid,pcategory,pname,pbrand,punit))
                            except:
                                messagebox.showinfo('Alert','product already exists')
                else:
                    #if deletedproducts contains id then assigns that id
                    print('hello')
                    pid = vls[0][0]
                    print(pid)
                    cur.execute(f"delete from deletedproducts where pid= '{pid}';")
                    cur.execute(f"insert into products values(?,?,?,?,?);",(pid,pcategory,pname,pbrand,punit))
                    tree.insert('','end',values=(pid,pcategory,pname,pbrand,punit))
                conn.commit()
                
        def editvalues(itemid,name,brand,unit):
            new_name = pnamee2.get().strip()
            new_brand = pbrande2.get().strip()
            new_unit = punitc2.get().strip()

            #check if any changes are done:
            if (name == new_name) and(brand == new_brand )and(new_unit == unit):
                messagebox.showinfo('alert','you havent done any changes')
            else:
                #update the database and reflect it in tree
                new_vals=(new_name,new_brand,new_unit,itemid)
                try:
                    cur.execute("update products set product=?,brand=?,unit = ? where pid=?;",new_vals)
                except Exception as e:
                    e=str(e)
                    messagebox.showinfo(e,'already exists in database')
                #update tree
                tree.item(tree.focus(),values=(itemid,pcategoryc.get(),new_name,new_brand,new_unit))
                conn.commit()
        def editb():
            global pnamee2,pbrande2,punitc2
            itemid=tree.item(tree.focus(),'values')[0]
            name=tree.item(tree.focus(),'values')[2]
            brand=tree.item(tree.focus(),'values')[3]
            unit=tree.item(tree.focus(),'values')[4]
            
            #opens new window
            
            topedit=Toplevel(productFrame,width=300,height=250,bg="pink")
            topedit.resizable(False,False)
            
            #VERY IMPORTANT
            topedit.grab_set() #only interact with toplevel VERY IMPORTANT
            #self.root.withdraw() can also use this and self.root.deiconify()
            #VERY IMPORTANT
            
            #======WIDGETS IN NEW WINDOW=============================================================================
            header2 = Label(topedit,text = "EDIT PRODUCTS",width=15,font='Times 20 bold',
                           fg="red",anchor=W,bd=5,relief='solid').place(x=0,y=0)
            
            pnamel2= Label(topedit,text="Product : ",font = LABEL_FONT).place(x=5,y=60)
            pbrandl2= Label(topedit,text="Brand : ",font = LABEL_FONT).place(x=5,y=100)
            punitl2= Label(topedit,text="Unit : ",font = LABEL_FONT).place(x=5,y=140)
            
            pnamee2 = Entry(topedit,width=19,bg="yellow",font='Georgia 10')
            pnamee2.place(x=100,y=60)
            pnamee2.insert(0,name)
            pnamee2.focus()
            
            
            pbrande2 = Entry(topedit,width=19,bg="yellow",font='Georgia 10')
            pbrande2.insert(0,brand)
            pbrande2.place(x=100,y=100)
            
            
            punitc2 = ttk.Combobox(topedit,width=25,state = "readonly")
            punitc2['values'] = ['Ton','Brass','KG','No.s','Ltr','Mtr','Bag']
            punitc2.set(unit)
            punitc2.place(x=100,y=140)

            #this button will update database
            editvaluesb = Button(topedit,width=10,text = 'SUBMIT',command = lambda:editvalues(itemid,name,brand,unit))
            editvaluesb.place(x=100,y=180)

            
            
            
            #====**************************************************************************************
            
        def deleteb():
            x=tree.selection()
            ids=[]
            category= []
            for i in range(len(x)):
                ids.append(tree.item(x[i],'values')[0])
                category.append(tree.item(x[i],'values')[1])
                tree.delete(x[i])
                cur.execute(f"insert into deletedproducts values(?,?);",(ids[-1],category[-1]))
            old=cur.execute("select * from products;")
            cur.execute(f"delete from products where pid in (?)",ids)
            new= cur.execute("select * from products;")
            print("old",old,"new",new)
            conn.commit()
                
            
        
        # fetches data from database 
        # upon start for treeview
        value_for_tree=cur.execute("select * from products;")
        value_for_tree=value_for_tree.fetchall()
    
        for i in range(len(value_for_tree)):
            tree.insert('','end',iid=i,values=value_for_tree[i])
        tree.selection_set('0')
          

        #buttons
        paddb = Button(productFrame,text="Add",bg="red",font=LABEL_FONT,command=addb)
        paddb.place(x=20,y=250)

        
        peditb = Button(productFrame,text="Edit",bg="red",font=LABEL_FONT,state=DISABLED,command=editb)
        peditb.place(x=70,y=250)
        
        pdeleteb = Button(productFrame,text="Delete",bg="red",font=LABEL_FONT,state=DISABLED,command=deleteb)
        pdeleteb.place(x=120,y=250)

        #======INWARD FRAME===============================================================================================
        #BUTTON DEFINITIONS=================================================================================
        def sendtodb(mdt,mt):
            x=cur.execute('select * from inward order by date desc limit 1;')
            x=x.fetchall()
            product=productc.get()
            brand=brandc.get()
            quantity=float(quantitye.get())
            vendor=vendore.get()
            dc=dce.get()
            remarks=remarkse.get()
            category=categoryselect.get()
            unit=unitc.get()
            

            if x==[]:
                try:
                    pid=cur.execute(f"select pid from products where category='{category}' and\
                            product='{product}' and brand='{brand}' and unit='{unit}';")
                    pid=pid.fetchall()[0][0]
                    cur.execute(f"insert into inward values('{mdt}','{mt}','{dc}','{category}',\
                            '{product}','{brand}',{quantity},'{unit}',\
                            '{vendor}','{remarks}');")
                    val=cur.execute(f"select quantity from stock where pid='{pid}';")
                    val=val.fetchall()
                    if val == []:
                        cur.execute(f"insert into stock values('{pid}','{category}',\
                        '{product}','{brand}','{quantity}','{unit}');")
                    else:
                        qty=val[0][0]
                        qty+=quantity
                        cur.execute(f"update stock set quantity={qty} where pid='{pid}';")

                    conn.commit()
                    if len(inwardtree.get_children()) %2 == 0:
                        inwardtree.insert('','end',values=(mdt,mt,dc,category,product,\
                                                       brand,quantity,unit,vendor,remarks),tags=('evenrow',))
                    else:
                        inwardtree.insert('','end',values=(mdt,mt,dc,category,product,\
                                                       brand,quantity,unit,vendor,remarks),tags=('oddrow',))
                    
                    messagebox.showinfo('succes','inserted successfully')
                    
                except:
                    messagebox.showinfo('warning','duplicate D.C. or vendor')
                        
            else:
                prevdate=x[0][0]
                prevtime=x[0][1]
                
                prevdate=datetime.strptime(prevdate,'%d-%m-%Y')
                
                prevtime=datetime.strptime(prevtime,'%H:%M:%S')

                if datetime.strptime(mdt,'%d-%m-%Y') >= prevdate :
                    try:
                        pid=cur.execute(f"select pid from products where category='{category}' and\
                                product='{product}' and brand='{brand}' and unit='{unit}';")
                        pid=pid.fetchall()[0][0]
                        cur.execute(f"insert into inward values('{mdt}','{mt}','{dc}','{category}',\
                                '{product}','{brand}',{quantity},'{unit}',\
                                '{vendor}','{remarks}');")
                        val=cur.execute(f"select quantity from stock where pid='{pid}';")
                        val=val.fetchall()
                        if val == []:
                            cur.execute(f"insert into stock values('{pid}','{category}',\
                            '{product}','{brand}','{quantity}','{unit}');")
                        else:
                            qty=val[0][0]
                            qty+=quantity
                            cur.execute(f"update stock set quantity={qty} where pid='{pid}';")


                        
                        conn.commit()                        
                        if len(inwardtree.get_children()) %2 == 0:
                            inwardtree.insert('','end',values=(mdt,mt,dc,category,product,\
                                                           brand,quantity,unit,vendor,remarks),tags=('evenrow',))
                        else:
                            inwardtree.insert('','end',values=(mdt,mt,dc,category,product,\
                                                           brand,quantity,unit,vendor,remarks),tags=('oddrow',))
                        messagebox.showinfo('succes','inserted successfully')
                        newWindow.destroy()
                    except:
                        messagebox.showinfo('warning','duplicate D.C. or vendor')
                        
                else:
                    messagebox.showinfo('warning','backdated entries not allowed...!!!')
        def cancelwindow():
            newWindow.destroy()
       
            
        def submittodb():
            currentdate=datetime.now()
            cdate=currentdate.strftime("%d-%m-%Y")
            currenttime=datetime.now()
            ctime=currenttime.strftime("%H:%M:%S")
            global newWindow
            
            if productc.get() == '' or brandc.get() == '' or quantitye.get()=='' or vendore.get()==''\
                    or dce.get()=='' or remarkse.get() == '':
                messagebox.showinfo('alert','required all fields..!!')
            else:
                try:
                    qt=float(quantitye.get())
                    if qt > 0:
    
                        newWindow=Toplevel(inwardFrame)
                        newWindow.title('CONFIRM INWARD DATA')
                        newWindow.geometry('400x400')
                        newWindow.resizable(False,False)
                        newWindow['bg']='white'
                        newWindow.grab_set()
                        
                        pcl=Label(newWindow,text='CATEGORY',width=12,anchor=W,font=LABEL_FONT,bg='khaki').place(x=5,y=5)
                        pul=Label(newWindow,text='UNIT',width=12,font=LABEL_FONT,anchor=W,bg='khaki').place(x=5,y=40)
                        pql=Label(newWindow,text='QUANTITY',width=12,font=LABEL_FONT,anchor=W,bg='khaki').place(x=5,y=75)
                        pvl=Label(newWindow,text='VENDOR',width=12,font=LABEL_FONT,anchor=W,bg='khaki').place(x=5,y=110)
                        pml=Label(newWindow,text='MATERIAL',width=12,font=LABEL_FONT,anchor=W,bg='khaki').place(x=5,y=145)
                        pbl=Label(newWindow,text='BRAND',width=12,font=LABEL_FONT,anchor=W,bg='khaki').place(x=5,y=180)
                        pdcl=Label(newWindow,text='D.C.',width=12,font=LABEL_FONT,anchor=W,bg='khaki').place(x=5,y=215)
                        prl=Label(newWindow,text='REMARKS',width=12,font=LABEL_FONT,anchor=W,bg='khaki').place(x=5,y=250)

                        gpcl=Label(newWindow,text=categoryselect.get(),width=25,
                                   anchor=W,font=LABEL_FONT,bg='salmon',fg='white').place(x=140,y=5)
                        gpul=Label(newWindow,text=unitc.get(),width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=40)
                        gpql=Label(newWindow,text=quantitye.get(),width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=75)
                        gpvl=Label(newWindow,text=vendore.get(),width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=110)
                        gpml=Label(newWindow,text=productc.get(),width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=145)
                        gpbl=Label(newWindow,text=brandc.get(),width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=180)
                        gpdcl=Label(newWindow,text=dce.get(),width=25,
                                    font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=215)
                        gprl=Label(newWindow,text=remarkse.get(),width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=250)
                        



                                        
                        gdate=Label(newWindow,text=cdate,width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=5,y=290)
                        gtime=Label(newWindow,text=ctime,width=25,
                                   font=LABEL_FONT,anchor=W,bg='salmon',fg='white').place(x=140,y=290)

                        #button images
                        self.imgconfirm=Image.open('button_confirm.png')
                        self.imgconfirm=self.imgconfirm.resize((80,40))
                        self.imgconfirm=ImageTk.PhotoImage(self.imgconfirm)
                        self.imgcancel=Image.open('button_cancel.png')
                        self.imgcancel=self.imgcancel.resize((80,40))
                        self.imgcancel=ImageTk.PhotoImage(self.imgcancel)
                        #button images
                        
                        confirmbutton=Button(newWindow,image=self.imgconfirm,border=0,font=LABEL_FONT,
                                             command=lambda:sendtodb(cdate,ctime)).place(x=80,y=320)

                        cancelbutton=Button(newWindow,image=self.imgcancel,border=0,
                                            font=LABEL_FONT,command=cancelwindow).place(x=200,y=320)
                    else:
                        messagebox.showinfo('alert','invalid quantity')
                except:
                    messagebox.showinfo('alert','quantity in digit')
            
                    
                    
        def resetfields():
            productc.delete(0,'end')
            brandc.delete(0,'end')
            quantitye.delete('0','end')
            vendore.delete('0','end')
            dce.delete('0','end')
            remarkse.delete('0','end')

            
        def populateproduct(e):
            cat=categoryselect.get()
            
            '''populate materials'''
            materials=cur.execute(f"select distinct product from products where category='{cat}';")
            materials=materials.fetchall()
            if materials != []:
                materials=sum(materials,())
                productc['values']=materials
                productc.current(0)
            else:
                productc['values']=''
                productc.set('')
                messagebox.showinfo('alert','no entries found..!!')
                
        def populatebrand(e):
            pro=productc.get()
            
            '''populate materials'''
            materials=cur.execute(f"select distinct brand from products where product='{pro}';")
            materials=materials.fetchall()

            materials2=cur.execute(f"select distinct unit from products where product='{pro}';")
            materials2=materials2.fetchall()
            if materials != []:
                materials=sum(materials,())
                brandc['values']=materials
                brandc.current(0)
            else:
                brandc['values']=''
                brandc.set('')
                messagebox.showinfo('alert','no entries found..!!')
            if materials2 !=[]:
                materials2=sum(materials2,())
                unitc['values']=materials2
                unitc.current(0)
        
        #getting data from database when selected category
        #-====END BUTTON DEFINITIONS==========================================================================================
            
        inwardscroll=Scrollbar(inwardFrame)
        inwardtree=ttk.Treeview(inwardFrame,column=("date","time","dc","category","product",'brand',"quantity",'unit',
                                                    "vendor","remarks"),
                                yscrollcommand=inwardscroll.set)

        inwardtree.column('#0',width=0,minwidth=0,stretch=YES)
        inwardtree.column('date',width=70,minwidth=70,stretch=NO,anchor=CENTER)
        inwardtree.column('time',width=70,minwidth=70,stretch=NO,anchor=CENTER)
        inwardtree.column('dc',width=80,minwidth=80,stretch=NO,anchor=CENTER)
        inwardtree.column('category',width=100,minwidth=100,stretch=NO,anchor=CENTER)
        inwardtree.column('product',width=100,minwidth=100,stretch=NO,anchor=CENTER)
        inwardtree.column('brand',width=100,minwidth=70,stretch=NO,anchor=CENTER)
        inwardtree.column('quantity',width=70,minwidth=70,stretch=NO,anchor=CENTER)
        inwardtree.column('unit',width=50,minwidth=100,stretch=NO,anchor=CENTER)
        inwardtree.column('vendor',width=100,minwidth=100,stretch=NO,anchor=CENTER)
        inwardtree.column('remarks',width=100,minwidth=70,stretch=NO)
        
        inwardtree.heading('date',text='Date')
        inwardtree.heading('time',text='Time')
        inwardtree.heading('dc',text='D.C.')
        inwardtree.heading('category',text='Category')
        inwardtree.heading('product',text='Product')
        inwardtree.heading('brand',text='Brand')
        inwardtree.heading('quantity',text='Quantity')
        inwardtree.heading('unit',text='Unit')
        inwardtree.heading('vendor',text='Vendor')
        inwardtree.heading('remarks',text='Remarks')
        
        inwardtree.place(x=0,y=0)
        inwardscroll.place(x=842,y=0,height=227)
        inwardscroll.config(command=inwardtree.yview)
        ttk.Style().map('Treeview',background=[('selected','#00009f')])
        inwardtree.tag_configure('oddrow',background="white")
        inwardtree.tag_configure('evenrow',background="lightblue")
        
        categorylabel=Label(inwardFrame,text='SELECT CATEOGRY',font=LABEL_FONT).place(x=10,y=240)
        
        #$$$$$$$$$$$$   $$
        categoryselect=ttk.Combobox(inwardFrame,width=25,state="readonly")
        categoryselect['values']=['Raw Material','Plumbing Material','Electric Material','Indoor Fittings','Floorings']
        categoryselect.current(0)
        categoryselect.place(x=10,y=270)
        categoryselect.bind("<<ComboboxSelected>>",populateproduct)
        
        
        productlabel=Label(inwardFrame,text='MATERIAL NAME',font=LABEL_FONT).place(x=10,y=320)
        productc=ttk.Combobox(inwardFrame,width=30,state='readonly')
        productc.bind("<<ComboboxSelected>>",populatebrand)
        productc.place(x=10,y=350)

        brandc=ttk.Combobox(inwardFrame,width=20,state='readonly')
        brandc.place(x=230,y=350)
        #$$$$$$$$$$$$$$$

        '''delete
        producte=Entry(inwardFrame,width=30,bg='yellow')
        producte.focus()
        producte.place(x=10,y=350)'''

        unitlabel=Label(inwardFrame,text='UNIT',font=LABEL_FONT).place(x=230,y=240)
        unitc = ttk.Combobox(inwardFrame,width=20,state = "readonly")
        unitc['values'] = ['Ton','Brass','KG','No.s','Ltr','Mtr','Bag']
        unitc.current(0)
        unitc.place(x=230,y=270)

        
        brandlabel=Label(inwardFrame,text='BRAND',font=LABEL_FONT).place(x=230,y=320)
        '''delete
        brande=Entry(inwardFrame,width=24,bg='yellow')
        brande.place(x=230,y=350)'''

        quantitylabel=Label(inwardFrame,text='QUANTITY',font=LABEL_FONT).place(x=400,y=240)
        quantitye=Entry(inwardFrame,width=30,bg='lightblue')
        quantitye.place(x=400,y=270)

        vendorlabel=Label(inwardFrame,text='VENDOR',font=LABEL_FONT).place(x=600,y=240)
        vendore=Entry(inwardFrame,width=30,bg='lightblue')
        vendore.place(x=600,y=270)

        dclabel=Label(inwardFrame,text='DELIVERY CHALLAN',font=LABEL_FONT).place(x=400,y=320)
        dce=Entry(inwardFrame,width=30,bg='lightblue')
        dce.place(x=400,y=350)

        remarkslabel=Label(inwardFrame,text='REMARKS',font=LABEL_FONT).place(x=600,y=320)
        remarkse=Entry(inwardFrame,width=30,bg='lightblue')
        remarkse.place(x=600,y=350)

        #button images
        self.imgsubmit=Image.open('button_submit.png')
        self.imgsubmit=self.imgsubmit.resize((80,40))
        self.imgsubmit=ImageTk.PhotoImage(self.imgsubmit)
        self.imgreset=Image.open('button_reset.png')
        self.imgreset=self.imgreset.resize((80,40))
        self.imgreset=ImageTk.PhotoImage(self.imgreset)
        #button images
        submitdata=Button(inwardFrame,image=self.imgsubmit,font=LABEL_FONT,border=0,fg='white',command=submittodb)
        submitdata.place(x=250,y=400)

        resetdata=Button(inwardFrame,image=self.imgreset,border=0,fg='white',command=resetfields)
        resetdata.place(x=400,y=400)
        
        # fetches data from database 
        # upon start for inwardtreeview
        cdate=datetime.now()
        cdate=cdate.strftime('%d-%m-%Y')

        value_for_inwardtree=cur.execute(f"select * from inward where date='{cdate}';")
        value_for_inwardtree=value_for_inwardtree.fetchall()

        
        for i in range(len(value_for_inwardtree)):
            if i%2 == 0:
                inwardtree.insert('','end',iid=i,values=value_for_inwardtree[i],tags=('evenrow',))
            else:
                inwardtree.insert('','end',iid=i,values=value_for_inwardtree[i],tags=('oddrow',))
                

        conn.commit()

          
        #*************END INWARD FRAME**************************************************88
        #==========STOCK FRAME======================================================================================
        def populateproduct2(e):
            cat=scategoryc.get()
            
            '''populate materials'''
            materials=cur.execute(f"select distinct product from inward where category='{cat}';")
            materials=materials.fetchall()
            if materials != []:
                materials=sum(materials,())
                sproductc['values']=materials
                sproductc.current(0)
            else:
                sproductc['values']=''
                sproductc.set('')
                messagebox.showinfo('alert','no entries found..!!')
                
        def showstock():
            savaile.delete(0,'end')
            product=sproductc.get()
            total=0;
            if product == "":
                messagebox.showinfo('alert','no entries found..!!')
            else:
                values_for_stree=cur.execute(f"select * from stock where product='{product}';")
                values_for_stree=values_for_stree.fetchall()
                if values_for_stree == []:
                    messagebox.showinfo('alert','no entries found..!!')
                else:
                    if stree.get_children() != ():
                        for j in range(len(stree.get_children())):
                            stree.delete(j)
                    for i in range(len(values_for_stree)):
                        if i%2 == 0:
                            stree.insert('','end',iid=i,values=values_for_stree[i],tags=('evenrow',))
                        else:
                            stree.insert('','end',iid=i,values=values_for_stree[i],tags=('oddrow',))
                        total+=values_for_stree[i][4]
                    savaile.insert(0,str(total)+" "+values_for_stree[0][5])
                    
                    
                    

                
        sheading=Label(stockFrame,font='helvetica 30 bold',text='Available Stock').place(x=5,y=5)

        scategoryl=Label(stockFrame,text='Select Category',font=LABEL_FONT,bg='#f14a7a',width=20,anchor=W).place(x=5,y=60)
        sproductl=Label(stockFrame,text='Select Product',font=LABEL_FONT,bg='#f583a4',width=20,anchor=W).place(x=250,y=60)
        sbrandl=Label(stockFrame,text='Select Brand',font=LABEL_FONT,bg='#f8a5bd',width=20,anchor=W).place(x=500,y=60)

        scategoryc=ttk.Combobox(stockFrame,width=30,state="readonly")
        scategoryc.place(x=5,y=100)
        sproductc=ttk.Combobox(stockFrame,width=30,state="readonly")
        sproductc.place(x=250,y=100)
        sbrandc=ttk.Combobox(stockFrame,width=30,state="readonly").place(x=500,y=100)

        scategoryc['values'] = ['Raw Material','Plumbing Material','Electric Material','Indoor Fittings','Floorings']
        scategoryc.current(0)
        scategoryc.bind("<<ComboboxSelected>>",populateproduct2)

        #button images
        self.imgshowstock=Image.open('button_show-stock.png')
        self.imgshowstock=self.imgshowstock.resize((100,45))
        self.imgshowstock=ImageTk.PhotoImage(self.imgshowstock)

        #button images
        
        sshowstockb=Button(stockFrame,image=self.imgshowstock,border=0,command=showstock)
        sshowstockb.place(x=730,y=80)
        stree=ttk.Treeview(stockFrame,column=("id","category","product","brand","quantity","unit"))
        stree.place(x=5,y=150)
        
        ttk.Style().map('Treeview',background=[('selected','#00009f')])
        stree.tag_configure('oddrow',background="white")
        stree.tag_configure('evenrow',background="lightblue")
        
        stree.column("#0",minwidth=0,width=0)
        stree.column("id",minwidth=120,width=120)
        stree.column("category",minwidth=120,width=120)
        stree.column("product",minwidth=120,width=120)
        stree.column("brand",minwidth=120,width=120)
        stree.column("quantity",minwidth=120,width=120)
        stree.column("unit",minwidth=120,width=120)
        
        stree.heading("id",text="ID")
        stree.heading("category",text="Category")
        stree.heading("product",text="Product")
        stree.heading("brand",text="Brand")
        stree.heading("quantity",text="Quantity")
        stree.heading("unit",text="Unit")

        savaill=Label(stockFrame,text='AVAILABLE QUANTITY : ',font=LABEL_FONT).place(x=5,y=400)
        savaile=Entry(stockFrame,state='normal',width=20)
        savaile.place(x=210,y=400)
    
        
        
        #**************END STOCK FRAME******************************************************************************
    
        
ob=DashboardFrame(root,'temp','temp')
ob.place(x=0,y=0)
root.mainloop()
conn.close()
