import sqlite3
db=sqlite3.connect('ProductDb.db')
try:        
    cur =db.cursor()
    cur.execute('''CREATE TABLE Product (
    ProductId INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductCode TEXT (50) NOT NULL,
    ProductType TEXT (50) NOT NULL,
    ProductName TEXT (50) NOT NULL,
    ProductDescription TEXT (100) NOT NULL,
    ProductCompany TEXT (100) NOT NULL);''')
    print ('Product table created successfully')
except:
    print ('Error while creating product table')
    db.rollback()
db.close()