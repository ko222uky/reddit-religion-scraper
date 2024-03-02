import pandas as pd # for Excel operations
import openpyxl # for Excel operations
import os

# read subreddit names from tracked_subreddits.txt
tracked_subreddits = []
with open('tracked_subreddits.txt', 'r') as f:
    tracked_subreddits = f.readlines()

# create a master data frame
master_df = pd.DataFrame()
# create a new file and write the headers to it
master_df.to_excel("subreddit_posts/master_df.xlsx", index=True)
master_df.to_csv("subreddit_posts/master_df.csv", index=False)

# create Excel file from each of the CSVs:
for tracked_subreddit in tracked_subreddits:
    subreddit_name = tracked_subreddit.strip()
    filename = subreddit_name + ".csv"
    directory = "subreddit_posts/" + subreddit_name + "/"
    full_path = directory + filename
    df = pd.read_csv(full_path, header=0)
    # create Excel file
    df.to_excel(directory + subreddit_name + ".xlsx", index=False)
    print(f"Excel file created for {subreddit_name}!")

    # append to master_df
    df.to_csv("subreddit_posts/master_df.csv", mode='a', index=False)

# create master Excel from the master CSV
df = pd.read_csv("subreddit_posts/master_df.csv")
df.to_excel("subreddit_posts/master_df.xlsx", index=True)

print("All Excel files created, along with master_df.csv and master_df.xlsx!")


# create master for sheeted data
master_df.to_excel("subreddit_posts/master_df_sheets.xlsx", index=True)

print("Creating master_df with data in separate sheets...")
for tracked_subreddit in tracked_subreddits:
    print(f"Adding {tracked_subreddit} to master_df.xlsx...")
    subreddit_name = tracked_subreddit.strip()
    filename = subreddit_name + ".xlsx"
    directory = "subreddit_posts/" + subreddit_name + "/"
    full_path = directory + filename
    df = pd.read_excel(full_path)
    # delete the headers from the first row
    df = df[1:]
    with pd.ExcelWriter("subreddit_posts/master_df_sheets.xlsx", mode='a', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=tracked_subreddit, index=False)
    
print("Done!")



