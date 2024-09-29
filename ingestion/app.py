from broker.message_receiver import  BasicMessageReceiver
from config import Config
from database.elasticsearch_database import ElasticSearchDatabase

queue = 'animal_created'
database = ElasticSearchDatabase(Config.ELASTICSEARCH_CONNSTRING)
receiver = BasicMessageReceiver(Config.BROKER_HOST,Config.BROKER_USERNAME,Config.BROKER_PASSWORD,database.create_animal,queue)
receiver.connect()
receiver.declare_queue(queue)
receiver.listen()