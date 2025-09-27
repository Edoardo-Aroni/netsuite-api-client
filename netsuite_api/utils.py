import secrets
import string
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504],
                    allowed_methods=["GET", "POST", "PUT", "DELETE"])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def debug(msg):
    print(msg)


def generate_state(length=32):
    chars = string.ascii_letters + string.digits + "-._~"
    return ''.join(secrets.choice(chars) for _ in range(length))
