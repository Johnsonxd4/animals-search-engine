import ssl
import pika

class Client:
    def __init__(self, rabbitmq_broker, rabbitmq_user, rabbitmq_password):
        url = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker}:5672"
        parameters = pika.URLParameters(url)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()