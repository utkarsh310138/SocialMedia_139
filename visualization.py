import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: Load dataset
df = pd.read_csv("engagement_analysis.csv")

# STEP 2: Convert date into datetime
df["post_date"] = pd.to_datetime(df["post_date"])

# STEP 3: Extract day and hour
df["posting_day"] = df["post_date"].dt.day_name()
df["posting_hour"] = df["post_date"].dt.hour

# STEP 4: Calculate content-type engagement
content_data = df.groupby("content_type")[
    "engagement_rate"
].mean().sort_values(ascending=False)

# GRAPH 1: Content Performance
plt.figure(figsize=(9, 5))
content_data.plot(kind="bar")
plt.title("Average Engagement Rate by Content Type")
plt.xlabel("Content Type")
plt.ylabel("Engagement Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("content_performance.png")
plt.show()


# GRAPH 2: Best Posting Day
day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

day_data = df.groupby("posting_day")[
    "engagement_rate"
].mean().reindex(day_order).dropna()

plt.figure(figsize=(9, 5))
day_data.plot(kind="bar")
plt.title("Average Engagement Rate by Day")
plt.xlabel("Day")
plt.ylabel("Engagement Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("best_posting_day.png")
plt.show()


# GRAPH 3: Best Posting Hour
hour_data = df.groupby("posting_hour")[
    "engagement_rate"
].mean().sort_index()

plt.figure(figsize=(9, 5))
hour_data.plot(kind="bar")
plt.title("Average Engagement Rate by Hour")
plt.xlabel("Posting Hour")
plt.ylabel("Engagement Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("best_posting_hour.png")
plt.show()


# GRAPH 4: Views vs Likes
valid_data = df.dropna(subset=["views", "likes"])

plt.figure(figsize=(9, 5))
plt.scatter(valid_data["views"], valid_data["likes"])
plt.title("Relationship Between Views and Likes")
plt.xlabel("Views")
plt.ylabel("Likes")
plt.tight_layout()
plt.savefig("views_vs_likes.png")
plt.show()

print("All four graphs created successfully!")
