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
        print(record)
        print("step 1")
        try:
            t = Tweet(topic_name=record[0], twitter_handle=record[1], posting_date=record[3], message=record[2])
        except Exception as e:
            print(e)
        print("step 2")
        try:
            t.save()
            print("Saved!!!!!")
        except Exception as e:
            print(e)
        print("Done!!!!!")
