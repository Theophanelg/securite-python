import argparse
from utils.shellcode import Shellcode
from utils.config import logger


def parse_shellcode_file(file_path: str) -> bytes:
    with open(file_path, "r") as f:
        content = f.read().strip()

    raw = b""
    parts = content.replace("\n", "").replace(" ", "").split("\\x")
    for part in parts:
        if part:
            raw += bytes.fromhex(part)
    return raw


def main():
    parser = argparse.ArgumentParser(description="TP2 - Analyseur de shellcode")
    parser.add_argument("-f", "--file", required=True, help="Fichier shellcode à analyser")
    args = parser.parse_args()

    raw = parse_shellcode_file(args.file)
    logger.info(f"Testing shellcode of size {len(raw)}B")

    shellcode = Shellcode(raw)

    strings = shellcode.get_shellcode_string()
    pylibemu_result = shellcode.get_pylibemu_shellcode()
    capstone_result = shellcode.get_capstone_shellcode()

    logger.info("Shellcode analysed !")

    llm_result = shellcode.get_llm_analysis(strings, pylibemu_result, capstone_result)
    logger.info(f"Explication LLM : {llm_result}")


if __name__ == "__main__":
    main()
