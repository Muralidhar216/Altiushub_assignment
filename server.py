from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)


invoices = []
invoice_number_counter = 1 
InvoiceHeader_Schema = {
    'properties': {
        'Id': {'type': 'uuid'},
        'Date': {'type': 'string'},
        'InvoiceNumber': {'type': 'number'},
        'CustomerName': {'type': 'string'},
        'TotalAmount': {'type': 'number'},
    }
}

InvoiceItems_Schema = {
    'properties': {
        'Id': {'type': 'uuid'},
        'itemName': {'type': 'string'},
        'Quantity': {'type': 'decimal'},
        'Price': {'type': 'decimal'},
        'Amount': {'type': 'decimal'},
    }
}

@app.route('/invoices', methods=['POST'])
def create_invoice():
    data = request.get_json()
    date = data.get('Date')
    customer_name = data.get('CustomerName')
    items_data = data.get('InvoiceItems', [])


    if not all([date, customer_name]):
        return jsonify({"error": "Date and CustomerName are required."}), 400

    items = []
    for item_data in items_data:
        quantity = item_data.get('Quantity')
        price = item_data.get('Price')
        if quantity <= 0 or price <= 0:
            return jsonify({"error": "Price and Quantity must be greater than zero."}), 400
        item = {
            'Id': str(uuid4()),
            'itemName': item_data['itemName'],
            'Quantity': quantity,
            'Price': price,
            'Amount': quantity * price,
        }
        items.append(item)


    global invoice_number_counter
    invoice = {
        'Id': str(uuid4()),
        'Date': date,
        'InvoiceNumber': invoice_number_counter,
        'CustomerName': customer_name,
        'TotalAmount': sum(item['Amount'] for item in items),
        'InvoiceItems': items,
    }
    invoice_number_counter += 1
    invoices.append(invoice)

    return jsonify({"message": "Invoice created successfully.", "invoice": invoice}), 201

@app.route('/invoices/<invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    data = request.get_json()
    for invoice in invoices:
        if invoice['Id'] == invoice_id:
  
            invoice['Date'] = data.get('Date', invoice['Date'])
            invoice['CustomerName'] = data.get('CustomerName', invoice['CustomerName'])

            items = []
            for item_data in data.get('InvoiceItems', []):
                quantity = item_data.get('Quantity')
                price = item_data.get('Price')
                if quantity <= 0 or price <= 0:
                    return jsonify({"error": "Price and Quantity must be greater than zero."}), 400
                item = {
                    'Id': str(uuid4()),
                    'itemName': item_data['itemName'],
                    'Quantity': quantity,
                    'Price': price,
                    'Amount': quantity * price,
                }
                items.append(item)
            
            invoice['InvoiceItems'] = items
            invoice['TotalAmount'] = sum(item['Amount'] for item in items)  
            return jsonify({"message": "Invoice updated successfully.", "invoice": invoice}), 200

    return jsonify({"error": "Invoice not found."}), 404

@app.route('/invoices/<invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    global invoices
    invoices = [invoice for invoice in invoices if invoice['Id'] != invoice_id]
    return jsonify({"message": "Invoice deleted successfully."}), 200

@app.route('/invoices/<invoice_id>', methods=['GET'])
def retrieve_invoice(invoice_id):
    for invoice in invoices:
        if invoice['Id'] == invoice_id:
            return jsonify(invoice), 200
    return jsonify({"error": "Invoice not found."}), 404

@app.route('/invoices', methods=['GET'])
def list_invoices():
    return jsonify(invoices), 200

if __name__ == '__main__':
    app.run(debug=True)
