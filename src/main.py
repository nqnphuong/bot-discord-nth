# main.py
from discord.ext import commands
import discord
from Notification.calendarGuild import CalendarGuild
from Notification.callMember import CallMember
from AutoReply.reply import BotResponder
from readData import read_schedule, read_quotes, read_reply
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.presences = True
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.reactions = True

client = commands.Bot(command_prefix='!', intents=intents)
announcement_channel_id = os.getenv('DISCORD_ROOM_ID')
schedule_old, schedule_even = read_schedule()
quote_mapping = read_quotes()
reply_mapping = read_reply()

@client.event
async def on_ready():
    print('Bot is ready!')
    calendar_guild = CalendarGuild(client, announcement_channel_id, schedule_old, schedule_even, quote_mapping)
    calendar_guild.update_activity.start()
    callMember = CallMember(client, calendar_guild)
    callMember.call_members_before_event.start()

@client.event
async def on_message(message):
    print(message.author, message.content)
    if message.author == client.user:
        return
    if message.content.startswith('!cat/'):
        command = message.content.split(' ', 1)[1]
        bot_responder = BotResponder(reply_mapping)
        response = bot_responder.process_command(command)
        await message.channel.send(response)

# Run the bot
client.run(os.getenv('DISCORD_BOT_TOKEN'))
