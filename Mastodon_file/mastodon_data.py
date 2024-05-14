import os
import re
import json
import pytz
import time
import requests
from tqdm import tqdm
from textblob import TextBlob
from mastodon import Mastodon
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sub import get_timeline, append_data, norma_date
from requests.exceptions import HTTPError, RequestException
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Load environment variables from .env file and initialize Mastodon
load_dotenv()


client_key = os.getenv('CLIENT_KEY_AUS')
client_secret = os.getenv('CLIENT_SECRET_AUS')
access_token = os.getenv('ACCESS_TOKEN_AUS')


mastodon = Mastodon(client_id=client_key, 
                    client_secret=client_secret, 
                    access_token=access_token,
                    api_base_url='https://aus.social')
                    #api_base_url='https://aus.social/explore')

'''
client_key = os.getenv('CLIENT_KEY_MAS')
client_secret = os.getenv('CLIENT_SECRET_MAS')
access_token = os.getenv('ACCESS_TOKEN_MAS')


mastodon = Mastodon(client_id=client_key, 
                    client_secret=client_secret, 
                    access_token=access_token,
                    api_base_url='https://mastodon.social')'''



#Get all time parameters
year_num = 0.05
utc_zone = pytz.utc
start_date = datetime.now(utc_zone)
norm_start_date = norma_date(start_date)
dead_line = start_date - timedelta(days=365*year_num)

#Initialization progress bar
pbar = tqdm(total= (start_date-dead_line).days)

#Set the file name for saving data
file_name = f"aus_social_new.json"


#Get data from Mastodon until specified deadline
max_id = None
all_toots = []
keep_going = True

while keep_going:
    
    try:
        #Successfully obtain data and add it to file
        toots_list, new_maxid = get_timeline(mastodon, max_id, dead_line)
        if not toots_list:
            print('No data returned in this iteration.')
            time.sleep(3)
            continue

        append_data(file_name, toots_list)
        
    except Exception as e:
        #When error occurs, printing the error type and extending the break to 5 seconds
        print(f"An error occurred: {e}")  
        time.sleep(5)
        continue 

    time.sleep(1)

    
    #Update progress bar
    current_date = utc_zone.localize(datetime.fromisoformat(toots_list[-1]['creat_time'][:19]))
    norm_current_date = norma_date(current_date)
    load_days = (norm_start_date - norm_current_date).days
    print(current_date)
    if load_days > 0:
        pbar.update(load_days) 
        norm_start_date = norm_current_date
        

    if not new_maxid or new_maxid == max_id:
        keep_going = False 
    max_id = new_maxid

#-----------------------------------------------------------------------------------------------
#Get data from Mastodon and return the processed list of posts and the new maximum ID
def get_timeline(mastodon, max_id, dead_line, hashtag='melbourne'):
    toots = mastodon.timeline_hashtag(hashtag, limit=40, max_id=max_id)
    toots_list = []
    new_maxid = None

    if toots:
        for toot in toots:
            creat_date = toot['created_at']
            if creat_date < dead_line:
                print('End to get data')
                break

            clean_content, sentiment_score = clean_toot(toot['content'])

            toot_info = {
                "id":toot['id'],
                "creat_time":toot['created_at'].isoformat(),
                "content":clean_content,
                "language":toot['language'],
                "sentiment":sentiment_score,                   
                "tag":[tag['name'] for tag in toot['tags']]
            }
            toots_list.append(toot_info)

        new_maxid = toots[-1]['id']

    return toots_list, new_maxid

#-----------------------------------------------------------------------------------------------
#find area key words in content

def find_area(content):
    if 'mel' in content:
        ADD_DATA = True
        return ADD_DATA

#-----------------------------------------------------------------------------------------------
#Save data to file
def append_data(file_name, new_data):

    with open(file_name, 'a') as f:
        #for i in all_data:
        for i in new_data:
            json.dump(i, f, ensure_ascii=False, separators=(',', ':'))
        #json.dump(all_data, f, ensure_ascii=False,indent=4, separators=(',', ':'))
            f.write('\n')

#-----------------------------------------------------------------------------------------------
#Get sentiment score, result will be slightly worse, supports multiple languages
def get_sentiment_textblob(content):
    result = TextBlob(content)
    return result.sentiment.polarity

#More accurate, but only for English
def get_senti_vader(content):
    result = SentimentIntensityAnalyzer().polarity_scores(content)
    return result['compound']

#-----------------------------------------------------------------------------------------------
#Clean the content of toots and get sentiment score
def clean_toot(content):
    #all lowercase
    content = content.lower()
    #delete URLs
    new_content = re.sub(r'https?://\S+|www\.\S+', ' ', content)
    #delete HTML
    new_content = re.sub(r'<[^>]+>', ' ', new_content)
    #delete non-literal symbols
    new_content = re.sub(r'[^\w\s]', ' ', new_content)
    #sentiment score[textblob/vader]
    sentiment_score = get_sentiment_textblob(new_content)
    #delete emoji
    new_content = re.sub(r'[\U00010000-\U0010ffff]', ' ', new_content)
    #delete words of length 1/2
    new_content = re.sub(r'\b\w{1,2}\b', ' ', new_content)
    #delete num
    new_content = re.sub(r'\d+', ' ', new_content)
    #delete space
    new_content = re.sub(r'\s+', ' ', new_content).strip()

    content_list = new_content.split()

    return content_list, sentiment_score


#-----------------------------------------------------------------------------------------------
#Update bar based on date, not time difference (24 hours)
def norma_date(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)



