import pandas as pd

# Load the geocoded dataset
df = pd.read_csv("E:/Data Vis/disasters_expanded_geocoded.csv")

# Drop rows where either Latitude or Longitude is missing (NaN)
df_cleaned = df.dropna(subset=["Latitude", "Longitude"])

# Optionally: you could also check for 0.0 values if needed:
# df_cleaned = df_cleaned[(df_cleaned["Latitude"] != 0.0) & (df_cleaned["Longitude"] != 0.0)]

# Save the cleaned dataset
df_cleaned.to_csv("E:/Data Vis/disasters_cleaned_expanded_geocoded.csv", index=False)
print("✅ Saved cleaned dataset to disasters_cleaned_geocoded.csv")
