## ⚡️ Energy404 API Guide (for Frontend Integration)

### 🔗 Base URL (Local)

```
http://127.0.0.1:8000
```

> If using Docker, it may appear as `http://0.0.0.0:8000`.

---

### 🧩 1. Root Check

Quick test to confirm the API is running:

```bash
GET /
```

**Response:**

```json
{
  "message": "☀️ Energy404 API is running! Use POST /predict to get predictions."
}
```

---

### ☀️ 2. Predict Solar Potential

**Endpoint**

```
POST /predict
```

**Request Body (JSON)**

```json
{
  "city": "Accra",
  "building_type": "commercial",
  "tilt": 20
}
```

**Response**

```json
{
  "city": "Accra",
  "building_type": "commercial",
  "tilt": 20,
  "predicted_kWh_per_m2": 267.47
}
```

---

### 💡 Parameter Reference

| Field           | Type   | Example        | Description                               |
| :-------------- | :----- | :------------- | :---------------------------------------- |
| `city`          | string | `"Accra"`      | Must match one of the 20 supported cities |
| `building_type` | string | `"commercial"` | Must match model training categories      |
| `tilt`          | number | `20`           | Roof tilt angle in degrees (0–60°)        |

---

### 🧱 Example with JavaScript (Fetch)

```javascript
fetch("http://127.0.0.1:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    city: "Accra",
    building_type: "commercial",
    tilt: 20
  })
})
  .then(res => res.json())
  .then(data => console.log("Predicted:", data.predicted_kWh_per_m2))
  .catch(err => console.error("Error:", err));
```

---

### ⚙️ Example with Python (Requests)

```python
import requests

url = "http://127.0.0.1:8000/predict"
payload = {
    "city": "Accra",
    "building_type": "commercial",
    "tilt": 20
}

response = requests.post(url, json=payload)
print(response.json())
```

---

### 🧪 Test via Swagger UI

Open your browser at:

> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Then click **“POST /predict” → Try it out → Execute** to test requests interactively.

---

### ✅ Expected Output

* `predicted_kWh_per_m2` → annual energy potential per square meter
* The frontend can multiply this by roof area (m²) to show total yearly kWh

---

