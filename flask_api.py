from flask import Flask, request, jsonify
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
    body INTEGER NOT NULL,
    h2 INTEGER NOT NULL,
    p INTEGER NOT NULL,
    img INTEGER NOT NULL
    );
    ''')

with conn:
    cursor.execute(creator_service)

INSERT_SERVICE = sql.SQL('''INSERT INTO service (url, body, h2, p, img) 
                            VALUES (%s, %s, %s, %s, %s) RETURNING id_task''')
SELECT_ID = sql.SQL('''SELECT url, body, h2, p, img FROM service WHERE id_task=(%s)''')
SELECT_UNIQUE_URL = sql.SQL('''SELECT DISTINCT url FROM service''')
SELECT_STATS = sql.SQL('''SELECT COUNT(DISTINCT url), COUNT(id_task),
                          SUM(body), SUM(h2), SUM(p), SUM(img) FROM service''')


#Функція для обробки тегів
def count_tag(url):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    body = len(soup.find_all('body'))
    h2 = len(soup.find_all('h2'))
    p = len(soup.find_all('p'))
    img = len(soup.find_all('img'))
    tag_count_list = [body, h2, p, img]
    return tag_count_list


@app.route('/endpoint/tags', methods=['POST'])
def create_task():
    if request.method == 'POST':
        url_data = request.data.decode('UTF-8')
        url_check = requests.get(url_data)
        if url_check.status_code == 200:
            list_data = count_tag(url_data)
            with conn:
                cursor.execute(INSERT_SERVICE, (url_data, list_data[0], list_data[1], list_data[2], list_data[3]))
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
                response_tuple = cursor.fetchone()
                response_id = {'body': response_tuple[1], 'h2': response_tuple[2],
                               'p': response_tuple[3], 'img': response_tuple[4]}
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
    if request.method == 'GET':
        with conn:
            cursor.execute(SELECT_STATS)
            data = cursor.fetchone()
            dict_data = {'unique_url': data[0],
                         'count_task': data[1],
                         'count_body': data[2],
                         'count_h2': data[3],
                         'count_p': data[4],
                         'count_img': data[5]}
    return jsonify(dict_data)


if __name__ == '__main__':
    app.run(debug=True)