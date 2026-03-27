#!/usr/bin/env python3
"""
TP4 - Crazy Decoder
ESGI 4A - Sécurité Python
"""

from pwn import context, remote
import base64
import re

HOST = "31.220.95.27"
PORT = 13337

MORSE_CODE = {
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
}


def is_morse(s: str) -> bool:
    return all(c in ".- " for c in s)


def is_hex(s: str) -> bool:
    try:
        bytes.fromhex(s)
        return True
    except ValueError:
        return False


def is_base64(s: str) -> bool:
    try:
        if not re.match(r"^[A-Za-z0-9+/=]+$", s):
            return False
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False


def decode_morse(s: str) -> str:
    return "".join(MORSE_CODE.get(word, "?") for word in s.split())


def decode_hex(s: str) -> str:
    return bytes.fromhex(s).decode()


def decode_base64(s: str) -> str:
    return base64.b64decode(s).decode()


def decode(data: str) -> str:
    data_lower = data.lower()

    if "décoder:" in data_lower:
        encoded = data.split(":", 1)[1].strip()
    elif "decoder:" in data_lower:
        encoded = data.split(":", 1)[1].strip()
    else:
        encoded = data.strip()

    if is_morse(encoded):
        return decode_morse(encoded)
    elif is_hex(encoded):
        return decode_hex(encoded)
    elif is_base64(encoded):
        return decode_base64(encoded)
    else:
        return encoded


def main() -> None:
    context.log_level = "error"
    conn = remote(HOST, PORT)

    round_num = 0
    while True:
        round_num += 1

        raw = conn.recvline(timeout=5)
        if not raw:
            print(f"[Round {round_num}] Connexion fermée")
            break

        data = raw.decode("utf-8", errors="ignore")

        data_lower = data.lower()
        if "décoder" not in data_lower and "decoder" not in data_lower:
            if any(word in data_lower for word in ["flag", "bravo", "congrat", "fini", "gagn"]):
                print(f"[Round {round_num}] Réponse finale : {data.strip()}")
                break
            continue

        decoded = decode(data)
        print(f"[Round {round_num}] Décodé : {decoded}")

        conn.sendline(decoded.encode())

    conn.close()


if __name__ == "__main__":
    main()
