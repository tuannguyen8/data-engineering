from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import time

project_id = "golden-monolith-456819-s6"
subscription_id = "MySub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

message_count = 0
print_interval = 10000  # Print after every 10,000 messages

start_time = time.time()

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    global message_count
    message.ack()
    message_count += 1

    if message_count % print_interval == 0:
        print(f"Received {message_count} messages so far...")

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...\n")

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

end_time = time.time()
duration = end_time - start_time

print(f"\nTotal messages received: {message_count}")
print(f"Subscriber finished in {duration:.2f} seconds.")