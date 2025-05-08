import pandas as pd
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load original data
df = pd.read_csv("public_emdat_custom_request_2025-04-28_e9726a26-897b-456f-9711-b082d849bed5.csv")  # Change to your actual filename

# Setup geocoder
geolocator = Nominatim(user_agent="cesium_location_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Define cleanup function
def clean_location(raw_loc):
    if pd.isna(raw_loc) or raw_loc.strip() == "":
        return []

    # Lowercase "near" removal, and words like province, region etc
    raw_loc = re.sub(r'\bnear\b', '', raw_loc, flags=re.IGNORECASE)
    raw_loc = re.sub(r'\b(province|region|state|district|departments?|municipality|county|city|prefecture|area)\b', '', raw_loc, flags=re.IGNORECASE)
    
    # Remove anything in brackets (e.g., "(Jiangxi)")
    raw_loc = re.sub(r'\([^)]*\)', '', raw_loc)

    # Normalize semicolons and commas to splits
    locations = re.split(r'[;,]', raw_loc)

    # Strip whitespace and filter empty
    cleaned = [loc.strip() for loc in locations if loc.strip()]
    return cleaned

# Collect all exploded locations
expanded_rows = []

for idx, row in df.iterrows():
    base_info = row.to_dict()
    cleaned_locations = clean_location(base_info.get("Location", ""))
    
    if not cleaned_locations:
        # If no valid location, fallback to Country (if any)
        if pd.notna(row.get("Country", "")):
            cleaned_locations = [row["Country"]]
        else:
            continue  # Skip row with no valid place

    for loc in cleaned_locations:
        new_row = base_info.copy()
        new_row["Cleaned Location"] = loc
        expanded_rows.append(new_row)

# Create a new DataFrame
expanded_df = pd.DataFrame(expanded_rows)

# Geocode each location
def get_coords(place):
    try:
        location = geocode(place)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        pass
    return pd.Series([None, None])

expanded_df[["Latitude", "Longitude"]] = expanded_df["Cleaned Location"].apply(get_coords)

# Save result
expanded_df.to_csv("disasters_expanded_geocoded.csv", index=False)
print("✅ Saved geocoded results to disasters_expanded_geocoded.csv")
