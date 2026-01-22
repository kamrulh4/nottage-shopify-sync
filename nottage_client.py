
import requests
import base64
import json
import logging

logger = logging.getLogger(__name__)

class NottageClient:
    def __init__(self, username, password):
        self.base_url = "http://niconceptws.com/api/NottageECommerceApi"
        auth_string = f"{username}:{password}"
        # self.auth_token = base64.b64encode(auth_string.encode()).decode()
        self.auth_token = "dXNlcm5hbWU6cGFzc3dvcmQ="
        self.headers = {
            "Content-Type": "application/json",
            "x-auth-token": self.auth_token
        }
        self.username = username
        self.password = password

    def _post(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}"
        
        if isinstance(payload, dict):
            payload["username"] = self.username
            payload["password"] = self.password

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Ensure we return a dict even if "data" is missing or null
            return (data.get("data") if data else {}) or {}
        except requests.RequestException as e:
            logger.error(f"Nottage API Request Failed ({endpoint}): {e}")
            return {}

    def get_product_inventory(self, item_numbers: list):
        # API expects comma separated string? Or list?
        # test.py used: "itemNumber": "HS1024,HS1001"
        item_string = ",".join(item_numbers)
        payload = {
            "itemNumber": item_string
        }
        data = self._post("GetProductInventory", payload)
        return data.get("listOfProductInventory", [])

    def get_product_details(self, item_number: str):
        # Fetch detailed info for a single item (or list, but usually creation is 1 by 1)
        payload = {
            "itemNumber": item_number
        }
        data = self._post("GetProduct", payload)
        products = data.get("listOfProducts", [])
        if products:
            return products[0] # Return the first matching product details
        return None
