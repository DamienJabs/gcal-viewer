def event_status(status):
    # Return an emoji based on the string retrieve from the Google Calendar Api
    if "accepted" in status or not status:
        return "✅"
    if "needsAction" in status:
        return "⏳"
    if "tentative" in status:
        return "🤷"
    if "declined" in status:
        return "❌"
    
def weather_status_icon(icon_code):
    # Return an emoji based on the key retrieve from the open weather api
    icons = {
        "01d": "☀️",
        "01n": "🌙",

        "02d": "🌤️",
        "02n": "☁️",

        "03d": "☁️",
        "03n": "☁️",

        "04d": "☁️☁️",
        "04n": "☁️☁️",

        "09d": "🌧️",
        "09n": "🌧️",

        "10d": "🌦️",
        "10n": "🌧️",

        "11d": "🌩️",
        "11n": "🌩️",

        "13d": "❄️",
        "13n": "❄️",

        "50d": "🌫️",
        "50n": "🌫️",
    }
    return icons.get(icon_code, "📅")