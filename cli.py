import requests

BASE_URL = "http://127.0.0.1:5000"

def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")
    items = response.json()
    for item in items:
        print(f"ID {item['id']}: {item['product_name']} | {item.get('brand','')} | KES {item.get('price')} | Qty: {item.get('quantity')}")

def add_item():
    product_name = input("Product name: ")
    brand = input("Brand: ")
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))
    barcode = input("Barcode: ")
    data = {
        "product_name": product_name,
        "brand": brand,
        "price": price,
        "quantity": quantity,
        "barcode": barcode
    }
    response = requests.post(f"{BASE_URL}/inventory", json=data)
    print(response.json())

def update_item():
    item_id = int(input("Item ID to update: "))
    product_name = input("New product name (leave blank to keep current): ")
    brand = input("New brand (leave blank to keep current): ")
    price_input = input("New price (leave blank to keep current): ")
    quantity_input = input("New quantity (leave blank to keep current): ")
    data = {}
    if product_name:
        data["product_name"] = product_name
    if brand:
        data["brand"] = brand
    if price_input:
        data["price"] = float(price_input)
    if quantity_input:
        data["quantity"] = int(quantity_input)
    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)
    print(response.json())

def delete_item():
    item_id = int(input("Item ID to delete: "))
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print(response.json())

def fetch_from_api():
    choice = input("Search by (b)arcode or (n)ame? ").strip().lower()
    payload = {}
    if choice == "b":
        payload["barcode"] = input("Barcode: ")
    else:
        payload["name"] = input("Product name: ")
    payload["price"] = float(input("Price to set: "))
    payload["quantity"] = int(input("Quantity to set: "))
    response = requests.post(f"{BASE_URL}/inventory/fetch", json=payload)
    print(response.json())

def main_menu():
    while True:
        print("\n--- Inventory CLI ---")
        print("1. View inventory")
        print("2. Add item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Fetch item from OpenFoodFacts")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            fetch_from_api()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main_menu()