from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue
from reportlab.lib.units import inch


def generate_chat_pdf(messages):
    """
    Generates a PDF from chat messages.
    Returns PDF as BytesIO object.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = darkblue

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    story = []

    # ==============================
    # TITLE
    # ==============================

    story.append(
        Paragraph("Academic Notes AI", title_style)
    )

    story.append(
        Paragraph("Chat Conversation", heading_style)
    )

    story.append(
        Paragraph("<br/><br/>", normal_style)
    )

    # ==============================
    # CHAT MESSAGES
    # ==============================

    for msg in messages:

        role = msg["role"].capitalize()

        story.append(
            Paragraph(
                f"<b>{role}</b>",
                heading_style
            )
        )

        story.append(
            Paragraph(
                msg["content"].replace("\n", "<br/>"),
                normal_style
            )
        )

        story.append(
            Paragraph("<br/>", normal_style)
        )

    # ==============================
    # BUILD PDF
    # ==============================

    doc.build(story)

    buffer.seek(0)

    return buffer