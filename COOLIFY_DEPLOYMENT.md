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

## Step 2: Create Application in Coolify

1. **Login to your Coolify dashboard**
   - Go to your VPS IP or domain where Coolify is installed

2. **Create New Resource**
   - Click **"+ New"** → **"Application"**
   - Select **"Public Repository"** or connect your GitHub/GitLab account
   - Enter your repository URL
   - Select branch: `main` (or your default branch)

3. **Configure Build Settings**
   - Coolify will auto-detect the `Dockerfile`
   - Build Method: **Dockerfile**
   - No changes needed - Coolify handles it automatically

---

## Step 3: Set Environment Variables

In your application settings, go to **Environment Variables** section and add:

```env
NOTTAGE_USER=
NOTTAGE_PASS=
SHOPIFY_URL=
SHOPIFY_TOKEN=
```

> **⚠️ Important**: Replace these with your actual credentials if different!

---

## Step 4: Configure Scheduled Execution

Coolify has built-in support for scheduled tasks. Here's how to set it up:

### Option A: Using Coolify's Scheduled Tasks (Recommended)

1. Go to your application → **Settings** → **Scheduled Tasks**
2. Click **"Add Scheduled Task"**
3. Configure:
   - **Schedule (Cron)**: `*/5 * * * *` (every 5 minutes)
   - **Command**: Leave empty (uses default CMD from Dockerfile)
   - **Container**: Select your app container

4. **Save** and enable the scheduled task

### Option B: Deploy as Service + External Cron

If Coolify doesn't have scheduled tasks feature in your version:

1. Deploy the application normally (it will run once and exit)
2. SSH into your VPS:
   ```bash
   ssh root@your-vps-ip
   ```

3. Find your container name:
   ```bash
   docker ps -a | grep technase
   ```

4. Add cron job:
   ```bash
   crontab -e
   ```
   
   Add this line:
   ```
   */5 * * * * docker start <your-container-name> >> /var/log/technase-sync.log 2>&1
   ```

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
