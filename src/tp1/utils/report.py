from fpdf import FPDF


class Report:
    def __init__(self, capture, filename, summary):
        self.capture = capture
        self.filename = filename
        self.title = "Rapport d'analyse reseau\n\n"
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

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 8, final_content)
        pdf.output(filename)

    def generate(self, param: str) -> None:
        """
        Generate graph and array
        """
        if param == "graph":
            protocols = self.capture.sort_network_protocols()
            max_count = max((count for _, count in protocols), default=1)

            lines = ["\n=== Graphique (barres texte) ==="]
            for proto, count in protocols:
                bar_len = int((count / max_count) * 40) if max_count > 0 else 0
                lines.append(f"{proto.upper():<8} | {'#' * bar_len} ({count})")

            self.graph = "\n".join(lines)
        elif param == "array":
            protocols = self.capture.sort_network_protocols()

            lines = [
                "\n=== Tableau des protocoles ===",
                "PROTOCOLE | PAQUETS",
                "--------------------",
            ]
            for proto, count in protocols:
                lines.append(f"{proto.upper():<9} | {count}")

            self.array = "\n".join(lines)
