import requests
import psutil
import time

TOKEN = '2090372641:AAHuhXyuHUBVqeAp_zq-GG-UK5nXsBM7zYw'
API_LINK = f'https://api.telegram.org/bot{TOKEN}'

updates = requests.get(API_LINK + '/getUpdates?offset=-1').json()
message = updates['result'][0]['message']
chat_id = message['from']['id']
text = message['text']


while True:
    cpu = psutil.cpu_percent(percpu=True)
    ram = psutil.virtual_memory()[2]


    def count_cpu(list_cpu):
        count = 0
        info = 'CPU utilization:\n'
        len_list_cpu = len(list_cpu)
        while len_list_cpu > count:
            info += f'Core {count + 1}: {list_cpu[count]}% \n'
            count += 1
        return info


    text_utilization = f'{count_cpu(cpu)}\nRAM utilization: {ram}%'
    send_message = requests.get(API_LINK + f'/sendMessage?chat_id={chat_id}&text={text_utilization}')
    time.sleep(3)
