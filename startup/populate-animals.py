import csv 
import requests 
import time

def already_seeded():
    time.sleep(10)
    response = requests.get('http://api:5000/animals')
    data = response.json()
    if len(data) > 199 and response.status_code == 200:
        return True
    return False

if  already_seeded():
    print('animals already inserted on database. No action needed')
else:
    with open('./animais_200_lista.csv',newline='') as csvfile:
        spamreader = csv.reader(csvfile,delimiter=',')
        for animal in  spamreader:
            print(f'posting animal: {animal}')
            response = requests.post('http://api:5000/animals', json={
                'name': animal[0],
                'specie': animal[1],
                'category': animal[2],
                'habitat': animal[3]
            })
            print(f'status: {response.status_code}')
            
            

