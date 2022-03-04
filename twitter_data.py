from doctest import DONT_ACCEPT_TRUE_FOR_1
import tweepy
import configparser
from datetime import date
import pandas as pd
import configi

#read from the config file
#this config file stores the access and api_keys for the twitter api
config = configparser.ConfigParser()
config.read('configi.ini')


#authentication

auth = tweepy.OAuthHandler(configi.api_key,configi.api_key_secret)
auth.set_access_token(configi.access_token,configi.access_token_secret)
api =tweepy.API(auth)



#Function for getting tweets with #greenhydrogen

def tweet_data():
    keywords = '#greenhydrogen'
    #date= "2022-01-02"
    limit = 100
    tweets = tweepy.Cursor(api.search_tweets,q=keywords,tweet_mode='extended').items(100)
    return tweets

#creating a dataframe

columns=['User','Content']
data= []

for tweet in tweet_data():
    data.append([tweet.user.screen_name,tweet.full_text])

df1 = pd.DataFrame(data,columns=columns)

#print (df1)
    


#Function for getting news from the google rss feed 
def get_news(rss=None):
    
    if rss is not None:
        
          # import the library only when url for feed is passed
        import feedparser
          
        # parsing blog feed
        blog_feed = blog_feed = feedparser.parse(rss)
          
        # getting lists of blog entries via .entries
        posts = blog_feed.entries
          
        # dictionary for holding posts details
        posts_details = {"Title" : blog_feed.feed.title,
                        #"Date" : blog_feed.feed.date
                        #"Link": blog_feed.feed.link
                        }
        
                        
          
        post_list = []
          
        # iterating over individual posts
        for post in posts:
            temp = dict()
              
            # if any post doesn't have information then throw error.
            try:
                temp["Title"] = post.title
                temp["Link"] = post.link
                temp["Author"] = post.author                
                temp["Summary"] = post.summary
            except:
                pass
              
            post_list.append(temp)
          
        # storing lists of posts in the dictionary
        posts_details["posts"] = post_list 
        
          
        return posts_details
    else:
        return None
  
if __name__ == "__main__":
  
  
  feed_url = "https://news.google.com/rss/search?hl=en-IN&gl=IN&ceid=IN%3Aen&oc=11&q=green%20hydrogen%20when%3A30d"
  
  data = get_news(rss = feed_url)
  #print(data)

df2 = pd.DataFrame(data)
#print(df2)



#Concatinating the two dataframes
frames = [df1, df2]  
result = pd.concat([df1, df2], axis=1, join='inner')
res = pd.DataFrame(result)
li1 = res.values.tolist()#converts  the dataframe to a list
#print(res)



#Sentiment Analysis On the csv file

# import tensorflow as tf
# from transformers import pipeline
# from feel_it import EmotionClassifier, SentimentClassifier
# df = pd.read_csv('file1.csv',encoding='UTF-8')
# # vals = df.values.tolist()

# # sentiment_classifier = SentimentClassifier()
# # sentiment_classifier.predict(vals)

# sentiment_pipeline = pipeline("sentiment-analysis")
# data = df
# sentiment_pipeline(data)




#Creating a REST API for the Whole program
from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/Result", methods=['GET'])
def get():
    return jsonify({'Result': li1})    

if __name__ =="__main__":
    app.run(debug=True)



#saving the dataframes as a 'csv' file
res.to_csv('file1.csv')