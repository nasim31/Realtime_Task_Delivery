from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import pika
from websocket import create_connection
import psycopg2
from psycopg2.extras import RealDictCursor



engine = psycopg2.connect(
    database="akshatProject",
    user="akshat",
    password="akshat1234",
    host="project.c55dan5ybmd7.us-east-1.rds.amazonaws.com",
    port='5432'
)

def callback(ch, method, properties, body):
    print(body.decode("utf-8"), end="\n")


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

     
    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if(text_data_json['from'] == 'Store'):
            if(text_data_json['message']=='Refresh Task'):
                cur = engine.cursor(cursor_factory=RealDictCursor)
                cur.execute("select * from task where task_status = 'New' order by  creation_date , priority  desc limit 1; ")
                res = cur.fetchall()
                cur.close()
               
                if(len(res)>0):
                    
                    self.send(text_data=json.dumps({
                        'message': "Next High Task",
                        'title': str(res[0]['title']),
                        'priority': str(res[0]['priority']),
                        'creationDate': str(res[0]['creation_date']),
                        'task_status': str(res[0]['task_status']),
                        'acceptedBy': str(res[0]['acceptedby']),
                        'createdby' : str(res[0]['createdby'])
                    }))
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                        'type': 'chat_message',
                        'message': "Next High Task",
                        'title': str(res[0]['title']),
                        'priority': str(res[0]['priority']),
                        'creationDate': str(res[0]['creation_date']),
                        'task_status': str(res[0]['task_status']),
                        'acceptedBy': str(res[0]['acceptedby']),
                         'createdby' : str(res[0]['createdby'])
                    }
                    )
                else:
                   
                    self.send(text_data=json.dumps({
                        'message': "Next High Task",
                        'title': '',
                        'priority': '',
                        'creationDate': '',
                        'task_status': '',
                        'acceptedBy': '',
                        'createdby' : ''
                    }))
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                        'type': 'chat_message',
                        'message': "Next High Task",
                        'title': '',
                        'priority': '',
                        'creationDate': '',
                        'task_status': '',
                        'acceptedBy': '',
                        'createdby' : ''
                    }
                    )

            else:
                url = 'amqp://dqxicnva:hzg8PpxVCRpqUFiOVL5fWV0O-kW9kfnt@llama.rmq.cloudamqp.com/dqxicnva'
                params = pika.URLParameters(url)
                connection = pika.BlockingConnection(params)
                channel = connection.channel()
                channel.basic_publish(exchange='', routing_key='Tasks', body=str(
                    text_data_json).replace('\"', '\''))
                connection.close()
                cur = engine.cursor()
                cur.execute("insert into task (title,priority,creation_date,createdby,task_status) values ('"+text_data_json['title']+"','"+text_data_json['Priority']+"','"+text_data_json['creationDate']+"','"+text_data_json['createdBy']+"','New')")
                engine.commit()
                cur.close()
                # pika.close()
               
        elif(text_data_json['from'] == 'RabbitMQ'):
            print("new Task is here from RabbitMQ")
            message = text_data_json['message']
            title = text_data_json['title']
            priority = text_data_json['Priority']
            creationDate = text_data_json['creationDate']
            by = text_data_json['acceptedBy']
            createdby = text_data_json['createdBy']
            Status = text_data_json['task_status']
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'title': title,
                    'priority': priority,
                    'creationDate': creationDate,
                    'task_status': Status,
                    'acceptedBy': by,
                    'createdby':createdby
                }
            )
        elif(text_data_json['from'] == 'DeliveryAgent'):
            if (text_data_json['message']=='Task Update'):
                
                if(text_data_json['Status']=='New'):
                    cur = engine.cursor()
                    cur.execute("update task set task_status='"+str(text_data_json['Status'])+"' , acceptedby = NULL where title = '"+str(text_data_json['title'])+"'")
                    engine.commit()
                    cur.close()
                    async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                            'type': 'chat_message',
                            'message': 'DeclinedNotification',
                            'title': text_data_json['title'],
                            'priority': '',
                            'creationDate': '',
                            'task_status': '',
                            'acceptedBy': text_data_json['acceptedBy'],
                            'createdby':text_data_json['createdby']
                        }
                        )
                else:
                    cur = engine.cursor()
                    cur.execute("update task set task_status='"+str(text_data_json['Status'])+"' , acceptedby = '"+str(text_data_json['acceptedBy'])+"' where title = '"+str(text_data_json['title'])+"'")
                    engine.commit()
                    cur.close()
                    async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                            'type': 'chat_message',
                            'message': '',
                            'title': '',
                            'priority': '',
                            'creationDate': '',
                            'task_status': '',
                            'acceptedBy': '',
                            'createdby':''
                    })
                
            else:
                
                cur = engine.cursor()
                cur.execute("update task set task_status='Accepted' , acceptedby = '"+str(text_data_json['acceptedBy'])+"' where title = '"+str(text_data_json['title'])+"'")
                engine.commit()
                cur.close()
                print("Got task update Message from DeliveryAgent")
                cur = engine.cursor(cursor_factory=RealDictCursor)
                cur.execute("select * from task where task_status = 'New' order by priority desc limit 1; ")
                res = cur.fetchall()
                cur.close()
                if(len(res)>0):

                    self.send(text_data=json.dumps({
                        'message': "Next High Task",
                        'title': str(res[0]['title']),
                        'priority': str(res[0]['priority']),
                        'creationDate': str(res[0]['creation_date']),
                        'task_status': str(res[0]['task_status']),
                        'acceptedBy': str(res[0]['acceptedby']),
                        'createdby' : str(res[0]['createdby'])
                    }))
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                        'type': 'chat_message',
                        'message': "Next High Task",
                        'title': str(res[0]['title']),
                        'priority': str(res[0]['priority']),
                        'creationDate': str(res[0]['creation_date']),
                        'task_status': str(res[0]['task_status']),
                        'acceptedBy': str(res[0]['acceptedby']),
                        'createdby' : str(res[0]['createdby'])
                    }
                    )
                else:
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                        'type': 'chat_message',
                        'message': '',
                        'title': '',
                        'priority': '',
                        'creationDate': '',
                        'task_status': '',
                        'acceptedBy': '',
                        'createdby' : ''
                    }
                    )
        # message = text_data_json['message']

        # Send message to room group
       

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        title = event['title']
        priority = event['priority']
        creationDate = event['creationDate']
        Status = event['task_status']
        by = event['acceptedBy']
        createdby = event['createdby']


        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'title': title,
            'priority': priority,
            'creationDate': creationDate,
            'task_status': Status,
            'acceptedBy': by,
            'createdby':createdby
        }))
