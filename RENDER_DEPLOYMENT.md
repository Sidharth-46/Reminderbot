# Deploy Discord Hydration Bot to Render (24/7)

A complete guide to host your water reminder bot on Render for 24/7 uptime.

## Prerequisites

- GitHub account (to host your code)
- Render account (free tier available at https://render.com)
- Discord bot token (from Discord Developer Portal)

## Step 1: Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name it "Water Bot"
3. Go to "Bot" section and click "Add Bot"
4. Click "Reset Token" and copy your bot token
5. Enable these Intents:
   - Message Content Intent
   - Server Members Intent
6. Go to "OAuth2" → "URL Generator":
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Send Messages in Threads`, `Embed Links`, `Read Message History`
7. Copy the generated URL and open it in browser to invite bot to your server

## Step 2: Push Code to GitHub

1. Go to https://github.com/new and create a new repository named "waterbot"
2. In your local terminal, navigate to your waterbot folder:
   ```bash
   cd c:\Users\sidha\Documents\waterbot
   git init
   git add .
   git commit -m "Initial commit: Water reminder bot"
   git remote add origin https://github.com/YOUR_USERNAME/waterbot.git
   git branch -M main
   git push -u origin main
   ```

## Step 3: Deploy to Render

1. Go to https://render.com and sign up (free)
2. Click "New +" and select "Web Service"
3. Select "Connect a repository" and authorize GitHub
4. Select your "waterbot" repository
5. Fill in the configuration:
   - **Name**: `waterbot` (or your preference)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you (e.g., Ohio, Frankfurt, Singapore)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: Choose "Free" tier

6. Under "Advanced":
   - Click "Add Environment Variable"
   - **Key**: `DISCORD_TOKEN`
   - **Value**: Paste your bot token from Discord Developer Portal
   
7. Click "Create Web Service"

✅ Your bot is now deploying! It will be live within 1-2 minutes.

## Step 4: Monitor Your Bot

1. On Render dashboard, click your service
2. Check "Logs" tab to see bot activity
3. Look for messages like:
   ```
   ✅ Bot logged in as YourBotName#1234
   🚀 Bot is ready!
   ```

## How It Stays Active 24/7

- **Procfile**: Tells Render to run Python bot
- **Flask Health Check**: Bot runs internal web server on port 8000
- **Render Worker**: Keeps the process running continuously
- **No Idle Timeout**: Worker dynos don't sleep on Render's free tier

## Testing the Bot

In your Discord server or DM with the bot:

```
/water 5
```

You should get a response: "✅ Water reminder set! You'll receive reminders every 5 minutes in your DMs."

In 5 minutes, you'll receive a DM with the water reminder!

## Updating Your Bot

To update the code:

1. Make changes locally
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```
3. Render automatically redeploys when you push to main branch

## Stopping the Bot

Go to Render dashboard → Your service → Click "Suspend" at the bottom

## Troubleshooting

**Bot not responding to commands:**
- Check Render logs for errors
- Verify bot has proper permissions in Discord server
- Make sure DISCORD_TOKEN environment variable is set

**Getting "Bot is offline" in Discord:**
- Check Render logs - look for connection errors
- Verify your bot token is correct
- Check Discord status page for outages

**Bot crashes after deployment:**
- View logs in Render dashboard
- Common issues:
  - Missing DISCORD_TOKEN environment variable
  - Outdated dependencies in requirements.txt

## Maintenance

The bot requires minimal maintenance:
- Render handles server uptime
- Bot automatically recovers from Discord connection issues
- Memory usage is minimal (under 50MB typically)

## Cost

Render's free tier includes:
- 750 hours per month of free web service runtime
- Enough for running 1 bot 24/7 (744 hours/month)
- Shared CPU resources
- No credit card required initially

## Next Steps

Consider enhancing your bot:
- Add database to persist user preferences
- Add `/water stats` command for hydration tracking
- Add role-based reminders for server members
- Add `/water list` to show all active reminders
