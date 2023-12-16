import datetime
import random
from dotenv import load_dotenv
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
load_dotenv()

class CalendarGuild:
    def __init__(self, client, announcement_channel_id, schedule_old, schedule_even, quote_mapping):
        self.client = client
        self.announcement_channel_id = int(announcement_channel_id)
        self.weekly_count = 1

        self.schedule_old = schedule_old
        self.schedule_even = schedule_even
        self.quote_mapping = quote_mapping

        self.intents = commands.Bot(command_prefix='!', intents=client.intents)

    @tasks.loop(hours=4)
    async def update_activity(self):
        await self.set_activity_based_on_day()

    async def set_activity_based_on_day(self):
        channel = self.client.get_channel(self.announcement_channel_id)
        if channel:
            today = datetime.datetime.utcnow().date()
            weekday = today.strftime('%A')
            self.check_next_week(weekday)
            self.activities = self.get_activities_for_day(weekday)
            await channel.send(self.print_notification())
        else:
            print('No channel found.')
            return

    def get_activities_for_day(self, weekday):
        for item in self.schedule_old:
            if item['day'] == weekday:
                activities = item
        if int(self.weekly_count) % 2 == 0:
            for item in self.schedule_even:
                if item['day'] == weekday:
                    activities = item
        return activities
    
    def print_notification(self):
        todo_messages = '\n'.join([f"{item}" for item in self.activities["todo"]])
        return f'**Hoạt động ngày { self.activities["day_vn"] }:**\n```{ todo_messages }```\nMỗi ngày vài câu :kissing_smiling_eyes:\n> {random.choice(self.quote_mapping)}'

    def check_next_week(self, weekday):
        if weekday == 'Monday':
            self.weekly_count += float(1/6)

