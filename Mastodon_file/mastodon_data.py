import os
import pytz
import time
from tqdm import tqdm
from mastodon import Mastodon
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sub import get_timeline, append_data, norma_date
import requests
from requests.exceptions import HTTPError, RequestException

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

