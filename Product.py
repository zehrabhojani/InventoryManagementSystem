from tkinter import *
from tkinter import ttk,messagebox
from connection import *
#from PIL import Image, ImageTk #pip install pillow
class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Team Avalanche")
        self.root.config(bg="white")
        self.root.focus_force()
        
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        
        self.var_category=StringVar()
        self.var_supplier=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        
        
        self.var_product=StringVar()
        self.var_price=StringVar()
        self.var_quantity=StringVar()
        self.var_product_id=StringVar()
        
        
        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)
        
        title=Label(product_Frame,text="Manage Product Details",bg="#0f4d7d",font=("times new roman",18),fg="white").pack(side=TOP,fill=X)
        
        lbl_category=Label(product_Frame,text="Category",bg="white",font=("times new roman",18)).place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",bg="white",font=("times new roman",18)).place(x=30,y=110)
        lbl_product=Label(product_Frame,text="Name",bg="white",font=("times new roman",18)).place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",bg="white",font=("times new roman",18)).place(x=30,y=210)
        lbl_quantity=Label(product_Frame,text="Quantity",bg="white",font=("times new roman",18)).place(x=30,y=260)
        lbl_product_id=Label(product_Frame,text="Product ID",bg="white",font=("times new roman",18)).place(x=30,y=310)
        
        
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_category,values=self.cat_list,state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)
        
        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_supplier,values=self.sup_list,state='readonly',justify=CENTER,font=("times new roman",15))
        # cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_supplier,values=","Vipul1"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)
        
        txt_name=Entry(product_Frame,textvariable=self.var_product,font=("times new roman",15),bg='lightyellow').place(x=150,y=160,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("times new roman",15),bg='lightyellow').place(x=150,y=210,width=200)
        txt_quantity=Entry(product_Frame,textvariable=self.var_quantity,font=("times new roman",15),bg='lightyellow').place(x=150,y=260,width=200)
        
        cmb_status=Entry(product_Frame,textvariable=self.var_product_id,justify=CENTER,font=("times new roman",15))
        cmb_status.place(x=150,y=310,width=200)
        
        
        btn_add=Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)


        #=======search frame========
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)
        #====== options======
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","category","Supplier","Name"),state='readonly',justify=CENTER,font=("times new roman",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="#f2d2bd").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        ##Product details

        p_Frame=Frame(self.root,bd=3,relief=RIDGE)
        p_Frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(p_Frame,orient=VERTICAL)
        scrollx=Scrollbar(p_Frame,orient=HORIZONTAL)
         #"Insert into item_master (id,product_id,name_of_product,Category,Supplier,price,total_qty)


        self.productTable=ttk.Treeview(p_Frame,columns=("id","product_id","name_of_product","price","total_qty","Category","Supplier"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("id",text="ID")
        self.productTable.heading("product_id",text="Product ID")
        self.productTable.heading("Category",text="Category")
        self.productTable.heading("total_qty",text="Quantity")
        self.productTable.heading("name_of_product",text="name")
        self.productTable.heading("price",text="price")
        self.productTable.heading("Supplier",text="Supplier")
        

        self.productTable["show"]="headings"

        self.productTable.column("id",width=90)
        self.productTable.column("product_id",width=90)
        self.productTable.column("Category",width=100)
        self.productTable.column("Supplier",width=100)
        self.productTable.column("name_of_product",width=100)
        self.productTable.column("price",width=100)
        self.productTable.column("total_qty",width=100)
        
    
        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()



    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        
        
        try:    
            db_cursor.execute("Select name from category")
            cat=db_cursor.fetchall()
            print(cat)
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            db_cursor.execute("Select name from supplier")
            sup=db_cursor.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
                        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def add(self):
        
        try:
            if self.var_category.get()=="Select" or self.var_category.get()=="Empty" or self.var_supplier.get()=="Select"  or self.var_product.get()=="":
                messagebox.showerror('Error','All feilds are required',parent=self.root)
            else:
                db_cursor.execute("Select * from item_master where name_of_product = %s",(self.var_product.get(),))
                row=db_cursor.fetchone()
                if row!=None:
                    messagebox.showerror('Error','Product already exist',parent=self.root)
                else:
                    db_cursor.execute("INSERT INTO item_master (Category, Supplier, name_of_product, price, total_qty, product_id) VALUES (%s, %s, %s, %s, %s, %s)", (
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_product.get(),
                            self.var_price.get(),
                            self.var_quantity.get(),
                            self.var_product_id.get(),
                        ))
                    db_connection.commit()
                    messagebox.showinfo('Success','Record Inserted Successfully!',parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        
        try:
            db_cursor.execute("select * from item_master")
            rows=db_cursor.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        # self.var_pid.set(row[0]),
        self.var_category.set(row[5]),
        self.var_supplier.set(row[6]),
        self.var_product.set(row[2]),
        self.var_price.set(row[3]),
        self.var_quantity.set(row[4]),
        self.var_product_id.set(row[1]),

        

    def update(self):
        
        try:
            if self.var_product_id.get()=="":
                messagebox.showerror('Error','Please select Product from list',parent=self.root)
            else:
                db_cursor.execute("Select * from item_master where product_id=%s",(self.var_product_id.get(),))
                row=db_cursor.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid Product Id',parent=self.root)
                else:
                     #"Insert into item_master (id,product_id,name_of_product,Category,Supplier,price,total_qty)

                    db_cursor.execute("Update item_master set Category=%s,Supplier=%s,name_of_product=%s,price=%s,total_qty=%s where product_id=%s",(
                        
                        self.var_category.get(),
                        self.var_supplier.get(),
                        self.var_product.get(),
                        self.var_price.get(),
                        self.var_quantity.get(),
                        self.var_product_id.get(),
                        # self.var_pid.get()
                
                    ))
                    db_connection.commit()
                    messagebox.showinfo('Success','Product Updated Successfully!',parent=self.root)
                    self.show()
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        
        try:
            if self.var_product_id.get()=="":
                messagebox.showerror('Error','Select product from the list',parent=self.root)
            else:
                db_cursor.execute("Select * from item_master where product_id=%s",(self.var_product_id.get(),))
                row=db_cursor.fetchone()
                if row==None:
                    messagebox.showerror('Error','Invalid product',parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete ?",parent=self.root)
                    if op==True:
                        db_cursor.execute("delete from item_master where product_id=%s",(self.var_product_id.get(),))
                        db_connection.commit()
                        messagebox.showinfo('Success','Record Deleted Successfully!',parent=self.root)
                        self.clear
                        self.show
                        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_category.set("Select"),
        self.var_price.set(""),
        self.var_product.set(""),
        self.var_quantity.set(""),
        self.var_searchby.set(""),
        # self.var_pid.set("")
        self.var_product_id.set(""),
        self.var_supplier.set("Select"),
        
        self.show()

    def search(self):
        
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select search by option", parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search text is required", parent=self.root)
            else:
                db_cursor.execute("select * from item_master where"+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                
                rows=db_cursor.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record Found", parent=self.root)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

            
if __name__=="__main__":
    root = Tk()
    obj=productClass(root)
    root.mainloop()