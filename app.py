from flask import Flask, render_template
import requests
import datetime

app = Flask(__name__)

API_KEY = '00551aca1abcaebf6682ec1bc46adac8'

def get_location():
    try:
        ip_data = requests.get('https://ipinfo.io').json()
        city = ip_data.get("city", "Unknown")
        return city
    except:
        return "Unknown"

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        print(f"📡 Requesting weather for: {city}")
        print(f"🌐 URL: {url}")

        response = requests.get(url)
        data = response.json()
        print(f"🔍 Response JSON: {data}")  # Debug output

        weather = {
            "description": data['weather'][0]['description'].title(),
            "icon": data['weather'][0]['icon'],
            "temperature": data['main']['temp']
        }

        return weather

    except Exception as e:
        print(f"❌ Weather Fetch Error: {e}")
        return {"description": "N/A", "icon": "01d", "temperature": "N/A"}

@app.route("/")
def home():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    day_str = now.strftime("%A")

    city = get_location()
    weather = get_weather(city)

    return render_template(
        "index.html",
        date=date_str,
        time=time_str,
        day=day_str,
        city=city,
        weather=weather
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)