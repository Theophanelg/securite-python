import re
from src.tp3.utils.logger import logger
from PIL import Image
from io import BytesIO
import pytesseract

class Captcha:
    def __init__(self, url):
        self.url = url
        self.image = None
        self.value = ""
        self.session = None

    def solve(self):
        """
        Fonction permettant la résolution du captcha.
        """
        if self.image is None:
            logger.error("No captcha image to solve")
            return

        img_gray = self.image.convert('L')

        raw = pytesseract.image_to_string(img_gray, config=("--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"))

        self.value = raw.strip().replace(" ", "").replace("\n", "")
        logger.debug(f"OCR : {raw.strip()}, Captcha value: {self.value}")

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
            image_url = self.url.rstrip("/") + "/" + self.image_src.lstrip("/")
        
        logger.debug(f"Captcha image URL: {image_url}")

        image_response = self.session.get(image_url)
        self.image = Image.open(BytesIO(image_response.content))
        logger.debug("Captcha image captured successfully")

    def get_value(self):
        """
        Fonction retournant la valeur du captcha
        """
        return self.value
