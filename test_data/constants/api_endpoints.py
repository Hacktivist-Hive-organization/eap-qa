class HealthEndpoints:
    HEALTH = "/api/v1/health/"


class AuthEndpoints:
    REGISTER = "/api/v1/auth/register"
    LOGIN = "/api/v1/auth/login"


class UserEndpoints:
    USERS = "/api/v1/users/"
    USERS_ME = "/api/v1/users/me"
    USER_BY_ID = "/api/v1/users/{user_id}"


class RequestsEndpoints:
    REQUESTS = "/api/v1/requests/"
    MY_REQUESTS = "/api/v1/requests/my-requests"
    REQUEST_BY_ID = "/api/v1/requests/{request_id}"
    REQUEST_TYPES = "/api/v1/types/"
    REQUEST_SUBTYPES = "/api/v1/subtypes/"
