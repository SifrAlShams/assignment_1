import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def visualize_data_trends(kaggle_df):
    # renewable energy consumption trend over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=kaggle_df, x="TIME", y="Value", marker="o", linewidth=2)
    plt.title("Renewable Energy Consumption Over Time")
    plt.xlabel("Year")
    plt.ylabel("Energy Consumption (KTOE)")
    plt.grid(True)
    plt.savefig("../graphs/kaggle/consumption_trend.png")

    # top countries by renewable energy consumption
    top_countries = kaggle_df.groupby("LOCATION")["Value"].sum().nlargest(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_countries.index, y=top_countries.values, hue=top_countries.index)
    plt.xlabel("Country")
    plt.ylabel("Total Renewable Energy Consumption (KTOE)")
    plt.title("Top 10 Countries by Renewable Energy Consumption")
    plt.xticks(rotation=45)
    plt.savefig("../graphs/kaggle/top_consumer_countries.png")



df = pd.read_csv("../datasets/raw/kaggle_dataset.csv")

print(f"Top 5 rows")
print(df.head())
print("---------------------------")
print(" ")

print(f"About Data")
print(df.info())
print("---------------------------")
print(" ")

print(f"Null values check")
print(df.isnull().sum())  # Check missing values
print("---------------------------")
print(" ")

# drop 'Flag Codes' column coz it has too many nulls and does not contribute to analysis
df = df.drop(columns=["Flag Codes"])

# since, "Value" columns also has nulls, remove rows with null values
df = df.dropna()

#cleaned dataset
print("---------------------------")
print(f"Statistical Summary")
print(df.describe())
print("---------------------------")
print(" ")

visualize_data_trends(df)


