import tweepy
import time
from datetime import datetime

class TweetAUTH():
    def __init__(self):
        # Enter twitter api keys here
        self.API_KEY = ''
        self.API_KEY_SECRET = ''
        
        self.ACCESS_TOKEN = ''
        self.ACCESS_TOKEN_SECRET = ''

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.API_KEY, self.API_KEY_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)
        # Verify credentials
        try:
            api.verify_credentials()
            return api
        except:
            return False

    def tweetSpace(self, api, new_tweets_f):
            for i in new_tweets_f:
                handle = new_tweets_f[i][0]
                link = new_tweets_f[i][1]
                tweet_text = "🚨{} is now live! 🎙: {} !".format(handle, link)
                api.update_status(status=tweet_text)
                print('Tweet sent....', tweet_text)
        
    def getFollowing(self, api):
        following = []
        for friend in tweepy.Cursor(api.friends).items():
            following.append(friend.id)
        return following
    
    def getTweets(self, api, following):
        tweet_list = []

        for follow in following:
             for tweet in tweepy.Cursor(api.user_timeline, id=follow, include_entities=True, include_rts=False).items(1):
                 for url in tweet.entities['urls']:
                     if 'twitter' in url['expanded_url']:
                         tweet_list.append((tweet.user.screen_name, url['expanded_url']))
        return tweet_list
        
class TweetMonitor():

       
    def runInstance(self):
        tweetBot = TweetAUTH()
        api = tweetBot.authenticate()
        following = tweetBot.getFollowing(api)
        if api == False:
            print('Error cant connect to twitter api')
            input()
        
        
        old_tweets = tweetBot.getTweets(api,following)
        while(True):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            new_tweets = []
            
            try:
                new_tweets = tweetBot.getTweets(api,following)
                print(new_tweets)
                
            except Exception as e:
                new_tweets = old_tweets
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(f'[{current_time}] Error - {e}')
            new_tweets_f = list(set(new_tweets) - set(old_tweets))
            print(new_tweets_f)
        
        
            if new_tweets_f != []:
                tweetBot.tweetSpace(api,new_tweets_f)
            else:
                print(f'[{current_time}] No new tweets!')
                
            old_tweets = new_tweets
            time.sleep(2)   

bot = TweetMonitor()
bot.runInstance()


