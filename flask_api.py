from flask import Flask, request
import psycopg2
from psycopg2 import sql
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

conn = psycopg2.connect('postgres://postgres:passworddb@localhost:5432/info_utilization')
cursor = conn.cursor()


creator_service = sql.SQL('''
CREATE TABLE IF NOT EXISTS service (
    id_task SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    tag_data TEXT NOT NULL
    );
    ''')

with conn:
    cursor.execute(creator_service)

INSERT_SERVICE = sql.SQL('''INSERT INTO service (url, tag_data) 
VALUES (%s, %s) RETURNING id_task''')
SELECT_ID = sql.SQL('''SELECT tag_data FROM service WHERE id_task=(%s)''')
SELECT_UNIQUE_URL = sql.SQL('''SELECT DISTINCT url FROM service''')


#Функція для обробки тегів
def count_tag(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    body = len(soup.find_all('body'))
    h2 = len(soup.find_all('h2'))
    p = len(soup.find_all('p'))
    img = len(soup.find_all('img'))
    return f'body: {body}, h2: {h2}, p: {p}, img: {img}'


@app.route('/endpoint/tags', methods=['POST'])
def create_task():
    if request.method == 'POST':
        url_data = request.data.decode('UTF-8')
        url_check = requests.get(url_data)
        if url_check.status_code == 200:
            tag_data = count_tag(url_data)
            with conn:
                cursor.execute(INSERT_SERVICE, (url_data, tag_data))
                return_task = f'id_task: {cursor.fetchone()[0]}'
        else:
            return_task = f'Сталась помилка, код відповіді: {url_check.status_code}'
    return return_task


@app.route('/endpoint/tags/<int:id>', methods=['GET'])
def get_data(id):
    if request.method == 'GET':
        with conn:
            cursor.execute(SELECT_ID, (id, ))
            try:
                response_id = cursor.fetchone()[0]
            except TypeError:
                response_id = 'Сталась помилка, можливо Ви ввели неіснуючий ID'
        return response_id


@app.route('/endpoint/urls', methods=['GET'])
def unique_url():
    with conn:
        cursor.execute(SELECT_UNIQUE_URL)
        list_unique_url = cursor.fetchall()
        return_info = f'Унікальні URL:\n'
        count = 1
        for i in list_unique_url:
            return_info += f'{count}: {i[0]}\n'
            count += 1
    return f'{return_info}'


@app.route('/endpoint/stats', methods=['GET'])
def unique_data():
    return 1


if __name__ == '__main__':
    app.run(debug=True)
