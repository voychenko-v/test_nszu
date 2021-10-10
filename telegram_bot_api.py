import requests
import psutil
import time
from datetime import datetime
import psycopg2
from psycopg2 import sql

conn = psycopg2.connect('postgres://postgres:passworddb@localhost:5432/info_utilization')
cursor = conn.cursor()

creator_utilization = sql.SQL('''
CREATE TABLE IF NOT EXISTS utilization (
    id_utilization SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    cpu_utilization TEXT NOT NULL,
    ram_utilization TEXT NOT NULL
    );
    ''')


with conn:
    cursor.execute(creator_utilization)


INSERT_UTILIZATION = sql.SQL('''INSERT INTO utilization (date, cpu_utilization, ram_utilization) 
                                VALUES (%s, %s, %s) RETURNING id_utilization''')

TOKEN = 'TOKEN'
API_LINK = f'https://api.telegram.org/bot{TOKEN}'
'''Реалізував безкінечний цикл для зручності. Вказав відправку кожні 5 сек. для зручності перевірки коду.'''


def count_cpu(list_cpu):
    count = 0
    info = 'CPU utilization:\n'
    len_list_cpu = len(list_cpu)
    while len_list_cpu > count:
        info += f'Core {count + 1}: {list_cpu[count]}% \n'
        count += 1
    return info


while True:
    dt = datetime.now()
    updates = requests.get(API_LINK + '/getUpdates?offset=-1').json()
    message = updates['result'][0]['message']
    chat_id = message['from']['id']
    text = message['text']
    if text == 'start':
        cpu = psutil.cpu_percent(percpu=True)
        ram = psutil.virtual_memory()[2]
        text_utilization = f'{count_cpu(cpu)}\nRAM utilization: {ram}%'
        send_message = requests.get(API_LINK + f'/sendMessage?chat_id={chat_id}&text={text_utilization}')
        with conn:
            cursor.execute(INSERT_UTILIZATION, (dt, cpu, ram))
        time.sleep(5)
    elif text == 'stop':
        time.sleep(3)
        continue
