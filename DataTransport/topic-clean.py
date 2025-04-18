from google.cloud import pubsub_v1

project_id = "golden-monolith-456819-s6"
topic_id = "MyTopic"
subscription_id = "MySub"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

topic_path = publisher.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Delete the subscription to clear backlog
try:
    subscriber.delete_subscription(subscription=subscription_path)
    print(f"Deleted subscription: {subscription_path}")
except Exception as e:
    print(f"Could not delete subscription: {e}")

# Recreate the subscription fresh
try:
    subscriber.create_subscription(name=subscription_path, topic=topic_path)
    print(f"Recreated subscription: {subscription_path}")
except Exception as e:
    print(f"Failed to create subscription: {e}")