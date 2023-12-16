import datetime
from discord.ext import tasks

class CallMember:
    def __init__(self, client, calendar_guild):
        self.client = client
        self.calendar_guild = calendar_guild

    @tasks.loop(minutes=5)
    async def call_members_before_event(self, minutes_before=10):
        today = datetime.datetime.utcnow().date()
        weekday = today.strftime('%A')
        activities = self.calendar_guild.get_activities_for_day(weekday)
        print("ủa sao không chạy")
        if activities:
            closest_event = None
            closest_time_difference = None
            for activity in activities['todo']:
                # tách thời gian và hoạt động đồng thời chuyển sang datetime object
                time_str, activity_str = activity.split(': ', 1)
                time_obj = self.convert_to_datetime(time_str)
                time_notification = time_obj - datetime.timedelta(minutes=minutes_before) # trừ đi 10 phút để thông báo
                
                if time_obj > datetime.datetime.now(): # tìm hd gần nhất
                    time_difference = time_obj - datetime.datetime.now()
                    if closest_time_difference is None or time_notification <= datetime.datetime.now(): 
                        closest_time_difference = time_difference 
                        closest_event = activity_str
                    break

            if closest_event:
                minutes_until_event = closest_time_difference.seconds // 60
                await self.client.get_channel(self.calendar_guild.announcement_channel_id).send(self.send_notification(minutes_until_event, closest_event))
                    

    def convert_to_datetime(self, time_str):
        time_obj = datetime.datetime.strptime(time_str, '%H:%M')
        time_obj = time_obj.replace(
            year=datetime.datetime.now().year,
            month=datetime.datetime.now().month,
            day=datetime.datetime.now().day
        )
        return time_obj
    

    def send_notification(self, minutes_until_event, activity):
        return f'<@{512116966320766976}> ơi! Còn {minutes_until_event} phút nữa là bắt đầu **{activity}**. Ai không đi xứng đáng bị trĩ c4'

