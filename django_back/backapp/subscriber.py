import os
from dotenv import load_dotenv
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError
load_dotenv()
credentials_path= os.getenv("GCP_CREDENTIALS_PATH")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
timeout = 5.0 
subscriber = pubsub_v1.SubscriberClient()
subscription_path=os.getenv("SUBSCRIBER_PATH")
def callback(message):
    print(f"Received message: {message.data}")
    message.ack()
streaming_pull_feature = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")
with subscriber: 
    try:
        streaming_pull_feature.result() #indefinitely
        # streaming_pull_feature.result(timeout=timeout) #timeout after some time
    except TimeoutError:
        streaming_pull_feature.cancel() 
        streaming_pull_feature.result()