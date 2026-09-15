import io, os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_REGULAR = os.path.join(BASE_DIR, 'fonts', 'Roboto-Regular.ttf')
FONT_BOLD = os.path.join(BASE_DIR, 'fonts', 'Roboto-Bold.ttf')

pdfmetrics.registerFont(TTFont('Roboto', FONT_REGULAR))
pdfmetrics.registerFont(TTFont('Roboto-Bold', FONT_BOLD))

def generate_pdf(cards, filename):
    base_filename = os.path.splitext(filename)[0]
    output_title = f"{base_filename}"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', 
        parent=styles['Heading1'], 
        fontName='Roboto-Bold', 
        fontSize=18, 
        textColor=colors.HexColor("#0f172a"), 
        spaceAfter=12, 
        alignment=1
    )
    text_style = ParagraphStyle(
        'TextStyle', 
        parent=styles['Normal'], 
        fontName='Roboto', 
        fontSize=10, 
        leading=13, 
        textColor=colors.HexColor("#1e2a3a")
    )
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Roboto-Bold',
        fontSize=10,
        textColor=colors.whitesmoke
    )

    story.append(Paragraph(output_title, title_style))
    story.append(Spacer(1, 10))

    table_data = [[
        Paragraph("", header_style), 
        Paragraph("Question", header_style), 
        Paragraph("Answer", header_style)
    ]]
    
    for idx, card in enumerate(cards, 1):
        q = Paragraph(card.get('question', ''), text_style)
        a = Paragraph(card.get('answer', ''), text_style)
        table_data.append([str(idx), q, a])

    t = Table(table_data, colWidths=[30, 250, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f6fe")])
    ]))

    story.append(t)
    doc.build(story)

    buffer.seek(0)
    return buffer, f"{base_filename}_flashcards.pdf"