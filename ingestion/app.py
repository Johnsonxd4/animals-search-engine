from broker.message_receiver import  BasicMessageReceiver
from config import Config

def teste(message):
    print(f'isso veio de lá da mensagem: {message}')
queue = 'animal_created'
receiver = BasicMessageReceiver(Config.BROKER_HOST,Config.BROKER_USERNAME,Config.BROKER_PASSWORD,teste,queue)
receiver.connect()
receiver.declare_queue(queue)
receiver.listen()