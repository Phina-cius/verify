# the auther name : phinacius wafula simiyu
# the auther email: phinaciussimiyu143@gmail.com
# the auther phone number: 0790681812




import requests
from django.core.exceptions import ObjectDoesNotExist
from barcodereader.models import Barcode

class BarcodeVerifier:
    def __init__(self, base_url="https://api.upcitemdb.com/prod/trial/lookup"):
        self.base_url = base_url

    def check_local_database(self, barcode):
        """Check if the barcode exists in the local database."""
        try:
            barcode_entry = Barcode.objects.get(barcode=barcode)
            product = barcode_entry.product
            product_info = {
                "ean": barcode_entry.barcode,
                "upc": barcode_entry.barcode,
                "title": product.name,
                "description": "Product from local database",
                "brand": product.manufacturer.company_name,
                "model": "N/A",
                "category": "N/A",
                "images": [img.image.url for img in product.images.all()],
                "asin": "N/A",
                "color": "N/A",
                "size": "N/A",
                "dimension": "N/A",
                "weight": "N/A",
                "lowest_recorded_price": "N/A",
                "highest_recorded_price": "N/A",
                "elid": "N/A",
                "offers": [],
                "created_t": "N/A",
                "updated_t": "N/A"
            }
            return product_info
        except Barcode.DoesNotExist:
            return None

    def verify_barcode(self, barcode):
        """Verifies the barcode using local database first, then UPCItemDB API."""
        # Check local database first
        local_product_info = self.check_local_database(barcode)
        if local_product_info:
            return local_product_info

        # If not found in local database, check the API
        url = f"{self.base_url}?upc={barcode}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data['code'] == 'OK' and data['total'] > 0:
                item = data['items'][0]
                product_info = {
                    "ean": item.get('ean', 'N/A'),
                    "upc": item.get('upc', 'N/A'),
                    "title": item.get('title', 'N/A'),
                    "description": item.get('description', 'N/A'),
                    "brand": item.get('brand', 'N/A'),
                    "model": item.get('model', 'N/A'),
                    "category": item.get('category', 'N/A'),
                    "images": item.get('images', []),
                    "asin": item.get('asin', 'N/A'),
                    "color": item.get('color', 'N/A'),
                    "size": item.get('size', 'N/A'),
                    "dimension": item.get('dimension', 'N/A'),
                    "weight": item.get('weight', 'N/A'),
                    "lowest_recorded_price": item.get('lowest_recorded_price', 'N/A'),
                    "highest_recorded_price": item.get('highest_recorded_price', 'N/A'),
                    "elid": item.get('elid', 'N/A'),
                    "offers": item.get('offers', []),
                    "created_t": item.get('created_t', 'N/A'),
                    "updated_t": item.get('updated_t', 'N/A')
                }
                return product_info
            else:
                return None  # No item found
        else:
            response.raise_for_status()