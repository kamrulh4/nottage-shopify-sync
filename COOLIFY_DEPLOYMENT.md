# Coolify Deployment Guide

## Quick Setup (5 Minutes)

This guide shows you how to deploy your Nottage-Shopify sync script on Coolify to run automatically every 5 minutes.

---

## Step 1: Push Your Code to Git

```bash
cd /Users/kamrul/Desktop/Projects/technase
git add .
git commit -m "Ready for Coolify deployment"
git push origin main
```

---

## Step 2: Create Resource in Coolify

1. **Login to your Coolify dashboard**
2. **Create New Resource**
   - Click **"+ New"** → **"Docker Compose"**
   - Select your Git repository
   - Select branch: `development` (or your preferred branch)
   - Coolify will load your `docker-compose.yml`

3. **Configure Settings**
   - Ensure the **"Restart Policy"** in Coolify is NOT set to "Always". 
   - Since we have `restart: "no"` in `docker-compose.yml`, it will run once and then stop properly.

---

## Step 3: Set Environment Variables

In your application settings, go to **Environment Variables** section and add:

```env
NOTTAGE_USER=
NOTTAGE_PASS=
SHOPIFY_URL=
SHOPIFY_TOKEN=
NOTTAGE_AUTH_TOKEN=
```

> **⚠️ Important**: 
> 1. Use **six** dollar signs (`$$$$$$`) for the password to escape them in Coolify.
> 2. `NOTTAGE_AUTH_TOKEN` is optional, it defaults to the token you provided.

---

## Step 4: Configure Scheduled Execution (Every 5 Minutes)

1. Go to your application → **Settings** → **Scheduled Tasks**
2. Click **"Add Scheduled Task"**
3. Configure:
   - **Name**: `sync-inventory`
   - **Schedule (Cron)**: `*/5 * * * *`
   - **Command**: `docker start technase-sync` (or whatever your container name is)
4. **Save** and enable.

---

## Why use Docker Compose?

Using Docker Compose is better because:
- ✅ **No Infinite Loop**: We set `restart: "no"`, so it stops after sync.
- ✅ **Environment Control**: All variables are passed clearly.
- ✅ **Volume Support**: Logs are saved to a persistent volume.


---

## Step 5: Deploy & Monitor

1. Click **"Deploy"** button in Coolify
2. Wait for build to complete (1-2 minutes)
3. Check **Logs** tab to verify first run
4. Monitor subsequent runs every 5 minutes

---

## Verification

After deployment, verify everything is working:

1. **Check Logs** in Coolify dashboard
   - You should see sync activity
   - Look for successful API calls

2. **Verify Shopify Inventory**
   - Login to Shopify Admin
   - Check products listed in your `ITEM_NUMBERS`
   - Confirm inventory quantities are updating

3. **Wait 10-15 Minutes**
   - Let it run 2-3 cycles
   - Verify automated execution is working

---

## Troubleshooting

### Container Exits Immediately
- **Expected behavior** if using scheduled tasks
- Coolify will restart it on schedule

### Environment Variables Not Working
- Check they're set in Coolify's environment section
- Make sure there are no trailing spaces
- Restart the deployment after adding variables

### Sync Not Running Every 5 Minutes
- Verify cron schedule: `*/5 * * * *`
- Check Coolify's scheduled tasks are enabled
- Review application logs for errors

---

## Architecture

```
Coolify Scheduler (every 5 min)
         ↓
  Docker Container Starts
         ↓
    main.py executes
         ↓
  Sync Nottage → Shopify
         ↓
  Container Exits (Success)
         ↓
  Wait for next schedule...
```

This is the **cleanest approach** - container does one job and exits. Coolify handles all scheduling.

---

## Next Steps

- ✅ Deployment complete
- ✅ Automated sync every 5 minutes
- ✅ Monitor logs in Coolify dashboard
- 📊 Set up monitoring/alerting (optional)
- 🔔 Configure notifications for failures (optional)
