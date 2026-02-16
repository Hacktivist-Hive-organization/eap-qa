import httpx
import logging

logger = logging.getLogger("api_logger")


class ApiClient:
    def __init__(self, api_url):
        self.api_url = api_url
        self.client = httpx.Client(base_url=api_url, timeout=10)

    def close(self):
        self.client.close()

    def log_request(self, method, endpoint):
        logger.info("Logging request")
        logger.info(f"Request method: {method}, URL: {self.api_url}{endpoint}")

    def log_response(self, response: httpx.Response):
        logger.info("Logging response")
        logger.info(
            "Response method: %s, Response URL: %s, Status code: %s",
            response.request.method,
            response.request.url,
            response.status_code
        )
        logger.info(f"Response body: {response.text}")

    def get(self, endpoint, **kwargs):
        self.log_request("GET", endpoint)
        response = self.client.get(endpoint, **kwargs)
        self.log_response(response)
        return response

    def post(self, endpoint, body, headers=None):
        self.log_request("POST", endpoint)
        response = self.client.post(endpoint, json=body, headers=headers)
        self.log_response(response)
        return response

    def put(self, endpoint, body):
        self.log_request("PUT", endpoint)
        response = self.client.put(endpoint, json=body)
        self.log_response(response)
        return response

    def delete(self, endpoint):
        self.log_request("DELETE", endpoint)
        response = self.client.delete(endpoint)
        self.log_response(response)
        return response
