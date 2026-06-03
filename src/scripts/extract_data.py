import json
from datetime import datetime
from src.config.settings import Settings
from src.utils.get_api_data import GetApiData
from src.utils.save_json import SaveJson  # Nueva clase para guardar json

class ExtractData:
    year = None
    month = None
    def __init__(self):
        self.settings = Settings()
        self.client = GetApiData(self.settings.BASE_URL, delay=5)
        self.save_json = SaveJson()  # Instancia para guardar json

    def extract_meetings(self, date_start: datetime, date_end: datetime):
        params = {
            "date_start>": date_start.strftime("%Y-%m-%d"),
            "date_start<": date_end.strftime("%Y-%m-%d")
        }
        self.year = date_start.year
        self.month = date_start.month
        period = date_start.strftime("%Y-%m-%d")[0:7]
        meetings = self.client.get_meetings(params)
        self.save_json.save(meetings, "meetings", self.year, self.month, f"meetings_{period}.json")
        return meetings

    def extract_sessions(self, meeting_key, period):
        sessions = self.client.get_sessions(meeting_key)
        self.save_json.save(sessions, "sessions", self.year, self.month, f"sessions_by_meeting_{meeting_key}___{period}.json")
        return sessions

    def extract_drivers(self, meeting_key, session_key, period):
        drivers = self.client.get_drivers(meeting_key, session_key)
        self.save_json.save(drivers, "drivers", self.year, self.month, f"drivers_by_meeting_{meeting_key}__by_session_{session_key}___{period}.json")
        return drivers

    def extract_laps(self, meeting_key, session_key, driver_number, period):
        laps = self.client.get_laps(meeting_key, session_key, driver_number)
        self.save_json.save(laps, "laps", self.year, self.month, f"laps_by_meeting_{meeting_key}__by_session_{session_key}__by_driver_{driver_number}___{period}.json")
        return laps

    def extract_cars(self, session_key, driver_number, period):
        cars = self.client.get_cars(session_key, driver_number, 310)
        self.save_json.save(cars, "cars", self.year, self.month, f"cars_by_session_{session_key}__by_driver_{driver_number}___{period}.json")
        return cars