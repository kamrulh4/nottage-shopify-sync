# Nottage-Shopify Sync

Automated inventory synchronization from Nottage to Shopify.

## Environment Variables

Required environment variables:
- `NOTTAGE_USER` - Nottage API username
- `NOTTAGE_PASS` - Nottage API password  
- `SHOPIFY_URL` - Shopify store URL (e.g., yourstore.myshopify.com)
- `SHOPIFY_TOKEN` - Shopify access token

## Deployment

### Deploy on Coolify

1. Create new application from this repository
2. Coolify auto-detects the Dockerfile
3. Add environment variables in Coolify dashboard
4. Set schedule: `*/5 * * * *` (every 5 minutes)
5. Deploy

### Local Development

```bash
# Set environment variables
export NOTTAGE_USER="your_user"
export NOTTAGE_PASS="your_pass"
export SHOPIFY_URL="yourstore.myshopify.com"
export SHOPIFY_TOKEN="your_token"

# Run once
python main.py
```

## Docker

```bash
# Build
docker build -t technase-sync .

# Run
docker run --rm \
  -e NOTTAGE_USER="your_user" \
  -e NOTTAGE_PASS="your_pass" \
  -e SHOPIFY_URL="yourstore.myshopify.com" \
  -e SHOPIFY_TOKEN="your_token" \
  technase-sync
```
