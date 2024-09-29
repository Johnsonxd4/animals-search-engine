import csv 
import requests 
import time

def constantly_updates():
    response = requests.get('http://api:5000/animals')
    data = response.json()
    for item in data:
        time.sleep(3)
        response = requests.put(f'http://api:5000/animals/{item['id']}', json=item)
    
while True:
    constantly_updates()