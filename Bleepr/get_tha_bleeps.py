import ConfigParser, sys, json, requests, time
from datetime import datetime
from twython import Twython, TwythonStreamer

settings = ConfigParser.ConfigParser()
settings.read('local.ini')
TWITTER_CONFIG = settings._sections['twitter']


class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        print data
        if 'text' in data and any(term.strip() in data.get('text').lower()
                              for term in TWITTER_CONFIG.get('track_terms').split(',')):
                bleep_payload = {'text': data.get('text'),
                           'author': data.get('user').get('screen_name'),
                           'tweet_url': 'https://twitter.com/{}/status/{}'.format(
                                        data.get('user').get('screen_name'),
                                        data.get('id_str')),
                           'created_at': time.strftime('%Y-%m-%dT%H:%M:%SZ',
                                         time.strptime(data.get('created_at'),
                                         '%a %b %d %H:%M:%S +0000 %Y'))}
                r = requests.post(TWITTER_CONFIG.get('bleep_hook_url'), json=bleep_payload)
                print bleep_payload
        else:
            # what's NOT bleeped
            print data.get('text').encode('utf-8')

    def on_error(self, status_code, data):
        self.disconnect()


if __name__ == "__main__":
    try:
        while True:
            stream = MyStreamer(TWITTER_CONFIG.get('consumer_key'), TWITTER_CONFIG.get('consumer_secret'),
                            TWITTER_CONFIG.get('access_token'), TWITTER_CONFIG.get('access_token_secret'))
            stream.statuses.filter(track=TWITTER_CONFIG.get('track_terms')) # everybody on twitter
            # stream.user() # only people I follow

    except KeyboardInterrupt:
        print 'Goodb**!'
