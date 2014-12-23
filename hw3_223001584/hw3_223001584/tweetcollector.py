# import statements
import tweepy
from random import randrange
import numpy
import HTMLParser

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="l6QGY3pKWEdxswCLCmiR9Q"
consumer_secret="9x9fakUwwwoGnmzy4SmLleFTZ7FYhh4jobrhEywcM"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="2415103321-y8lKMuQvCwr4B6Ywvi4o0F2JAD0WSjwPPuBHB6o"
access_token_secret="Qkdmf0KAN2ha4MEZzbFc8KN2zHmClEGfPKCAdBNFT9pNq"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# creating files for each query ie each document
list_of_queries = ["#katyperry", "#katycats", "#darkhorse", "#iHeartRadio", "#ladygaga", "#TaylorSwift", "#sxsw", "Rolling Stone","@DwightHoward", "#rockets", "jeremy lin", "toyota center", "kevin mchale", "houston nba", "James Harden", "linsanity", "Jan Koum", "WhatsApp", "#SEO", "facebook", "#socialmedia", "Zuckerberg", "user privacy", "#Instagram","Obama", "#tcot", "Russia", "Putin", "White House", "Ukraine", "Rand Paul", "foreign policy"]

# tweet results are stored in the files created
count1 = 0
for query in list_of_queries :
    count1 = count1 + 1
    filename = list_of_queries[count1-1] + ".txt"
    f = open(filename,'w')
    query = list_of_queries[count1-1],"-RT"
    result = api.search(q = query, count=50, lang='en')
    count2 = 0
    for t in result['statuses']:
        count2 = count2 + 1
        f.write(str(count2)+":")
        h=HTMLParser.HTMLParser()
        tweetstring=h.unescape(t['text'])
        tweetstring=tweetstring.encode('ascii','ignore').lower()
        f.write(tweetstring)
        f.write('\n')
    f.close()