import pika
import logging
import time

class BasicMessageReceiver(object):
    def __init__(self, rabbitmq_broker, rabbitmq_user, rabbitmq_password ,callback, queue_name):
        self.parameters = pika.ConnectionParameters(
            host=rabbitmq_broker,
            credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password))
        self.queue_name = queue_name
        self.callback = callback
        
    
    def connect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)

    def listen(self):
        self.channel.basic_consume(self.queue_name,self.on_message)
        self.channel.start_consuming()

        
    def close(self):
        self.channel.close()
        self.connection.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        try:
            print(f'consuming message: {body}'
            self.callback(body)
            self.acknowledge_message(basic_deliver.delivery_tag)
        except Exception as e:
            print(e)

    def acknowledge_message(self, delivery_tag):
        print('Acknowledging message %s', delivery_tag)
        self.channel.basic_ack(delivery_tag)