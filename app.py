import os
import logging
import threading
from datetime import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv
from utils.sync_manager import SyncManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
NOTTAGE_USER = os.getenv("NOTTAGE_USER", "")
NOTTAGE_PASS = os.getenv("NOTTAGE_PASS", "")
SHOPIFY_URL = os.getenv("SHOPIFY_URL", "")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN", "")

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

# State tracking
sync_status = {"status": "idle", "last_run": None, "error": None}

def run_sync_task():
    global sync_status
    try:
        sync_status["status"] = "running"
        sync_status["error"] = None
        
        manager = SyncManager(
            nottage_user=NOTTAGE_USER, 
            nottage_pass=NOTTAGE_PASS, 
            shopify_url=SHOPIFY_URL, 
            shopify_token=SHOPIFY_TOKEN,
            item_numbers=ITEM_NUMBERS
        )
        
        logger.info("Starting Flask-based background sync...")
        manager.run_full_sync()
        
        sync_status["status"] = "completed"
        sync_status["last_run"] = datetime.now().isoformat()
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        sync_status["status"] = "failed"
        sync_status["error"] = str(e)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Nottage-Shopify Sync Flask API", "status": sync_status})

@app.route('/sync', methods=['GET'])
def trigger_sync():
    if sync_status["status"] == "running":
        return jsonify({"message": "Sync is already in progress"}), 409
    
    # Run in a separate thread so the request returns immediately
    thread = threading.Thread(target=run_sync_task)
    thread.start()
    
    return jsonify({"message": "Sync started in background"}), 202

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(sync_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
