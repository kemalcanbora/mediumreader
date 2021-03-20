from fastapi import FastAPI
from medium import run
from models.model import MediumModel
from rq import Queue
from settings import REDIS_URL
import redis

app = FastAPI()
conn = redis.from_url(REDIS_URL)
q = Queue(connection=conn)


@app.post("/")
def api(mediumModel: MediumModel):
    url = mediumModel.url
    job = q.enqueue_call(
        func=run,
        args=(url,),
        result_ttl=5000
    )
    return {"status": job.get_id()}
