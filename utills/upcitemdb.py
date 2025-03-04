# the auther name :phinacius wafula simiyu
# the auther email:phinaciussimiyu143@gmail.com
# the auther phonenumber:+254798681812





import requests


class BarcodeVerifier:
    def __init__(self, base_url="https://api.upcitemdb.com/prod/trial/lookup"):
        self.base_url = base_url

    def verify_barcode(self, barcode):
        """Verifies the barcode using UPCItemDB API."""
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



