import pika
import time
import os

rabbitmq_host = os.environ.get('RABBITMQ_HOST')
rabbitmq = pika.ConnectionParameters(host=rabbitmq_host)


start_time = time.time()
timeout = 30
sleep_time = 1
while (time.time() - start_time < timeout):
    try:
        conn = pconnection = pika.BlockingConnection(rabbitmq)
        print("Rabbitmq is ready!")
        conn.close()
        break
    except:
        print(f"Rabbitmq isn't ready. Waiting for {sleep_time} seconds...")
        time.sleep(sleep_time)


connection = pika.BlockingConnection(rabbitmq)
channel = connection.channel()

channel.queue_declare(queue='update_user', durable=True)
channel.queue_declare(queue='update_item', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='update_user', on_message_callback=callback)
channel.basic_consume(queue='update_item', on_message_callback=callback)

channel.start_consuming()