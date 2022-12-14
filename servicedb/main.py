import json
import pika
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models import Base, Obrashenie
from database import engine, SessionLocal


app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/')
async def get_and_send(db: Session = Depends(get_db)):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) # Need to change the host
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        obrashenie1 = Obrashenie(first_name=data['first'],
                             last_name=data['last'],
                             middle_name=data['middle'],
                             phone=data['phone'],
                             obrashenie=data['obrashenie'])
        db.add(obrashenie1)
        db.commit()
        print(f" [x] Received {data}") 
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()
