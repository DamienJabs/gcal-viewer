from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import zoneinfo
from datetime import datetime, timedelta 

from utils.color import Color
from utils.format import format_date, format_hour, format_email
from utils.status import event_status, weather_status_icon
from utils.weather import weather_temp, weather_status

def gday(compact, path, day, ):
    def my_calendar() -> str:
        # Return the connected email address 
        calendar = service.calendars().get(calendarId='primary').execute()
        return calendar['summary']

    def get_events(start_date, end_of_day):
        return service.events().list(
            calendarId='primary',
            timeMin=start_date,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy='startTime'
        ).execute().get("items", [])

    def compact_calendar(start_date, end_of_day):
        print("\n" f"Hello {Color.green(format_email(my_calendar()))} You are connect to {Color.blue(my_calendar())}" + "\n")

        #Print weather and date time
        print(weather_status_icon(weather_status(day)), weather_temp(day), "-", Color.cyan(format_date(start_date), bold=True), "-",  format_hour(str(datetime.now())))

        for event in get_events(start_date, end_of_day):
            #Whole day event are not in the same key as time slot event
            #Print an emoji based on whether you accepted or not the event
            if event["start"].get("dateTime") == None:
                print("\t",
                    #Self created event are accepted by default, so only search for attendees with your email address  
                    event_status([attendee.get("responseStatus") for attendee in event.get("attendees", []) if attendee.get("email") == my_calendar()]),
                    Color.blue(event["summary"]))
            else:
                print("\t",
                    event_status([attendee.get("responseStatus") for attendee in event.get("attendees", []) if attendee.get("email") == my_calendar()]),
                    format_hour(event["start"].get("dateTime")), 
                    "-", 
                    format_hour(event["end"].get("dateTime")),
                    event["summary"],
                    "by",
                    Color.green(format_email(event["creator"].get("email")), bold=True))

    def table_calendar(start_date,end_of_day):
        pass

    def get_day_range(calendar_timezone):
        tz = zoneinfo.ZoneInfo(calendar_timezone)
        now_date = datetime.now(tz)

        if day.lower() == "today":
            start = now_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif day.lower() in ["tomorrow", "demain"]:
            start = now_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        else:
            raise ValueError(f"Only today and tomorrow can be specified. \nSpecified : {day}")
        return start.isoformat(), start.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()

  
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    # Call the Calendar API
    creds = Credentials.from_authorized_user_file(path, SCOPES)
    service = build("calendar", "v3", credentials=creds)

    # Get the calendar timezone set in the Google Calendar API
    calendar_timezone = service.calendars().get(calendarId='primary').execute()['timeZone']

    start_date, end_date = get_day_range(calendar_timezone)
    if compact:
        compact_calendar(start_date, end_date)
    else:
        table_calendar(start_date, end_date)