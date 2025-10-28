import pandas as pd
import requests, time

# === Step 1: Load city coordinates file ===
coords = pd.read_csv("C:/Users/User/Desktop/ML/Project/solar-potential-analysis-github-setup/test_weather/city_coords.csv")
print(f"Found {len(coords)} cities")

all_rows = []

# === Step 2: Loop through each city ===
for i, row in coords.iterrows():
    city, lat, lon = row["City"], row["Latitude"], row["Longitude"]
    print(f"\n🔹 Fetching data for {city} ({lat:.2f}, {lon:.2f})...")

    url = (
        "https://power.larc.nasa.gov/api/temporal/monthly/point?"
        "parameters=ALLSKY_SFC_SW_DWN,T2M,ALLSKY_KT,PRECTOTCORR&"
        "community=RE&longitude="
        f"{lon}&latitude={lat}&start=2024&end=2024&format=JSON"
    )

    try:
        r = requests.get(url, timeout=30)
        data = r.json()["properties"]["parameter"]
        df = pd.DataFrame(data).iloc[:12]  # keep only 12 months

        all_rows.append({
            "City": city,
            "avg_GHI_kWhm2_day": df["ALLSKY_SFC_SW_DWN"].mean(),
            "avg_temp_C": df["T2M"].mean(),
            "clearness_index": df["ALLSKY_KT"].mean(),
            "precip_mm_day": df["PRECTOTCORR"].mean(),
        })
        print(f"✅ Done: {city}")
        time.sleep(1)  # small pause to be polite to API

    except Exception as e:
        print(f"⚠️ Failed for {city}: {e}")

# === Step 3: Save results ===
weather_df = pd.DataFrame(all_rows)
weather_df.to_csv("city_weather.csv", index=False)
print("\n🌤️ Saved city_weather.csv with", len(weather_df), "cities")
print(weather_df.head())
