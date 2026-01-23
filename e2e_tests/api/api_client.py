import httpx


class ApiClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def get(self, endpoint, params=None):
        url = f"{self.api_url}{endpoint}"
        response = httpx.get(url, params=params)
        return response.json()
