import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

reminders = {}


app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running!", 200

def run_flask():
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot logged in as {bot.user}")
    print(f"🚀 Bot is ready!")


@bot.tree.command(name="water", description="Set a hydration reminder")
@app_commands.describe(minutes="How many minutes between each reminder")
async def water(interaction: discord.Interaction, minutes: int):
    
    user_id = interaction.user.id
    
    if minutes <= 0:
        await interaction.response.send_message("❌ Please specify a positive number of minute(s).")
        return
    
    if user_id in reminders:
        reminders[user_id]["task"].cancel()
        await interaction.response.send_message(f"🔄 Updating reminder from {reminders[user_id]['interval']} minute(s) to {minutes} minute(s).")
    else:
        await interaction.response.send_message(f"✅ Water reminder set! You'll receive reminders every {minutes} minute(s) in your DMs.")
    
    task = asyncio.create_task(remind_water(interaction.user, minutes))
    reminders[user_id] = {"interval": minutes, "task": task}


@bot.tree.command(name="water-remove", description="Remove your water reminder")
async def water_remove(interaction: discord.Interaction):
    
    user_id = interaction.user.id
    
    if user_id in reminders:
        reminders[user_id]["task"].cancel()
        del reminders[user_id]
        await interaction.response.send_message("✅ Water reminder removed!")
    else:
        await interaction.response.send_message("❌ You don't have an active water reminder.")



async def remind_water(user: discord.User, interval: int):
    try:
        await asyncio.sleep(interval * 60)
        
        while True:
            try:
                embed = discord.Embed(
                    title="💧 Water Reminder",
                    description="Time to drink water! Stay hydrated!",
                    color=discord.Color.blue(),
                    timestamp=datetime.now()
                )
                embed.set_footer(text=f"Reminder interval: {interval} minute(s)")
                
                await user.send(embed=embed)
                
                await asyncio.sleep(interval * 60)
                
            except discord.errors.HTTPException:
                if user.id in reminders:
                    del reminders[user.id]
                break
            except asyncio.CancelledError:
                break
    
    except asyncio.CancelledError:
        pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing argument.")
    else:
        print(f"Error: {error}")


def main():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    if not TOKEN:
        print("❌ Error: DISCORD_TOKEN environment variable not set!")
        print("Please set your bot token in Render environment variables.")
        return
    
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    try:
        print("🚀 Starting bot...")
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")


if __name__ == "__main__":
    main()
