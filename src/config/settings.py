import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Settings:
    BASE_URL = "https://api.openf1.org/v1"
    BASE_DIR = os.getcwd()
    SESSIONS_ENDPOINT = "/sessions"  ##PARAMS: date_start>{}&date_end<{}
    MEETINGS_ENDPOINT = "/meetings" ##/meetings?date_start>2025-02-01T00:00:00+00:00&date_start<2025-02-28T00:00:00+00:00&year=2025
    DRIVERS_ENDPOINT = "/drivers?session_key={}"
    CARS_ENDPOINT = "/car_data?driver_number={}&session_key={}&speed>=290"
    LAPS_ENDPOINT = "/laps?session_key={}&driver_number={}"
    BASE_DIR = os.getcwd()