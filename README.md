# 🌊 Digana Flood Monitor & Sentinel Alert System

A hyper-local, automated flood warning system designed specifically for **Digana, Sri Lanka**.

I built this tool during the **2025 Sri Lanka Floods** to monitor my hometown in real-time. With my parents living in Digana and the situation changing rapidly, I needed a way to get instant, reliable alerts about flood risks and the **Victoria Dam** status without relying on delayed news reports.

---

## 🚀 How It Works

This system uses a **"Sentinel City"** strategy to predict flood risks before they hit Digana:

1.  **📍 Digana (Home):** Monitors for **immediate heavy rainfall** (>40mm) directly at my parents' location.
2.  **🌪️ Mahiyanganaya (Upwind):** Monitors for storms approaching from the **East**. Rain here indicates a storm front arriving in Digana within 1-2 hours.
3.  **🌊 Nuwara Eliya (Upstream):** Monitors the catchment area. Heavy rain here (>50mm) signals a high risk of the **Victoria Dam** opening its spill gates.
4.  **📢 News Monitor:** Scrapes Google News RSS for real-time reports of "Victoria Dam" or "Polgolla" spill gate openings (checked every 30 mins).

---

## 🛠️ Tech Stack

* **Language:** Python 3.9
* **Automation:** GitHub Actions (Cron Schedule: `*/30 * * * *`)
* **Data Sources:**
    * [OpenWeatherMap API](https://openweathermap.org/api/one-call-3) (One Call 3.0) for rainfall data.
    * [Google News RSS](https://news.google.com/) for breaking news on dam spills.
* **Notifications:** Telegram Bot API.

---

## ⚙️ Setup Guide

### 1. Prerequisites
You need the following API keys:
* **OpenWeatherMap API Key:** Subscribe to the "One Call 3.0" plan (Free tier).
* **Telegram Bot Token:** Create a bot via [@BotFather](https://t.me/BotFather).
* **Telegram Chat ID:** The ID of the user/group receiving alerts (get it via [@userinfobot](https://t.me/userinfobot)).

### 2. Installation
1.  **Fork or Clone** this repository.
2.  **Add Secrets:** Go to `Settings` -> `Secrets and variables` -> `Actions` and add:
    * `OWM_API_KEY`
    * `TELEGRAM_TOKEN`
    * `TELEGRAM_CHAT_ID`

3.  **Enable Workflow:** Go to the `Actions` tab and enable the "Sentinel Weather Monitor" workflow.

---

## 📂 File Structure

* `monitor.py`: The core logic script. Fetches weather/news and sends Telegram messages.
* `.github/workflows/weather_check.yml`: The automation config. Tells GitHub to run `monitor.py` every 30 minutes.
* `requirements.txt`: List of Python libraries needed (`requests`, `feedparser`).

---

## ⚠️ Alert Logic

| Location | Role | Alert Threshold | Message Type |
| :--- | :--- | :--- | :--- |
| **Digana** | Direct Impact | > 40.0mm Rain | 🚨 **IMMEDIATE THREAT** |
| **Mahiyanganaya** | Early Warning | > 30.0mm Rain | 🌪️ **STORM FRONT INCOMING** |
| **Nuwara Eliya** | Dam Risk | > 50.0mm Rain | 🌊 **DAM FILL RISK** |
| **News Feed** | Dam Status | Keywords | 📢 **FRESH NEWS ALERT** |

*Note: News alerts are filtered to only notify if the article was published within the last 45 minutes to prevent spam.*

---

**Author:** Ahmed Rashad
**License:** MIT