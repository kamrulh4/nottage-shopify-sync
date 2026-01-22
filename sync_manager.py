import logging
import time
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from nottage_client import NottageClient
from shopify_client import ShopifyClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SyncManager:
    def __init__(self, nottage_user, nottage_pass, shopify_url, shopify_token, item_numbers: List[str], max_workers=3):
        self.nottage = NottageClient(username=nottage_user, password=nottage_pass)
        self.shopify = ShopifyClient(shop_url=shopify_url, access_token=shopify_token)
        self.item_numbers = item_numbers
        self.max_workers = max_workers  # Number of concurrent threads (reduced to 3 for rate limits)

    def run_full_sync(self):
        logger.info("Starting Full Sync...")
        
        # 1. Fetch ALL Inventory Headers first (Lightweight)
        logger.info(f"Fetching inventory headers for {len(self.item_numbers)} items...")
        nottage_inventory_list = self.nottage.get_product_inventory(self.item_numbers)
        if not nottage_inventory_list:
            logger.error("No inventory data received. Aborting.")
            return

        # 2. Build Shopify Map
        logger.info("Fetching existing products from Shopify...")
        shopify_map = self.shopify.get_all_products_map() 
        # map: sku -> {product_id, variant_id, inventory_item_id}
        logger.info(f"Found {len(shopify_map)} variants in Shopify.")

        # 3. Process Each Nottage Item (Parent) - WITH THREADING
        logger.info(f"Processing items with {self.max_workers} concurrent threads...")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all items for processing
            future_to_item = {
                executor.submit(self._process_item, item_inv, shopify_map): item_inv
                for item_inv in nottage_inventory_list
            }
            
            # Process results as they complete
            for future in as_completed(future_to_item):
                item_inv = future_to_item[future]
                try:
                    future.result()  # This will raise any exceptions that occurred
                except Exception as e:
                    item_number = item_inv.get("itemNumber")
                    logger.error(f"Error processing item {item_number}: {e}")
                    
        logger.info("Sync Completed.")
    
    def _process_item(self, item_inv, shopify_map):
        """Process a single item (product creation + inventory sync)"""
        item_number = item_inv.get("itemNumber")
        skus_list = item_inv.get("listOfProductSKU", [])
        
        # Check if *any* SKU from this parent exists in Shopify
        existing_skus = [s for s in skus_list if s.get("sku") in shopify_map]
        
        if not existing_skus:
            logger.info(f"Item {item_number} (Parent) not found in Shopify. Creating fully...")
            # Fetch Rich Details
            details = self.nottage.get_product_details(item_number)
            if details:
                created_product = self.shopify.create_full_product(details, item_inv)
                if created_product:
                    logger.info(f"Created Product: {created_product.get('title')} (ID: {created_product.get('id')})")
                    # Update Map with new variants so we can sync stock immediately
                    for v in created_product.get("variants", []):
                        sku = v.get("sku")
                        if sku:
                            shopify_map[sku] = {
                                "product_id": created_product["id"],
                                "variant_id": v["id"],
                                "inventory_item_id": v["inventory_item_id"]
                            }
                else:
                    logger.error(f"Failed to create product {item_number}")
            else:
                logger.error(f"Could not fetch details for {item_number}. Skipping creation.")
        else:
            if len(existing_skus) < len(skus_list):
                logger.warning(f"Item {item_number}: Partial variants found in Shopify. Missing variants are NOT created automatically in this version.")
        
        # 4. Sync Inventory for ALL SKUs (Existing or Newly Created)
        for sku_data in skus_list:
            sku = sku_data.get("sku")
            qty = sku_data.get("available", 0)
            
            if sku in shopify_map:
                mapped = shopify_map[sku]
                self.shopify.update_inventory(mapped["inventory_item_id"], qty)
            else:
                # SKU still missing (e.g. failed creation or partial sync)
                logger.warning(f"SKU {sku} not in map, skipping inventory update.")
