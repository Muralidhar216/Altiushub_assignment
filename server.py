from flask import Flask,request,jsonify
from flask_json_schema import JsonSchema, JsonValidationError
from uuid import uuid4

app = Flask(__name__)
schema = JsonSchema(app)

InvoiceHeader = []
InvoiceItems = []
InvoiceBillSundry = []


InvoiceHeader_Schema = {
    'properties': {
        'Id' : { 'type': 'uuid' },
        'Date':{ 'type': 'string' },
        'InvoiceNumber':{ 'type': 'number' },
        'CustomerName':{ 'type': 'string' },
        'BillingAddress':{ 'type': 'string' },
        'ShippingAddress':{ 'type': 'string' },
        'GSTIN' :{ 'type': 'string' },
        'TotalAmount' : { 'type': 'number' },
    }
}
InvoiceItems_Schema = {
    'properties': {
        'Id' : { 'type': 'uuid' },
        'itemName': { 'type': 'string' },
        'Quantity': { 'type': 'decimal' },
        'Price': { 'type': 'decimal' },
        'Amount': { 'type': 'decimal' },

    }
}
InvoiceBillSundry_Schema = {
    'properties': {
        'Id' : { 'type': 'uuid' },
        'billSundryName': { 'type': 'decimal' },
        'Amount': { 'type': 'decimal' },
    }
}

@app.route('/createItem',methods=['POST'])
def createitem():
    data = request.get_json()
    if(data.itemName == "" or data.Quantity == "" or data.Price == ""):
        return "All Feilds are required"
    
    newItem = {
        'Id' : str(uuid.uuid4()),
        'itemName' : (data.itemName),
        "Quantity" : float(data.Quantity),
        "Price" : float(data.Price),
        'Amount' : (data.itemName) * (data.Price)
    }
    InvoiceItems.append({newItem.Id : newItem})
    return "New Item is added Sucessfully"


# @app.route('/updateItem',methods=['POST'])
# def updateitem():
#     data = request.get_json()
#     if(data.itemName == "" or data.Quantity == '' or data.Price == ''):
#         return "All Feilds are required"
    
#     newItem = {
#         'Id' : str(uuid.uuid4()),
#         'itemName' : data.itemName,
#         "Quantity" : data.Quantity,
#         "Price" : data.Price,
#         'Amount' : (data.itemName) * (data.Price)
#     }
#     InvoiceItems.append(newItem)
#     return "New Item is added Sucessfully"
    


@app.route('/deleteItem',methods=['POST'])
def deleteitem(Itemid):
    if(Itemid not in InvoiceItems):
        return "Invalid Itemid"
    
    deletedId = ""
    for item in InvoiceItems:
        if item.Id == Itemid:
            deletedId = Itemid
    
    if(deletedId == ''):
        return "Item not found"
    InvoiceItems.remove(deletedId)
    return "successfully Item deleted"



@app.route('/getItems',methods=['GET'])
def getitem():
    return jsonify(InvoiceItems)


if __name__ == '__main__':
    app.run(debug=True)