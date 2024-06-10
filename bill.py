from tkinter import *
from PIL import ImageTk
from tkinter import ttk,messagebox
from tkinter import filedialog

from tomlkit import key
from connection import *
import qrcode
import base64
import PIL.Image
import http.client  # For Python 3, use 'http.client' instead of 'httplib'
import urllib.parse  # For Python 3, use 'urllib.parse' instead of 'urllib'
import time
class billClass:
    def __init__(self,root):
            self.root=root
            self.root.geometry("800x480+220+130")
            self.root.title("Inventory Management System | Developed by PVPIT Team")
            self.root.config(bg="white")
            self.root.focus_force()

            self.var_search=StringVar()
            self.var_searchtxt=StringVar()


            cTitle=Label(self.root,text="Customer Details",font=("times new roman",15),bg="lightgray").pack(side=TOP,fill=X)
            cal_cart_frame=Frame(root,bd=4,relief=RIDGE,bg="white")        
            cal_cart_frame.place(x=10,y=40,width=430,height=430)
            cart_frame=Frame(cal_cart_frame,bd=3,relief=RIDGE)
            cart_frame.place(x=1,y=1, width=420,height=390)
            cartTitle=Label(cart_frame,font=("times new roman",15),bg="lightgray").pack(side=TOP,fill=X)

            scrolly=Scrollbar(cart_frame,orient=VERTICAL)
            scrollx=Scrollbar(cart_frame,orient=HORIZONTAL)

            self.cart_Table=ttk.Treeview(cart_frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            scrollx.pack(side=BOTTOM,fill=X)
            scrolly.pack(side=RIGHT,fill=Y)
            scrollx.config(command=self.cart_Table.xview)
            scrolly.config(command=self.cart_Table.yview)

            self.cart_Table.heading("pid",text="PID")
            self.cart_Table.heading("name",text="Name")
            self.cart_Table.heading("price",text="Price")
            self.cart_Table.heading("qty",text="Qty")
            # self.cart_Table.heading("status",text="Status")
    
            self.cart_Table["show"]="headings"

            self.cart_Table.column("pid",width=70)
            self.cart_Table.column("name",width=100)
            self.cart_Table.column("price",width=90)
            self.cart_Table.column("qty",width=10)
            self.cart_Table.bind("<ButtonRelease-1>",self.get_data)
            # self.cart_Table.column("status",width=90)
    
            self.cart_Table.pack(fill=BOTH,expand=1)

            lbl_total=Label(cal_cart_frame,text="Total Bill :",font=("times new roman",14,"bold"),bg="white").place(x=1,y=392)
            self.txt_total=Entry(cal_cart_frame,font=("times new roman",15),bg="#f2d2bd",state="readonly")
            self.txt_total.place(x=300,y=393,width=100)
            lbl_name=Label(self.root,text="Product No",font=("times new roman",15,"bold"),bg="white").place(x=480,y=45)
            self.txt_search=Entry(self.root,textvariable=self.var_search,font=("times new roman",15),bg="#f2d2bd")
            self.txt_search.place(x=600,y=47,width=150,height=22)
            self.txt_search.focus()
            btn_delete=Button(self.root,text="delete",command=self.delete,font=("times new roman",15),bg="#f44336",fg="white",cursor="hand2").place(x=480,y=100,width=100,height=25)
            btn_generate_bill=Button(self.root,text="Generate Bill",command=self.generate_bill,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=630,y=100,width=150,height=25)
            
        

            self.txt_search.bind("<Return>", self.f1)
    def f1(self, event):
        self.add()
    # def add(self):
    #     try:
    #         barcode = self.var_search.get()
    #         print(barcode)
    #         if not barcode:
    #             messagebox.showerror("Error", "Barcode is required", parent=self.root)
    #         else:
    #             # Retrieve product information from the database based on the scanned barcode
    #             query = "SELECT product_id, name_of_product, price FROM item_master WHERE product_id = %s"
    #             # query="select pid ,name, customer.price ,qty from customer right JOIN item_master ON customer.pid=item_master.product_id where product_id=%s"

    #             db_cursor.execute(query, (barcode,))
    #             product_data = db_cursor.fetchone()

    #             if product_data:
    #                 # Update the cart table with the scanned data
    #                 self.update_cart_table(product_data)
    #                 # Clear the entry after successfully adding the product
    #                 self.clear()
    #                 self.show()
    #             else:
    #                 messagebox.showinfo("Info", "Product not found in the database", parent=self.root)
                    
           
    #     except Exception as ex:
    #         messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
    def add(self):
        try:
            barcode = self.var_search.get()
            print(barcode)
            if not barcode:
                messagebox.showerror("Error", "Barcode is required", parent=self.root)
            else:
                # Retrieve product information from the database based on the scanned barcode
                query = "SELECT product_id, name_of_product, price, total_qty FROM item_master WHERE product_id = %s"
                db_cursor.execute(query, (barcode,))
                product_data = db_cursor.fetchone()

                if product_data:
                    pid, name, price, total_qty = product_data[0], product_data[1], product_data[2], product_data[3]
                    if total_qty == 0:
                        messagebox.showinfo("Info", f"Product with ID {pid} which is {name} is out of stock.", parent=self.root)
                    else:
                        # Update the cart table with the scanned data
                        self.update_cart_table(product_data)
                        # Clear the entry after successfully adding the product
                        self.clear()
                        self.show()
                else:
                    messagebox.showinfo("Info", "Product not found in the database", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    
    def update_cart_table(self, product_data):
        pid, name, price = product_data[0], product_data[1], product_data[2]
        qty, status = 1, "In Stock"

        # Check if the product is already in the cart
        item_ids = self.cart_Table.get_children()
        for item_id in item_ids:
            values = self.cart_Table.item(item_id, 'values')
            if values[0] == pid:
                # Update the quantity and total price for the existing product in the cart
                current_qty = int(values[3])
                new_qty = current_qty + 1
                self.cart_Table.item(item_id, values=(pid, name, price, new_qty, status))

                # Update the quantity in the 'customer' table
                self.update_quantity_in_customer_table(pid, new_qty)

                # Update the total price and display it in self.txt_total
                current_total = float(self.txt_total.get()) if self.txt_total.get() else 0.0
                total_price = current_total + float(price)
                self.txt_total.config(state=NORMAL)
                self.txt_total.delete(0, END)
                self.txt_total.insert(0, f"{total_price:.2f}")
                return

        # If the product is not in the cart, insert a new row
        self.cart_Table.insert('', 'end', values=(pid, name, price, qty, status))

        # Update the quantity in the 'customer' table
        self.update_quantity_in_customer_table(pid, qty)

        # Update the total price and display it in self.txt_total
        current_total = float(self.txt_total.get()) if self.txt_total.get() else 0.0
        total_price = current_total + float(price)
        self.txt_total.config(state=NORMAL)
        self.txt_total.delete(0, END)
        self.txt_total.insert(0, f"{total_price:.2f}")

        # Insert data into the 'customer' table
        self.insert_into_customer_table(pid, name, price, qty)

    def update_quantity_in_customer_table(self, pid, qty):
        try:
            # Update the quantity in the 'customer' table
            query = "UPDATE customer SET qty = %s WHERE pid = %s"
            values = (qty, pid)
            db_cursor.execute(query, values)
            db_connection.commit()

        except Exception as ex:
            messagebox.showerror("Error", f"Error updating quantity in 'customer' table: {str(ex)}", parent=self.root)

    def insert_into_customer_table(self, pid, name, price, qty):
        try:
        # Define the SQL query to insert data into the 'customer' table
            query = "INSERT INTO customer (pid, name, price, qty) VALUES (%s, %s, %s, %s)"
            values = (pid, name, price, qty)

            # Execute the query
            db_cursor.execute(query, values)
            db_connection.commit()

            # messagebox.showinfo("Info", "Data added to the 'customer' table", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error inserting data to 'customer' table: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_search.set(""),
        self.show()

    def delete(self):
        try:
            if self.var_search.get() == "":
                messagebox.showerror('Error', 'Please select a product', parent=self.root)
            else:
                # Get the selected product information before deleting
                selected_product_data = self.get_selected_product_data()

                db_cursor.execute("SELECT * FROM customer WHERE pid=%s", (self.var_search.get(),))
                row = db_cursor.fetchone()

                if row is None:
                    messagebox.showerror('Error', 'Invalid Product ID', parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        # Delete the selected product from the 'customer' table
                        db_cursor.execute("DELETE FROM customer WHERE pid=%s", (self.var_search.get(),))
                        db_connection.commit()
                        messagebox.showinfo('Success', 'Record Deleted Successfully!', parent=self.root)
                        
                        # Recalculate and update the total price after deletion
                        self.update_total_after_deletion(selected_product_data)
                        
                        # Clear the search entry field and update the cart display
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_selected_product_data(self):
        # Get the selected row's data in the cart table
        selected_row = self.cart_Table.focus()
        selected_content = self.cart_Table.item(selected_row)
        selected_product_data = selected_content['values']
        return selected_product_data

    def update_total_after_deletion(self, selected_product_data):
        # Get the price of the deleted product
        deleted_product_price = selected_product_data[2]

        # Get the current total from self.txt_total
        current_total = float(self.txt_total.get()) if self.txt_total.get() else 0.0

        # Calculate the new total by subtracting the price of the deleted product
        new_total = max(0, current_total - float(deleted_product_price))

        # Update self.txt_total with the new total
        self.txt_total.config(state=NORMAL)
        self.txt_total.delete(0, END)
        self.txt_total.insert(0, f"{new_total:.2f}")
        # self.txt_total.config(state="readonly")

    def show(self):
        
        try:
            db_cursor.execute("select * from customer")
            rows=db_cursor.fetchall()
            self.cart_Table.delete(*self.cart_Table.get_children())
            for row in rows:
                self.cart_Table.insert('',END,values=row)
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.cart_Table.focus()
        content=(self.cart_Table.item(f))
        row=content['values']
        self.var_search.set(row[0])


    def generate_bill(self):
        try:
            # Get all items in the cart
            items = self.cart_Table.get_children()

            if not items:
                messagebox.showinfo("Info", "No items in the cart to generate a bill.", parent=self.root)
                return

            # Prepare the bill content
            bill_content = "Product ID\tName\tPrice\tQty\n"
            total_amount = 0.0
            for item in items:
                values = self.cart_Table.item(item, 'values')
                total_amount += float(values[2]) * float(values[3])  # price * qty
                bill_content += f"{values[0]}\t\t{values[1]}\t{values[2]}\t{values[3]}\n"

            bill_content += f"\nTotal Amount: {total_amount:.2f}"

            # Generate QR code for payment
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            payment_info = f"Total Amount: {total_amount:.2f}"
            qr.add_data(payment_info)
            qr.make(fit=True)

            # Create an image from the QR code
            qr_image = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code image
            

            # Convert the QR code image to base64 for inclusion in the text file
            from PIL import Image
            from io import BytesIO
            buffered = BytesIO()
           
            
            qr_image_path = "payment_qr_code1.png"
            qr_image.save(qr_image_path)

            # Open the QR code image using Pillow
            qr_image_pillow = Image.open(qr_image_path)
            

            # Display the bill in a new window
            self.show_bill_window(bill_content,qr_image_pillow)

            # Save the bill with QR code as a text file
            self.save_bill_to_file(bill_content)

            self.update_total_qty_in_item_master()

            # Truncate the 'customer' table
            self.truncate_customer_table()

            self.cart_Table.delete(*self.cart_Table.get_children())

        except Exception as ex:
            messagebox.showerror("Error", f"Error generating bill: {str(ex)}", parent=self.root)

    def update_total_qty_in_item_master(self):
        try:
            # Get all items in the cart
            items = self.cart_Table.get_children()

            for item in items:
                values = self.cart_Table.item(item, 'values')
                pid, qty = values[0], values[3]

                # Update total_qty in the 'item_master' table
                query = "UPDATE item_master SET total_qty = total_qty - %s WHERE product_id = %s"
                values = (qty, pid)
                db_cursor.execute(query, values)
                db_connection.commit()

                # Display a message if total_qty is zero
                query = "SELECT total_qty FROM item_master WHERE product_id = %s"
                db_cursor.execute(query, (pid,))
                total_qty = db_cursor.fetchone()[0]
                if total_qty == 0:
                    messagebox.showinfo("Info", f"Product with ID {pid} is out of stock.", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error updating total_qty in 'item_master' table: {str(ex)}", parent=self.root)

    
            
    # def show_bill_window(self, bill_content, qr_image_pillow):
    # #      Create a new window for displaying the bill
    #     bill_window = Toplevel(self.root)
    #     bill_window.title("Bill")
    #     bill_window.geometry("400x300")

    #     # Display the bill content in a Label or Text widget
    #     bill_label = Label(bill_window, text=bill_content, font=("times new roman", 12), justify=LEFT)
    #     bill_label.pack(padx=10, pady=10)

    #     qr_image_label = Label(bill_window, image=ImageTk.PhotoImage(qr_image_pillow))
    #     qr_image_label.pack(padx=10, pady=10)
    #     canvas = Canvas(bill_window, width=200, height=200)
    #     canvas.pack()

    # # Convert the Pillow image to PhotoImage for displaying in Canvas
    #     qr_image_tk = ImageTk.PhotoImage(qr_image_pillow)
    #     canvas.create_image(100, 100, anchor=CENTER, image=qr_image_tk)

    # #     # You may add additional elements to the bill window as needed
    def show_bill_window(self, bill_content, qr_image_pillow):
        # Create a new window for displaying the bill
        bill_window = Toplevel(self.root)
        bill_window.title("Bill")
        bill_window.geometry("400x300")

        # Display the bill content in a Label or Text widget
        bill_label = Label(bill_window, text=bill_content, font=("times new roman", 12), justify=LEFT)
        bill_label.pack(padx=10, pady=10)

        # Display the QR code in a Label
        qr_image_tk = ImageTk.PhotoImage(qr_image_pillow)
        qr_image_label = Label(bill_window, image=qr_image_tk)
        qr_image_label.pack(padx=10, pady=10)

        # You may add additional elements to the bill window as needed

        # Important: Keep a reference to the ImageTk.PhotoImage object to prevent it from being garbage collected
        qr_image_label.image = qr_image_tk


    def save_bill_to_file(self, bill_content):
        try:
            # Ask user for the file location and name
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

            # Check if the user canceled the file dialog
            if file_path:
                with open(file_path, "w") as file:
                    file.write(bill_content)
                messagebox.showinfo("Info", f"Bill saved successfully to {file_path}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error saving bill to file: {str(ex)}", parent=self.root)

    def truncate_customer_table(self):
        try:
            # Truncate the 'customer' table
            db_cursor.execute("TRUNCATE TABLE customer")
            db_connection.commit()
            # messagebox.showinfo("Info", "Customer table truncated successfully.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error truncating customer table: {str(ex)}", parent=self.root)


    key = "2G1WTHI08XYDGESB"  # Put your API Key here

    def thermometer():
        while True:
            # Calculate CPU temperature of Raspberry Pi in Degrees C
            temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3  # Get Raspberry Pi CPU temp
            params = urllib.parse.urlencode({'field1': temp, 'key': key})  # For Python 3, use 'urllib.parse.urlencode'
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

            conn = http.client.HTTPConnection("api.thingspeak.com:80")
            
            try:
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                print(temp)
                print(response.status, response.reason)
                data = response.read()
                conn.close()
            except Exception as e:
                print("Connection failed:", e)

            time.sleep(15)  # Adjust the sleep duration according to your needs
if __name__=="__main__":
    root = Tk()
    obj=billClass(root)
    root.mainloop()
    