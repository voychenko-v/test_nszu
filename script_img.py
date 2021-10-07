import matplotlib.pyplot as plt
import numpy as np
from test_db import conn, cursor, SELECT_CPU

with conn:
    cursor.execute(SELECT_CPU)
    list_cpu = cursor.fetchall()

print(list_cpu)
print(list_cpu[0][0].strftime("%H:%M:%S"))

date_list = []
avg_cpu = []

for i in list_cpu:
    date_list.append(i[0].strftime("%H:%M:%S"))
    avg_cpu.append(i[1][1:-1])
    
print(date_list)
print(avg_cpu)

