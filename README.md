# Customer Integration

This project manages a customer catalog on the backend with other external services through a message broker, in our case RabbitMQ.

## Running the entire customer sync workflow

1. Start the RabbitMQ server first.
2. Start the Django server on `localhost:8000` which will run the producer and the Django server making sure the MySQL DB is already connected.
3. Then start the `consumer.py` file present in `backendCatalog/StripeWorker` which will start the consumer process to listen to messages from the RabbitMQ server.
4. Create a webhook in Stripe that notifies the webhook listener endpoint `stripe_webhook/` in the backend server.
5. Create a URL using ngrok that will be passed on to Stripe for setting up the webhook and also add it to the `ALLOWED_HOSTS` list in Django `settings.py` along with `127.0.0.1` (localhost).
6. Changes to the MySQL DB are made through a REST API that does CRUD operations on the database.

## Handling integrations with Salesforce customers

1. We would have to create another `SalesforceWorker/consumer.py` file that would listen to messages from the queue and do the same.
2. Specifically for such processes even in the current code with Salesforce integration we have set the exchange type for RabbitMQ as `fanout` wherein the message is given to all the consumers bound to the particular exchange in RabbitMQ and would also create a separate queue for Salesforce messages too.

## To extend the integrations with your product’s customer catalog to support other systems

1. We would create a new module for that system's consumer file which will pop messages from its queue and update their system.
2. We could also start each of these separate consumer files corresponding to these external systems as threads for more efficient working.