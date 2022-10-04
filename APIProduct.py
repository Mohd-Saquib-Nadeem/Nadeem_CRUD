import flask
from flask import request, jsonify, render_template
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def connect_to_db():
    db=sqlite3.connect('ProductDb.db')
    return db
    
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Product API</h1>
<p>A prototype API for Product CRUD operations</p>'''


#Get Products
@app.route('/api/v1/product/GetProducts', methods=['GET'])
def GetProducts():
    productList = []
    try:
        db=connect_to_db()
        db.row_factory = sqlite3.Row
        cur = db.cursor()
        cur.execute("SELECT * FROM Product")
        rows = cur.fetchall()

        for i in rows:
            product = {}
            product["ProductId"] = i["ProductId"]
            product["ProductCode"] = i["ProductCode"]
            product["ProductType"] = i["ProductType"]
            product["ProductName"] = i["ProductName"]
            product["ProductDescription"] = i["ProductDescription"]
            product["ProductCompany"] = i["ProductCompany"]
            
            productList.append(product)

    except:
        productList = []

    return productList
 
 #Add Product
@app.route('/api/v1/product/AddProduct', methods=['POST'])
def AddProduct():
    product = request.get_json() 
    productList = {}
    db=connect_to_db()
    try:        
        cur =db.cursor()
        cur.execute("INSERT INTO Product (ProductId, ProductCode, ProductType, ProductName, ProductDescription, ProductCompany) VALUES (?, ?, ?, ?, ?, ?)", (product['ProductId'], product['ProductCode'], product['ProductType'], product['ProductName'], product['ProductDescription'], product['ProductCompany']))
        db.commit()
        productList = GetProducts()
    except:
        db.rollback()

    finally:
        db.close()

    return productList

#Update Product
@app.route('/api/v1/product/UpdateProduct', methods=['POST'])
def updateEmployee():
    product = request.get_json()
    productList = {}
    db=connect_to_db()
    try:        
        cur =db.cursor()
        cur.execute("UPDATE Product SET ProductCode = ?, ProductType = ?, ProductName = ?, ProductDescription = ?, ProductCompany = ? WHERE ProductId =?",  
                     (product['ProductCode'], product['ProductType'], product['ProductName'], product['ProductDescription'], product['ProductCompany'], product['ProductId']))
        db.commit()
        productList = GetProducts()
    except:
        db.rollback()

    finally:
        db.close()

    return productList
#Delete Product
@app.route('/api/v1/product/DeleteProduct/<int:id>', methods=['DELETE'])
def DeleteProduct(id):
    message = {}
    db=connect_to_db()
    try:        
        cur =db.cursor()
        cur.execute("DELETE from Product WHERE ProductId = ?",     
                      (id,))
        db.commit()
        message["status"] = "Product deleted successfully"
    except:
        db.rollback()
        message["status"] = "Error while deleting product"
    finally:
        db.close()

    return message
    
app.run()