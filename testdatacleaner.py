import pandas as pd
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load original data
df = pd.read_csv("E:/Data Vis/public_emdat_custom_request_2025-04-28_e9726a26-897b-456f-9711-b082d849bed5.csv", encoding="ISO-8859-1")

# Setup geocoder
geolocator = Nominatim(user_agent="cesium_location_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Clean country names (remove anything in parentheses)
df["Country"] = df["Country"].str.replace(r"\s*\(.*?\)", "", regex=True).str.strip()

# Function to clean and split locations
def split_locations(loc_str):
    if pd.isna(loc_str) or not loc_str.strip():
        return []

    # Replace "and" with comma to separate into new rows
    loc_str = re.sub(r'\band\b', ',', loc_str, flags=re.IGNORECASE)

    # Remove descriptive geography terms (add more as needed)
    loc_str = re.sub(r'\b(provinces?|near|regon|districts?|departments?|municipalities|municipality|county|city|prefecture|areas?|regencies|regency|states?)\b', '', loc_str, flags=re.IGNORECASE)

    # Remove directional terms (e.g., NW, NE, SW, SE)
    loc_str = re.sub(r'\b(northwest|northeast|southwest|northeast|NW|NE|SW|SE)\b', '', loc_str, flags=re.IGNORECASE)

    # Remove anything in parentheses
    loc_str = re.sub(r'\([^)]*\)', '', loc_str)

    # Split into separate locations
    locations = re.split(r'[;,]', loc_str)
    return [loc.strip() for loc in locations if loc.strip()]

# Expand rows
expanded_rows = []

for _, row in df.iterrows():
    base_data = row.to_dict()
    locations = split_locations(row.get("Location", ""))

    if not locations and pd.notna(row.get("Country", "")):
        locations = [row["Country"]]

    for loc in locations:
        new_row = base_data.copy()
        new_row["Location"] = loc
        expanded_rows.append(new_row)

# Create new dataframe
expanded_df = pd.DataFrame(expanded_rows)

# Geocoding using both Location and Country
def get_coords(row):
    location_str = f"{row['Location']}, {row['Country']}"
    try:
        location = geocode(location_str)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except Exception as e:
        print(f"Geocoding failed for '{location_str}': {e}")
    return pd.Series([None, None])

expanded_df[["Latitude", "Longitude"]] = expanded_df.apply(get_coords, axis=1)

# Save result
expanded_df.to_csv("E:/Data Vis/disasters_expanded_geocoded.csv", index=False)
print("✅ Saved geocoded results to disasters_expanded_geocoded.csv")
