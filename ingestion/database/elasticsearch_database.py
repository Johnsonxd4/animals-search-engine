from datetime import datetime
from elasticsearch import Elasticsearch
class ElasticSearchDatabase:
    def __init__(self, url):
        self.client = Elasticsearch(url)

    def create_animal(self,animal):
        resp = self.client.index(index="animals", id=animal['id'], document=animal)
        print(resp['result'])
        print(f'animal {animal} created on elastic search')

    def update_animal(self,animal):
        resp = self.client.update(index="animals", id=animal['id'], doc=animal)
        print(resp['result'])
        print(f'Chamou o update correto !!!!!!!!!!!!!!')