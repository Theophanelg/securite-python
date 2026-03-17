from src.tp3.utils.captcha import Captcha
import re 
import requests
from src.tp3.utils.logger import logger


class Session:
    """
    Class representing a session to solve a captcha and submit a flag.

    Attributes:
        url (str): The URL of the captcha.
        captcha_value (str): The value of the solved captcha.
        flag_value (str): The value of the flag to submit.
        valid_flag (str): The valid flag obtained after processing the response.
    """

    def __init__(self, url):
        """
        Initializes a new session with the given URL.

        Args:
            url (str): The URL of the captcha.
        """
        self.url = url
        self.captcha_value = ""
        self.flag_value = ""
        self.valid_flag = ""
        self.http_session = requests.Session()
        self.response = None

    def prepare_request(self):
        """
        Prepares the request for sending by capturing and solving the captcha.
        """
        captcha = Captcha(self.url)
        captcha.session = self.http_session
        captcha.capture()
        captcha.solve()

        self.captcha_value = captcha.get_value()
        self.flag_value = ""
        logger.debug(f"Captcha value: {self.captcha_value}")

    def submit_request(self):
        """
        Sends the flag and captcha.
        """
        data = {
            "captcha": self.captcha_value,
            "flag": self.flag_value
        }
        self.response = self.http_session.post(self.url, data=data) 
        logger.debug(f"Response status code: {self.response.status_code}")

    def process_response(self):
        """
        Processes the response.
        """
        if self.response is None:
            logger.error("No response to process")
            return False

        html = self.response.text
        logger.debug(f"Response HTML: {html}")

        match = re.search(r"[A-Z]+\{.*?\}", html, re.IGNORECASE)
        if match:
            self.valid_flag = match.group(0)
            logger.debug(f"Valid flag found: {self.valid_flag}")
            return True
        logger.debug("No valid flag found")
        return False

    def get_flag(self):
        """
        Returns the valid flag.

        Returns:
            str: The valid flag.
        """
        return self.valid_flag
