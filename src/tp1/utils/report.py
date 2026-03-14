class Report:
    def __init__(self, capture, filename, summary):
        self.capture = capture
        self.filename = filename
        self.title = "Rapport d'analyse réseau\n\n"
        self.summary = summary
        self.array = ""
        self.graph = ""

    def concat_report(self) -> str:
        """
        Concat all data in report
        """
        content = ""
        content += self.title
        content += self.summary
        content += self.array
        content += self.graph

        return content

    def save(self, filename: str) -> None:
        """
        Save report in a file
        :param filename:
        :return:
        """
        final_content = self.concat_report()
        with open(filename, "w") as report:
            report.write(final_content)

    def generate(self, param: str) -> None:
        """
        Generate graph and array
        """
        if param == "graph":
            # TODO: generate graph
            protocols = self.capture.sort_network_protocols()
            max_count = max((count for _, count in protocols), default=1)

            lignes = []
            lignes.append("\n=== Graphique des protocoles capturés ===")
            for proto, count in protocols:
                bar_length = int((count / max_count) * 50)
                bar = "#" * bar_length
                lignes.append(f"{proto.upper():<10}: {bar} ({count} paquets)")
            self.graph = "\n".join(lignes)

        elif param == "array":
            # TODO: generate array
            protocols = self.capture.sort_network_protocols()
            lignes = []
            lignes.append("\n=== Tableau des protocoles capturés ===")
            for proto, count in protocols:
                lignes.append(f"{proto.upper():<10}: {count} paquets")
            self.array = "\n".join(lignes)
