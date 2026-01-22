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
@app_commands.describe(value="Minutes between reminders, or 'remove' to stop")
async def water(interaction: discord.Interaction, value: str):
    
    user_id = interaction.user.id
    
    if value.lower() == "remove":
        if user_id in reminders:
            reminders[user_id]["task"].cancel()
            del reminders[user_id]
            await interaction.response.send_message("✅ Water reminder removed!")
        else:
            await interaction.response.send_message("❌ You don't have an active water reminder.")
        return
    
    try:
        interval = int(value)
        
        if interval <= 0:
            await interaction.response.send_message("❌ Please specify a positive number of minutes.")
            return
        
        if user_id in reminders:
            reminders[user_id]["task"].cancel()
            await interaction.response.send_message(f"🔄 Updating reminder from {reminders[user_id]['interval']} minutes to {interval} minutes.")
        else:
            await interaction.response.send_message(f"✅ Water reminder set! You'll receive reminders every {interval} minutes in your DMs.")
        
        task = asyncio.create_task(remind_water(interaction.user, interval))
        reminders[user_id] = {"interval": interval, "task": task}
        
    except ValueError:
        await interaction.response.send_message("❌ Please specify a valid number of minutes or use 'remove'")


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
                embed.set_footer(text=f"Reminder interval: {interval} minutes")
                
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
