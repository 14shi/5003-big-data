from pathlib import Path
import markdown
from bs4 import BeautifulSoup

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm

SRC = Path("docs/proposal_final.md")
OUT = Path("docs/proposal_final.pdf")

md_text = SRC.read_text(encoding="utf-8")
# Convert markdown to HTML first, then render without markdown symbols.
html = markdown.markdown(md_text, extensions=["extra", "sane_lists"])
soup = BeautifulSoup(html, "html.parser")

styles = getSampleStyleSheet()

h1 = ParagraphStyle(
    "h1",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=17,
    leading=21,
    alignment=TA_CENTER,
    spaceAfter=6,
)
h2 = ParagraphStyle(
    "h2",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=13.5,
    leading=18,
    alignment=TA_LEFT,
    spaceBefore=8,
    spaceAfter=4,
)
h3 = ParagraphStyle(
    "h3",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=11.5,
    leading=15,
    alignment=TA_LEFT,
    spaceBefore=6,
    spaceAfter=2,
)
body = ParagraphStyle(
    "body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=14.5,
    alignment=TA_LEFT,
    spaceAfter=4,
)
bullet = ParagraphStyle(
    "bullet",
    parent=body,
    leftIndent=12,
    bulletIndent=0,
)

story = []

for node in soup.children:
    if getattr(node, "name", None) is None:
        continue

    if node.name == "h1":
        story.append(Paragraph(node.get_text(strip=True), h1))
        story.append(Spacer(1, 2))
    elif node.name == "h2":
        story.append(Paragraph(node.get_text(strip=True), h2))
    elif node.name == "h3":
        story.append(Paragraph(node.get_text(strip=True), h3))
    elif node.name == "p":
        text = " ".join(node.stripped_strings)
        if text:
            story.append(Paragraph(text, body))
    elif node.name == "ul":
        for li in node.find_all("li", recursive=False):
            text = " ".join(li.stripped_strings)
            if text:
                story.append(Paragraph(f"• {text}", bullet))
        story.append(Spacer(1, 2))
    elif node.name == "ol":
        idx = 1
        for li in node.find_all("li", recursive=False):
            text = " ".join(li.stripped_strings)
            if text:
                story.append(Paragraph(f"{idx}. {text}", bullet))
                idx += 1
        story.append(Spacer(1, 2))
    elif node.name == "hr":
        story.append(Spacer(1, 6))

pdf = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin=18 * mm,
    rightMargin=18 * mm,
    topMargin=16 * mm,
    bottomMargin=16 * mm,
    title="Wide Project Proposal",
)
pdf.build(story)
print(f"Generated polished PDF: {OUT}")
