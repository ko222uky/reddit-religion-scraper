import praw # for Reddit API
import csv # for CSV operations
import time # to add delays to prevent rate limit overloads
import os # to check if directories exist, to create directories, and to get environment variables
from datetime import datetime # to get the current time, and to convert Reddit's created_utc
import pytz # for timezones
from dotenv import load_dotenv # to load environment variables from .env file
import pandas as pd # for Excel operations


load_dotenv('.env') # Load environment variables from .env file

client_id_env = os.getenv('REDDIT_CLIENT_ID')
client_secret_env = os.getenv('REDDIT_SECRET')
user_agent_env = os.getenv('REDDIT_USER')

reddit = praw.Reddit(
    client_id=client_id_env,
    client_secret=client_secret_env,
    user_agent=user_agent_env
)

#read subreddit names from tracked_subreddits.txt
tracked_subreddits = []
with open('tracked_subreddits.txt', 'r') as f:
    tracked_subreddits = f.readlines()

# Fetch new posts from the subreddits
for tracked_subreddit in tracked_subreddits:
    print("*********************************")
    print(f"Pulling data from {tracked_subreddit}...")

    timezone = pytz.timezone("America/New_York") # Eastern Time Zone
    local_time = datetime.now(timezone) # Get the current time in Eastern Time Zone
    local_time_str = local_time.strftime("%Y-%m-%d-%H:%M:%S") # Format the time to string
                                                            # This is the time when the data is collected

    subreddit_name = tracked_subreddit.strip()
    print(f"Pulling data from subreddit: {subreddit_name} ")

    filename = subreddit_name + ".csv"
    directory = "subreddit_posts/" + subreddit_name + "/"
    full_path = directory + filename

    # headers defined for CSV
    headers = ['title', 'score', 'id', 'url', 'comms_num', 'created', #'body', 
               'date_data_collected','subreddit']

    if not os.path.exists(directory):
        os.makedirs(directory)



        print("*********************************")
        print("FETCHING LATEST POSTS FROM REDDIT...")
        print("*********************************")

    else:
        print("Directory exists. Checking for file...")
        print("*********************************")
    if os.path.exists(full_path):
        print("File found...")
    else:
        print("File not found. Creating a new file...")
        # create a new file and write the headers to it
        with open(full_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            # Write the column headers
            writer.writeheader()

    # Open the existing CSV file in read mode to get the existing post IDs
    with open(full_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print("Reading existing data from file...")
        existing_ids = {row['id'] for row in reader}  # ID column is named 'id'; store them in a set

    ###    MAKE OUR REQUESTS TO REDDIT API
    new_counter = 0

    # Convert to list, so that we can iterate over it multiple times
    new_posts = list(reddit.subreddit(subreddit_name).new(limit=1000)) # currently, 1000 is the limit for the API, which approximates 10 requests.

    utc_time = datetime.fromtimestamp(reddit.auth.limits['reset_timestamp'], pytz.utc)
    local_timezone = pytz.timezone('America/New_York')  # Replace with your timezone
    local_time = utc_time.astimezone(local_timezone)        
    
    counter = 0
    for post in new_posts:
        counter+=1

    print(f"Grabbed {counter} posts...")

###    WRITE THE DATA TO CSV
    # Open or create a CSV file and write the data

    with open(full_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)

        for post in new_posts:
            if post.id not in existing_ids:
                print(f"Found new post id {post.id}!")
                # add id to existing ids
                existing_ids.add(post.id)
                new_counter+=1
                utc_time = datetime.fromtimestamp(post.created, pytz.utc)
                created_local_timezone = pytz.timezone('America/New_York')  # Replace with your timezone
                created_local_time = utc_time.astimezone(local_timezone)
                created_local_time_str = created_local_time.strftime("%Y-%m-%d-%H:%M:%S")
                
                writer.writerow({
                    'title': post.title,
                    'score': post.score,
                    'id': post.id,
                    'url': post.url,
                    'comms_num': post.num_comments,
                    'created': created_local_time_str,
                    # 'body': post.selftext, # Body can cause issues. So I will handle this separately
                    'date_data_collected': local_time_str,
                    'subreddit': subreddit_name
                })
            else:
                pass # Do nothing
    if not os.path.exists(directory + 'body/'):
        os.makedirs(directory + 'body/')
    for post in new_posts: # Let's save the body of the post as a separate file with post id as the name
        with open(directory + 'body/' + post.id + ".txt", 'w', encoding='utf-8') as f:
            f.write(post.selftext)


    print("*********************************")
    print(f"Found {new_counter} new posts from {subreddit_name}!")
    print(f"Rate limit remaining: {reddit.auth.limits['remaining']}")
    print(f"Rate limit reset time: {local_time}")
    print("*********************************")
    print("Waiting for 20 seconds...")
    time.sleep(20)
print("Done!")



# prompt for appending new posts!
'''
# PROMPT FOR UPDATING DATA
update_data = input("Do you want to update the existing data? (yes/no): ")
if update_data.lower() == 'yes':
    if os.path.exists(full_path):
        print("File found...")
    else:
        print("File not found! Exiting program...")
        exit()
    # UPDATE THE EXISTING DATA
    print("*********************************")
    print("UPDATING EXISTING DATA...")
    print("*********************************")
    # open existing data
    with open(full_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        posts = list(reader)

    # update the data with latest score and comments
    for post in posts:
        reddit_post = reddit.submission(id=post['id'])
        post['score'] = reddit_post.score
        post['comms_num'] = reddit_post.num_comments
        print(f"Fetching data for post: {post['id']}, score = {post['score']}, comm_num = {post['comms_num']}")

        # Add a delay of 2 seconds to avoid API rate limit
        time.sleep(2)

    # write the updated data to the file
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=posts[0].keys())
        writer.writeheader()
        writer.writerows(posts)
        print("Data updated successfully!")
    print("Done!")
else:
    print("Data not updated!")

print("Exiting program...")
'''


# Path: fetch.py