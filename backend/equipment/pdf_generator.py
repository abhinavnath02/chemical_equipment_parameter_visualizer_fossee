from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

def generate_pdf_report(data):
    """
    Generate a PDF report from analysis data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>Chemical Equipment Analysis Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Date
    date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    date_para = Paragraph(f"Generated: {date_str}", styles['Normal'])
    elements.append(date_para)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Summary Statistics
    summary_title = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
    elements.append(summary_title)
    elements.append(Spacer(1, 0.1 * inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment', str(data.get('total_equipment', 0))],
        ['Average Flowrate', f"{data.get('avg_flowrate', 0):.2f}"],
        ['Average Pressure', f"{data.get('avg_pressure', 0):.2f}"],
        ['Average Temperature', f"{data.get('avg_temperature', 0):.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Equipment Distribution
    if 'equipment_by_type' in data and data['equipment_by_type']:
        dist_title = Paragraph("<b>Equipment Distribution by Type</b>", styles['Heading2'])
        elements.append(dist_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        dist_data = [['Equipment Type', 'Count']]
        for eq_type, count in data['equipment_by_type'].items():
            dist_data.append([eq_type, str(count)])
        
        dist_table = Table(dist_data, colWidths=[3 * inch, 2 * inch])
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(dist_table)
        elements.append(Spacer(1, 0.3 * inch))
    
    # Equipment Details
    if 'equipment_data' in data and data['equipment_data']:
        details_title = Paragraph("<b>Detailed Equipment Data</b>", styles['Heading2'])
        elements.append(details_title)
        elements.append(Spacer(1, 0.1 * inch))
        
        details_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        for eq in data['equipment_data']:
            details_data.append([
                eq['name'],
                eq['type'],
                f"{eq['flowrate']:.1f}",
                f"{eq['pressure']:.1f}",
                f"{eq['temperature']:.1f}",
            ])
        
        details_table = Table(details_data, colWidths=[1.8*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(details_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
