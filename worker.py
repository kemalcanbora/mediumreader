import redis
from settings import REDIS_URL
from rq import Worker, Queue, Connection

listen = ['default']

conn = redis.from_url(REDIS_URL)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()