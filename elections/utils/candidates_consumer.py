# coding = utf-8
import tweepy
import os

ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')
FILE_NAME = "candidates.txt"
MAX_TWEETS = 200

class CandidatesConsumer():
    def __init__(self, twitter_api):
        self.twitter_api = twitter_api
        self.candidates = []

    def fetch_candidates(self):
        try: 
            candidates_file = open(ROOT(FILE_NAME), "r")
        except IOError:
            print("Cannot open " + FILE_NAME)
        else:
            for i, line in enumerate(candidates_file):
                self.candidates.insert(i, "@"+line)
            
            candidates_file.close()

    def get_all_tweets(self, candidate):
        all_tweets = []

        new_tweets = self.twitter_api.api.user_timeline(screen_name = candidate,count = MAX_TWEETS)
        all_tweets.extend(new_tweets)
        oldest_tweet = all_tweets[-1].id - 1
        
        while len(new_tweets) > 0:
        
            new_tweets = self.twitter_api.api.user_timeline(screen_name = candidate,count=MAX_TWEETS, max_id=oldest_tweet)

            all_tweets.extend(new_tweets)
            
            oldest_tweet = all_tweets[-1].id - 1

        return all_tweets