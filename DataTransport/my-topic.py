import json
import time
from google.cloud import pubsub_v1

# GCP settings
project_id = "golden-monolith-456819-s6"
topic_id = "MyTopic"
file_path = "busses-100.json"

# Initialize publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Load JSON data
with open(file_path, "r") as f:
    records = json.load(f)

start_time = time.time()

# Publish messages
count = 0
for record in records:
    data = json.dumps(record).encode("utf-8")
    future = publisher.publish(topic_path, data)
    future.result()
    count += 1

end_time = time.time()
duration = end_time - start_time

# Print only once at the end
print(f"Published total: {count} messages in {duration:.2f} seconds.")