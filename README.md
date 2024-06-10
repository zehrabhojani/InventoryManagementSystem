# Inventory Management System

## Overview
This project implements an Inventory Management System using Python, Tkinter, and MySQL. The system allows users to manage inventory by adding, viewing, updating, and deleting items. The graphical user interface (GUI) is built with Tkinter, making it user-friendly and easy to navigate.

## Features
- Add new inventory items
- View all inventory items
- Update existing inventory items
- Delete inventory items
- Search for items in the inventory
- Export inventory data to a CSV file

## Requirements
- Python 3.6+
- Tkinter (included with standard Python installation)
- MySQL Server
- MySQL Connector for Python
- pandas (for exporting data to CSV)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/inventory-management-system.git
   cd inventory-management-system
   ```

2. **Create a virtual environment and activate it**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL Database**
   - Install MySQL Server from the official website: [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
   - Open MySQL Command Line Client and create a database:
     ```sql
     CREATE DATABASE inventory_db;
     ```
   - Create a user and grant privileges:
     ```sql
     CREATE USER 'inventory_user'@'localhost' IDENTIFIED BY 'your_password';
     GRANT ALL PRIVILEGES ON inventory_db.* TO 'inventory_user'@'localhost';
     FLUSH PRIVILEGES;
     ```
   - Import the `inventory_db.sql` file (if provided) to create necessary tables:
     ```bash
     mysql -u inventory_user -p inventory_db < db/inventory_db.sql
     ```

5. **Configure database connection**
   - Update the `config.py` file with your MySQL database credentials:
     ```python
     DB_HOST = 'localhost'
     DB_USER = 'inventory_user'
     DB_PASSWORD = 'your_password'
     DB_NAME = 'inventory_db'
     ```

## Usage

1. **Run the inventory management application**
   ```bash
   python main.py
   ```

2. **Main Features**
   - **Add Item:** Allows users to add new items to the inventory by entering details such as item name, quantity, price, and description.
   - **View Items:** Displays all items in the inventory in a tabular format.
   - **Update Item:** Users can select an item and update its details.
   - **Delete Item:** Users can select an item and delete it from the inventory.
   - **Search Items:** Provides a search functionality to find items by name.
   - **Export Data:** Exports the inventory data to a CSV file for external use.

## Configuration

- **Database Configuration**
  - The system uses MySQL as the database. Ensure MySQL Server is running and the database is correctly configured as per the instructions above.

## Directory Structure

```
inventory-management-system/
│
├── main.py
├── config.py
├── db/
│   └── inventory_db.sql  # SQL script to create necessary tables
├── requirements.txt
├── README.md
└── assets/
    └── icon.png  # Application icon (if applicable)
```

## Screenshots

![Main Screen](assets/main_screen.png)
*Main screen of the Inventory Management System.*

![Add Item](assets/add_item.png)
*Add new inventory item.*

![View Items](assets/view_items.png)
*View all inventory items.*

## References

- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
- [MySQL Connector for Python Documentation](https://dev.mysql.com/doc/connector-python/en/)

