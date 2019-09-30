import geocoder
import logging
import os
import json
from redis import Redis

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

def consumer(redis, queues = None):
    if queues is None:
        queues = ['queue']
    while True:
        consume(redis, queues)

def consume(redis, queues):

    popped = redis.blpop(queues)
    if popped is None:
        return
    payload = json.loads(popped[1])
    address = payload.get('address')
    logging.info(f'Popped {address} off of the queue')

if __name__ == '__main__':
    redis = Redis(host='redis', decode_responses=True)
    consumer(redis)

