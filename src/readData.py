import json
import os
from dotenv import load_dotenv
load_dotenv()

def read_schedule():
    file_path = os.getenv('DIRECTORY_CALENDAR')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        schedule_old = data['odd']['calendar']
        schedule_even = data['even']['calendar']
    return schedule_old, schedule_even

def read_quotes():
    file_path = os.getenv('DIRECTORY_QUOTE')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def read_reply():
    file_path = os.getenv('DIRECTORY_REPLY')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data