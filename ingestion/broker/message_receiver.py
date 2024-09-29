import pika
import logging
import time
import json

class BasicMessageReceiver(object):
    def __init__(self, rabbitmq_broker, rabbitmq_user, rabbitmq_password):
        self.parameters = pika.ConnectionParameters(
            host=rabbitmq_broker,
            credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password))

        self.callbacks: dict = {}
        
    
    def connect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def declare_and_listen_queue(self, queue_name, callback):
        print(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(queue=queue_name)
        self.callbacks[queue_name] = callback

    def listen(self):
        for queue,callback in self.callbacks.items():
            self.channel.basic_consume(queue=queue,on_message_callback=self.on_message)
        self.channel.start_consuming()

        
    def close(self):
        self.channel.close()
        self.connection.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        source_queue = basic_deliver.routing_key
        try:
            print(f'consuming message: {body}')
            message = json.loads(body)
            self.callbacks[source_queue](message)
            self.acknowledge_message(basic_deliver.delivery_tag)
        except Exception as e:
            print(e)

    def acknowledge_message(self, delivery_tag):
        print('Acknowledging message %s', delivery_tag)
        self.channel.basic_ack(delivery_tag)