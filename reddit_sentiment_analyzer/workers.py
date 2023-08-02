from .models import Topic, Tweet
import time
from reddit_sentiment_analyzer.utils import SingletonQueue
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_comment(message):
    q = SingletonQueue()
    if not q.stream:
        return
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'broadcast_group',  # Change this to the appropriate WebSocket group name if necessary
        {
            'type': 'send_message',
            'message': message,
        }
    )


def create_worker(stop_event, q):
    while (True):
        if stop_event.is_set():
            break
        record = q.fetch()
        if not record:
            time.sleep(5)
            continue

        try:
            t = Tweet(topic_name=record[0], twitter_handle=record[1], posting_date=record[3], message=record[2])
            if record[0].lower() == q.activeTopic.lower():
                send_comment(f"{record[2]}({record[1]})")
        except Exception as e:
            print(e)

        try:
            t.save()

        except Exception as e:
            print(e)
