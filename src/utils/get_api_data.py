import requests
import time
import logging

logging.basicConfig(level=logging.INFO)

class GetApiData:
    def __init__(self, base_url: str, delay: int = 0):
        self.base_url = base_url
        self.delay = delay

    def _get(self, endpoint: str, params: dict = None):
        logging.info(f"GET {endpoint} | params={params}")
        try:
            if self.delay > 0:
                time.sleep(self.delay)
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return {"error": str(e)}

    def get_meetings(self, params: dict):
        return self._get(f"{self.base_url}/meetings", params)

    def get_sessions(self, meeting_key: str):
        return self._get(f"{self.base_url}/sessions", {"meeting_key": meeting_key})

    def get_drivers(self, meeting_key: str, session_key: str):
        return self._get(f"{self.base_url}/drivers", {
            "meeting_key": meeting_key,
            "session_key": session_key
        })

    def get_laps(self, meeting_key: str, session_key: str, driver_number: str):
        return self._get(f"{self.base_url}/laps", {
            "meeting_key": meeting_key,
            "session_key": session_key,
            "driver_number": driver_number
        })

    def get_cars(self, session_key: str, driver_number: str, speed: int):
        return self._get(f"{self.base_url}/car_data", {
            # "meeting_key": meeting_key,
            "session_key": session_key,
            "driver_number": driver_number,
            "speed>": speed
        })