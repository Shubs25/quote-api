import json
import uuid

import pika
import redis

import constants

if constants.REDIS_URL:
    redis_client = redis.Redis.from_url(
        constants.REDIS_URL,
        decode_responses=True
    )
else:
    redis_client = redis.Redis(
        host=constants.REDIS_HOST,
        port=constants.REDIS_PORT,
        decode_responses=True
    )

def create_quote_job(subject: str):
    job_id = str(uuid.uuid4())
    redis_key = f'{constants.REDIS_JOB_ID_PREFIX}{job_id}'

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
        if constants.RABBITMQ_URL:
            connection_parameters = pika.URLParameters(
                constants.RABBITMQ_URL
            )
        else:
            connection_parameters = pika.ConnectionParameters(
                host=constants.RABBITMQ_HOST,
                port=constants.RABBITMQ_PORT,
                credentials=pika.PlainCredentials(
                    constants.RABBITMQ_USER,
                    constants.RABBITMQ_PASSWORD
                )
            )
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        channel.queue_declare(queue='queue1', durable=True, arguments={'x-queue-type': constants.RABBITMQ_QUEUE_TYPE})

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


