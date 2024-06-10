# from tkinter import *
# from PIL import ImageTk
# from tkinter import ttk,messagebox
# from tkinter import filedialog
# from connection import *
# import qrcode
# import base64
# import PIL.Image
# class product_details:
#     def __init__(self,root):
#             self.root=root
#             self.root.geometry("1100x500+220+130")
#             self.root.title("Inventory Management System | Developed by PVPIT Team")
#             self.root.config(bg="white")
#             self.root.focus_force()
#             style = ttk.Style()
#             style.configure("Center.TEntry", justify=CENTER)

#             cTitle=Label(self.root,text="InStock Details",font=("times new roman",15),bg="lightgray").pack(side=TOP,fill=X)
#             cal_cart_frame=Frame(root,bd=4,relief=RIDGE,bg="white")        
#             cal_cart_frame.place(x=30,y=40,width=1050,height=430)
#             cart_frame=Frame(cal_cart_frame,bd=3,relief=RIDGE)
#             cart_frame.place(x=20,y=1, width=1000,height=417)
#             cartTitle=Label(cart_frame,font=("times new roman",15),bg="lightgray").pack(side=TOP,fill=X)

#             scrolly=Scrollbar(cart_frame,orient=VERTICAL)
#             scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

#             self.cart_Table=ttk.Treeview(cart_frame,columns=("id","pid","name","price","total_qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,style="Center.TEntry")
#             scrollx.pack(side=BOTTOM,fill=X)
#             scrolly.pack(side=RIGHT,fill=Y)
#             scrollx.config(command=self.cart_Table.xview)
#             scrolly.config(command=self.cart_Table.yview)

#             self.cart_Table.heading("id",text="ID")
#             self.cart_Table.heading("pid",text="Product_ID")
#             self.cart_Table.heading("name",text="Name")
#             self.cart_Table.heading("price",text="Price")
#             self.cart_Table.heading("total_qty",text="Total Quantity")
#             # self.cart_Table.heading("status",text="Status")
    
#             self.cart_Table["show"]="headings"

#             self.cart_Table.column("id",width=20)
#             self.cart_Table.column("pid",width=70)
#             self.cart_Table.column("name",width=100)
#             self.cart_Table.column("price",width=90)
#             self.cart_Table.column("total_qty",width=10)
#             self.cart_Table.bind("<ButtonRelease-1>",self.get_data)
#             # self.cart_Table.column("status",width=90)
    
#             self.cart_Table.pack(fill=BOTH,expand=1)
#             self.show()
            

#     def get_data(self,ev):
#         f=self.cart_Table.focus()
#         content=(self.cart_Table.item(f))
#         row=content['values']
        
#     def show(self):
#         try:
#             db_cursor.execute("select * from item_master")
#             rows = db_cursor.fetchall()
#             self.cart_Table.delete(*self.cart_Table.get_children())
#             for row in rows:
#                 self.cart_Table.insert('', END, values=row)
#         except Exception as ex:
#             messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


# if __name__=="__main__":
#     root = Tk()
#     obj=product_details(root)
#     root.mainloop()

from tkinter import *
from tkinter import ttk, messagebox
from connection import *

class ProductDetails:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Team Avalanche")
        self.root.config(bg="white")
        self.root.focus_force()
        style = ttk.Style()
        style.configure("Center.TEntry", justify=CENTER)

        self.create_gui()

    def create_gui(self):
        c_title = Label(self.root, text="InStock Details", font=("times new roman", 15), bg="lightgray")
        c_title.pack(side=TOP, fill=X, pady=(0, 10))

        input_frame = Frame(self.root, bg="white")
        input_frame.pack(pady=(0, 10))

        product_label = Label(input_frame, text="Select Product:", font=("times new roman", 12), bg="white")
        product_label.grid(row=0, column=0, padx=(30, 10))

        self.product_combobox = ttk.Combobox(input_frame, state="readonly", font=("times new roman", 12), width=25)
        self.product_combobox.grid(row=0, column=1, padx=10)

        self.product_combobox.set("Select Product")
        self.product_combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        qty_label = Label(input_frame, text="Quantity:", font=("times new roman", 12), bg="white")
        qty_label.grid(row=0, column=2, padx=10)

        self.qty_entry = Entry(input_frame, font=("times new roman", 12), width=10,bg="#f2d2bd")
        self.qty_entry.grid(row=0, column=3, padx=10)

        add_qty_button = Button(input_frame, text="Add Quantity", command=self.add_quantity,font=("times new roman", 12), bg="#4caf50", fg="white", cursor="hand2")
        add_qty_button.grid(row=0, column=4, padx=(10, 30))

        cal_cart_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        cal_cart_frame.pack()

        cart_frame = Frame(cal_cart_frame, bd=3, relief=RIDGE)
        cart_frame.pack()

        scrolly = Scrollbar(cart_frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)

        self.cart_Table = ttk.Treeview(cart_frame, columns=("id", "pid", "name", "price", "total_qty"),
                                       yscrollcommand=scrolly.set, xscrollcommand=scrollx.set, style="Center.TEntry")
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.cart_Table.xview)
        scrolly.config(command=self.cart_Table.yview)

        self.cart_Table.heading("id", text="ID")
        self.cart_Table.heading("pid", text="Product_ID")
        self.cart_Table.heading("name", text="Name")
        self.cart_Table.heading("price", text="Price")
        self.cart_Table.heading("total_qty", text="Total Quantity")

        self.cart_Table["show"] = "headings"

        self.cart_Table.column("id", width=20)
        self.cart_Table.column("pid", width=70)
        self.cart_Table.column("name", width=100)
        self.cart_Table.column("price", width=50)
        self.cart_Table.column("total_qty", width=10)
        self.cart_Table.bind("<ButtonRelease-1>", self.get_data)
        self.cart_Table.pack(fill=BOTH, expand=1)

        self.show()

    
    def on_combobox_select(self, event):
        self.qty_entry.delete(0, END)  # Clear the entry field
        selected_product = self.product_combobox.get()

    def add_quantity(self):
        selected_product = self.product_combobox.get()
        quantity = self.qty_entry.get()

        if selected_product == "Select Product":
            messagebox.showerror("Error", "Please select a product", parent=self.root)
        elif not quantity.isdigit():
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid number", parent=self.root)
        else:
            query = "UPDATE item_master SET total_qty = total_qty + %s WHERE name_of_product = %s"
            db_cursor.execute(query, (quantity, selected_product))
            db_connection.commit()
            messagebox.showinfo("Success", f"Quantity added successfully for {selected_product}", parent=self.root)
            self.show()

    def get_data(self, ev):
        selected_row = self.cart_Table.focus()
        content = self.cart_Table.item(selected_row)
        row = content['values']
        # Do something with the selected data

    def show(self):
        try:
            db_cursor.execute("SELECT name_of_product FROM item_master")
            products = db_cursor.fetchall()
            product_names = ["Select Product"] + [product[0] for product in products]
            self.product_combobox["values"] = product_names

            db_cursor.execute("SELECT * FROM item_master")
            rows = db_cursor.fetchall()
            self.cart_Table.delete(*self.cart_Table.get_children())
            for row in rows:
                self.cart_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching data from the database: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = ProductDetails(root)
    root.mainloop()
