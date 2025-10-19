# Task 1 — Data Standardization

### 📂 Folder purpose
This folder contains the script used to clean and standardize all rooftop solar datasets before merging.

---

## 🚀 Steps to Run

### 1️⃣ Requirements
Make sure you have Python 3.11+ and the following packages installed:
```bash
pip install pandas scikit-learn
```

### 2️⃣ Folder setup
Place all your raw NEO files (e.g., `accra_rooftop_solarpotential.csv`, `colombo_rooftop_solarpotential.csv`, etc.) inside:
```
datasets/
```

### 3️⃣ Run the script
Execute the standardization script:
```bash
python standardize_solar_data.py
```

This will:
- Keep only the common agreed columns
- Label encode `Assumed_building_type`
- Save standardized outputs under:
```
cleaned_data/
```

### 4️⃣ Output
After running, you’ll find files such as:
```
cleaned_data/accra.csv
cleaned_data/colombo.csv
...
```
Upload your cleaned `.csv` into the **`/cleaned_datasets/`** folder in the main repo.
---

## ✅ Final Notes
- Do **not** rename column headers manually — the script ensures consistency.
- Check that your CSV opens correctly before pushing.
- Each teammate should commit only their own city’s cleaned CSV.
- Once all cities are uploaded, we’ll merge them in the next task.
