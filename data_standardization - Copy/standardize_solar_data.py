import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

input_folder = "datasets"
output_folder = "cleaned_data"
os.makedirs(output_folder, exist_ok=True)

common_columns = [
    "City",
    "Surface_area",
    "Potential_installable_area",
    "Peak_installable_capacity",
    "Energy_potential_per_year",
    "Assumed_building_type",
    "Estimated_tilt",
    "Estimated_building_height",
    "Estimated_capacity_factor"
]

for file in os.listdir(input_folder):
    if file.endswith(".csv") and "rooftop" in file.lower():
        file_path = os.path.join(input_folder, file)
        print(f"\nProcessing: {file}")

        df = pd.read_csv(file_path)
        existing_cols = [col for col in common_columns if col in df.columns]
        df = df[existing_cols]

        if "City" in df.columns and df["City"].isna().any():
            city_guess = file.split("_")[0].capitalize()
            df["City"].fillna(city_guess, inplace=True)

        if "Assumed_building_type" in df.columns:
            le = LabelEncoder()
            df["Assumed_building_type"] = le.fit_transform(df["Assumed_building_type"].astype(str))

        city_name = file.split("_")[0].lower()
        output_file = f"{city_name}.csv"
        output_path = os.path.join(output_folder, output_file)

        df.to_csv(output_path, index=False)
        print(f"✅ Saved standardized file: {output_path}")

print("\nAll datasets standardized and saved in:", output_folder)
