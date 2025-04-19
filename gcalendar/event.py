from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import zoneinfo
from datetime import datetime, timedelta
from tabulate import tabulate

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
            
def table_calendar(service, start_date, end_date, calendar_email, highlight=False):
    events = get_events(service, start_date, end_date)
    list_event = []
    show_date = True
    for event in events:
        raw_date = format_date(start_date)
        date_col = Color.cyan(raw_date) if show_date and highlight else (raw_date if show_date else "")
        if event["start"].get("dateTime") == None:
            line = [
                date_col,
                "Day",
                event_status([attendee.get("responseStatus") for attendee in event.get("attendees", []) if attendee.get("email") == calendar_email]),
                Color.blue(event["summary"]),
                format_email(event["creator"].get("email")),
                len([attendee for attendee in event.get("attendees", []) if attendee.get("responseStatus") == "accepted"]),
                event["hangoutLink"] if "hangoutLink" in event else ""
            ]
            list_event.append(line)
            show_date = False
        else:
            line = [
                date_col,
                format_hour(event["start"].get("dateTime")) + "-" +format_hour(event["end"].get("dateTime")),
                event_status([attendee.get("responseStatus") for attendee in event.get("attendees", []) if attendee.get("email") == calendar_email]),
                event["summary"],
                format_email(event["creator"].get("email")),
                len([attendee for attendee in event.get("attendees", []) if attendee.get("responseStatus") == "accepted"]),
                event["hangoutLink"] if "hangoutLink" in event else ""
            ]
            list_event.append(line)
            show_date = False
    return list_event

def day_event(compact, path, period):
    service = gauth(path)
    calendar_email = get_calendar_email(service)
    #STRING_TIMEZONE
    calendar_timezone = get_calendar_timezone(service)
    #CLASS_TIMEZONE
    tz = zoneinfo.ZoneInfo(calendar_timezone)
    start_date = get_start_day(period, tz)
    str_start_date = start_date.isoformat()
    end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    str_end_date = end_date.isoformat()
    print("\n" f"Hello {Color.green(format_email(calendar_email))} You are connect to {Color.blue(calendar_email)}" + "\n")

    if compact:
        print(weather_status_icon(weather_status(period, str_start_date)), weather_temp(period, str_start_date), "-", Color.cyan(format_date(str_start_date), bold=True), "-",  format_hour(str(datetime.now())), "\n")
        compact_calendar(service, str_start_date, str_end_date, calendar_email)        
    else:
        headers = [Color.red("Date"), Color.red("Time"), Color.red("Status"), Color.red("Event"),Color.red("Creator"), Color.red("Attendees"), Color.red("Link")]
        print(weather_status_icon(weather_status(period, str_start_date)), weather_temp(period, str_start_date), "-", Color.cyan(format_date(str_start_date), bold=True), "-",  format_hour(str(datetime.now())), "\n")
        table = table_calendar(service, str_start_date, str_end_date, calendar_email)
        print(tabulate(table, headers, tablefmt="simple"))
        

def week_event(path, period):
    service = gauth(path)
    calendar_email = get_calendar_email(service)
    #STRING_TIMEZONE
    calendar_timezone = get_calendar_timezone(service)
    #CLASS_TIMEZONE
    tz = zoneinfo.ZoneInfo(calendar_timezone)
    date_now = datetime.now(tz)
    start_date = get_start_day(period, tz)
    print("\n" f"Hello {Color.green(format_email(calendar_email))} You are connect to {Color.blue(calendar_email)}", "\n")
    weekly_events = []
    for week_day in range(7):
        start_all_week_dates = start_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=week_day)
        str_start_all_week_dates = start_all_week_dates.isoformat()
        end_all_week_dates = start_date.replace(hour=23, minute=59, second=59, microsecond=999999) + timedelta(days=week_day)
        str_end_all_week_dates = end_all_week_dates.isoformat()
        is_today = date_now.date() == start_all_week_dates.date()

        headers = [Color.red("Date"), Color.red("Time"), Color.red("Status"), Color.red("Event"),Color.red("Creator"), Color.red("Attendees"), Color.red("Link")]
        day_events  = table_calendar(service, str_start_all_week_dates, str_end_all_week_dates, calendar_email, highlight=is_today)
        weekly_events.extend(day_events)
       
    print(tabulate(weekly_events, headers, tablefmt="simple"))