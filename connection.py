import mysql.connector

db_connection = mysql.connector.connect(host="localhost", user="root", password="omicron", auth_plugin="mysql_native_password")
db_cursor = db_connection.cursor(buffered=True)
db_cursor.execute("use smart_trolley")
