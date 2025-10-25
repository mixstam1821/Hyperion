# ☀️ Hyperion – Surface Solar Radiation Emulator

**Hyperion** is a Random Forest emulator that predicts monthly **Surface Solar Radiation (SSR)**  
from 2 basic atmospheric parameters: **Cloud cover**, and **AOD**.  
It was trained on radiative-transfer model inputs/outputs from the **EarthSenseData (Stamatis et al., 2025)** (https://zenodo.org/records/17382343).

---

## 🧠 Features
- Predict SSR for **single input values** or **entire time-series files (CSV/XLSX)**  
- Download results instantly in CSV format  
- Interactive **Bokeh dashboard** 
- Fully portable via Docker  
- Uses **scikit-learn 1.7** compatible `.pkl` model

---

## 🎬 Demo
![Hyperion Demo](assets/hyperion.gif)

---

## 📦 Model

First, download the model and place it in the Hyperion folder:

Zenodo DOI: https://zenodo.org/records/17429272

Filename: Hyperion_RF.pkl (~40 MB)

---

## 🚀 Run Locally (Python)
```bash
# 1. Clone and enter repo
git clone https://github.com/mixstam1821/Hyperion.git
cd Hyperion

# 2. Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
bokeh serve --show Hyperion_GUI.py --port=9959

# 5. Open http://localhost:9959/Hyperion_GUI
```

## 🐳 Run with Docker
```bash
# Build image
docker build -t hyperion-app .

# Run container
docker run -p 7860:7860 hyperion-app

# Open http://localhost:7860/Hyperion_GUI
```
