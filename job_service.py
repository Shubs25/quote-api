import json
import uuid

import pika
import redis


redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create_quote_job(subject: str):
    job_id = str(uuid.uuid4())
    redis_key = f'quote_job:{job_id}'

    redis_client.hset(
        redis_key,
        mapping = {
            'job_id': job_id,
            'subject': subject,
            'status': 'pending',
        }
    )

    job = {
        'job_id': job_id,
        'subject': subject,
    }

    connection = None
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='queue1', durable=True, arguments={'x-queue-type': 'quorum'})

        channel.confirm_delivery()
        channel.basic_publish(
            exchange='',
            routing_key='queue1',
            body=json.dumps(job),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json',
            ),
            mandatory=True,
        )
        return job_id

    except Exception:
        redis_client.hset(redis_key, mapping={"status": "failed"})
        raise
    finally:
        if connection is not None and connection.is_open:
            connection.close()

    return None


