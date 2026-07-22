from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

styles = getSampleStyleSheet()


class PDFReport:

    def __init__(self):

        os.makedirs("reports/generated", exist_ok=True)

    def generate(

        self,

        student_name,

        exam_name,

        question,

        answer_key,

        student_answer,

        result

    ):

        filename = f"reports/generated/{student_name}_{exam_name}.pdf"

        pdf = SimpleDocTemplate(filename)

        elements = []

        elements.append(
            Paragraph(
                "<b>EvalAI - Automated Answer Sheet Evaluation Report</b>",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 0.25 * inch))

        info = Table([

            ["Student", student_name],

            ["Exam", exam_name],

            ["Marks", str(result["marks"])],

            ["Percentage", str(result["percentage"]) + "%"],

            ["Grade", result["grade"]]

        ])

        info.setStyle(

            TableStyle([

                ("GRID", (0,0), (-1,-1), 1, colors.black),

                ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),

                ("BOTTOMPADDING",(0,0),(-1,-1),8)

            ])

        )

        elements.append(info)

        elements.append(Spacer(1,0.3*inch))

        elements.append(
            Paragraph("<b>Question</b>", styles["Heading2"])
        )

        elements.append(
            Paragraph(question, styles["BodyText"])
        )

        elements.append(Spacer(1,0.15*inch))

        elements.append(
            Paragraph("<b>Official Answer</b>", styles["Heading2"])
        )

        elements.append(
            Paragraph(answer_key, styles["BodyText"])
        )

        elements.append(Spacer(1,0.15*inch))

        elements.append(
            Paragraph("<b>Student Answer</b>", styles["Heading2"])
        )

        elements.append(
            Paragraph(student_answer, styles["BodyText"])
        )

        elements.append(Spacer(1,0.15*inch))

        elements.append(
            Paragraph("<b>AI Feedback</b>", styles["Heading2"])
        )

        elements.append(
            Paragraph(result["feedback"], styles["BodyText"])
        )

        elements.append(Spacer(1,0.2*inch))

        elements.append(
            Paragraph("<b>Strengths</b>", styles["Heading2"])
        )

        for point in result["strengths"]:

            elements.append(
                Paragraph("• " + point, styles["BodyText"])
            )

        elements.append(Spacer(1,0.15*inch))

        elements.append(
            Paragraph("<b>Missing Points</b>", styles["Heading2"])
        )

        for point in result["missing_points"]:

            elements.append(
                Paragraph("• " + point, styles["BodyText"])
            )

        elements.append(Spacer(1,0.15*inch))

        elements.append(
            Paragraph("<b>Mistakes</b>", styles["Heading2"])
        )

        for point in result["mistakes"]:

            elements.append(
                Paragraph("• " + point, styles["BodyText"])
            )

        pdf.build(elements)

        return filename


pdf_report = PDFReport()