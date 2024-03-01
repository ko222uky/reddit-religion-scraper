import praw
import csv
import time
import datetime
import os
import pandas as pd
import glob
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv('.env')

client_id_env = os.getenv('REDDIT_CLIENT_ID')
client_secret_env = os.getenv('REDDIT_SECRET')
user_agent_env = os.getenv('REDDIT_USER')

reddit = praw.Reddit(
    client_id=client_id_env,
    client_secret=client_secret_env,
    user_agent=user_agent_env
)
# Eastern Time Zone
timezone = pytz.timezone("America/New_York")
local_time = datetime.now(timezone)
local_time_str = local_time.strftime("%Y-%m-%d") # for the file name
exact_local_time_str = local_time.strftime("%Y-%m-%d-%H:%M:%S") # for when data was collected


print(f"Local time: {local_time}")
## Fetches subreddit information

filename = "popular_subreddits/" + local_time_str + ".csv"
counter = 0
requests = 0
# headers defined for CSV
headers = ['display_name', 'title', 'description', 'subscribers', 'over18', 'url','date_data_collected']

if not os.path.exists('popular_subreddits'):
    print("Creating directory to store popular subreddits...")
    os.makedirs('popular_subreddits/master_data') # The master data file contains all the data collected from the popular subreddits
else:
    print("Directory already exists. Fetching popular subreddits...")

# Fetch popular subreddits
for i in range(1):

    popular_subreddits = list(reddit.subreddits.popular(limit=5000))  # currently, 1000 is the limit for the API, which approximates 10 requests. 
    
    utc_time = datetime.fromtimestamp(reddit.auth.limits['reset_timestamp'], pytz.utc)
    local_timezone = pytz.timezone('America/New_York')  # Replace with your timezone
    local_time = utc_time.astimezone(local_timezone)

    
   
    # Open or create a CSV file and write the data
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for subreddit in popular_subreddits:
            writer.writerow({
                'display_name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.public_description,
                'subscribers': subreddit.subscribers,
                'over18': subreddit.over18,
                'url': subreddit.url,
                'date_data_collected': exact_local_time_str
            })
    time.sleep(2)

print(f"Rate limit remaining: {reddit.auth.limits['remaining']}")
print(f"Rate limit reset time: {local_time}")

print("*********************************")
print("Combining CSVs into a single master data file...")
print("*********************************")

# Combine all the CSV files into a single master data file
# Get list of all CSV files
csv_files = glob.glob('popular_subreddits/*.csv')

# Use the first and last names (which are dates) to name the excel
first_csv_file = os.path.basename(csv_files[0])
last_csv_file = os.path.basename(csv_files[-1])
# split by '.'
first_csv_file = first_csv_file.split('.')[0]
last_csv_file = last_csv_file.split('.')[0]

master_name = 'popular_subreddits/master_data/' + first_csv_file + '-to-' + last_csv_file + '.xlsx'



# Writes each CSV to a separate sheet in the Excel file.
with pd.ExcelWriter(master_name, engine='xlsxwriter') as writer:
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)

        csv_name = os.path.basename(csv_file).split('.')[0]
        print(f"Writing {csv_name} to Excel...")
        df.to_excel(writer, sheet_name=csv_name, index=False)

print("Saved master data file in popular_subreddits/master_data")

print("Exiting program...")
# Open the existing CSV file in read mode to get the existing post IDs
