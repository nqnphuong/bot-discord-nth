import discord
from discord.ext import tasks, commands
import datetime
import random
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.presences = True
intents.messages = True
intents.guilds = True
intents.reactions = True

client = commands.Bot(command_prefix='!', intents=intents)

# Định dạng lịch hoạt động
schedule_old = [
    {'day': 'Saturday', 'activities': ['7:00 PM: Bang chiến trận 1']},
    # Thêm các bước theo định dạng lịch của bạn
]

schedule_even = [
    {'day': 'Saturday', 'activities': ['7:30 PM: Bang chiến trận 2']},
    {'day': 'Sunday', 'activities': ['8:00 PM: Bang hoa']},
    # Thêm các bước theo định dạng lịch của bạn
]

quote_mapping = [
    'Nếu anh là hình thì em là bóng. Nếu anh là bóng thì mình là chị em',
    'Nghe nói anh có nụ cười tỏa nắng. Thật tình cờ em có chậu quần áo chưa phơi',
    'Nhan sắc là thứ có thì tốt, mà không có thì mình dùng filter',
    'Thằng toái mộng kia, mày cất cái skill hút cừu hận vào đi',
    'Trong tất cả các loại cà: cà pháo, cà rốt, cà chua, cà thẻ,… Em lại thích nhất Cà khịa',
    'Dậy sớm để thành công, không thành công thì mình thành thụ'
    'Khi nào chị Vân cưa được a Ly ?',
    'Tập thể dục ba năm không bằng nằm thêm một lúc'
]

day_mapping = {
    'Monday': 'Thứ 2',
    'Tuesday': 'Thứ 3',
    'Wednesday': 'Thứ 4',
    'Thursday': 'Thứ 5',
    'Friday': 'Thứ 6',
    'Saturday': 'Thứ 7',
    'Sunday': 'Chủ nhật'
}

# ID của kênh để gửi thông báo
announcement_channel_id = 1164461560744398880

weekly_count = 1

@client.event
async def on_ready():
    print('Bot is ready!')
    # Lập lịch để thiết lập lịch hoạt động mỗi ngày lúc 00:00 (UTC)
    update_activity.start()

@tasks.loop(hours=4)
async def update_activity():
    await set_activity_based_on_day()

async def set_activity_based_on_day():
    global weekly_count
    today = datetime.datetime.utcnow().date()
    weekday = today.strftime('%A')
    if weekday == 'Monday':
        weekly_count += float(1/6)
        print(f'Weekly count: {weekly_count}')
    print(f'Today is {weekday}.')
    activities = get_activities_for_day(weekday)
    weekday_vn = day_mapping.get(weekday, 'Không xác định')

    if activities:
        activity_message = "\n".join(activities)
        print(f'**Hoạt động ngày {weekday_vn}:**\n```{activity_message}```\nMỗi ngày vài câu::kissing_smiling_eyes:\n> {random.choice(quote_mapping)}')
    else:
        activity_message = 'Không có hoạt động nào được lên lịch cho ngày hôm nay.'
        print('Không có hoạt động nào được lên lịch cho ngày hôm nay.')
    
    # Gửi thông báo đến kênh đã chọn
    channel = client.get_channel(announcement_channel_id)
    await channel.send(f'**Hoạt động ngày {weekday_vn}:**\n```{activity_message}```\nMỗi ngày vài câu::kissing_smiling_eyes:\n> {random.choice(quote_mapping)}')


def get_activities_for_day(weekday):
    activities = []
    for item in schedule_old:
        if item['day'] == weekday:
            activities += item['activities']
    if int(weekly_count) % 2 == 0:
        for item in schedule_even:
            if item['day'] == weekday:
                activities += item['activities']
    return activities

# Đăng nhập bằng token
client.run(os.getenv('DISCORD_BOT_TOKEN'))  # Thay thế bằng token của bạn
