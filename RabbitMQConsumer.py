import pika
import json
from websocket import create_connection


ws = create_connection("ws://35.168.60.242:8000/ws/chat/TaskStore/")


def callback(ch, method, properties, body):
    print(body.decode("utf-8"), end="\n")
    data = json.loads(str(body.decode("utf-8")).replace('\'', '\"'))
    data['from'] = 'RabbitMQ'
    try:
        ws.send(str(data).replace('\'', '\"'))
    except:
        ws = create_connection("ws://35.168.60.242:8000/ws/chat/TaskStore/")
        ws.send(str(data).replace('\'', '\"'))


url = 'amqp://dqxicnva:hzg8PpxVCRpqUFiOVL5fWV0O-kW9kfnt@llama.rmq.cloudamqp.com/dqxicnva'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='Tasks')
channel.queue_purge(queue='Tasks')
channel.basic_consume(queue='Tasks', auto_ack=True,
                      on_message_callback=callback)
print("Starting to Consume on queue hello")
channel.start_consuming()
