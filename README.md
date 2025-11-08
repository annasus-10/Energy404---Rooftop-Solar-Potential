## ☀️ Energy404 — Rooftop Solar Potential Predictor

This project predicts annual rooftop **solar energy potential (kWh/m²/year)** using a stacked ensemble model (LGBM + XGBoost + RandomForest + Ridge meta-learner).
The system includes both:

* 🧠 **FastAPI backend** for programmatic predictions
* 💡 **Streamlit app** for interactive user interface

---

### 📁 Project Structure

```
FINAL/
├── app.py                # Streamlit web interface
├── api.py                # FastAPI backend
├── pipeline/
│   └── predict.py        # Model loading & inference logic
├── data/
│   └── city_weather.csv  # Static city-level weather inputs
├── dataset/
│   └── dataset.parquet   # Cleaned training dataset
├── requirements.txt      # Dependencies
└── Dockerfile            # Docker setup
```

---

## ⚙️ 1. Local Setup (Recommended for Development)

### 🧩 Step 1 — Clone the Repository

```bash
git clone https://github.com/annasus-10/Energy404---Rooftop-Solar-Potential.git
cd Energy404---Rooftop-Solar-Potential/FINAL
```

### 🧩 Step 2 — Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate     # On Mac/Linux
# OR
.venv\Scripts\activate        # On Windows
```

### 🧩 Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 2. Run Locally

### 🌐 Option A — Streamlit UI

Launch the graphical interface:

```bash
streamlit run app.py
```

Then open:

> [http://localhost:8501](http://localhost:8501)

You can:

* Choose city, building type, and tilt
* See predicted **solar energy (kWh/m²/year)** and **total roof output**

---

### ⚙️ Option B — FastAPI (Backend)

Run the API locally:

```bash
uvicorn api:app --reload --port 8000
```

Access the docs at:

> [http://localhost:8000/docs](http://localhost:8000/docs)

Example request:

```bash
POST /predict
{
  "city": "Accra",
  "building_type": "commercial",
  "tilt": 20
}
```

Example response:

```json
{
  "city": "Accra",
  "building_type": "commercial",
  "tilt": 20,
  "predicted_kWh_per_m2": 267.47
}
```

---

## 🐋 3. Run with Docker (Deployment-Ready)

### 🧱 Build Image

Run this in the project root:

```bash
docker build -t energy404-api -f FINAL/Dockerfile .
```

### ▶️ Run Container

```bash
docker run -p 8000:8000 energy404-api
```

The API will be live at:

> [http://127.0.0.1:8000](http://127.0.0.1:8000)
> or
> [http://0.0.0.0:8000](http://0.0.0.0:8000)

Swagger UI:

> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 💾 Notes for Developers

* Large `.pkl` model files are **excluded** from GitHub for size limits.
  Place trained models under `FINAL/models/` or use `models_local_backup/` as a placeholder for local testing.
* City weather data is static and loaded from `data/city_weather.csv`.
* All scripts assume Python **3.11+** environment.

---

## 🧩 Team: Energy404

**November 2025**

---
