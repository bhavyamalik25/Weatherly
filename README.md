# Weatherly

A minimal real-time weather dashboard built with Python and Streamlit.

Live demo → https://weatherly-g7s4seginssabckd64sjkq.streamlit.app/

---

## Features

- Search any city worldwide
- Current temperature, feels-like, humidity, wind, pressure, visibility
- Sunrise & sunset times
- 5-day forecast cards
- Temperature trend chart
- Cornflower blue glassmorphism UI

## Tech Stack

- Python
- Streamlit
- OpenWeather API
- Pandas + Plotly

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add your [OpenWeather API key](https://openweathermap.org/api) to `app.py`:

```python
API_KEY = "your_key_here"
```

## Deployment

Deployed on Streamlit Community Cloud. API key stored securely via Streamlit Secrets.
