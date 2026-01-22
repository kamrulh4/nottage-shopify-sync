import logging
from dotenv import load_dotenv
import time
import os
from sync_manager import SyncManager

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# -----------------------------
# CONFIGURATION
# -----------------------------
# Read from environment variables (for Coolify/Docker deployment)
NOTTAGE_USER = os.getenv("NOTTAGE_USER", "")
NOTTAGE_PASS = os.getenv("NOTTAGE_PASS", "")

SHOPIFY_URL = os.getenv("SHOPIFY_URL", "")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN", "")

# ITEM_NUMBERS = [
#     "HS1024", "HS1001", "HS1004", "HS1017", "HS1025", "HS1014", 
#     "EL026", "TL1003", "HS1008", "EL003", "DA1007"
# ]

ITEM_NUMBERS = [
    "HS1024", "HS1001", "HS1004", "HS1017", "HS1025",
    "EL003", "EL026", "TL1003", "HS1008", "HS1014",
    "DA1007", "EL011", "HS1015", "HS1022", "DA1015",
    "TK1048", "HS1018", "HS1012", "EL002", "HS1020",
    "TK1047", "AZ1006", "TK1067", "AZ1026", "AZ1028",
    "AZ1022", "TK1064", "AZ1014", "AZ1021", "TK1068",
    "AZ1029", "AZ1015", "AZ1019", "AZ1017", "AZ1024",
    "5263", "4075", "4073", "AZ1025", "4177",
    "TK1052", "HS1010", "7890", "PB1004", "7893",
    "PB1003", "HS1016", "TK1017", "GIFT1014",
    "TK1028", "4245", "HS1021", "TKC1005",
    "7763", "7766", "DA1017", "750"
]

def main():
    if SHOPIFY_TOKEN == "PASTE_TOKEN_HERE":
        print("ERROR: Please update main.py with the actual Shopify Access Token from auth_generator.py")
        return

    manager = SyncManager(
        nottage_user=NOTTAGE_USER, 
        nottage_pass=NOTTAGE_PASS, 
        shopify_url=SHOPIFY_URL, 
        shopify_token=SHOPIFY_TOKEN,
        item_numbers=ITEM_NUMBERS
    )
    
    print("Starting Nottage -> Shopify Sync...")
    manager.run_full_sync()
    print("Done.")

if __name__ == "__main__":
    main()
