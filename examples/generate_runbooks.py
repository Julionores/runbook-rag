"""Genere les 5 PDF de runbooks fictifs utilises comme corpus documentaire.
Produit volontairement un en-tete et un pied de page repetitifs sur chaque
page, pour reproduire une vraie documentation interne a nettoyer."""

import os
import sys
from fpdf import FPDF

sys.path.insert(0, os.path.dirname(__file__))
from runbook_content import RUNBOOKS  # noqa: E402


class RunbookPDF(FPDF):
    def __init__(self, titre):
        super().__init__()
        self.titre = titre
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"CloudOps Interne - {self.titre}", align="L")
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Document confidentiel - Page {self.page_no()}", align="C")


def generate_runbooks(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    paths = []
    for filename, titre, paragraphs in RUNBOOKS:
        pdf = RunbookPDF(titre)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(20, 20, 20)
        pdf.cell(0, 12, titre, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        pdf.set_font("Helvetica", "", 11)
        for para in paragraphs:
            pdf.multi_cell(0, 7, para)
            pdf.ln(4)

        path = os.path.join(output_dir, f"{filename}.pdf")
        pdf.output(path)
        paths.append(path)
    return paths


if __name__ == "__main__":
    generated = generate_runbooks("runbooks")
    for path in generated:
        print("genere:", path)
