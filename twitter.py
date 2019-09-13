from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
from pykafka import KafkaClient
import json

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        message = json.loads(data)
        if message['place'] is not None:
            client = get_kafka_client()
            topic = client.topics['twitterdata2']
            producer = topic.get_sync_producer()
            producer.produce(data.encode('ascii'))
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    listener = StdOutListener()
    stream = Stream(auth, listener)
    #stream.filter(track=['codeanddogs'])
    stream.filter(locations=[-180,-90,180,90])
