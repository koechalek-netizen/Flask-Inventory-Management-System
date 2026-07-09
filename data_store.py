from flask import Flask, request, jsonify
import data_store

app = Flask(__name__)

@app.route("/api/inventory", methods=["GET"])
def get_items():
    items = data_store.get_all_items()
    return jsonify(items), 200

inventory = [
    {
        "id": 1,
        "product_name": "Laptop",
        "brand": "Dell",
        "price": 999.99,
        "barcode": "123456789012",
        "quantity": 10
    },
    {
        "id": 2,
        "product_name": "Smartphone",
        "brand": "Apple",
        "price": 699.99,
        "barcode": "098765432109",
        "quantity": 20
    }
]

# Retrieve an item by its ID
def get_item_by_id(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None
# Retrieve all items in the inventory
def get_all_items():
    return inventory


# Add a new item to the inventory
def add_item(data):
    new_id = max(item["id"] for item in inventory) + 1 if inventory else 1
    new_item = {
        "id": new_id,
        "product_name": data.get("product_name"),
        "brand": data.get("brand"),
        "price": data.get("price"),
        "barcode": data.get("barcode"),
        "quantity": data.get("quantity")
    }
    inventory.append(new_item)
    return new_item


# Update an existing item in the inventory
def update_item(item_id, data):
    item = get_item_by_id(item_id)
    if item:
        item["product_name"] = data.get("product_name", item["product_name"])
        item["brand"] = data.get("brand", item["brand"])
        item["price"] = data.get("price", item["price"])
        item["barcode"] = data.get("barcode", item["barcode"])
        item["quantity"] = data.get("quantity", item["quantity"])
        return item
    return None


# Delete an item from the inventory
def delete_item(item_id):
    item = get_item_by_id(item_id)
    if item:
        inventory.remove(item)
        return True
    return False

if __name__ == "__main__":
    app.run(debug=True)