
import pandas as pd

# Creating sample social media data
data = {
    "post_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    
    "platform": [
        "YouTube", "Instagram", "YouTube", "Instagram",
        "YouTube", "Instagram", "YouTube", "Instagram",
        "YouTube", "Instagram", "YouTube", "Instagram"
    ],

    "content_type": [
        "Video", "Reel", "Short", "Image",
        "Video", "Reel", "Short", "Image",
        "Video", "Reel", "Short", "Image"
    ],

    "post_date": [
        "2026-11-01 09:00",
        "2026-11-02 12:00",
        "2026-11-03 15:00",
        "2026-11-04 18:00",
        "2026-11-05 10:00",
        "2026-11-06 14:00",
        "2026-11-07 19:00",
        "2026-11-08 11:00",
        "2026-11-09 16:00",
        "2026-11-10 20:00",
        "2026-11-11 13:00",
        "2026-11-12 17:00"
    ],

    "views": [
        1000, 2500, 0, 4000, 1500, 8000,
        500, 1200, 1000000, 3000, 2000, 0
    ],

    "likes": [
        100, 300, 0, 400, 150, 900,
        50, 100, 150000, 350, 200, 0
    ],

    "comments": [
        10, 25, 0, 40, 15, 90,
        5, 10, 20000, 35, 20, 0
    ],

    "shares": [
        5, 30, 0, 20, 10, 80,
        3, 8, 50000, 25, 15, 0
    ],

    "status": [
        "Active", "Active", "Active", "Active",
        "Active", "Active", "Active", "Active",
        "Active", "Active", "Deleted", "Active"
    ]
}

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Save dataset as CSV
df.to_csv("social_media_data.csv", index=False)

print("Dataset created successfully!")
print(df.head())
