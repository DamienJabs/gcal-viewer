# gcal-viewer

[![Made with Typer](https://img.shields.io/badge/Made%20with-Typer-22aadd.svg?logo=fastapi)](https://github.com/tiangolo/typer) [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python)](https://www.python.org/)

**gcal-viewer** is a lightweight command-line tool to view your Google Calendar events directly from the terminal. Built with [Typer](https://typer.tiangolo.com/) and Python, this project is a small personal app created to learn Python through a practical use case.

## ✨ Features

- Display today's or tomorrow's events from your Google Calendar
- Optional weather forecast for events using OpenWeatherMap
- Compact display mode for concise terminal output

## ⚠ Limitations

- The `--week` option is not implemented yet
- The non-compact display mode is currently unavailable

## 🔧 Installation

Make sure you have Python 3.7 or higher installed.

```bash
git clone https://github.com/DamienJabs/gcal-viewer.git
cd gcal-viewer
pip install -r requirements.txt
```

## 🔑 Setup

### 1. Google Calendar API

- Create a project in the [Google Cloud Console](https://developers.google.com/workspace/calendar/api/quickstart/python#enable_the_api)

- Enable the Google Calendar API

- Download your OAuth2 credentials as credentials.json

- Place the credentials.json file in the root of the project directory (or whether you want but you will need to specify it with `--path` option within the `auth` command)

The first time you run the script, a token.json file will be generated after authentication.

### 2. OpenWeatherMap API (optional)

To display weather information, you need an API key from OpenWeatherMap:

Register at https://openweathermap.org/api

Set the API key as an environment variable:

```bash
export OPENWEATHER_API_KEY=your_api_key_here
```

## 🚀 Usage

Run the app with:

```bash
python main.py [COMMANDS]
```

### Commands:

| Commands   | Description                                                     |
|------------|-----------------------------------------------------------------|
| `auth`     | Logs to your google calendar.                                   |
| `test`     | Retrieve last 10 events.                                        |
| `day`      | List events in Google Calender for whether today or tomorrow.   |

### Options:

```bash
python main.py day [OPTIONS]
```

| Option       | Description                                                     |
|--------------|-----------------------------------------------------------------|
| `--compact`  | Use compact mode.                                               |
| `--path`     | Use this if you want to use another json token file.            |
| `--day`      | Which day to show. Only today and tomorrow can be specified.    |

### Help:

Each command are listed using the `--help` option

```bash
python main.py --help
```

## 🙏 Acknowledgments

This project is a small utility developed as part of my Python learning journey. Contributions, feedback, and suggestions are welcome!