import scapy.all as scapy
from src.tp1.utils.lib import choose_interface
from src.tp1.utils.config import logger


class Capture:
    def __init__(self) -> None:
        self.interface = choose_interface()
        self.summary = ""
        self.packets = []

    def capture_trafic(self) -> None:
        """
        Capture network trafic from an interface
        """
        logger.info(f"Démarrage de la capture sur {self.interface} (max 20 paquets, timeout 10s)...")
        self.packets = scapy.sniff(iface=self.interface, count=20, timeout=10)
        logger.info(f"Capture terminée : {len(self.packets)} paquets capturés")

    def sort_network_protocols(self) -> list:
        """
        Sort and return all captured network protocols
        """
        protocols = self.get_all_protocols()
        return sorted(protocols.items(), key=lambda item: item[1], reverse=True)

    def get_all_protocols(self) -> dict:
        """
        Return all protocols captured with total packets number
        """
        protocols_count = {"tcp": 0, "udp": 0, "icmp": 0, "arp": 0, "other": 0}
        for packet in self.packets:
            if packet.haslayer(scapy.TCP):
                protocols_count["tcp"] += 1
            elif packet.haslayer(scapy.UDP):
                protocols_count["udp"] += 1
            elif packet.haslayer(scapy.ICMP):
                protocols_count["icmp"] += 1
            elif packet.haslayer(scapy.ARP):
                protocols_count["arp"] += 1
            else:
                protocols_count["other"] += 1
        return protocols_count

    def analyse(self, protocols: str) -> None:
        """
        Analyse all captured data and return statement
        Si un tra c est illégitime (exemple : Injection SQL, ARP
        Spoo ng, etc)
        a Noter la tentative d'attaque.
        b Relever le protocole ainsi que l'adresse réseau/physique
        de l'attaquant.
        c (FACULTATIF) Opérer le blocage de la machine
        attaquante.
        Sinon a cher que tout va bien
        """
        all_protocols = self.get_all_protocols()
        sort = self.sort_network_protocols()
        total_packets = len(self.packets)
        arp_count = all_protocols.get("arp", 0)

        alerts = []

        if total_packets > 0 and arp_count > total_packets * 0.5:
            alerts.append("Activité arp suspecte détectée")
        self.summary = self.gen_summary(sort, alerts)

    def get_summary(self) -> str:
        return self.summary

    def gen_summary(self, sort: list, alerts: list) -> str:
        """
        Generate summary
        """
        lignes = []
        lignes.append("=== Rapport de capture ===")
        lignes.append(f"Interface: {self.interface}")
        lignes.append(f"Nombre de paquets capturés: {len(self.packets)}")
        lignes.append("")
        lignes.append("=== Protocoles capturés ===")

        for protocol, count in sort:
            lignes.append(f"{protocol.upper()}: {count} paquets")

        lignes.append("")
        if alerts:
            lignes.append("=== Alertes détectées ===")
            for alert in alerts:
                lignes.append(f"- {alert}")
        else:
            lignes.append("Aucune alerte détectée.")

        summary = "\n".join(lignes)
        return summary
