import streamlit as st      
import requests             
import pandas as pd        
import plotly.express as px 
from datetime import datetime 

API_KEY = "api_key"  

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather_emoji(condition_id):
    """Return an emoji based on the weather condition code."""
    if condition_id < 300:
        return "Thunderstorm"   
    elif condition_id < 400:
        return "Drizzle"   
    elif condition_id < 600:
        return "Rain"  
    elif condition_id < 700:
        return "Snow"   
    elif condition_id < 800:
        return "Fog/Mist/Haze"   
    elif condition_id == 800:
        return "Clear Sky"   
    elif condition_id <= 804:
        return "Cloudy"   
    else:
        return "Fallback" 

#FETCH CURRENT WEATHER
def fetch_current_weather(city_name):
    """Call OpenWeather current weather endpoint for a city."""
    params = {
        "q": city_name,          # City name typed by user
        "appid": API_KEY,    
        "units": "metric",       # "metric" = Celsius, "imperial" = Fahrenheit
    }
    try:
        response = requests.get(CURRENT_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json() 
        elif response.status_code == 404:
            return None             
        else:
            st.error(f"API error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ No internet connection. Please check your network.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏳ Request timed out. Try again.")
        return None

#FETCH 5-DAY FORECAST
def fetch_forecast(city_name):
    """Call OpenWeather 5-day/3-hour forecast endpoint."""
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
    }
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


#PAGE CONFIGURATION & STYLING
st.set_page_config(
    page_title="Weatherly",
    page_icon="🌧️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

#CSS
st.markdown("""
<style>
/* ── Google Font — soft and feminine ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300&display=swap');

/* ────────────────────────────────────────────
   PALETTE
   Background : soft dusty blue gradient
   Cards      : white at 18% opacity — frosted glass
   Text main  : #f0f6ff  (icy white)
   Text muted : rgba(220,233,248,0.75) (pale blue-white)
   Accent     : #dce9f8  (pale ice blue)
   Border     : rgba(220,233,248,0.30)
   ──────────────────────────────────────────── */

/* ── Full page ── */
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: linear-gradient(160deg, #8aaee0 0%, #6595ce 35%, #4a78b8 65%, #3a5fa8 100%) !important;
    background-attachment: fixed !important;
    color: #f0f6ff !important;
    min-height: 100vh;
}

/* ── Streamlit containers transparent so gradient shows through ── */
.stApp, section[tabindex="0"], .block-container {
    background: transparent !important;
}

/* ── Hide Streamlit default header/footer ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── GLASS CARD ── */
.weather-card {
    background: rgba(255, 255, 255, 0.18) !important;
    backdrop-filter: blur(28px) !important;
    -webkit-backdrop-filter: blur(28px) !important;
    border-radius: 24px !important;
    padding: 28px 32px !important;
    margin: 16px 0 !important;
    border: 1px solid rgba(220, 233, 248, 0.35) !important;
    box-shadow: 0 8px 32px rgba(40, 70, 140, 0.18) !important;
}

/* ── Big temperature number ── */
.temp-display {
    font-size: 80px;
    font-weight: 300;
    color: #ffffff;
    line-height: 1;
    letter-spacing: -3px;
}

/* ── City name ── */
.city-name {
    font-size: 26px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}

/* ── Weather description ── */
.condition-text {
    font-size: 15px;
    color: rgba(220, 233, 248, 0.80);
    text-transform: capitalize;
    margin-bottom: 20px;
    font-weight: 400;
    font-style: italic;
}

/* ── Stat pills ── */
.stat-pill {
    background: rgba(255, 255, 255, 0.16) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    text-align: center !important;
    margin: 4px !important;
    display: inline-block !important;
    min-width: 100px !important;
    border: 1px solid rgba(220, 233, 248, 0.28) !important;
}
.stat-label {
    font-size: 10px;
    color: rgba(220, 233, 248, 0.70);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}
.stat-value {
    font-size: 17px;
    font-weight: 600;
    color: #ffffff;
    margin-top: 3px;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid rgba(220, 233, 248, 0.25);
    margin: 20px 0;
}

/* ── Error card ── */
.error-card {
    background: rgba(255, 220, 220, 0.18);
    border: 1px solid rgba(255, 200, 200, 0.35);
    border-radius: 20px;
    padding: 24px;
    color: #fff0f0;
    text-align: center;
    backdrop-filter: blur(14px);
}

/* ── App title ── */
@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@200;300&display=swap');

.app-title {
    font-family: 'Josefin Sans', sans-serif !important;
    font-size: 26px;
    font-weight: 200;
    color: #ffffff;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 10px;
    margin-bottom: 4px;
}
.app-subtitle {
    font-size: 15px;
    color: rgba(220, 233, 248, 0.75);
    text-align: center;
    margin-bottom: 32px;
    font-weight: 400;
    font-style: italic;
}

/* ── Search input ── */
input[type="text"], .stTextInput input {
    background: rgba(255, 255, 255, 0.18) !important;
    border: 1px solid rgba(220, 233, 248, 0.40) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
}
input[type="text"]::placeholder {
    color: rgba(220, 233, 248, 0.55) !important;
}

/* ── Go button ── */
.stButton > button {
    background: rgba(255, 255, 255, 0.22) !important;
    color: #ffffff !important;
    border: 1px solid rgba(220, 233, 248, 0.45) !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    backdrop-filter: blur(10px) !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: rgba(255, 255, 255, 0.32) !important;
}

/* ── Section headings ── */
h3 {
    color: #ffffff !important;
    font-weight: 600 !important;
    letter-spacing: -0.3px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    color: rgba(220, 233, 248, 0.85) !important;
}
</style>
""", unsafe_allow_html=True)

#APP HEADER
st.markdown('<div class="app-title">Weatherly</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle"> </div>', unsafe_allow_html=True)

#SEARCH BAR
col_input, col_btn = st.columns([5, 1])

with col_input:
    # Text input, user types city name here
    city = st.text_input(
        label="",
        placeholder="🔍  Search a city... e.g. Delhi, Tokyo, Paris",
        label_visibility="collapsed"
    )

with col_btn:
    #search button
    search = st.button("Go →", use_container_width=True)

#MAIN LOGIC-runs when user clicks Go or presses enter
if city and (search or city):   # Triggers on button click OR pressing Enter
    
    # Show a loading spinner while fetching data
    with st.spinner("Fetching weather data..."):
        weather_data = fetch_current_weather(city)
        forecast_data = fetch_forecast(city)

    # ── ERROR ──
    if weather_data is None:
        st.markdown("""
        <div class="error-card">
            <div style="font-size:40px">🔍</div>
            <div style="font-size:18px; font-weight:700; margin:8px 0">City not found</div>
            <div style="font-size:14px">Please check the spelling and try again.<br>
            Try: "London", "New York", "Mumbai"</div>
        </div>
        """, unsafe_allow_html=True)

    # ── SUCCESS──
    else:
        city_name    = weather_data["name"]
        country      = weather_data["sys"]["country"]
        temp         = round(weather_data["main"]["temp"])          # °C
        feels_like   = round(weather_data["main"]["feels_like"])    # °C
        humidity     = weather_data["main"]["humidity"]             # %
        wind_speed   = round(weather_data["wind"]["speed"] * 3.6, 1)  # m/s → km/h
        condition    = weather_data["weather"][0]["description"]   # e.g. "clear sky"
        cond_id      = weather_data["weather"][0]["id"]            # Numeric code
        emoji        = get_weather_emoji(cond_id)
        visibility   = weather_data.get("visibility", 0) // 1000  # m → km
        pressure     = weather_data["main"]["pressure"]            # hPa

        # Sunrise/sunset — convert Unix timestamp → readable time
        sunrise_ts = weather_data["sys"]["sunrise"]
        sunset_ts  = weather_data["sys"]["sunset"]
        sunrise    = datetime.fromtimestamp(sunrise_ts).strftime("%H:%M")
        sunset     = datetime.fromtimestamp(sunset_ts).strftime("%H:%M")

        # ── CURRENT WEATHER CARD ──
        st.markdown(f"""
        <div class="weather-card">
            <div class="city-name">{emoji} {city_name}, {country}</div>
            <div class="condition-text">{condition}</div>
            <div class="temp-display">{temp}°C</div>
            <div style="color:rgba(220,233,248,0.80); font-size:14px; margin-top:8px">
                Feels like {feels_like}°C
            </div>
            <hr class="divider">
            <div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center;">
                <div class="stat-pill">
                    <div class="stat-label">💧 Humidity</div>
                    <div class="stat-value">{humidity}%</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-label">💨 Wind</div>
                    <div class="stat-value">{wind_speed} km/h</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-label">👁 Visibility</div>
                    <div class="stat-value">{visibility} km</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-label">🌡 Pressure</div>
                    <div class="stat-value">{pressure} hPa</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-label">🌅 Sunrise</div>
                    <div class="stat-value">{sunrise}</div>
                </div>
                <div class="stat-pill">
                    <div class="stat-label">🌇 Sunset</div>
                    <div class="stat-value">{sunset}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        
        # 📅 5-DAY FORECAST SECTION
        
        if forecast_data:
            st.markdown("### 5-Day Forecast")

            # The API returns 40 entries (every 3 hrs for 5 days)
            # We filter entries at noon (12:00:00) to get 1 reading per day
            forecast_list = forecast_data["list"]

            # Build a list of daily summaries
            daily_rows = []
            seen_dates = set()   # Track which dates added

            for entry in forecast_list:
                # entry["dt_txt"] looks like: "2024-03-21 12:00:00"
                dt_str = entry["dt_txt"]
                date   = dt_str.split(" ")[0]       # e.g. "2024-03-21"
                time   = dt_str.split(" ")[1]       # e.g. "12:00:00"

                # Only keep the noon entry for each date (avoids duplicates)
                if time == "12:00:00" and date not in seen_dates:
                    seen_dates.add(date)

                    day_temp  = round(entry["main"]["temp"])
                    day_cond  = entry["weather"][0]["description"].capitalize()
                    day_emoji = get_weather_emoji(entry["weather"][0]["id"])
                    day_hum   = entry["main"]["humidity"]

                    # Format date nicely: "2024-03-21" → "Thu, Mar 21"
                    day_label = datetime.strptime(date, "%Y-%m-%d").strftime("%a, %b %d")

                    daily_rows.append({
                        "Date":      day_label,
                        "Condition": f"{day_emoji} {day_cond}",
                        "Temp (°C)": day_temp,
                        "Humidity":  f"{day_hum}%",
                    })

            # ── FORECAST CARDS (one per day) ──
            cols = st.columns(len(daily_rows))   # Creates N side-by-side columns
            for i, (col, row) in enumerate(zip(cols, daily_rows)):
                with col:
                    st.markdown(f"""
                    <div class="weather-card" style="text-align:center; padding:16px;">
                        <div style="font-size:12px; color:rgba(220,233,248,0.75);">{row['Date']}</div>
                        <div style="font-size:28px; margin:8px 0;">
                            {row['Condition'].split()[0]}
                        </div>
                        <div style="font-size:20px; font-weight:600; color:#ffffff;">
                            {row['Temp (°C)']}°C
                        </div>
                        <div style="font-size:12px; color:rgba(220,233,248,0.75); margin-top:4px;">
                            {row['Humidity']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # ── TEMPERATURE TREND CHART ──
            st.markdown("### Temperature Trend")

            #DataFrame from the full 40-entry list for a smooth chart
            chart_data = []
            for entry in forecast_list:
                chart_data.append({
                    "Time": entry["dt_txt"],
                    "Temperature (°C)": round(entry["main"]["temp"]),
                })

            df = pd.DataFrame(chart_data)  # Convert list of dicts to DataFrame

            #line chart using Plotly Express
            fig = px.line(
                df,
                x="Time",
                y="Temperature (°C)",
                markers=True,                              #Show dots on each point
                color_discrete_sequence=["#dce9f8"],       #Pale ice blue line
                title=f"Temperature over next 5 days — {city_name}",
            )

            #chart style
            fig.update_layout(
                plot_bgcolor  = "rgba(255, 255, 255, 0.07)",
                paper_bgcolor = "rgba(0, 0, 0, 0)",
                font          = dict(family="DM Sans", color="#f0f6ff"),
                title_font    = dict(size=15, color="#ffffff"),
                xaxis         = dict(showgrid=False, tickangle=-45,
                                     color="rgba(220,233,248,0.70)"),
                yaxis         = dict(showgrid=True,
                                     gridcolor="rgba(220,233,248,0.15)",
                                     color="rgba(220,233,248,0.70)"),
                margin        = dict(l=20, r=20, t=50, b=40),
            )
            fig.update_traces(
                line=dict(width=2.5, color="#dce9f8"),
                marker=dict(size=6, color="#ffffff"),
                fill="tozeroy",
                fillcolor="rgba(220, 233, 248, 0.12)"
            )

            st.plotly_chart(fig, use_container_width=True)  

# 🦶 FOOTER
st.markdown("""
<div style="text-align:center; color:rgba(220,233,248,0.55); font-size:13px; margin-top:48px; padding-bottom:24px;">
    Weatherly · Powered by
    <a href="https://openweathermap.org" style="color:rgba(220,233,248,0.85);">OpenWeatherMap</a>
</div>
""", unsafe_allow_html=True)
