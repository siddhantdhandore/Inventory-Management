import sqlite3
from reportlab.pdfgen import canvas
from reportlab.platypus import Table,Frame,TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
import os
from PIL import Image
from datetime import datetime
from math import ceil
conn=sqlite3.connect('newdatabase.db')
cur=conn.cursor()

class OutPdf:
    def __init__(self,data):
    #==============================================================================================================
        self.data=data
        #INITIALIZE ALL VARIABLES
        self.pdfpath=self.data[0]
        
        #initialize all variables for inserting in DATABASE & PDF
        self.gatePassNumber = 1001
        self.prefix='SA-'
        self.count=1
        self.printed=0
        
        self.list_of_entries=self.data[1:-4]
  
        self.date_outward=self.data[-4]
        self.time_outward=self.data[-3]
        self.numberOfRows=15
        self.recipient=self.data[-2]
        self.remark=self.data[-1]
        s = getSampleStyleSheet()
        self.newStyle = ParagraphStyle('yourtitle',
                                   fontName="Helvetica-Bold",
                                   fontSize=12,
                                   parent=s['Heading2'],
                                   alignment=0,
                                   spaceAfter=14,
                                   textColor='black')
        
        #create pdf file
        self.pdf=canvas.Canvas(f'{self.pdfpath}.pdf')
        
        self.createGP()
        self.pageCreation()
        #TOP PART OF PDF=====================================================================================
        #1a) add header to pdf
        #create header in pdf
##        self.createHeader()

        #1b) add date to pdf
##        self.createDate()
        #============================================================================================

        
        #MIDDLE PART OF PDF==========================================================================
        #1c) add table to pdf
##        self.createTable()
        #============================================================================================
        

        #BOTTOM PART OF PDF==========================================================================
        #1d) add remark to pdf
        self.insertIntoDatabase()
        self.createRemark()
        
        #1e) add remark to pdf
        self.createRecipient()
        #============================================================================================
        
        #save in harddrive
        self.pdf.save()

        #open in window
        os.startfile(f'{self.pdfpath}.pdf','open')



        #2a)
        #Add to database
        #createGP
        
    #=================================================================================================================

  
    #1a)   HEADER FRAME IN PDF===================================================================================
    def createHeader(self):
        flow_obj_header=[]
##        print('i am in createHeader')
        text='''Shree Associates'''
        headerlogo='letterheader.png'
        footerlogo='footerletter.png'
        self.pdf.drawImage(footerlogo,50,0,width=500,height=50)
        self.pdf.drawImage(headerlogo,50,740,width=500,height=80)
        s = getSampleStyleSheet()
        yourStyle = ParagraphStyle('yourtitle',
                                   fontName="Helvetica-Bold",
                                   fontSize=40,
                                   parent=s['Heading2'],
                                   alignment=1,
                                   spaceAfter=14,
                                   textColor='red')
##        p_text=Paragraph(text,style=yourStyle)
##        flow_obj_header.append(p_text)
        headerFrame=Frame(50,50,500,70,showBoundary=0)
        headerFrame.addFromList(flow_obj_header,self.pdf)
        
    #============================================================================================================

    #1b)  DATE FRAME IN PDF=======================================================================
    def createDate(self):
        flow_obj_date=[]
        text=f'Date : {self.date_outward}'
        s=getSampleStyleSheet()

        d_text=Paragraph(text,style=self.newStyle)
        dateFrame=Frame(400,710,200,30,showBoundary=0)
        flow_obj_date.append(d_text)
        dateFrame.addFromList(flow_obj_date,self.pdf)
    #================================================================================
        
    #1c) GATE PASS FRAME IN PDF=====================================================================
    def createGP(self):
        #create UNIQUE GATE PASS
        #gate pass will be prefix+gatePassNumber

        #initialize all variables for inserting in DATABASE & PDF
        

        #if OUTWARD TABLE Is blank create new GATEPASS = prefix+gatePassNumber            =('SA-1001')
        #else increment gatePassNumber by 1 new GATEPASS = prefix+last(gatePassNumber+1)  =('SA-2534')
        x=cur.execute('select * from outward2 order by gatepass DESC LIMIT 1;')
        x=x.fetchall()

        print(x)
        #if OUTWARD IS EMPTY
        if x == []:
            self.gatePass = self.prefix+str(self.gatePassNumber)
##            print('gatepass : ',self.gatePass)
##            print('path : ',self.pdfpath)
##            print('list_of_entries : ',self.list_of_entries)
##            print('recipient : ',self.recipient)
##            print('remark : ',self.remark)
##            print('date_outward : ',self.date_outward)
##            print('time_outward : ',self.time_outward)
        else:
            self.gatePassNumber = int(x[0][2].split('-')[1])
            print('gpt',type(self.gatePassNumber),self.gatePassNumber)
            self.gatePass= self.prefix+str(self.gatePassNumber+1)
            print('gp',self.gatePass)

    def createGPBOX(self):
        flow_obj_gatepass=[]
        text="GATEPASS : " + self.gatePass
        gatepass_text=Paragraph(text,style=self.newStyle)
        flow_obj_gatepass.append(gatepass_text)
        gatepassFrame=Frame(50,690,300,50,showBoundary=0)
        gatepassFrame.addFromList(flow_obj_gatepass,self.pdf)
    def insertIntoDatabase(self):
        for i in range(len(self.list_of_entries)):
            cur.execute(f"insert into outward2 values('{self.date_outward}','{self.time_outward}','{self.gatePass}',\
                            '{self.list_of_entries[i][1]}','{self.list_of_entries[i][2]}','{self.list_of_entries[i][3]}',\
                            '{self.list_of_entries[i][4]}','{self.list_of_entries[i][5]}','{self.recipient}','{self.remark}');")
        conn.commit()
    #==================================================================================================
        
    #======MAIN CONTENT TABLE==========================================================================
    def createTable(self):
        flow_obj_table=[]
        ts=TableStyle([("GRID",(0,0),(-1,-1),2,colors.red),
                       ("BACKGROUND",(0,1),(-1,-1),colors.lightblue),
                       ("BACKGROUND",(0,0),(-1,0),colors.yellow),
                       ("FONTSIZE",(0,0),(-1,-1),12),
                       ("BOTTOMPADDING",(0,0),(-1,-1),10),
                       ('colWidths', (1,0),(-4,-1), 140),
                       ('RIGHTPADDING', (2,2), (2,2), 70),])

        data=[['SR.No','Product','Brand','Quantity','Unit']]


  
        ''''''
        j=0
        for i in range(self.printed,len(self.list_of_entries)):
            print(i)
            try:
                print(self.list_of_entries[i][2])
                
                print(self.list_of_entries[i][3])
            
                print(self.list_of_entries[i][4])
                
                print(self.list_of_entries[i][5])
                
            except:
                print('error')
            
            data.append([self.count,self.list_of_entries[i][2],self.list_of_entries[i][3],
                         self.list_of_entries[i][4],self.list_of_entries[i][5]])
            j+=1
            self.count+=1
            if j == self.numberOfRows:
                break
        self.printed += self.numberOfRows

                
        table=Table(data)
        table.setStyle(ts)
        table._argW[0]=55
        table._argW[1]=150
        table._argW[2]=150
        flow_obj_table.append(table)
        tableFrame=Frame(50,200,500,500,showBoundary=0)
        tableFrame.addFromList(flow_obj_table,self.pdf)
    #=======================================================================================================

    #=======REMARKS FRAME==================================================================================
    def createRemark(self):
        flow_obj_remark=[]
        text="REMARKS : " + self.remark
        remark_text=Paragraph(text,style=self.newStyle)
        flow_obj_remark.append(remark_text)
        remarkFrame=Frame(50,100,300,50,showBoundary=0)
        remarkFrame.addFromList(flow_obj_remark,self.pdf)
    #======================================================================================================

    #=======RECIPIENT FRAME==================================================================================
    def createRecipient(self):
        flow_obj_recipient=[]
        text="Received by : \n" + self.recipient
        recipient_text=Paragraph(text,style=self.newStyle)
        flow_obj_recipient.append(recipient_text)
        recipientFrame=Frame(370,100,300,50,showBoundary=0)
        recipientFrame.addFromList(flow_obj_recipient,self.pdf)
    #======================================================================================================

    def pageCreation(self):
        print('data length',len(self.list_of_entries))
        loop=ceil(len(self.list_of_entries)/self.numberOfRows)
        print('lopp',loop)
        for i in range(loop):
            print('inside pagecreateion')
            self.createHeader()
            self.createDate()
            self.createGPBOX()
            self.createTable()
            if i< loop-1:
                self.pdf.showPage()
        
            
                
            










        
