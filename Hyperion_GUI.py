
import base64
from io import BytesIO
import gc
import json
import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.models import (GlobalInlineStyleSheet,InlineStyleSheet,
    ColumnDataSource, Div, TextInput, Slider, Button, FileInput, Select,
    DataTable, TableColumn, NumberFormatter,DateFormatter, HoverTool, CustomJS, Tabs, TabPanel
)
from bokeh.plotting import figure
from bokeh.layouts import column, row, Spacer

gstyle = GlobalInlineStyleSheet(css=""" html, body, .bk, .bk-root {background-color: #2F2F2F; margin: 0; padding: 0; height: 100%; color: white; font-family: 'Consolas', 'Courier New', monospace; } .bk { color: white; } .bk-input, .bk-btn, .bk-select, .bk-slider-title, .bk-headers, .bk-label, .bk-title, .bk-legend, .bk-axis-label { color: white !important; } .bk-input::placeholder { color: #aaaaaa !important; } """)
tabs_style = InlineStyleSheet(css=""" /* Main tabs container */ :host { background: #2d2d2d !important; border-radius: 14px !important; padding: 8px !important; margin: 10px !important; box-shadow: 0 6px 20px #00ffe055, 0 2px 10px rgba(0, 0, 0, 0.3) !important; border: 1px solid rgba(0, 191, 255, 0.3) !important; } /* Tab navigation bar */ :host .bk-tabs-header { background: transparent !important; border-bottom: 2px solid #00bfff !important; margin-bottom: 8px !important; } /* Individual tab buttons */ :host .bk-tab { background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%) !important; color: #00bfff !important; border: 1px solid #555 !important; border-radius: 8px 8px 0 0 !important; padding: 12px 20px !important; margin-right: 4px !important; font-family: 'Arial', sans-serif !important; font-weight: 600 !important; font-size: 0.95em !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; position: relative !important; overflow: hidden !important; } /* Tab hover effect */ :host .bk-tab:hover { background: linear-gradient(135deg, #dc1cdd 0%, #ff1493 100%) !important; color: #ffffff !important; border-color: #dc1cdd !important; box-shadow: 0 4px 15px rgba(220, 28, 221, 0.5) !important; transform: translateY(-2px) !important; } /* Active tab styling */ :host .bk-tab.bk-active { background: linear-gradient(135deg, #00bfff 0%, #0080ff 100%) !important; color: #000000 !important; border-color: #00bfff !important; box-shadow: 0 4px 20px rgba(0, 191, 255, 0.6), inset 0 2px 0 rgba(255, 255, 255, 0.3) !important; transform: translateY(-1px) !important; font-weight: 700 !important; } /* Active tab glow effect */ :host .bk-tab.bk-active::before { content: '' !important; position: absolute !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important; background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%) !important; animation: shimmer 2s infinite !important; } @keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } } /* Tab content area */ :host .bk-tab-content { background: transparent !important; padding: 16px !important; border-radius: 0 0 10px 10px !important; } /* Focus states for accessibility */ :host .bk-tab:focus { outline: 2px solid #00bfff !important; outline-offset: 2px !important; } /* Disabled tab state */ :host .bk-tab:disabled { background: #1a1a1a !important; color: #666 !important; cursor: not-allowed !important; opacity: 0.5 !important; } """)
base_variables = """ :host { /* CSS Custom Properties for easy theming */ --primary-color: #8b5cf6; --secondary-color: #06b6d4; --background-color: #1f2937; --surface-color: #343838; --text-color: #f9fafb; --accent-color: #f59e0b; --danger-color: #ef4444; --success-color: #10b981; --border-color: #4b5563; --hover-color: #6366f1; background: none !important; } """
file_input_style = InlineStyleSheet(css=base_variables + """ :host input[type="file"] { background: var(--surface-color) !important; color: var(--text-color) !important; border: 2px dashed var(--border-color) !important; border-radius: 6px !important; padding: 20px !important; font-size: 14px !important; cursor: pointer !important; transition: all 0.2s ease !important; } :host input[type="file"]:hover { border-color: var(--primary-color) !important; background: rgba(139, 92, 246, 0.05) !important; } :host input[type="file"]::file-selector-button { background: var(--primary-color) !important; color: white !important; border: none !important; border-radius: 4px !important; padding: 8px 16px !important; margin-right: 12px !important; cursor: pointer !important; font-weight: 600 !important; } """)
textinput_css = InlineStyleSheet(css=""" /* Outer container styling */ :host { background: #181824 !important; border-radius: 14px !important; padding: 12px !important; box-shadow: 0 4px 18px #0006 !important; } /* Title label styling */ :host .bk-input-group label, :host .bk-textinput-title { color: #34ffe0 !important; font-size: 1.05em !important; font-family: 'Fira Code', monospace; font-weight: bold !important; margin-bottom: 8px !important; letter-spacing: 0.5px !important; text-shadow: 0 2px 10px #34ffe077, 0 1px 3px #222; } /* The input box — reduced height */ :host input[type="text"] { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; padding: 6px 12px !important;     /* 🔹 smaller padding = less height */ font-size: 0.95em !important;     /* 🔹 slightly smaller text */ transition: border 0.12s, box-shadow 0.12s; box-shadow: none !important; } /* On hover/focus */ :host input[type="text"]:hover, :host input[type="text"]:focus { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 12px #ff3049aa !important; outline: none !important; } /* Placeholder text */ :host input[type="text"]::placeholder { color: #9ca3af !important; opacity: 0.7 !important; font-style: italic !important; } """)
slider_style = InlineStyleSheet(css=""" /* Host: set the widget's container background */ :host { background: #16161e !important;   /* even darker than black for modern dark UI */ border-radius: 12px !important; padding: 12px !important; box-shadow: 0 4px 12px #0006 !important; } /* Slider title */ :host .bk-slider-title { color: #00ffe0 !important;     /* bright cyan for the title */ font-size: 0.95em !important; font-weight: bold !important; letter-spacing: 1px !important; font-family: 'Fira Code', 'Consolas', 'Menlo', monospace !important; margin-bottom: 14px !important; text-shadow: 0 2px 12px #00ffe099; } /* Track (background) */ :host .noUi-base, :host .noUi-target { background: #23233c !important; border: 1px solid #2a3132 !important; } /* Filled portion */ :host .noUi-connect { background: linear-gradient(90deg, #00ffe0 10%, #d810f7 90%) !important; box-shadow: 0 0 12px #00ffe099; border-radius: 12px !important; } /* Handle */ :host .noUi-handle { background: #343838 !important; border: 2px solid #00ffe0 !important; border-radius: 50%; width: 20px; height: 20px; } /* Handle hover/focus */ :host .noUi-handle:hover, :host .noUi-handle:focus { border-color: #ff2a68 !important; box-shadow: 0 0 10px #ff2a6890; } /* Tooltip */ :host .noUi-tooltip { background: #343838 !important; color: #00ffe0 !important; font-family: 'Consolas', monospace; border-radius: 6px; border: 1px solid #00ffe0; } """)
select_css = InlineStyleSheet(css=""" /* Widget container */ :host { background: #181824 !important; border-radius: 14px !important; padding: 16px !important; box-shadow: 0 4px 24px #0007 !important; } /* Title styling */ :host .bk-input-group label, :host .bk-select-title { color: #06f0ff !important; font-size: 1.18em !important; font-family: 'Fira Code', monospace; font-weight: bold !important; margin-bottom: 12px !important; letter-spacing: 1px !important; text-shadow: 0 2px 12px #06f0ff88, 0 1px 6px #111b; } /* Dropdown select */ :host select { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; padding: 10px 14px !important; font-size: 1.07em !important; transition: border 0.1s, box-shadow 0.1s; box-shadow: none !important; } /* Glow effect on hover/focus */ :host select:hover, :host select:focus { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 18px #ff3049cc !important; outline: none !important; } """)
button_style = InlineStyleSheet(css=base_variables + """ :host button { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important; color: white !important; border: none !important; border-radius: 6px !important; padding: 10px 20px !important; font-size: 14px !important; font-weight: 600 !important; cursor: pointer !important; transition: all 0.2s ease !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; } :host button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important; background: linear-gradient(135deg, var(--hover-color), var(--primary-color)) !important; } :host button:active { transform: translateY(0) !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important; } :host button:disabled { background: #6b7280 !important; cursor: not-allowed !important; transform: none !important; box-shadow: none !important; } """)
dark_table_style = InlineStyleSheet(css=""" /* Container styling */ :host { background: #2e2e30 !important; border-radius: 14px !important; padding: 16px !important; box-shadow: 0 4px 18px #0006 !important; margin: 10px !important; } /* Headers */ :host div[class*="header"], :host div[class*="slick-header"], :host th, :host [class*="header"] { background: #2e2e30 !important; color: #34ffe0 !important; font-weight: bold !important; font-family: 'Fira Code', monospace !important; border-bottom: 1px solid #06b6d4 !important; } /* cells */ :host div[class*="cell"], :host div[class*="slick-cell"], :host td { background: #565755 !important; color: #fff4da !important; border-right: 1px solid #908e8e !important; border-bottom: 1px solid #908e8e !important; font-family: 'Fira Code', monospace !important; font-size: 1.2em !important; } /* Alternating rows */ :host div[class*="row"]:nth-child(even) div[class*="cell"], :host div[class*="slick-row"]:nth-child(even) div[class*="slick-cell"], :host tr:nth-child(even) td { background: #2a2a2c !important; color: #fff4da !important; border-right: 1px solid #908e8e !important; border-bottom: 1px solid #908e8e !important; font-family: 'Fira Code', monospace !important; font-size: 1.2em !important; } /* Hover effects */ :host div[class*="row"]:hover div[class*="cell"], :host div[class*="slick-row"]:hover div[class*="slick-cell"], :host tr:hover td { background: #3eafff !important; color: #0c0c0c !important; border-color: #ff0000 !important; border-style: solid !important; border-width: 1px !important; } /* Selected cells */ :host div[class*="slick-cell"][class*="selected"], :host div[class*="cell"][class*="selected"] { background: pink !important; color: red !important; border: 1px solid #ff1493 !important; } /* Selected cells */ :host div[class*="row"]:nth-child(even) div[class*="cell"][class*="selected"], :host div[class*="slick-row"]:nth-child(even) div[class*="slick-cell"][class*="selected"]{ background: pink !important; color: black !important; border: 1px solid #ff1493 !important; } /* Scrollbars */ :host *::-webkit-scrollbar { width: 9px !important; height: 8px !important; background: #1a1a2e !important; } :host *::-webkit-scrollbar-thumb { background: #06b6d4 !important; border-radius: 4px !important; } :host *::-webkit-scrollbar-track { background: #1c2e1a !important; border-radius: 4px !important; } /* Firefox scrollbars */ :host .bk-data-table { scrollbar-color: #06b6d4 #1c2e1a !important; scrollbar-width: thin !important; } /* But restore specific dark backgrounds where needed */ :host div[class*="header"] * { background-color: #1a1a2e !important; } :host [class*="header"] * { color: #34ffe0 !important; } """)
pulse_shadow_css = InlineStyleSheet(css=""" :host { position: relative; background: #444444; border-radius: 20px; text-align: center; padding: 18px; margin: 40px auto; box-shadow: 0 0 38px 10px rgba(255,70,0,0.46), 0 0 70px 18px rgba(255,200,40,0.12), 0 0 26px 5px rgba(255,235,90,0.22); box-sizing: border-box; z-index: 0; animation: pulse-shadow 2.2s infinite alternate; } @keyframes pulse-shadow { 0% { box-shadow: 0 0 16px 3px rgba(230, 70, 10, 0.90), 0 0 32px 8px rgba(255, 185, 25, 0.60), 0 0 10px 1px rgba(255, 240, 170, 0.82); } 30% { box-shadow: 0 0 32px 10px rgba(255, 130, 10, 0.82), 0 0 44px 14px rgba(252, 200, 40, 0.40), 0 0 22px 3px rgba(255, 235, 120, 0.62); } 50% { box-shadow: 0 0 42px 12px rgba(239, 110, 30, 0.98), 0 0 70px 20px rgba(255, 208, 50, 0.23), 0 0 32px 6px rgba(255, 245, 100, 0.79); } 70% { box-shadow: 0 0 60px 14px rgba(255, 162, 12, 0.83), 0 0 90px 32px rgba(254, 200, 60, 0.22), 0 0 38px 7px rgba(255, 246, 143, 0.61); } 100% { box-shadow: 0 0 80px 22px rgba(255, 80, 0, 0.78), 0 0 120px 38px rgba(255, 220, 70, 0.15), 0 0 60px 12px rgba(255, 248, 192, 0.53); } } """)
# ──────────────────────────────────────────────────────────────────────────────
# 1) Load your trained model 
# ──────────────────────────────────────────────────────────────────────────────
import joblib

class _SSRWrapper:
    """Tiny wrapper to keep interface consistent (predict expects arrays)."""
    def __init__(self, path="Hyperion_RF.pkl"):
        data = joblib.load(path)
        self.model = data["model"]
        self.scaler = data["scaler"]
        self.is_trained = data["trained"]

    def _normalize(self, X):
        return (X - self.scaler["mean"]) / self.scaler["std"]

    def predict(self, cloud_cover, aod, lat, month):
        x = np.column_stack([
            np.atleast_1d(cloud_cover).astype(np.float32),
            np.atleast_1d(aod).astype(np.float32),
            np.atleast_1d(lat).astype(np.float32),
            np.atleast_1d(month).astype(np.float32),
        ])
        x = self._normalize(x)
        return self.model.predict(x)

MODEL_PATH = "Hyperion_RF.pkl"
try:
    model = _SSRWrapper(MODEL_PATH)
except Exception as e:
    model = None
    _load_err = str(e)




######################################################
# ------THIS IS USED TO READ THE PKL ONLINE -------#
# import io
# import joblib
# import numpy as np
# import requests

# class _SSRWrapper:
#     """Tiny wrapper to keep interface consistent (predict expects arrays)."""
#     def __init__(self, url="https://zenodo.org/records/17434541/files/Hyperion_RF.pkl?download=1"):
#         print("📦 Downloading model from Zenodo...")
#         resp = requests.get(url, stream=True)
#         resp.raise_for_status()
#         buffer = io.BytesIO(resp.content)

#         print("🧠 Loading model from memory...")
#         data = joblib.load(buffer)

#         self.model = data["model"]
#         self.scaler = data["scaler"]
#         self.is_trained = data.get("trained", True)

#     def _normalize(self, X):
#         return (X - self.scaler["mean"]) / self.scaler["std"]

#     def predict(self, cloud_cover, aod, lat, month):
#         x = np.column_stack([
#             np.atleast_1d(cloud_cover).astype(np.float32),
#             np.atleast_1d(aod).astype(np.float32),
#             np.atleast_1d(lat).astype(np.float32),
#             np.atleast_1d(month).astype(np.float32),
#         ])
#         x = self._normalize(x)
#         return self.model.predict(x)


# # --- Usage
# try:
#     model = _SSRWrapper()
#     print("✅ Model successfully loaded!")
# except Exception as e:
#     model = None
#     print(f"❌ Model not loaded: {e}")

##############################################




# ──────────────────────────────────────────────────────────────────────────────
# 2) Styling / Header
# ──────────────────────────────────────────────────────────────────────────────
curdoc().title = "Hyperion - SSR Emulator"

curdoc().theme = 'dark_minimal'

header = Div(text="""

  <h1 style="margin:0;color:#8be9fd;font-weight:800;letter-spacing:2.5px;">
    ☀️ Hyperion ☀️
  </h1>
             
  <p style="margin:6px 0 0;font-size:14px;color:#c8d1dc;">
    A Random Forest SSR Emulator trained with the EarthSenseData (Stamatis et al., 2025).<br>Predict Surface Solar Radiation (W/m²) from <b>Cloud</b> and <b>AOD</b> inputs.
    Use <b>Single</b> inputs or upload a <b>CSV/XLSX</b> to generate a time-series and download results.
  </p>
""", stylesheets=[pulse_shadow_css], width=800 )

# Status / alerts
status = Div(text="", width=800,styles = {"font-size": "14px"})

# ──────────────────────────────────────────────────────────────────────────────
# 3) Widgets — shared
# ──────────────────────────────────────────────────────────────────────────────
cloud_in = TextInput(title="Cloud Cover (0–1 or %)", value="0.5", width=220,stylesheets=[textinput_css])
aod_in   = TextInput(title="AOD (e.g., 0.15)", value="0.15", width=220,stylesheets=[textinput_css])
lat_in   = TextInput(title="Latitude", value="40.0", width=150,stylesheets=[textinput_css])
month_sl = Slider(title="Month (1–12)", start=1, end=12, step=1, value=6, width=190,height = 80,stylesheets=[slider_style])

mode_select = Select(title="Mode", value="Single value", options=["Single value", "Batch via file"], width=220,stylesheets=[select_css])

# ──────────────────────────────────────────────────────────────────────────────
# 4) SINGLE MODE
# ──────────────────────────────────────────────────────────────────────────────
single_predict_btn = Button(label="🔮 Predict SSR", button_type="primary", width=220,stylesheets=[button_style])
single_source = ColumnDataSource(data=dict(name=["SSR"], value=[0.0]))

bar = figure(height=300, width=520, title="Predicted SSR (W/m²)",
             toolbar_location=None, x_range=["SSR"], y_range=(0, 400))
bar.vbar(x="name", top="value", width=0.6, color="#ffa200",hover_line_color="red",source=single_source)
bar.add_tools(HoverTool(tooltips=[("SSR", "@value{0.00} W/m²")]))


def _parse_float(txt, name, minv=None, maxv=None):
    try:
        x = float(txt)
        if minv is not None and x < minv: raise ValueError
        if maxv is not None and x > maxv: raise ValueError
        return x, ""
    except Exception:
        return None, f"❌ {name} invalid."

def do_single_predict():
    if model is None or not model.is_trained:
        status.text = f"❌ Model not loaded. ({_load_err if ' _load_err' in globals() else 'missing file'})"
        return

    # allow % for cloud
    cloud_txt = cloud_in.value.strip()
    if cloud_txt.endswith("%"):
        cloud_txt = cloud_txt[:-1]
        cloud_val, err = _parse_float(cloud_txt, "Cloud")
        if err == "" and cloud_val is not None:
            cloud_val /= 100.0
    else:
        cloud_val, err = _parse_float(cloud_txt, "Cloud")
        if err == "":
            # assume user may pass 0–100; auto-scale if > 1
            if cloud_val > 1.001: cloud_val /= 100.0

    aod_val, err2 = _parse_float(aod_in.value.strip(), "AOD", 0)
    lat_val, err3 = _parse_float(lat_in.value.strip(), "Latitude", -90, 90)
    month_val = int(month_sl.value)

    errs = " ".join([e for e in [err, err2, err3] if e])
    if errs:
        status.text = errs
        return

    pred = model.predict(cloud_val, aod_val, lat_val, month_val)[0]
    single_source.data = dict(name=["SSR"], value=[float(pred)])
    status.text = f"✅ Predicted SSR: <b>{pred:.2f}</b> W/m² (lat={lat_val}, month={month_val}, cloud={cloud_val:.3f}, AOD={aod_val:.3f})"

single_predict_btn.on_click(do_single_predict)

single_panel = TabPanel(child=column(
    row(column(cloud_in, aod_in), column(lat_in, month_sl), column(mode_select, single_predict_btn)),
    row(bar, Spacer(width=20)),
    status
), title="Single value",)

# ──────────────────────────────────────────────────────────────────────────────
# 5) BATCH MODE (File upload → time-series + download)
# ──────────────────────────────────────────────────────────────────────────────
file_in = FileInput(accept=".csv,.xlsx,.xls", width=280, stylesheets=[file_input_style],)
batch_predict_btn = Button(label="📈 Predict Time Series", button_type="primary", width=220,stylesheets=[button_style])
download_btn = Button(label="💾 Download CSV", button_type="success", width=220,stylesheets=[button_style])

batch_src = ColumnDataSource(data=dict(idx=[], time=[], cloud=[], aod=[], lat=[], month=[], ssr=[]))

ts = figure(height=360, width=900, x_axis_type="datetime", title="Predicted SSR Time Series",
            tools="pan,wheel_zoom,box_zoom,reset,save")
ts.line("time", "ssr", source=batch_src, line_color = 'gold',line_width=2, legend_label="Predicted SSR")
ts.scatter("time", "ssr", source=batch_src, size=10, color = 'gold')
ts.add_tools(HoverTool(tooltips=[("time", "@time{%F}"),
                                 ("SSR", "@ssr{0.00} W/m²"),
                                 ("cloud", "@cloud{0.000}"),
                                 ("AOD", "@aod{0.000}")],
                       formatters={"@time": "datetime"}))
ts.legend.location = "top_left"

table = DataTable(
    source=batch_src,
    columns=[
        TableColumn(field="time", title="Time", formatter=DateFormatter(format="%Y-%m")),
        TableColumn(field="cloud", title="Cloud", formatter=NumberFormatter(format="0.000")),
        TableColumn(field="aod",   title="AOD",   formatter=NumberFormatter(format="0.000")),
        TableColumn(field="ssr",   title="SSR (W/m²)", formatter=NumberFormatter(format="0.00")),
    ],
    width=900, height=220, index_position=None, selectable=True,stylesheets=[dark_table_style],
)

def _read_upload(file_input: FileInput) -> pd.DataFrame:
    if not file_input.value:
        raise ValueError("No file uploaded.")
    raw = base64.b64decode(file_input.value)
    name = (file_input.filename or "").lower()

    if name.endswith(".csv"):
        df = pd.read_csv(BytesIO(raw))
    elif name.endswith(".xlsx") or name.endswith(".xls"):
        df = pd.read_excel(BytesIO(raw))
    else:
        # try CSV fallback
        df = pd.read_csv(BytesIO(raw))
    return df

def _standardize_cols(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c.lower().strip(): c for c in df.columns}
    # map possible cloud/aod names
    cloud_col = None
    for cand in ["cloud", "cloud_cover", "catotal", "ccld", "clouds"]:
        if cand in cols:
            cloud_col = cols[cand]; break
    aod_col = None
    for cand in ["aod", "aerosol_optical_depth"]:
        if cand in cols:
            aod_col = cols[cand]; break
    if cloud_col is None or aod_col is None:
        raise ValueError("Input file must contain columns for Cloud and AOD (try: cloud/cloud_cover/CAtotal and aod).")

    out = pd.DataFrame({
        "cloud": df[cloud_col].astype(float),
        "aod": df[aod_col].astype(float)
    })
    # optional time
    time_col = None
    for cand in ["time", "date", "datetime", "month_date"]:
        if cand in cols:
            time_col = cols[cand]; break
    if time_col:
        out["time"] = pd.to_datetime(df[time_col], errors="coerce")
    else:
        out["time"] = pd.NaT
    return out

def do_batch_predict():
    if model is None or not model.is_trained:
        status.text = "❌ Model not loaded."
        return

    lat_val, err3 = _parse_float(lat_in.value.strip(), "Latitude", -90, 90)
    if err3:
        status.text = err3
        return
    month_val = int(month_sl.value)

    try:
        df = _read_upload(file_in)
        df = _standardize_cols(df)
    except Exception as e:
        status.text = f"❌ File error: {e}"
        return

    # normalize cloud if coming in percent
    if df["cloud"].max() > 1.001:
        df["cloud"] = df["cloud"] / 100.0

    # fill time if missing
    if df["time"].isna().all():
        # create synthetic monthly index for plotting only
        df["time"] = pd.date_range("2000-01-01", periods=len(df), freq="MS")

    # 🔹 NEW: Extract month numbers from time column if available
    if "time" in df and not df["time"].isna().all():
        df["month"] = df["time"].dt.month
    else:
        df["month"] = month_val  # fallback to slider if no valid time column

    # 🔹 Predict with per-row months (variable seasonal input)
    preds = model.predict(
        df["cloud"].values,
        df["aod"].values,
        np.full(len(df), lat_val, dtype=np.float32),
        df["month"].values.astype(np.float32)
    )

    df["ssr"] = preds.astype(float)
    df["lat"] = lat_val
    df.reset_index(drop=True, inplace=True)
    gc.collect()

    batch_src.data = dict(
        idx=df.index.values,
        time=df["time"].values.astype("datetime64[ms]"),
        cloud=df["cloud"].values,
        aod=df["aod"].values,
        lat=df["lat"].values,
        month=df["month"].values,
        ssr=df["ssr"].values
    )
    status.text = f"✅ Generated {len(df)} SSR predictions (lat={lat_val}) using months from file."


# Download CSV via CustomJS from ColumnDataSource
download_btn.js_on_click(CustomJS(args=dict(source=batch_src), code="""
    const data = source.data;
    const N = data['ssr'].length;
    if (N === 0) { return; }
    const cols = Object.keys(data);
    // order columns nicely
    const order = ['idx','time','cloud','aod','lat','month','ssr'];
    const cols_ordered = order.filter(c => cols.includes(c)).concat(cols.filter(c => !order.includes(c)));
    let csv = cols_ordered.join(',') + '\\n';
    for (let i = 0; i < N; i++) {
        let row = [];
        for (const c of cols_ordered) {
            let v = data[c][i];
            if (v instanceof Date) v = v.toISOString();
            row.push(v);
        }
        csv += row.join(',') + '\\n';
    }
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ssr_predictions.csv';
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
"""))

batch_predict_btn.on_click(do_batch_predict)

batch_panel = TabPanel(child=column(
    row(file_in,column(batch_predict_btn, download_btn),
    row(lat_in, month_sl)),
    ts,
    table,
    status
), title="Batch via file")

# ──────────────────────────────────────────────────────────────────────────────
# 6) Tabs + Mode sync
# ──────────────────────────────────────────────────────────────────────────────
tabs = Tabs(tabs=[single_panel, batch_panel], stylesheets=[tabs_style])

def sync_mode(attr, old, new):
    if new == "Single value":
        tabs.active = 0
    else:
        tabs.active = 1

mode_select.on_change("value", sync_mode)

# ──────────────────────────────────────────────────────────────────────────────
# 7) Initial status
# ──────────────────────────────────────────────────────────────────────────────
if model is None:
    status.text = f"❌ Could not load model: <code>{MODEL_PATH}</code>."
elif not model.is_trained:
    status.text = "⚠️ Model loaded but marked as not trained."
else:
    status.text = "✅ Model ready. Choose a mode to start."

# ──────────────────────────────────────────────────────────────────────────────
# 8) Layout
# ──────────────────────────────────────────────────────────────────────────────
curdoc().add_root(column(header, tabs,stylesheets=[gstyle]))
