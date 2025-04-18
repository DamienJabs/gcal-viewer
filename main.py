import typer

from pathlib import Path
from auth.auth import gauth
from auth.test import gtest
#from gcalendar.day import gday
#from gcalendar.week import gweek
from gcalendar.event import day_event, week_event


app = typer.Typer()

@app.command("auth")
def auth(path: str = typer.Option("credentials.json", help="JSON file containing your Google Calendar API credentials.")):
  """
  Auth to the Google Calendar API.
  """
  gauth(path)


@app.command("test")
def test(path: str = typer.Option("~/.config/gcal-viewer/token.json", help="Use this if you want to use another json token file.")):
  """
  Use this to test if the auth is working.
  """
  token_path = Path(path).expanduser().resolve()
  gtest(token_path)

@app.command("day")
def day( compact: bool = typer.Option(False, "--compact", help="Use compact mode."),
        path: str = typer.Option("~/.config/gcal-viewer/token.json", help="Use this if you want to use another json token file."),
        period: str = typer.Option("today", help="Which day to show. Only today and tomorrow can be specified")):
  """
  List events in Google Calender for whether today or tomorrow
  """
  token_path = Path(path).expanduser().resolve()
  day_event(compact, token_path, period)

@app.command("week")
def week( compact: bool = typer.Option(False, "--compact", help="Use compact mode."),
        path: str = typer.Option("~/.config/gcal-viewer/token.json", help="Use this if you want to use another json token file."),
        period: str = typer.Option("actual", help="Which week to show. Only actual and next can be specified")):
  """
  List events in Google Calender for whether today or tomorrow
  """
  token_path = Path(path).expanduser().resolve()
  week_event(compact, token_path, period)

if __name__ == '__main__':
  app()