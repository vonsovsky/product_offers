from datetime import datetime

from redis import Redis
from rq_scheduler import Scheduler
import worker


REPEAT = 5  # repeat schedule only several times for testing purposes


scheduler = Scheduler('po-task', connection=Redis.from_url('redis://'))
job = scheduler.schedule(scheduled_time=datetime.utcnow(), func=worker.update_offers, interval=60, repeat=REPEAT)
scheduler.run()
