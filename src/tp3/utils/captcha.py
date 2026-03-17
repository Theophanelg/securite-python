import re
from src.tp3.utils.logger import logger
from PIL import Image
from io import BytesIO
import pytesseract

class Captcha:
    def __init__(self, url):
        self.url = url
        self.image = ""
        self.value = ""
        self.session = None

    def solve(self):
        """
        Fonction permettant la résolution du captcha.
        """
        self.value = "FIXME"

    def capture(self):
        """
        Fonction permettant la capture du captcha.
        """
        response = self.session.get(self.url)
        html = response.text
        logger.debug(f"HTML: {html}")

        match = re.search(r'<img[^>]+src="(.*?)"', html, re.IGNORECASE)
        if match:
            self.image_src = match.group(1)
        else:
            logger.error("Captcha image not found in HTML")
            return

        if self.image_src.startswith('http'):
            image_url = self.image_src
        else:
            image_url = self.url.rsplit("/") + "/" + self.image_src.lstrip("/")
        
        logger.debug(f"Captcha image URL: {image_url}")

        image_response = self.session.get(image_url)
        self.image = Image.open(BytesIO(image_response.content))
        logger.debug("Captcha image captured successfully")

    def get_value(self):
        """
        Fonction retournant la valeur du captcha
        """
        return self.value
