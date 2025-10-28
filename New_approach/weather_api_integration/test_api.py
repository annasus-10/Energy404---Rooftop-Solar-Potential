import requests
import pandas as pd

city = "Bangkok"
lat, lon = 13.7563, 100.5018

url = (
    "https://power.larc.nasa.gov/api/temporal/monthly/point?"
    "parameters=ALLSKY_SFC_SW_DWN,T2M,ALLSKY_KT,PRECTOTCORR&"
    "community=RE&longitude="
    f"{lon}&latitude={lat}&start=2024&end=2024&format=JSON"
)

r = requests.get(url)
print("Status code:", r.status_code)

data = r.json()
if "properties" not in data or "parameter" not in data["properties"]:
    print("❌ Unexpected response:")
    print(data)
    raise SystemExit()

df = pd.DataFrame(data["properties"]["parameter"])
df = df.iloc[:12]  # ✅ remove annual summary row
df["month"] = range(1, 13)

annual = pd.DataFrame({
    "City": [city],
    "avg_GHI_kWhm2_day": [df["ALLSKY_SFC_SW_DWN"].mean()],
    "avg_temp_C": [df["T2M"].mean()],
    "clearness_index": [df["ALLSKY_KT"].mean()],
    "precip_mm_day": [df["PRECTOTCORR"].mean()],
})

print("\n✅ Annual weather summary:")
print(annual)
