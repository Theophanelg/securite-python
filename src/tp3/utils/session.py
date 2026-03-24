from src.tp3.utils.captcha import Captcha
import re
import requests
from src.tp3.utils.config import logger


class Session:
    def __init__(self, url):
        self.url = url
        self.captcha_value = ""
        self.flag_value = None
        self.valid_flag = ""
        self.http_session = requests.Session()
        self.http_session.headers.update({"Connection": "close"})
        self.response = None

    def prepare_request(self):
        captcha = Captcha(self.url)
        captcha.session = self.http_session
        captcha.capture()
        captcha.solve()

        self.captcha_value = captcha.get_value()
        logger.debug(f"Captcha value: {self.captcha_value}")

    def submit_request(self):
        data = {"flag": str(self.flag_value), "captcha": self.captcha_value, "submit": "Envoyer"}
        self.response = self.http_session.post(self.url, data=data, timeout=10)
        logger.debug(f"Response status code: {self.response.status_code}")

    def process_response(self):
        if self.response is None:
            logger.error("No response to process")
            return False

        html = self.response.text
        logger.debug(f"Response HTML: {html}")

        match = re.search(r"FLAG-\d\{[^}]+\}", html)
        if match:
            self.valid_flag = match.group(0)
            logger.debug(f"Valid flag found: {self.valid_flag}")
            return True
        logger.debug("No valid flag found")
        return False

    def get_flag(self):
        return self.valid_flag
