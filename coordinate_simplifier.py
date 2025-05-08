import csv

input_file = 'Downloads/Data Vis/Disasters_expanded_geocoded.csv'
output_file = 'Downloads/Data Vis/disaster_coords_simplified.csv'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # Write header for Unity
    writer.writerow(['Name', 'Latitude', 'Longitude', 'Height'])

    for row in reader:
        name = row['DisNo.'].strip() if row['DisNo.'] else "Unnamed"
        lat = row['Latitude'].strip()
        lon = row['Longitude'].strip()

        if lat and lon:
            writer.writerow([name, lat, lon, 150])
