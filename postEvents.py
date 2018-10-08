import tweepy
from bs4 import BeautifulSoup
from astropy.utils.data import download_file
import json

soup = BeautifulSoup(open(download_file("https://jobregister.aas.org"), 'r', encoding="utf-8"), 'html.parser')

postdocs = soup.find_all('table')[2]

### send tweet!
### The Twitter-Posting Script... ###
CONSUMER_KEY = 'y4AbQJJYvoHjNl8mJfsNlKhBR'
CONSUMER_SECRET = open('consumer_secret.txt', 'r').read().strip()

ACCESS_KEY = '1043255268757258240-IcNlZPQADDUKrxXlBwmFSydfQ6auzR'
ACCESS_SECRET = open('access_secret.txt', 'r').read().strip()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

entries = json.load(open('/Users/bmmorris/git/jobot/posts.json', 'r'))
# entries = dict()

for listing in postdocs.find_all('tr')[1:]:
    data = listing.find_all('td')
    link = listing.find_all('a')[0]
    url = 'https://jobregister.aas.org' + link.get('href')
    tweet = "{0} @ {1}: {2}".format(data[0].text, data[1].text, url)

    if tweet not in entries:
        print('New tweet: {0}'.format(tweet))
        entries[tweet] = 0
        api.update_status(tweet)

json.dump(entries, open('/Users/bmmorris/git/jobot/posts.json', 'w'))
