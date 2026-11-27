import pandas as pd

# STEP 1: Load engagement analysis dataset
df = pd.read_csv("engagement_analysis.csv")

# STEP 2: Convert post_date into datetime format
df["post_date"] = pd.to_datetime(df["post_date"])

# STEP 3: Extract day name
df["posting_day"] = df["post_date"].dt.day_name()

# STEP 4: Extract posting hour
df["posting_hour"] = df["post_date"].dt.hour

# STEP 5: Find average engagement by day
day_analysis = (
    df.groupby("posting_day")["engagement_rate"]
    .agg(["mean", "count"])
    .sort_values("mean", ascending=False)
)

print("\nAVERAGE ENGAGEMENT BY DAY")
print(day_analysis.round(2))

# STEP 6: Find average engagement by hour
hour_analysis = (
    df.groupby("posting_hour")["engagement_rate"]
    .agg(["mean", "count"])
    .sort_values("mean", ascending=False)
)

print("\nAVERAGE ENGAGEMENT BY HOUR")
print(hour_analysis.round(2))

# STEP 7: Find the best posting day
best_day = day_analysis["mean"].idxmax()

print("\nBEST POSTING DAY:", best_day)

# STEP 8: Find the best posting hour
best_hour = hour_analysis["mean"].idxmax()

print("BEST POSTING HOUR:", best_hour)

# STEP 9: Save analysis results
day_analysis.to_csv("best_posting_day.csv")
hour_analysis.to_csv("best_posting_hour.csv")

print("\nPosting time analysis completed!")
