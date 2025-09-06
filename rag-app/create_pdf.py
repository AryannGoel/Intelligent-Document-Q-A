# create_pdf.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def create_test_pdf():
    """
    Creates a test PDF document named 'Innovate_Robotics_Report_2025.pdf'.
    """
    doc = SimpleDocTemplate("Innovate_Robotics_Report_2025.pdf")
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['h1']
    title_style.alignment = 1 # Center alignment
    title = Paragraph("Innovate Robotics - 2025 Annual Report Summary", title_style)
    story.append(title)
    story.append(Spacer(1, 0.25*inch))

    # Body Style
    body_style = styles['BodyText']
    body_style.spaceAfter = 12 # Space after paragraph

    # Introduction Section
    heading_style = styles['h2']
    intro_heading = Paragraph("1. Introduction and Mission", heading_style)
    story.append(intro_heading)

    intro_text = """
    Innovate Robotics, founded in 2018, is a leading technology firm based in Bangalore, India.
    Our mission is to develop autonomous systems that enhance productivity and safety across various
    industries. This document summarizes our key achievements, financial performance, and future
    outlook for the fiscal year 2025, which concluded on March 31, 2025.
    """
    story.append(Paragraph(intro_text, body_style))
    story.append(Spacer(1, 0.2*inch))

    # Financial Highlights Section
    finance_heading = Paragraph("2. Financial Highlights", heading_style)
    story.append(finance_heading)
    
    finance_text = """
    The company demonstrated robust financial health in 2025. Total revenue reached 
    <b>₹50 crore</b>, a significant increase of 20% compared to the previous fiscal year's
    revenue of ₹41.5 crore. The net profit margin stood strong at <b>15%</b>. Our primary revenue
    driver was the industrial automation sector, contributing 60% of the total revenue.
    """
    story.append(Paragraph(finance_text, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Add a page break
    story.append(PageBreak())

    # Key Achievements Section
    achievements_heading = Paragraph("3. Key Achievements in 2025", heading_style)
    story.append(achievements_heading)

    achievements_text = """
    This year was marked by several milestones. In August 2024, we successfully launched our flagship
    product, the <b>'Guardian Drone'</b>. This drone utilizes a proprietary AI-powered navigation system,
    making it ideal for infrastructure inspection and security surveillance. Furthermore, we expanded
    our operations by opening a new state-of-the-art R&D center in <b>Hyderabad</b>.
    Our team also grew significantly, with the hiring of 50 new engineers, bringing our total
    employee count to 250.
    """
    story.append(Paragraph(achievements_text, body_style))
    story.append(Spacer(1, 0.2*inch))

    # Future Outlook Section
    future_heading = Paragraph("4. Future Outlook for 2026", heading_style)
    story.append(future_heading)

    future_text = """
    Looking ahead to 2026, our primary focus will be on entering the consumer market. We are currently
    developing a new line of domestic assistant bots, codenamed 'Project Companion', with a planned
    launch in the third quarter. We project a revenue target of <b>₹75 crore</b> for the next
    fiscal year, driven by both our existing industrial clients and new consumer products.
    """
    story.append(Paragraph(future_text, body_style))

    # Build the PDF
    doc.build(story)
    print("✅ PDF 'Innovate_Robotics_Report_2025.pdf' created successfully.")


if __name__ == '__main__':
    create_test_pdf()