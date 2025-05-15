from confluent_kafka import Producer
import json
import os
import time

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(**conf)

start_latitude = 19.0760
start_longitude = 72.8777

end_latitude = 18.0760
end_longitude = 73.8567

num_steps = 1000
step_size_lat = (end_latitude - start_latitude) / num_steps
step_size_long = (end_longitude - start_longitude) / num_steps

current_steps = 0

def delivery_report(err,msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))



topic = 'location'
while True:
    current_latitude = start_latitude + (step_size_lat * current_steps)
    current_longitude = start_longitude + (step_size_long * current_steps)

    data = {
        'latitude': current_latitude,
        'longitude': current_longitude,
        
    }
    print(data)
     
    producer.produce(topic, json.dumps(data).encode('utf-8'), callback=delivery_report)
    producer.flush()
    current_steps +=1 
    if current_steps >= num_steps:
        current_steps = 0
    
    time.sleep(2)