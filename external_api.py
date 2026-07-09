import requests

BASE_URL = "https://world.openfoodfacts.org"
HEADERS = {"User-Agent": "InventoryManagementApp/1.0 (student project)"}

def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()
    if data.get("status") == 1:
        return data["product"]
    else:
        return None

def search_product_by_name(name):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={name}&search_simple=1&action=process&json=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()
    products = data.get("products", [])
    if products:
        return products
    else:
        return None
