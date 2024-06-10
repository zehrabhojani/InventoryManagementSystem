from tkinter import *
from tkinter import ttk,messagebox
from connection import *
#from PIL import Image, ImageTk #pip install pillow
class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Team Avalanche")
        self.root.config(bg="white")
        self.root.focus_force()
        #====================== All Variables ================================
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_invoice_no=StringVar()
        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()
        self.invoice_list=[]
        self.fetch_invoice()


        #=======search frame========
    
        #====== options======
        lbl_invoice=Label(self.root,text="Invoice No",bg="white",font=("times new roman",15)).place(x=670,y=80)
        cmb_search=ttk.Combobox(self.root,text="Invoice no",font=("times new roman",15),textvariable=self.var_invoice_no,values=self.invoice_list)
        cmb_search.place(x=780,y=80)

        
        #====== options======
        
        

        # txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="#f2d2bd").place(x=800,y=80,width=160)
        # btn_search=Button(self.root,text="search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=980,y=79,width=100,height=28)

        #=====title=====
        title=Label(self.root,text="Supplier Details",bg="#0f4d7d",font=("times new roman",20),fg="white").place(x=50,y=10,width=1000,height=40)

        #====content=====
        #======== row 1 ========
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",bg="white",font=("times new roman",15)).place(x=50,y=60)
        lbl_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,bg="#f2d2bd",font=("times new roman",15)).place(x=180,y=60,width=180)

        #========= row 2 ============
        lbl_name=Label(self.root,text="Name",bg="white",font=("times new roman",15)).place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,bg="#f2d2bd",font=("times new roman",15)).place(x=180,y=100,width=180)
       
        #========= row 3 ============
        lbl_contact=Label(self.root,text="Contact",bg="white",font=("times new roman",15)).place(x=50,y=140)
        txt_contact=Entry(self.root,textvariable=self.var_contact,bg="#f2d2bd",font=("times new roman",15)).place(x=180,y=140,width=180)

        #========= row 4 ============
        lbl_desc=Label(self.root,text="Description",bg="white",font=("times new roman",15)).place(x=50,y=180)
        self.txt_desc=Text(self.root,bg="#f2d2bd",font=("times new roman",15))
        self.txt_desc.place(x=180,y=180,width=470,height=90)
        #======buttons==========
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=320,width=110,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=320,width=110,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=320,width=110,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=320,width=110,height=35)

        #=============employee details (tree view)=============
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=670,y=120,width=400,height=350)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice no")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")
       
    

        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=50)
        self.supplierTable.column("name",width=60)
        self.supplierTable.column("contact",width=60)
        self.supplierTable.column("desc",width=60)
        
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#===============================================================================
    def add(self):
        
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror('Error','Invoice must be required ',parent=self.root)
            else:
                db_cursor.execute("Select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                row=db_cursor.fetchone()
                if row!=None:
                    messagebox.showerror('Error','Invoice no. is already exist',parent=self.root)
                else:
                    db_cursor.execute("Insert into supplier (invoice,name,contact,desc) values(%s,%s,%s,%s)",(
                       self.var_sup_invoice.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_desc.get('1.0',END),
                
                    ))
                    db_connection.commit()
                    messagebox.showinfo('Success','Supplier Added Successfully!',parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        
        try:
            db_cursor.execute("select * from supplier")
            rows=db_cursor.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
               self.supplierTable.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.supplierTable.focus()
        content=self.supplierTable.item(f)
        row=content['values']

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3])

    def update(self):
        
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror('Error','Invoice no must be required',parent=self.root)
            else:
                db_cursor.execute("Select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                row=db_cursor.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Invoice no ',parent=self.root)
                else:
                    db_cursor.execute("Update supplier set name=%s,contact=%s,desc=%s, where invoice=%s",(
                        
                        self.var_name.get(),
                        self.var_contact.get(),
                       
                        self.txt_desc.get('1.0',END),
                       
                        self.var_sup_invoice.get(),
                
                    ))
                    db_connection.commit()
                    messagebox.showinfo('Success','supplier Updated Successfully!',parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror('Error','Please enter Invoice no',parent=self.root)
            else:
                db_cursor.execute("Select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                row=db_cursor.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Invoice no',parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete ?",parent=self.root)
                    if op==True:
                        db_cursor.execute("delete from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                        db_connection.commit()
                        messagebox.showinfo('Success','supplier Deleted Successfully!',parent=self.root)
                        self.clear
                        self.show
                        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),
        self.txt_desc.delete('1.0',END),
       
        self.show()

    def search(self):
        
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice no is required", parent=self.root)
            else:
                db_cursor.execute("select * from supplier where invoice=%s",(self.var_searchtxt.get(),))
                rows=db_cursor.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                       self.supplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record Found", parent=self.root)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def fetch_invoice(self):
        
        self.invoice_list.append("Empty")
        
        try:    
            db_cursor.execute("select * from supplier")
            inlist=db_cursor.fetchall()
            print(inlist)
            if len(inlist)>0:
                del self.invoice_list[:]
                self.invoice_list.append("Select")
                for i in inlist:
                    self.invoice_list.append(i[0])
            
                        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)





if __name__=="__main__":
    root = Tk()
    obj=supplierClass(root)
    root.mainloop()