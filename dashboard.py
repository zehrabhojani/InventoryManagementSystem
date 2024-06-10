# from tkinter import *
# from PIL import Image,ImageTk 
# from tkinter import ttk,messagebox
# from connection import *
# from tkinter import scrolledtext
# import PIL.Image

from tkinter import *
from Employee import employeeClass
from tkinter import ttk,messagebox
from sales import salesClass
from supplier import supplierClass
from category import categoryClass
from Product import productClass
from bill import billClass
from connection import *
import os
#from PIL import Image, ImageTk #pip install pillow
class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed by Avalanche")
        self.root.config(bg="white")
        #====title=====
       # self.icon_title=PhotoImage(file="image\logo1.png")
        #title=Label(self.root,text="Inventory Management System",image=self.icon_title,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        title=Label(self.root,text="Inventory Management System",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)
       
        #=====btn_logout===
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #====clock====
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date:DD-MM-YYYY \t\t Time:HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #===left menu ====
        #self.MenuLogo=Image.open("image\menu.png")
        #self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        #self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)
        #lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        #lbl_menuLogo.pack(side=TOP,Fill=X)

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",padx=30,anchor="w").pack(side=TOP,fill=X)
        # btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",padx=30,anchor="w").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",padx=30,anchor="w").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product",command=self.Product,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",padx=30,anchor="w").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",padx=30,anchor="w").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2",padx=30,anchor="w").pack(side=TOP,fill=X)
       
       #=====Content=====
        self.lbl_employee=Label(self.root,text="Total Employee \n [0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="Total Supplier \n [0]",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="Total Category \n [0]",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="Total Product \n [0]",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales \n [0]",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        #====footer====
        lbl_footer=Label(self.root,text="IMS-Inventory Management System | Developed by Avalanche \n For any technical issue contact:xxxxxxx",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.update_content()
#===============================================================================================================
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)
    
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
        
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
        
    def Product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)
    
    def update_content(self):
        try:
            db_cursor.execute("select * from item_master")
            product=db_cursor.fetchall()
            self.lbl_product.config(text=f'Total Products \n [ {str(len(product))}]')
            
            db_cursor.execute("select * from supplier")
            supplier=db_cursor.fetchall()
            self.lbl_supplier.config(text=f'Total suppliers \n [ {str(len(supplier))}]')
            
            db_cursor.execute("select * from category")
            category=db_cursor.fetchall()
            self.lbl_category.config(text=f'Total category \n [ {str(len(category))}]')
            
            db_cursor.execute("select * from employee")
            employee=db_cursor.fetchall()
            self.lbl_employee.config(text=f'Total Employee \n [ {str(len(employee))}]')
            
            self.lbl_sales.config(text=f'Total Sales [{str(len(os.listdir("bill")))}]')

        except Exception as ex:
            
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

if __name__=="__main__":
    root = Tk()
    obj=IMS(root)
    root.mainloop()


