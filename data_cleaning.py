import pandas as pd

# STEP 1: Load original dataset
df = pd.read_csv("social_media_data.csv")

print("ORIGINAL DATA")
print("Total posts:", len(df))

# STEP 2: Remove duplicate post IDs
df = df.drop_duplicates(subset="post_id", keep="first")

# STEP 3: Convert date into datetime format
df["post_date"] = pd.to_datetime(
    df["post_date"], errors="coerce"
)

# STEP 4: Convert numerical columns into numbers
numeric_columns = ["views", "likes", "comments", "shares"]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

# STEP 5: Remove deleted posts
deleted_posts = (df["status"] == "Deleted").sum()

df = df[df["status"] != "Deleted"].copy()

print("\nDeleted posts removed:", deleted_posts)

# STEP 6: Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# STEP 7: Identify zero-view posts
zero_views = df["views"] == 0

print("\nZero-view posts:", zero_views.sum())

# Keep zero-view posts because they are valid records.
# We will handle their engagement rate later.

# STEP 8: Detect viral outliers using IQR
positive_views = df.loc[df["views"] > 0, "views"]

Q1 = positive_views.quantile(0.25)
Q3 = positive_views.quantile(0.75)

IQR = Q3 - Q1

upper_limit = Q3 + (1.5 * IQR)

df["viral_outlier"] = df["views"] > upper_limit

print("\nViral outlier limit:", upper_limit)
print("Viral outliers:", df["viral_outlier"].sum())

# STEP 9: Save cleaned dataset
df.to_csv("cleaned_social_media_data.csv", index=False)

# STEP 10: Display final results
print("\nCLEANING COMPLETED")

print("Final total posts:", len(df))

print("\nCleaned dataset:")
print(df)

print("\nCleaned dataset saved successfully!")
