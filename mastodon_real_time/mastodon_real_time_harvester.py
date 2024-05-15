import re
import pytz
from textblob import TextBlob
from mastodon import Mastodon
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from elasticsearch import Elasticsearch

#Load environment variables from .env file and initialize Mastodon
def secret(key: str) -> str:
    """Read secret from k8s secret volume"""
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()


host = secret("ES_URL")
# host = "https://127.0.0.1:9200"
# basic_auth = ("elastic", "gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x")
basic_auth = (secret("ES_USERNAME"), secret("ES_PASSWORD"))
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)
mastodon = Mastodon(api_base_url='https://aus.social')
                    # api_base_url='https://aus.social/explore')
#Set the file name for saving data
# file_name = f"leatest_data_mastodon.json"


def main():
    try:
        utc_zone = pytz.utc
        start_date = datetime.now(utc_zone)
        dead_line = start_date - timedelta(minutes=30)
        toots_list = get_timeline(mastodon)
        for toot in toots_list:
            es.index(
                index="mastodon_melbourne",
                id=toot["id"],
                document=toot,
            )
        # append_data(file_name, toots_list)
        return "OK"
    except Exception as e:
        return str(e)

#-----------------------------------------------------------------------------------------------
#Get data from Mastodon and return the processed list of posts and the new maximum ID
def get_timeline(mastodon, hashtag='melbourne'):
    toots = mastodon.timeline_hashtag(hashtag, limit=20)
    toots_list = []

    if toots:
        for toot in toots:
            # creat_date = toot['created_at']
            # if creat_date < dead_line:
            #     print('End to get data')
            #     break
            clean_content, sentiment_score = clean_toot(toot['content'])

            toot_info = {
                "id":toot['id'],
                "creat_time":mel_time(toot['created_at'].isoformat()),
                "content":clean_content,
                "language":toot['language'],
                "sentiment":sentiment_score,
                "tag":[tag['name'] for tag in toot['tags']]
            }
            toots_list.append(toot_info)

    return toots_list


#-----------------------------------------------------------------------------------------------
#Save data to file
# def append_data(file_name, new_data):
#
#     with open(file_name, 'a') as f:
#         #for i in all_data:
#         for i in new_data:
#             json.dump(i, f, ensure_ascii=False, separators=(',', ':'))
#         #json.dump(all_data, f, ensure_ascii=False,indent=4, separators=(',', ':'))
#             f.write('\n')


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
#Change UTC to AEST
def mel_time(time):
    utc_time = datetime.fromisoformat(time)
    mel_tz = pytz.timezone("Australia/Melbourne")
    #utc_time = utc_zone.localize(utc_time)
    melbourne_time = utc_time.astimezone(mel_tz)
    return melbourne_time.isoformat()

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
#Get data from Mastodon until specified deadline





