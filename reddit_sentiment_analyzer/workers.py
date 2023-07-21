from .models import Topic, Tweet
import time


def create_worker(stop_event, q):
    while (True):
        if stop_event.is_set():
            break
        record = q.fetch()
        if not record:
            time.sleep(5)
            continue
        t = Tweet(topic=q[0], twitter_handle=q[1][0], posting_date=q[1][1], message=q[1][2])
        t.save()
