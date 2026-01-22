# Discord Hydration Reminder Bot

A simple Discord bot that sends hydration (water) reminders at user-specified intervals. **Runs 24/7 on Render.**

## Features

✅ Set custom reminder intervals (in minutes)
✅ Update reminders by setting a new interval
✅ Remove reminders with `/water remove`
✅ Works in both DMs and server channels
✅ Sends all reminders to user DMs only
✅ Beautiful embedded reminder messages
✅ **Hosted on Render for 24/7 uptime**

## Quick Start - Deploy to Render (Recommended)

For 24/7 hosting with zero cost:

1. **Push to GitHub** (5 minutes)
   ```bash
   cd c:\Users\sidha\Documents\waterbot
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/waterbot.git
   git push -u origin main
   ```

2. **Deploy on Render** (2 minutes)
   - Go to https://render.com (sign up free)
   - Connect your GitHub repository
   - Add `DISCORD_TOKEN` environment variable
   - Click deploy!

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions.

## Local Development

### 1. Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "Water Bot")
3. Go to the "Bot" section and click "Add Bot"
4. Copy your bot token
5. Under "OAUTH2" → "URL Generator", select:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Send Messages in Threads`, `Embed Links`
6. Use the generated URL to invite the bot to your server

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:
```
DISCORD_TOKEN=your_bot_token_here
```

Or copy from example:
```bash
copy .env.example .env
# Then edit .env with your token
```

### 4. Run Locally

```bash
python bot.py
```

You should see:
```
✅ Bot logged in as YourBotName#1234
🚀 Bot is ready!
```

## Usage

### Set a Reminder
```
/water 30
```
Sends you a water reminder every 30 minutes in your DM.

### Update a Reminder
```
/water 60
```
If you already have a reminder, this updates the interval to 60 minutes.

### Remove a Reminder
```
/water remove
```
Cancels your active water reminder.

## Command Details

- **Location**: Works in both server channels and direct messages
- **Reminders**: All reminders are sent to your DM (even if you use the command in a server)
- **Multiple Users**: Each user can have their own independent reminder schedule
- **Update Behavior**: Setting a new interval automatically cancels the old one

## Technical Details

- Built with `discord.py` 2.3.2
- Uses `asyncio` for non-blocking reminder tasks
- Tracks reminders per user ID
- Flask web server for Render health checks
- Gracefully handles DM failures (removes reminder if user has DMs disabled)

## Project Structure

```
waterbot/
├── bot.py                    # Main bot code
├── requirements.txt          # Python dependencies
├── Procfile                  # For Render deployment
├── .env.example              # Environment variable template
├── config.py                 # Configuration template
├── README.md                 # This file
├── RENDER_DEPLOYMENT.md      # Detailed Render setup guide
└── .gitignore                # Git ignore rules
```

## Troubleshooting

**Bot not responding to commands?**
- Make sure the bot has the `Send Messages` permission
- Ensure you're using the correct prefix: `/` (slash commands)

**Not receiving DMs?**
- Check your Discord privacy settings allow DMs from server members
- The bot will automatically remove the reminder if it can't send DMs

**Bot crashes on startup?**
- Verify your token is correct
- Check your internet connection
- View Render logs if hosted there

**On Render - bot goes offline?**
- Check the Logs tab in Render dashboard
- Verify `DISCORD_TOKEN` environment variable is set correctly
- Restart the service from Render dashboard

## Security Note

Never share your bot token! Keep `config.py` and `.env` out of version control if they contain your real token.

## Support

For issues with:
- **Discord.py**: Check [documentation](https://discordpy.readthedocs.io/)
- **Render**: Check [Render docs](https://render.com/docs)
- **This bot**: Check code comments or create an issue
