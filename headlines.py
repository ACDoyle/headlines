import feedparser
import json
import urllib2
import urllib
from flask import render_template #Jinja temlate use, converts to html
from flask import Flask
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition_technology.rss',
             'au':'http://www.dailytelegraph.com.au/news/breaking-news/rss'}

def get_weather(query):
   api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=59bde91a9f41d926ad4a94ea3d935d40'
   query = urllib.quote(query)
   url = api_url.format(query)
   data = urllib2.urlopen(url).read()
   parsed = json.loads(data)
   weather = None
   if parsed.get("weather"):
      weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"]}
   return weather

@app.route("/")
def get_news():
   query = request.args.get("publication")
   if not query or query.lower() not in RSS_FEEDS:
      publication = "bbc"
   else:
      publication = query.lower()
   feed = feedparser.parse(RSS_FEEDS[publication])
   weather = get_weather("London,UK")
   return render_template("home.html", articles=feed["entries"],weather=weather)

if __name__ == '__main__':
   app.run(port=5000, debug=True)
