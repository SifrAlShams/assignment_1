import time
import pandas as pd
from pytrends.request import TrendReq
import seaborn as sns
import matplotlib.pyplot as plt

pytrends = TrendReq(hl='en-US', tz=360)

keywords = ["renewable energy", "solar power", "wind energy"]

def fetch_data(topic_keywords):
    for attempt in range(5):
        try:
            pytrends.build_payload(kw_list=topic_keywords, timeframe='today 12-m')
            data = pytrends.interest_over_time()
            if 'isPartial' in data.columns:
                data = data.drop(columns=['isPartial'])
            return data
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error - {e}")
            time.sleep(60)
    return None


def save_data(scrapped_data):
    melted_data = scrapped_data.reset_index().melt(id_vars=['date'], var_name='keyword',
                                                        value_name='interest_score')
    melted_data.to_csv("../datasets/raw/google_trends_data.csv", index=False)


def analyze_data(google_df):
    print("Statistical Summary of Data:")
    print(google_df.describe())

    # time series analysis
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=google_df, x="date", y="interest_score", hue="keyword", marker="o")
    plt.title("Google Search Trends for Renewable Energy")
    plt.xlabel("Date")
    plt.ylabel("Interest Score")
    plt.xticks(rotation=45)
    plt.legend(title="Keyword")
    plt.grid(True)
    plt.savefig("../graphs/google_trends/google_trends.png")


def visualize_data_trend(google_df):
    #histogram of interest score
    plt.figure(figsize=(10, 5))
    sns.histplot(google_df["interest_score"], bins=20, kde=True)
    plt.title("Distribution of Interest Scores")
    plt.xlabel("Interest Score")
    plt.ylabel("Frequency")
    plt.savefig("../graphs/google_trends/hist_interest_score.png")

    # heatmap
    pivot_table = google_df.pivot(index="date", columns="keyword", values="interest_score")
    plt.figure(figsize=(8, 5))
    sns.heatmap(pivot_table.corr(), annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Between Keyword Search Trends")
    plt.savefig("../graphs/google_trends/keywords_heatmap.png")


# start_time = time.time_ns()
# google_trends_data = fetch_data(keywords)
# end_time = time.time()
#
# if google_trends_data is not None:
#     save_data(google_trends_data)
#     print(f"Data scrapped in {end_time - start_time} seconds, and saved successfully!")

df = pd.read_csv("../datasets/raw/google_trends_data.csv")
print(df.isna().sum())
print(" ")
analyze_data(df)
visualize_data_trend(df)