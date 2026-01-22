import requests
import time
import logging

logger = logging.getLogger(__name__)

class ShopifyClient:
    def __init__(self, shop_url: str, access_token: str):
        self.shop_domain = shop_url.replace("https://", "").replace("/", "")
        self.base_url = f"https://{self.shop_domain}/admin/api/2024-01"
        self.headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }
        self._location_id = None  # Cache for location ID

    def _request(self, method, endpoint, json_data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        for attempt in range(3):
            try:
                response = requests.request(method, url, headers=self.headers, json=json_data, params=params, timeout=60)
                if response.status_code == 429:
                    try:
                        retry_after = int(float(response.headers.get('Retry-After', 2)))
                    except:
                        retry_after = 2
                    logger.warning(f"Rate limit hit, sleeping {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                response.raise_for_status()
                
                # Smart rate limiting: Add delay after successful request
                time.sleep(0.5)
                
                return response.json()
            except requests.RequestException as e:
                logger.error(f"Shopify API Request Failed ({method} {endpoint}): {e}")
                if 'response' in locals() and response:
                     try:
                        logger.error(f"Response: {response.text}")
                     except:
                        pass
                # Retry on last attempt
                if attempt == 2:
                    raise e
                time.sleep(1)
        return None

    def get_all_products_map(self):
        products_map = {}
        endpoint = "products.json"
        params = {"limit": 250, "fields": "id,title,variants"}
        # Simple loop for now (assuming <250 for testing, strictly needs cursor for production)
        while True:
            data = self._request("GET", endpoint, params=params)
            products = data.get("products", [])
            for p in products:
                for v in p.get("variants", []):
                    sku = v.get("sku")
                    if sku:
                        products_map[sku] = {
                            "product_id": p["id"],
                            "variant_id": v["id"],
                            "inventory_item_id": v["inventory_item_id"]
                        }
            if len(products) < 250:
                break
            break 
        return products_map

    def update_inventory(self, inventory_item_id: int, quantity: int):
        # Use cached location_id to avoid repeated API calls
        if self._location_id is None:
            locations = self._request("GET", "locations.json").get("locations", [])
            if not locations:
                logger.error("No location found in Shopify store.")
                return
            self._location_id = locations[0]["id"]
            logger.info(f"Cached location ID: {self._location_id}")
        
        # Convert quantity to int (handles strings like '2.0')
        try:
            quantity = int(float(str(quantity)))
        except (ValueError, TypeError):
            logger.error(f"Invalid quantity value: {quantity}")
            return

        endpoint = "inventory_levels/set.json"

        payload = {
            "location_id": self._location_id,
            "inventory_item_id": inventory_item_id,
            "available": quantity
        }
        self._request("POST", endpoint, json_data=payload)
        logger.info(f"Updated inventory item {inventory_item_id} to {quantity}")

    def create_full_product(self, details, inventory_data):
        # details = From GetProduct (Description, Images, Colours)
        # inventory_data = From GetProductInventory (SKUs, Qty)

        title = details.get("productName", inventory_data.get("productName"))
        
        # Enhanced Description
        description_parts = [details.get("description") or ""]
        
        features = details.get("features")
        if features:
            description_parts.append(f"<strong>Features:</strong><br>{features}")
            
        # Add technical specs to description
        specs = []
        if details.get("size"):
            specs.append(f"Size: {details['size']}")
        if details.get("material"):
            specs.append(f"Material: {details['material']}")
        if details.get("packing"):
            specs.append(f"Packing: {details['packing']}")
        if details.get("weightCarton") and details.get("qtyPerCarton"):
             specs.append(f"Carton Info: {details['qtyPerCarton']} pcs / {details['weightCarton']}kg")

        if specs:
            description_parts.append("<strong>Specifications:</strong>")
            description_parts.append("<ul>" + "".join([f"<li>{s}</li>" for s in specs]) + "</ul>")

        body_html = "<br><br>".join(filter(None, description_parts))
        
        # Vendor & Type
        vendor = "Nottage"
        brands = details.get("listOfBrand", [])
        if brands:
            vendor = brands[0].get("brandName", "Nottage")
            
        product_type = "Imported" # Default fallback
        # Try to infer type or use category if available? 'nativeWorld' is "The Range", not quite type.
        # We'll stick to Imported for now or user can update later.

        # Tags
        tags = []
        if details.get("isNew"): tags.append("New")
        if details.get("isEco"): tags.append("Eco")
        if details.get("isClearance"): tags.append("Clearance")
        if details.get("nativeWorld"): tags.append(details["nativeWorld"])
        
        # Prepare Images
        # images = []
        # raw_images = details.get("listOfImages", [])
        # seen_images = set()
        
        # # Base URL for images
        # IMAGE_BASE_URL = "https://imageserver.com.au/large/"

        # # Sort: Hero -> Alternate -> Others
        # def image_sort_key(img):
        #     itype = img.get("imageType", "")
        #     if itype == "Hero": return 0
        #     if itype == "Alternate": return 1
        #     return 2
            
        # sorted_raw_images = sorted(raw_images, key=image_sort_key)

        # for img in sorted_raw_images:
        #     fname = img.get("imageFileName")
        #     if fname and fname not in seen_images:
        #         image_url = f"{IMAGE_BASE_URL}{fname}"
        #         images.append({"src": image_url})
        #         seen_images.add(fname)

        # Prepare Variants & Options
        # We need to map SKUs to Options (Color)
        colour_map = {c["sku"]: c["skuColourDescription"] for c in details.get("colours", [])}
        
        variants = []
        skus_list = inventory_data.get("listOfProductSKU", [])
        
        
        # Determine if we have options (Color)
        has_colors = any(sku.get("sku") in colour_map for sku in skus_list)
        
        options = []
        if has_colors:
            options.append({"name": "Color"})

        for sku_info in skus_list:
            sku_code = sku_info.get("sku")
            color_name = colour_map.get(sku_code, "Default Title")
            
            variant = {
                "sku": sku_code,
                "price": "0.00",
                "inventory_management": "shopify",
                "inventory_policy": "deny"
            }
            
            # Map weight if we can calculate it? 
            # (Optional: Logic to calculate weight per unit could go here if critical)
            
            if has_colors:
                variant["option1"] = color_name
            
            variants.append(variant)

        product_payload = {
            "product": {
                "title": title,
                "body_html": body_html,
                "vendor": vendor,
                "product_type": product_type,
                "tags": ", ".join(tags),
                "variants": variants,
                "options": options,
                # "images": images
            }
        }

        response = self._request("POST", "products.json", json_data=product_payload)
        return response.get("product")
