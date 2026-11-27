import pandas as pd

# STEP 1: Load engagement dataset
df = pd.read_csv("engagement_analysis.csv")

# STEP 2: Group data by content type
content_analysis = (
    df.groupby("content_type")["engagement_rate"]
    .agg(["mean", "count"])
)

# STEP 3: Rename columns
content_analysis.columns = [
    "average_engagement_rate",
    "number_of_posts"
]

# STEP 4: Sort by average engagement rate
content_analysis = content_analysis.sort_values(
    by="average_engagement_rate",
    ascending=False
)

# STEP 5: Assign ranking
content_analysis["rank"] = range(
    1, len(content_analysis) + 1
)

# STEP 6: Display results
print("\nCONTENT PERFORMANCE RANKING")

print(content_analysis.round(2).to_string())

# STEP 7: Find best content type
best_content = content_analysis.index[0]

print("\nBEST PERFORMING CONTENT TYPE:")
print(best_content)

# STEP 8: Save results
content_analysis.to_csv("content_performance.csv")

print("\nContent analysis completed!")
print("Results saved successfully!")
