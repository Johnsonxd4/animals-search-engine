from broker.message_receiver import  BasicMessageReceiver
from config import Config
from database.elasticsearch_database import ElasticSearchDatabase

animal_created_queue = 'animal_created'
animal_updated_queue  = 'animal_updated'
database = ElasticSearchDatabase(Config.ELASTICSEARCH_CONNSTRING)
receiver = BasicMessageReceiver(Config.BROKER_HOST,Config.BROKER_USERNAME,Config.BROKER_PASSWORD)
receiver.connect()
receiver.declare_and_listen_queue(animal_created_queue, database.create_animal)
receiver.declare_and_listen_queue(animal_updated_queue, database.update_animal)
receiver.listen()