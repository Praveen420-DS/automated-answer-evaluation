from pathlib import Path


def generate_evaluation_report(evaluation: dict) -> str | None:
    """Create a compact PDF from a canonical evaluation document.

    ReportLab is imported lazily so report support never affects API startup.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen.canvas import Canvas
    except ImportError:
        return None
    output = Path(__file__).resolve().parents[1] / "reports" / "generated"
    output.mkdir(parents=True, exist_ok=True)
    path = output / f"evaluation_{evaluation['_id']}.pdf"
    pdf = Canvas(str(path), pagesize=A4)
    pdf.drawString(72, 800, "EvalAI - Evaluation Report")
    pdf.drawString(72, 780, f"Exam: {evaluation.get('examName', '')}")
    pdf.drawString(72, 760, f"Score: {evaluation.get('totalScore', 0)} / {evaluation.get('totalMarks', 0)}")
    pdf.drawString(72, 740, f"Percentage: {evaluation.get('percentage', 0)}%   Grade: {evaluation.get('overallGrade', '')}")
    y = 710
    for result in evaluation.get("questionResults", []):
        pdf.drawString(72, y, f"Q{result.get('questionNumber')}: {result.get('score')} / {result.get('maxScore')} - {result.get('grade')}")
        y -= 18
        if y < 72:
            pdf.showPage(); y = 800
    pdf.save()
    return str(path)
