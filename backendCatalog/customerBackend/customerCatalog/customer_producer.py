import json
import pika
from pika.exchange_type import ExchangeType

class RabbitMQProducer:
    def __init__(self, exchange_name='', routing_key='', queue='', host='localhost'):
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=ExchangeType.fanout)

    def publish(self, event_type, message):
        properties = pika.BasicProperties(content_type=event_type,delivery_mode=2)
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.routing_key, 
                                   body=json.dumps(message), properties=properties)

    def close(self):
        self.connection.close()

