import discord
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug print to check if Railway is reading the variables
print(f"🔍 DEBUG: DISCORD_BOT_TOKEN: {os.getenv('DISCORD_BOT_TOKEN')}")
print(f"🔍 DEBUG: MENTION_LOG_CHANNEL_ID: {os.getenv('MENTION_LOG_CHANNEL_ID')}")
print(f"🔍 DEBUG: USER_TO_TRACK_ID: {os.getenv('USER_TO_TRACK_ID')}")

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
MENTION_LOG_CHANNEL_ID = os.getenv("MENTION_LOG_CHANNEL_ID")
USER_TO_TRACK_ID = os.getenv("USER_TO_TRACK_ID")

if not TOKEN or not MENTION_LOG_CHANNEL_ID or not USER_TO_TRACK_ID:
    print("❌ ERROR: One or more environment variables are missing.")
    exit(1)

MENTION_LOG_CHANNEL_ID = int(MENTION_LOG_CHANNEL_ID)  # Convert to integer
USER_TO_TRACK_ID = int(USER_TO_TRACK_ID)  # Convert to integer

# Enable intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot client
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    print(f'🔎 Tracking mentions of user ID: {USER_TO_TRACK_ID}')

@bot.event
async def on_message(message):
    """Only process messages that contain mentions"""
    if message.author == bot.user or not message.mentions:
        return  # Ignore bot messages and messages without mentions

    # Check if the tracked user is mentioned
    if any(mention.id == USER_TO_TRACK_ID for mention in message.mentions):
        print("🔔 Tracked user was mentioned!")  # Debug log

        log_channel = bot.get_channel(MENTION_LOG_CHANNEL_ID)
        if log_channel:
            # Generate a clickable message link
            message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"

            embed = discord.Embed(
                title="🔔 You Were Mentioned!",
                description=message.content,
                color=discord.Color.blue()
            )
            embed.add_field(name="Jump to Message", value=f"[Click here]({message_link})", inline=False)
            embed.set_footer(text=f"By {message.author} in #{message.channel.name}")
            embed.timestamp = message.created_at

            await log_channel.send(embed=embed)
            print("✅ Mention logged successfully.")
        else:
            print(f"❌ ERROR: Could not find log channel with ID {MENTION_LOG_CHANNEL_ID}")

# Run bot
bot.run(TOKEN)