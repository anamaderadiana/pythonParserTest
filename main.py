import tweepy
import re
import json

from tweepy import OAuthHandler
from flask import Flask
from flask_restful import Api, Resource, reqparse

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

apiTweepy = tweepy.API(auth)
app = Flask(__name__)
apiFlask = Api(app)

# @app.route("/")
# def result():
#     return getWeatherFromTwitter()
#
# if __name__ == "__main__":
#     app.run()

class Weather(Resource):
    def get(self, name):
        for status in tweepy.Cursor(apiTweepy.user_timeline, screen_name='@MontbauMeteo').items(1):
            return getFormatData(status.text)

    def getFormatData(text):
        text = text.encode('utf-8')
        return json.dumps({
            'temperature': re.findall(r'Temp:(\d+\.\d+)', text)[0],
            'humidity': re.findall(r'Hum:(\d+)', text)[0],
            'wind': re.findall(r'Vent:(\d+\.\d+)', text)[0],
            'rain': re.findall(r'Pluja:\s\s(\d+\.\d+)', text)[0]
        })

app.run(debug=True)
