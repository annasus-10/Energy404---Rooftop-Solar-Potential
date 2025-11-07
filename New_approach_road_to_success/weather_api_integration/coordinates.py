from geopy.geocoders import Nominatim
import pandas as pd, time

cities = [
    "Accra","Almaty","Antigua","Beirut","Colombo","Dar es Salaam","Dhaka","Dominica",
    "Grenada","Izmir","Johannesburg","Karachi","Lagos State","Maldives","Manila",
    "Mexico City","Nairobi","Panama City","Rustavi","Samarkand","San Pedro Sula",
    "Sint Maarten","Saint Lucia","Saint Vincent and the Grenadines","Tegucigalpa"
]
  
geolocator = Nominatim(user_agent="solar_project")

rows = []
for city in cities:
    loc = geolocator.geocode(city)
    if loc:
        rows.append({"City": city, "Latitude": loc.latitude, "Longitude": loc.longitude})
        print(f"{city}: {loc.latitude:.4f}, {loc.longitude:.4f}")
    time.sleep(1)  # pause to avoid rate limits

pd.DataFrame(rows).to_csv("city_coords.csv", index=False)
print("✅ Saved city_coords.csv")
