from django.core.management.base import BaseCommand
from confluent_kafka import Consumer, KafkaException
import json
from home.models import LocationUpdate


class Command(BaseCommand):
    help = 'Consume messages from Kafka topic and save to database'
    
    def handle(self, *args, **options):
            conf = {
                'bootstrap.servers': 'localhost:9092',
                'group.id': 'location',
                'auto.offset.reset': 'earliest',
            }
            consumer = Consumer(conf)
            consumer.subscribe(['location'])
            try:
                while True:
                    msg = consumer.poll(timeout = 1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaException._PARTITION_EOF:
                            continue
                        else:
                            print(f"Error: {msg.error()}")
                            break
                    data = json.loads(msg.value().decode('utf-8'))
                    LocationUpdate.objects.create(
                        latitude=data['latitude'],
                        longitude=data['longitude'],
                    )
                    print(f"Consumed message: {data}")
            except KeyboardInterrupt:
                print("Aborted by user")
            finally:
                consumer.close()
                    
            return super().handle(*args, **options)