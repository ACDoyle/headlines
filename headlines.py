import feedparser
import json
import urllib2
import urllib
from flask import render_template #Jinja temlate use, converts to html
from flask import Flask
from flask import request

DEFAULTS = {'publication':'bbc',
            'city':'London,UK'}

app = Flask(__name__)

RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition_technology.rss',
             'au':'http://www.dailytelegraph.com.au/news/breaking-news/rss'}

WEATHER_URL='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=59bde91a9f41d926ad4a94ea3d935d40'

@app.route("/")
def home():
   #get customized headlines, based on user input or defaults
   publication = request.args.get('publication')
   if not publication:
      publication = DEFAULTS['publication']
   articles = get_news(publication)
   city = request.args.get('city')
   if not city:
      city = DEFAULTS['city']
   weather = get_weather(city)
   return render_template("home.html", articles=articles,weather=weather)

 
def get_weather(query):
   query = urllib.quote(query)
   url = WEATHER_URL.format(query)
   data = urllib2.urlopen(url).read()
   parsed = json.loads(data)
   weather = None
   if parsed.get("weather"):
      weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"]}
   return weather

def get_news(query):
   if not query or query.lower() not in RSS_FEEDS:
      publication = DEFAULTS["publication"]
   else:
      publication = query.lower()
   feed = feedparser.parse(RSS_FEEDS[publication])
   return feed['entries']

if __name__ == '__main__':
   app.run(port=5000, debug=True)
