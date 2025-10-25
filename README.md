# ☀️ Hyperion – Surface Solar Radiation Emulator

**Hyperion** is a Random Forest emulator that predicts monthly **Surface Solar Radiation (SSR)**  
from 2 basic atmospheric parameters: **Cloud cover**, and **AOD**.  
It was trained on radiative-transfer model outputs from the **EarthSenseData (Stamatis et al., 2025)** (https://zenodo.org/records/17382343).

---

## 🧠 Features
- Predict SSR for **single input values** or **entire time-series files (CSV/XLSX)**  
- Download results instantly in CSV format  
- Interactive **Bokeh dashboard** 
- Fully portable via Docker  
- Uses **scikit-learn 1.7** compatible `.pkl` model

---

## 🚀 Run Locally (Python)
```bash
# 1. Clone and enter repo
git clone https://github.com/yourusername/Hyperion.git
cd Hyperion

# 2. Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
bokeh serve . --allow-websocket-origin="*" --port 9942 --session-token-expiration=86400000
```

## 🐳 Run with Docker
```bash
# Build image
docker build -t hyperion-app .

# Run container
docker run -p 7860:7860 hyperion-app
```
