from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


class PDFService:
    @staticmethod
    def generate_report(title, content_sections):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 12))
        for section_title, body in content_sections:
            story.append(Paragraph(section_title, styles["Heading2"]))
            story.append(Paragraph(body, styles["Normal"]))
            story.append(Spacer(1, 12))
        doc.build(story)
        buffer.seek(0)
        return buffer
