from src.utils.get_api_data import GetApiData

class ExtractData:
    params = None
    def __init__(self, spark):
        self.get_api_data = GetApiData()