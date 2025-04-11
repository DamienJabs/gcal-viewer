from datetime import datetime 

def format_date(start_date):
    #Return a formated date used to display an easier to read date
    dt = datetime.fromisoformat(start_date)
    return dt.strftime("%a %d %B")
  
def format_hour(date_str: str) -> str:
    #Return a formated date time used to display an easier to read date time
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%H:%M")
  
def format_email(email):
    #Retrieve used email and transform it
    username = email.split('@')[0]
    parts = username.split('.')
    if len(parts) >= 2:
        first = parts[0].capitalize()
        last_initial = parts[1][0].upper()
        return f"{first} {last_initial}."
    else:
        return username.capitalize()