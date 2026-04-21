import pandas as pd
import json
from datetime import datetime
from src.config.settings import Settings
from src.utils.get_api_data import GetApiData

class ExtractData:
    def __init__(self):
        self.settings = Settings()
        self.client = GetApiData(self.settings.BASE_URL, delay=5)
        self.data = pd.DataFrame()
        self.json_data = None

    def extract_meetings(self, date_start: datetime, date_end: datetime):
        params = {
            "date_start>": date_start.strftime("%Y-%m-%d"),
            "date_start<": date_end.strftime("%Y-%m-%d")
        }
        meetings = self.client.get_meetings(params)
        self.data = pd.DataFrame(meetings if isinstance(meetings, list) else [meetings])
        return self.data

    def extract_sessions(self):
        self.data["sessions"] = self.data["meeting_key"].apply(self.client.get_sessions)
        self.data = self.data.explode("sessions").reset_index(drop=True)
        return self.data

    def extract_drivers(self):
        self.data["drivers"] = self.data.apply(
            lambda row: self.client.get_drivers(row["meeting_key"], row["sessions"]["session_key"]),
            axis=1
        )
        self.data = self.data.explode("drivers").reset_index(drop=True)
        return self.data

    def extract_laps(self):
        laps = self.data.copy()
        laps["laps"] = laps.apply(
            lambda row: self.client.get_laps(row["meeting_key"], row["sessions"]["session_key"], row["drivers"]["driver_number"]),
            axis=1
        )
        laps = laps.explode("laps").reset_index(drop=True)
        laps["laps"] = laps["laps"].apply(lambda x: json.dumps(x) if isinstance(x, dict) else None)
        return laps

    def extract_cars(self):
        cars = self.data.copy()
        cars["cars"] = cars.apply(
            lambda row: self.client.get_cars(row["sessions"]["session_key"], row["drivers"]["driver_number"], 310),
            axis=1
        )
        cars = cars.explode("cars").reset_index(drop=True)
        cars["cars"] = cars["cars"].apply(lambda x: json.dumps(x) if isinstance(x, dict) else None)
        return cars