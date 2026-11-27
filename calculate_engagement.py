import pandas as pd
# STEP 1: Load cleaned dataset
df = pd.read_csv("cleaned_social_media_data.csv")

# STEP 2: Calculate total engagements
df["total_engagement"] = (
    df["likes"] + df["comments"] + df["shares"]
)

# STEP 3: Calculate engagement rate
df["engagement_rate"] = (
    df["total_engagement"] / df["views"].where(df["views"] > 0)
) * 100

# STEP 4: Round engagement rate to 2 decimal places
df["engagement_rate"] = df["engagement_rate"].round(2)

# STEP 5: Display results for first 10 posts
print("\nENGAGEMENT RATE ANALYSIS")

columns = [
    "post_id",
    "views",
    "likes",
    "comments",
    "shares",
    "total_engagement",
    "engagement_rate"
]

print(
    df[columns].head(10).to_string(
        index=False,
        na_rep="N/A"
    )
)

# STEP 6: Manually verify first post
first_post = df.iloc[0]

manual_rate = (
    (first_post["likes"] +
     first_post["comments"] +
     first_post["shares"])
    / first_post["views"]
) * 100

print("\nMANUAL VERIFICATION")
print("Post ID:", first_post["post_id"])
print("Calculated Engagement Rate:", manual_rate, "%")
print("Python Engagement Rate:", first_post["engagement_rate"], "%")

# STEP 7: Save final results
df.to_csv("engagement_analysis.csv", index=False)

print("\nEngagement analysis completed!")
print("File saved successfully!")
