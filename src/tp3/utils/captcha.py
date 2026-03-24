import re
from src.tp3.utils.config import logger
from PIL import Image
from io import BytesIO
import pytesseract
from urllib.parse import urljoin


class Captcha:
    def __init__(self, url):
        self.url = url
        self.image = None
        self.value = ""
        self.session = None

    def solve(self):
        if self.image is None:
            logger.error("No captcha image to solve")
            return

        img_gray = self.image.convert("L")
        w, h = img_gray.size
        img_resized = img_gray.resize((w * 3, h * 3), Image.LANCZOS)
        img_threshold = img_resized.point(lambda x: 0 if x < 128 else 255, "1")
        raw = pytesseract.image_to_string(
            img_threshold, config="--psm 8 -c tessedit_char_whitelist=0123456789 digits"
        )
        self.value = raw.strip().replace(" ", "").replace("\n", "")
        logger.debug(f"OCR : {raw.strip()}, Captcha value: {self.value}")

    def capture(self):
        response = self.session.get(self.url, timeout=10)
        html = response.text
        logger.debug(f"HTML: {html}")

        match = re.search(r'<img[^>]+src="(.*?)"', html, re.IGNORECASE)
        if match:
            self.image_src = match.group(1)
        else:
            logger.error("Captcha image not found in HTML")
            return

        if self.image_src.startswith("http"):
            image_url = self.image_src
        else:
            image_url = urljoin(self.url, self.image_src)

        logger.debug(f"Captcha image URL: {image_url}")

        image_response = self.session.get(image_url, timeout=10)
        self.image = Image.open(BytesIO(image_response.content))
        logger.debug("Captcha image captured successfully")

    def get_value(self):
        return self.value
