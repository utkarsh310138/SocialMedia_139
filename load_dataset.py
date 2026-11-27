# Step 1: Import Pandas
import pandas as pd

# Step 2: Load CSV file
df = pd.read_csv("social_media_data.csv")

# Step 3: Display first 5 rows
print("\nFIRST 5 ROWS")
print(df.head())

# Step 4: Display last 5 rows
print("\nLAST 5 ROWS")
print(df.tail())

# Step 5: Display total rows and columns
print("\nDATASET SHAPE")
print(df.shape)

# Step 6: Display column names
print("\nCOLUMN NAMES")
print(df.columns)

# Step 7: Display dataset information
print("\nDATASET INFORMATION")
df.info()

# Step 8: Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())
