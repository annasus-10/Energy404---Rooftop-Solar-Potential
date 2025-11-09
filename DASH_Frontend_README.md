# 🌟 Energy404 — Dash Frontend

This is the **Dash-based web frontend** for the Energy404 solar potential prediction system.
You treat the same as you did in app.py
we won't use app.py instead energy_dash.py is the one we'll use 

---

## 📁 File Structure

\`\`\`
FINAL/
├── energy_dash.py           # ← Dash web application (this file)
├── api.py                # FastAPI backend
├── pipeline/
│   └── predict.py        # Model inference
└── requirements.txt # added Dash dependencies
\`\`\`

---

## 🚀 Quick Start

### Step 1: Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 2: Start the FastAPI Backend

In one terminal, run:

\`\`\`bash
uvicorn api:app --reload --port 8000
\`\`\`

This starts the backend API at `http://127.0.0.1:8000`

### Step 3: Launch the Dash Frontend

In another terminal, run:

\`\`\`bash
python app_dash.py
\`\`\`

The Dash app will be available at:

> **http://127.0.0.1:8050**

---

## 🎨 Features

- **Dynamic Dropdown Menus**: City and building type options fetched from API `/metadata` endpoint
- **Interactive Slider**: Adjust tilt angle from 0° to 60°
- **Real-time Predictions**: Instant results displayed after clicking "Predict Solar Potential"
- **Clean, Professional Design**: Energy-themed golden/amber color palette
- **Error Handling**: Clear error messages if backend is unavailable

---

## 🔧 Configuration

### Change API URL

Edit `API_BASE_URL` in `app_dash.py`:

\`\`\`python
API_BASE_URL = "http://127.0.0.1:8000"  # Change this if your API runs elsewhere
\`\`\`

### Change Dash Port

Edit the last line in `app_dash.py`:

\`\`\`python
app.run_server(debug=True, host='127.0.0.1', port=8050)  # Change port here
\`\`\`

---

## 📊 How It Works

1. **User selects** city, building type, and tilt angle
2. **Dash sends POST request** to `http://127.0.0.1:8000/predict`
3. **FastAPI backend** calls `predict.py` to run the ensemble model
4. **Result displayed** showing predicted kWh/m²/year

---

## 🐛 Troubleshooting

### "Connection Error" message

**Problem**: Dash cannot connect to the FastAPI backend.

**Solution**: 
- Ensure `api.py` is running: `uvicorn api:app --reload --port 8000`
- Check that both servers are using compatible ports (API: 8000, Dash: 8050)

### Dropdown menus are empty

**Problem**: API `/metadata` endpoint not responding.

**Solution**: 
- The app has fallback hardcoded values
- Verify API is running and accessible at `http://127.0.0.1:8000/metadata`

---

## 🎯 Team: Energy404

**November 2025**
