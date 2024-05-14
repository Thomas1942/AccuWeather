import requests

from models import LocationModel

class LocationClient(requests.Session):

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token
        self.base_url = f"http://dataservice.accuweather.com/locations/v1/cities/search?q="
        self.auth_url = f"&apikey={self.token}"
    
    def get_location(
            self, 
            loc: str, 
            *args, 
            **kwargs
        ) -> LocationModel:

        url = self.base_url + loc + self.auth_url

        return LocationModel(response=super().request(method='GET', url=url).json())