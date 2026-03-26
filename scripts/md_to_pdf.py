from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm

src = Path('docs/proposal_final.md')
out = Path('docs/proposal_final.pdf')

text = src.read_text(encoding='utf-8').splitlines()

styles = getSampleStyleSheet()
normal = ParagraphStyle(
    'NormalLeft',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10.5,
    leading=14,
    alignment=TA_LEFT,
)
heading1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20)
heading2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=17)
heading3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=11.5, leading=15)

story = []
for line in text:
    line = line.rstrip()
    if not line:
        story.append(Spacer(1, 4))
        continue

    if line.startswith('### '):
        story.append(Paragraph(line[4:].replace('&', '&amp;'), heading3))
        story.append(Spacer(1, 3))
    elif line.startswith('## '):
        story.append(Paragraph(line[3:].replace('&', '&amp;'), heading2))
        story.append(Spacer(1, 3))
    elif line.startswith('# '):
        story.append(Paragraph(line[2:].replace('&', '&amp;'), heading1))
        story.append(Spacer(1, 5))
    elif line.startswith('- '):
        story.append(Paragraph(f'• {line[2:].replace("&", "&amp;")}', normal))
    elif line.startswith('```'):
        # skip markdown fences for simple conversion
        continue
    else:
        safe = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        story.append(Paragraph(safe, normal))

pdf = SimpleDocTemplate(
    str(out),
    pagesize=A4,
    rightMargin=18*mm,
    leftMargin=18*mm,
    topMargin=18*mm,
    bottomMargin=18*mm,
)
pdf.build(story)
print(f'Generated: {out}')
