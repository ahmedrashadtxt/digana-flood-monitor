import requests
import feedparser
import os
from datetime import datetime, timedelta, timezone

# --- CONFIGURATION ---
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
OWM_KEY = os.environ["OWM_API_KEY"]

# --- SENTINEL CITIES SETUP ---
# We monitor 3 zones to predict the threat before it hits Digana fully.
LOCATIONS = [
    {
        "name": "Digana (Home)",
        "lat": "7.2942",
        "lon": "80.7381",
        "role": "DIRECT_IMPACT",
        "threshold_mm": 40.0, 
        "msg": "🚨 **IMMEDIATE THREAT (Digana):**\nHeavy rain detected at your location."
    },
    {
        "name": "Mahiyanganaya (East/Upwind)",
        "lat": "7.3300",
        "lon": "81.0500",
        "role": "EARLY_WARNING",
        "threshold_mm": 30.0, 
        "msg": "🌪️ **STORM FRONT WARNING:**\nHeavy rain in Mahiyanganaya. Storm likely moving West towards Digana (1-2 hours away)."
    },
    {
        "name": "Nuwara Eliya (Upstream Catchment)",
        "lat": "6.9708",
        "lon": "80.7829",
        "role": "DAM_RISK",
        "threshold_mm": 50.0, 
        "msg": "🌊 **DAM FILL RISK:**\nMassive rainfall in Nuwara Eliya catchment area. High risk of Victoria Dam spill gates opening."
    }
]

DAM_KEYWORDS = ["Victoria Dam", "Victoria Reservoir", "Polgolla", "Spill Gates", "Mahaweli"]

def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
        print(f"Sent Alert: {message[:30]}...")
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_weather():
    print(f"[{datetime.now()}] Starting Sentinel Scan...")
    
    for loc in LOCATIONS:
        # One Call API 3.0
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={loc['lat']}&lon={loc['lon']}&exclude=minutely,hourly&appid={OWM_KEY}&units=metric"
        
        try:
            data = requests.get(url).json()
            
            # 1. Check for Govt "Red Alerts" (Official Warnings)
            if "alerts" in data:
                for alert in data['alerts']:
                    # Filter for severe alerts only to reduce noise
                    if "Red" in alert.get('description', '') or "Severe" in alert.get('event', ''):
                        send_alert(f"⚠️ **OFFICIAL ALERT ({loc['name']}):**\n{alert['event']}")

            # 2. Check Rainfall Volume
            if "daily" in data:
                rain_today = data['daily'][0].get('rain', 0)
                
                # Logic: If rain > threshold, send specific warning
                if rain_today > loc['threshold_mm']:
                    alert_text = f"{loc['msg']}\n"
                    alert_text += f"📉 **Measured:** {rain_today}mm forecast today."
                    send_alert(alert_text)
                    
        except Exception as e:
            print(f"Error checking {loc['name']}: {e}")

def check_dam_news():
    """Checks Google News for updates released in the LAST 45 MINUTES."""
    rss_url = "https://news.google.com/rss/search?q=Victoria+Dam+Sri+Lanka+spill+gates+OR+Mahaweli+alert&hl=en-LK&gl=LK&ceid=LK:en"
    
    try:
        feed = feedparser.parse(rss_url)
        current_time = datetime.now(timezone.utc)
        
        # Look at the top 5 news items
        for entry in feed.entries[:5]:
            # 1. Get the published time (It is already in UTC)
            if hasattr(entry, 'published_parsed'):
                pub_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                
                # 2. Calculate how old the news is
                time_difference = current_time - pub_time
                
                # 3. ONLY alert if news is less than 45 minutes old
                # (We use 45 mins to be safe since script runs every 30 mins)
                if time_difference < timedelta(minutes=45):
                    if any(k.lower() in entry.title.lower() for k in DAM_KEYWORDS):
                        send_alert(f"📢 **FRESH DAM ALERT:**\n[{entry.title}]({entry.link})")
                        
    except Exception as e:
        print(f"RSS Error: {e}")

if __name__ == "__main__":
    check_weather()
    check_dam_news()
