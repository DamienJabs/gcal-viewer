from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import zoneinfo
from datetime import datetime, timedelta 

from utils.color import Color
from utils.format import format_date, format_hour, format_email
from utils.status import event_status, weather_status_icon
from utils.weather import weather_temp, weather_status

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def gauth(path):
    # Call the Calendar API
    creds = Credentials.from_authorized_user_file(path, SCOPES)
    return build("calendar", "v3", credentials=creds)

def get_calendar_email(service):
    calendar = service.calendars().get(calendarId='primary').execute()
    return calendar["summary"]

def get_calendar_timezone(service):
    return service.calendars().get(calendarId='primary').execute()['timeZone']

def get_start_day(period, tz):
    now_date = datetime.now(tz)
    if period.lower() == "today":
        start = now_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period.lower() in ["tomorrow", "demain"]:
        start = now_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    elif period.lower() == "actual":
        start = now_date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days = now_date.replace(hour=0, minute=0, second=0, microsecond=0).weekday())
    elif period.lower() == "next":
        start = now_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=7) - timedelta(days = now_date.replace(hour=0, minute=0, second=0, microsecond=0).weekday())
    else:
        raise ValueError(f"Only today and tomorrow can be specified. \nSpecified : {period}")
    return start

def get_events(service, start_date, end_of_day):
    return service.events().list(
        calendarId='primary',
        timeMin=start_date,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy='startTime'
    ).execute().get("items", [])

def compact_calendar(service, start_date, end_date, calendar_email):
    events = get_events(service, start_date, end_date)
    for event in events:
        if event["start"].get("dateTime") == None:
            print("\t",
                #Self created event are accepted by default, so only search for attendees with your email address  
                event_status([attendee.get("responseStatus") for attendee in event.get("attendees", []) if attendee.get("email") == calendar_email]),
                Color.blue(event["summary"]))
        else:
            print("\t",
                event_status([attendee.get("responseStatus") for attendee in event.get("attendees", []) if attendee.get("email") == calendar_email]),
                format_hour(event["start"].get("dateTime")), 
                "-", 
                format_hour(event["end"].get("dateTime")),
                event["summary"],
                "by",
                Color.green(format_email(event["creator"].get("email")), bold=True))

def day_event(compact, path, period):
    service = gauth(path)
    calendar_email = get_calendar_email(service)
    #STRING_TIMEZONE
    calendar_timezone = get_calendar_timezone(service)
    #CLASS_TIMEZONE
    tz = zoneinfo.ZoneInfo(calendar_timezone)
    start_date = get_start_day(period, tz)
    str_start_date = start_date.isoformat()

    if compact:
        print("\n" f"Hello {Color.green(format_email(calendar_email))} You are connect to {Color.blue(calendar_email)}" + "\n")
        print(weather_status_icon(weather_status(period, str_start_date)), weather_temp(period, str_start_date), "-", Color.cyan(format_date(str_start_date), bold=True), "-",  format_hour(str(datetime.now())))
        end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        str_end_date = end_date.isoformat()
        compact_calendar(service, str_start_date, str_end_date, calendar_email)
        
    else:
        ...

def week_event(compact, path, period):
    service = gauth(path)
    calendar_email = get_calendar_email(service)
    #STRING_TIMEZONE
    calendar_timezone = get_calendar_timezone(service)
    #CLASS_TIMEZONE
    tz = zoneinfo.ZoneInfo(calendar_timezone)
    date_now = datetime.now(tz)
    start_date = get_start_day(period, tz)
    if compact:
        print("\n" f"Hello {Color.green(format_email(calendar_email))} You are connect to {Color.blue(calendar_email)}" + "\n")
        for week_day in range(7):
            start_all_week_dates = start_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=week_day)
            str_start_all_week_dates = start_all_week_dates.isoformat()
            end_all_week_dates = start_date.replace(hour=23, minute=59, second=59, microsecond=999999) + timedelta(days=week_day)
            str_end_all_week_dates = end_all_week_dates.isoformat()
            color_day = Color.blue(format_date(str_start_all_week_dates))

            if date_now.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d") == start_all_week_dates.strftime("%Y-%m-%d"): 
                color_day = Color.cyan(format_date(str_start_all_week_dates))

            print('\n', weather_status_icon(weather_status(period, str_start_all_week_dates)), weather_temp(period, str_start_all_week_dates), "-", color_day)
            compact_calendar(service, str_start_all_week_dates, str_end_all_week_dates, calendar_email)
            
    else:
        ...