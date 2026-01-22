import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Dictionary to store reminders: {user_id: {"interval": minutes, "task": asyncio.Task}}
reminders = {}


# Flask app for Render health checks (keeps bot alive)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_flask():
    """Run Flask server in a separate thread"""
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)


@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    print(f"🚀 Bot is ready!")


@bot.hybrid_command(name="water", description="Set a hydration reminder")
async def water(ctx, value: str = None):
    """
    Set, update, or remove a water reminder.
    Usage:
    /water <minutes> - Set reminder every X minutes
    /water remove - Remove the reminder
    """
    
    user_id = ctx.author.id
    
    # Check if command is valid
    if value is None:
        await ctx.send("❌ Please specify a value. Usage: `/water <minutes>` or `/water remove`")
        return
    
    # Handle remove command
    if value.lower() == "remove":
        if user_id in reminders:
            # Cancel existing task
            reminders[user_id]["task"].cancel()
            del reminders[user_id]
            await ctx.send("✅ Water reminder removed!")
        else:
            await ctx.send("❌ You don't have an active water reminder.")
        return
    
    # Handle setting/updating reminder
    try:
        interval = int(value)
        
        if interval <= 0:
            await ctx.send("❌ Please specify a positive number of minutes.")
            return
        
        # If user already has a reminder, cancel it
        if user_id in reminders:
            reminders[user_id]["task"].cancel()
            await ctx.send(f"🔄 Updating reminder from {reminders[user_id]['interval']} minutes to {interval} minutes.")
        else:
            await ctx.send(f"✅ Water reminder set! You'll receive reminders every {interval} minutes in your DMs.")
        
        # Create new reminder task
        task = asyncio.create_task(remind_water(ctx.author, interval))
        reminders[user_id] = {"interval": interval, "task": task}
        
    except ValueError:
        await ctx.send("❌ Please specify a valid number of minutes or use `/water remove`")


async def remind_water(user: discord.User, interval: int):
    """
    Send periodic water reminders to the user via DM.
    
    Args:
        user: The Discord user to send reminders to
        interval: Reminder interval in minutes
    """
    try:
        # Initial delay before first reminder
        await asyncio.sleep(interval * 60)
        
        while True:
            try:
                # Send DM reminder
                embed = discord.Embed(
                    title="💧 Water Reminder",
                    description="Time to drink water! Stay hydrated!",
                    color=discord.Color.blue(),
                    timestamp=datetime.now()
                )
                embed.set_footer(text=f"Reminder interval: {interval} minutes")
                
                await user.send(embed=embed)
                
                # Wait for next reminder
                await asyncio.sleep(interval * 60)
                
            except discord.errors.HTTPException:
                # User might have blocked DMs, remove reminder
                if user.id in reminders:
                    del reminders[user.id]
                break
            except asyncio.CancelledError:
                # Task was cancelled (reminder updated or removed)
                break
    
    except asyncio.CancelledError:
        pass


@bot.event
async def on_command_error(ctx, error):
    """Error handler for commands"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing argument. Usage: `/water <minutes>` or `/water remove`")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `/water` for hydration reminders.")
    else:
        await ctx.send(f"❌ An error occurred: {str(error)}")
        print(f"Error: {error}")


def main():
    """Start the bot"""
    # Load environment variables
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN environment variable not set!")
        print("Please set your bot token in Render environment variables.")
        return
    
    # Start Flask in background thread for health checks
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    try:
        print("🚀 Starting bot...")
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")


if __name__ == "__main__":
    main()
