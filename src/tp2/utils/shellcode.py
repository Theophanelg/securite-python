from utils.config import logger
import pylibemu
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
import requests


class Shellcode:
    def __init__(self, shellcode: bytes):
        self.shellcode = shellcode

    # Extraire les chaînes de caractères imprimables de la shellcode
    def get_shellcode_string(self, min_length: int = 4) -> list:
        string = []
        current = ""

        for byte in self.shellcode:
            char = chr(byte)
            if char.isprintable():
                current += char
            else:
                if len(current) >= min_length:
                    string.append(current)
                current = ""

        if len(current) >= min_length:
            string.append(current)
            current = ""

        logger.info(f"Strings extraites : {string}")
        return string

    # Utiliser pylibemu pour analyser la shellcode
    def get_pylibemu_shellcode(self) -> str:
        emul = pylibemu.Emulator()
        offset = emul.shellcode_getpc_test(self.shellcode)
        emul.prepare(self.shellcode, offset)
        emul.test()
        result = emul.emu_profile_output
        logger.info(f"Analyse de la shellcode : {result}")
        return result

    # Utiliser Capstone pour désassembler la shellcode
    def get_capstone_shellcode(self) -> str:
        md = Cs(CS_ARCH_X86, CS_MODE_32)
        instructions = []
        for i in md.disasm(self.shellcode, 0x1000):
            instruction = f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}"
            instructions.append(instruction)
        result = "\n".join(instructions)
        logger.info(f"Instructions désassemblées : {result}")
        return result

    # Utiliser un LLM pour analyser les résultats précédents
    def get_llm_analysis(self, string: list, pylibemu_res: str, capstone_res: str) -> str:
        prompt = f"""Tu es un expert en cybersécurité et en analyse de shellcode.
            Voici les résultats d'analyse d'un shellcode :

            ---Strings extraites---
            {chr(10).join(string)}

            ---Analyse Pylibemu---
            {pylibemu_res}

            ---Désassemblage Capstone---
            {capstone_res}

            Explique en détail ce que fait ce shellcode, son origine probable,
            les appels systèmes qu'il utilise, et s'il est dangereux.
            Réponds en français.
            """
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=300,
        )
        result = response.json().get("response", "aucune réponse")
        logger.info(f"Analyse LLM : {result}")
        return result
