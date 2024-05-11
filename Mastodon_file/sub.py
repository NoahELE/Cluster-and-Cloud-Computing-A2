import re
import json
import time
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#-----------------------------------------------------------------------------------------------
#Get data from Mastodon and return the processed list of posts and the new maximum ID
def get_timeline(mastodon, max_id, dead_line):
    toots = mastodon.timeline_public(limit=40, max_id=max_id)
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

