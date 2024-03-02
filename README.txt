reddit-religion-scraper

Author: Kenneth O'Dell Jr.

************
Description:
************

A simple set of scripts to extract post data from a list of tracked subreddits.
Topical contents of the tracked subreddit center on larger religious subreddits, with a particular focus on Christianity.
The goal is to gather a bunch of basic textual data, with the ability to pull comments that meet a criteria (future implementation).
This is a pre-requisite little project for gather some data to use with a model.
Additional data may be obtained via human respondents regarding the post data (TBD).

Data is saved as CSV and XLSX in appropriate directories.

************
Environment:
************

The environment can be created using conda and the provided environment.yml

$ conda env create -f environment.yml

************
Environment Variables:
************

The scripts use the Reddit API.
You will need to provide your own client id, client secret, and user agent information.
Set these in a .env file.

REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_SECRET=your-reddit-secret
REDDIT_USER=your-reddit-user 



