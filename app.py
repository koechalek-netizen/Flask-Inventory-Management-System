from flask import Flask, request, jsonify
import data_store

app = Flask(__name__)

# API endpoint to retrieve all items in the inventory
@app.route("/inventory", methods=["GET"])
def get_items():
    items = data_store.get_all_items()
    return jsonify(items), 200

#fetch a singleitem by id
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = data_store.get_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# API endpoint to create a new item in the inventory
@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "product_name" not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_item = data_store.add_item(data)
    return jsonify(new_item), 201

# API endpoint to update an existing item in the inventory
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def patch_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    updated_item = data_store.update_item(item_id, data)
    if updated_item:
        return jsonify(updated_item), 200
    return jsonify({"error": "Item not found"}), 404


# API endpoint to delete an item from the inventory
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    deleted_item = data_store.delete_item(item_id)
    if deleted_item:
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"error": "Item not found"}), 404



if __name__ == "__main__":
    app.run(debug=True)