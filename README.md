# test

## telegram_bot_api.py 
Телеграм бота на основі HTTP BOT API буде кожні N часу присилати повідомлення про стан загруженості кожного ядра
процесора (в відсотках) а також інформацію про загруженість оперативної памяті
для отримання інформації про стан ресурсів використовується бібліотека psutil
також бот записує отримані заміри в базу даних.

## flask_api.py
Cервіс на FLASK/Django реалізовує Rest API
1) при POST запиті на endpoint/tags з url веб сторінки в якості тіла сервіс пертає
ідентифікатор задачі
2) при GET запиті на endpoint/tags/<ідентифікатор задачі>; вертає підраховану
кількість html тегів які знаходяться на сторінці
приклад: {body: 1, h2: 1, p: 1, img: 2} або помилку якщо url вказує не на
html сторінку
3) при GET запиті на endpoint/urls вертає перелік унікальних url які були надані
сервісу
4) при GET запиті на endpoint/stats/ вертає json з даними які повинні містити :
кількість унікальних url, кількість задач, сумарну кількість по кожному типу тега

## Біблшотеки:
requests==2.26.0 |
psutil==5.8.0 |
psycopg2-binary==2.9.1 |
beautifulsoup4==4.10.0 |
Flask==2.0.2
