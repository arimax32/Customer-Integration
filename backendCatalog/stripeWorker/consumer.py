import stripe
import threading
import pika
import json
import signal
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("API_KEY")

class RabbitMQConsumer():
    def __init__(self, exchange_name = '', queue = ''):
        # threading.Thread.__init__(self)

        self.exchange_name = exchange_name
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        self.channel.queue_declare(queue=self.queue, exclusive=False,durable=True)
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue)

        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        
    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)

            if properties.content_type == "user_created":
                self.create_customer(message['id'], message['name'], message['email'])

            elif properties.content_type == "user_updated":
                self.update_customer(message['name'], message['old-email'], message['email'])
            
            elif properties.content_type == "user_deleted":
                self.delete_customer(message['email'])

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except:
            print("Consumer process couldn't execute the message")

    def close(self):
        self.connection.close()

    def create_customer(self, id, name, email):
        customer = stripe.Customer.create(
            name=name,
            email=email,
            metadata={"product_id" : id}
        )
        return customer
    
    def update_customer(self, name, old_email, email):
        stripe_id = self.retreiveStripeId(old_email)
        updated_customer = stripe.Customer.modify(
            stripe_id,
            name = name,
            email = email,
        )
        return updated_customer

    def delete_customer(self, email):
        stripe_id = self.retreiveStripeId(email)
        stripe.Customer.delete(stripe_id)

    def start(self):
        print ('Stripe worker started')
        self.channel.start_consuming()
    
    def retreiveStripeId(self,email):
        customer = stripe.Customer.list(email = email)
        return customer['data'][0]['id']


if __name__ == "__main__":
    stripe_consumer = RabbitMQConsumer(exchange_name="customerCatalog",queue='Stripe Service')
    stripe_consumer.start()