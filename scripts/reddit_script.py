import praw
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud

load_dotenv()

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
    client_id=os.getenv("reddit_client_id"),
    client_secret=os.getenv("reddit_client_secret"),
    user_agent=os.getenv("reddit_user_agent")
)

# Define search query
query = "renewable energy"
num_posts = 100

def scrap_posts(reddit_query, posts_count):
    # Fetch posts
    data = []
    for submission in reddit.subreddit("all").search(reddit_query, limit=posts_count):
        data.append({
            "title": submission.title,
            "post_text": submission.selftext,
            "author": str(submission.author),
            "date": datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "upvotes": submission.score,
            "subreddit": submission.subreddit.display_name
        })
    return data


def save_to_csv(scrapped_data):
    df = pd.DataFrame(scrapped_data)

    df.to_csv("../datasets/raw/reddit_posts.csv", index=True)


def analyze_data(reddit_df):
    print(f"Statistical Summary of Data:")
    print(reddit_df.describe())

    print("Categorical Summaries:")
    print(df[['author', 'subreddit']].describe())

def visualize_data_trends(reddit_df):
    # posting trends over time
    reddit_df['date'] = pd.to_datetime(reddit_df['date'])  # Convert to datetime
    df = reddit_df.sort_values(by='date')
    df['date'] = df['date'].dt.to_period("M")
    df_trend = df.groupby('date').size().reset_index(name='num_posts')
    df_trend['date'] = df_trend['date'].dt.to_timestamp()
    df_trend['smoothed'] = df_trend['num_posts'].rolling(window=3, min_periods=1).mean()
    plt.figure(figsize=(12, 6))
    plt.plot(df_trend['date'], df_trend['smoothed'], color='blue', marker='o', linestyle='-')
    plt.title("Number of Posts Over Time (Trend)")
    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.grid(True)
    plt.savefig("../graphs/reddit/reddit_posting_trend")

    # wordcloud
    text = " ".join(title for title in df['title'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Most Common Words in Titles")
    plt.savefig("../graphs/reddit/reddit_wordcloud.png")


# start_time = time.time()
# reddit_data = scrap_posts(query, num_posts)
# end_time = time.time()
# save_to_csv(reddit_data)
#
# print(f"Scraping completed in {end_time - start_time} seconds. Data saved to 'renewable_energy_posts.csv'")


df = pd.read_csv("../datasets/raw/reddit_posts.csv")
analyze_data(df)
visualize_data_trends(df)


