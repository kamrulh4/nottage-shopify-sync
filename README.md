# Nottage-Shopify Sync

Automated inventory synchronization from Nottage to Shopify.

## 🚀 Deploy on Coolify

See **[COOLIFY_DEPLOYMENT.md](COOLIFY_DEPLOYMENT.md)** for complete step-by-step deployment instructions.

**Quick Summary:**
1. Push code to Git
2. Create app in Coolify (auto-detects Dockerfile)
3. Add environment variables
4. Set schedule: `*/5 * * * *` (every 5 minutes)
5. Deploy!

## 🔧 Local Development

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run sync once
python main.py
```

## 📋 Environment Variables

- `NOTTAGE_USER` - Nottage API username
- `NOTTAGE_PASS` - Nottage API password
- `SHOPIFY_URL` - Shopify store URL
- `SHOPIFY_TOKEN` - Shopify access token

## 📁 Project Structure

- `main.py` - Entry point
- `sync_manager.py` - Sync orchestration
- `nottage_client.py` - Nottage API client
- `shopify_client.py` - Shopify API client
- `Dockerfile` - Containerization
- `requirements.txt` - Dependencies
