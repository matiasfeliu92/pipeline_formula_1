import requests
from src.config.settings import Settings

##https://openf1.org/docs

class GetApiData:
    def __init__(self):
        self.settings = Settings()
        self.url = self.settings.BASE_URL

    def execute(self, endpoint: str, params: dict):
        full_url = f"{self.url}{endpoint}"
        print(f"Sending GET request to {full_url}")
        try:
            response = requests.get(full_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}