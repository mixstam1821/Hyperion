# ───────────── Base ─────────────
FROM python:3.11-slim

# Prevent Python buffering
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies efficiently
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose Bokeh default port
EXPOSE 7860

# Start Bokeh server with long session timeout
CMD ["bokeh", "serve", "--show", \
     "Hyperion_GUI.py", \
     "--port=7860"]
