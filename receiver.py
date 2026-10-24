import pika, os, sys
import json, redis
from quote_service import ask_llm

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


def callback(ch, method, properties, body):
    job = json.loads(body.decode('utf-8'))
    job_id = job['job_id']
    subject = job['subject']
    redis_key = f'quote_job:{job_id}'

    redis_client.hset(redis_key, mapping={'status': 'processing'})

    quote_from_llm = ask_llm(subject)

    if quote_from_llm:
        redis_client.hset(redis_key, mapping={'status': 'success', 'quote': quote_from_llm})
    else:
        redis_client.hset(redis_key, mapping={'status': 'failed'})

    ch.basic_ack(delivery_tag=method.delivery_tag)

    print(f" [x] Job {job_id}: {redis_client.hgetall(redis_key)}")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='queue1', durable=True, arguments={'x-queue-type': 'quorum'})
    channel.basic_consume(queue='queue1', on_message_callback=callback, auto_ack=False)

    print(" [x] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)