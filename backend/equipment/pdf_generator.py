from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, Frame, PageTemplate
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Safety thresholds (configurable)
THRESHOLDS = {
    'flowrate': {'min': 50, 'max': 500, 'critical_max': 600},
    'pressure': {'min': 100, 'max': 800, 'critical_max': 1000},
    'temperature': {'min': 50, 'max': 350, 'critical_max': 400}
}

def check_safety_warnings(data):
    """Check for equipment operating outside safe parameters"""
    warnings = []
    equipment_data = data.get('equipment_data', [])
    
    for eq in equipment_data:
        eq_warnings = []
        
        # Check flowrate
        if eq['flowrate'] < THRESHOLDS['flowrate']['min']:
            eq_warnings.append(f"⚠ Low flowrate ({eq['flowrate']:.1f})")
        elif eq['flowrate'] > THRESHOLDS['flowrate']['critical_max']:
            eq_warnings.append(f"🔴 CRITICAL: Flowrate too high ({eq['flowrate']:.1f})")
        elif eq['flowrate'] > THRESHOLDS['flowrate']['max']:
            eq_warnings.append(f"⚠ High flowrate ({eq['flowrate']:.1f})")
        
        # Check pressure
        if eq['pressure'] < THRESHOLDS['pressure']['min']:
            eq_warnings.append(f"⚠ Low pressure ({eq['pressure']:.1f})")
        elif eq['pressure'] > THRESHOLDS['pressure']['critical_max']:
            eq_warnings.append(f"🔴 CRITICAL: Pressure too high ({eq['pressure']:.1f})")
        elif eq['pressure'] > THRESHOLDS['pressure']['max']:
            eq_warnings.append(f"⚠ High pressure ({eq['pressure']:.1f})")
        
        # Check temperature
        if eq['temperature'] < THRESHOLDS['temperature']['min']:
            eq_warnings.append(f"⚠ Low temperature ({eq['temperature']:.1f})")
        elif eq['temperature'] > THRESHOLDS['temperature']['critical_max']:
            eq_warnings.append(f"🔴 CRITICAL: Temperature too high ({eq['temperature']:.1f})")
        elif eq['temperature'] > THRESHOLDS['temperature']['max']:
            eq_warnings.append(f"⚠ High temperature ({eq['temperature']:.1f})")
        
        if eq_warnings:
            warnings.append({
                'equipment': eq['name'],
                'type': eq['type'],
                'warnings': eq_warnings
            })
    
    return warnings

def create_bar_chart(data):
    """Create bar chart for average parameters"""
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
    
    categories = ['Flowrate', 'Pressure', 'Temperature']
    values = [
        data.get('avg_flowrate', 0),
        data.get('avg_pressure', 0),
        data.get('avg_temperature', 0)
    ]
    colors_list = ['#ef4444', '#3b82f6', '#22c55e']
    
    bars = ax.bar(categories, values, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax.set_ylabel('Value', fontweight='bold', fontsize=11)
    ax.set_title('Average Equipment Parameters', fontweight='bold', fontsize=13, pad=15)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    # Save to buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def create_pie_chart(data):
    """Create pie chart for equipment distribution"""
    equipment_by_type = data.get('equipment_by_type', {})
    
    if not equipment_by_type:
        return None
    
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
    
    labels = list(equipment_by_type.keys())
    sizes = list(equipment_by_type.values())
    colors_list = plt.cm.Set3.colors[:len(labels)]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors_list, startangle=90,
                                        textprops={'fontsize': 9, 'weight': 'bold'})
    
    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    ax.set_title('Equipment Distribution by Type', fontweight='bold', fontsize=13, pad=15)
    
    plt.tight_layout()
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def create_trend_chart(data):
    """Create line chart showing parameter trends across equipment"""
    equipment_data = data.get('equipment_data', [])
    
    if not equipment_data:
        return None
    
    # Limit to first 15 for readability
    equipment_data = equipment_data[:15]
    
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='white')
    
    names = [eq['name'][:15] for eq in equipment_data]
    flowrates = [eq['flowrate'] for eq in equipment_data]
    pressures = [eq['pressure'] for eq in equipment_data]
    temperatures = [eq['temperature'] for eq in equipment_data]
    
    x = np.arange(len(names))
    
    ax.plot(x, flowrates, marker='o', color='#ef4444', label='Flowrate', linewidth=2, markersize=6)
    ax.plot(x, pressures, marker='s', color='#3b82f6', label='Pressure', linewidth=2, markersize=6)
    ax.plot(x, temperatures, marker='^', color='#22c55e', label='Temperature', linewidth=2, markersize=6)
    
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', fontsize=7)
    ax.set_ylabel('Value', fontweight='bold', fontsize=10)
    ax.set_title('Equipment Parameter Trends', fontweight='bold', fontsize=13, pad=15)
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

def create_safety_chart(data):
    """Create chart showing equipment in different safety zones"""
    equipment_data = data.get('equipment_data', [])
    
    if not equipment_data:
        return None
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(9, 3), facecolor='white')
    
    def categorize_values(values, param):
        safe = sum(1 for v in values if THRESHOLDS[param]['min'] <= v <= THRESHOLDS[param]['max'])
        warning = sum(1 for v in values if (v > THRESHOLDS[param]['max'] and v <= THRESHOLDS[param]['critical_max']) or v < THRESHOLDS[param]['min'])
        critical = sum(1 for v in values if v > THRESHOLDS[param]['critical_max'])
        return [safe, warning, critical]
    
    flowrates = [eq['flowrate'] for eq in equipment_data]
    pressures = [eq['pressure'] for eq in equipment_data]
    temperatures = [eq['temperature'] for eq in equipment_data]
    
    # Flowrate safety
    flow_counts = categorize_values(flowrates, 'flowrate')
    ax1.bar(['Safe', 'Warning', 'Critical'], flow_counts, color=['#22c55e', '#f59e0b', '#ef4444'])
    ax1.set_title('Flowrate Safety', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Equipment Count', fontsize=9)
    
    # Pressure safety
    press_counts = categorize_values(pressures, 'pressure')
    ax2.bar(['Safe', 'Warning', 'Critical'], press_counts, color=['#22c55e', '#f59e0b', '#ef4444'])
    ax2.set_title('Pressure Safety', fontsize=10, fontweight='bold')
    
    # Temperature safety
    temp_counts = categorize_values(temperatures, 'temperature')
    ax3.bar(['Safe', 'Warning', 'Critical'], temp_counts, color=['#22c55e', '#f59e0b', '#ef4444'])
    ax3.set_title('Temperature Safety', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

class HeaderCanvas(canvas.Canvas):
    """Custom canvas with header banner on each page"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        
    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        page_count = len(self.pages)
        for page_num, page in enumerate(self.pages, 1):
            self.__dict__.update(page)
            self.draw_header_banner(page_num, page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_header_banner(self, page_num, page_count):
        """Draw modern header banner"""
        # Dark banner background
        self.setFillColor(colors.HexColor('#000000'))
        self.rect(0, letter[1] - 80, letter[0], 80, fill=1, stroke=0)
        
        # Accent stripe
        self.setFillColor(colors.HexColor('#3b82f6'))
        self.rect(0, letter[1] - 85, letter[0], 5, fill=1, stroke=0)
        
        # Title
        self.setFillColor(colors.white)
        self.setFont('Helvetica-Bold', 18)
        self.drawString(40, letter[1] - 40, "Chemical Equipment")
        
        self.setFont('Helvetica', 14)
        self.drawString(40, letter[1] - 60, "Parameter Analysis Report")
        
        # Page number
        self.setFont('Helvetica', 9)
        self.setFillColor(colors.HexColor('#a1a1aa'))
        self.drawRightString(letter[0] - 40, letter[1] - 50, f"Page {page_num} of {page_count}")

def generate_pdf_report(data):
    """
    Generate a comprehensive PDF report with modern design
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        topMargin=100,  # Space for header banner
        bottomMargin=0.5*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles with modern fonts
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#000000'),
        spaceAfter=6,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#71717a'),
        spaceAfter=20,
        fontName='Helvetica',
        alignment=TA_LEFT
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#18181b'),
        spaceAfter=10,
        spaceBefore=16,
        fontName='Helvetica-Bold',
        leftIndent=0
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#3f3f46'),
        spaceAfter=6,
        fontName='Helvetica',
        leading=14
    )
    
    warning_style = ParagraphStyle(
        'Warning',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#dc2626'),
        leftIndent=15,
        fontName='Helvetica',
        leading=13
    )
    
    critical_style = ParagraphStyle(
        'Critical',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#991b1b'),
        leftIndent=15,
        fontName='Helvetica-Bold',
        leading=13
    )
    
    # Report metadata section
    date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Overview section with colored card
    overview_data = [
        ['Report Overview', ''],
        ['Generated', date_str],
        ['Total Equipment', str(data.get('total_equipment', 0))],
        ['Avg Flowrate', f"{data.get('avg_flowrate', 0):.2f}"],
        ['Avg Pressure', f"{data.get('avg_pressure', 0):.2f}"],
        ['Avg Temperature', f"{data.get('avg_temperature', 0):.2f}"]
    ]
    
    overview_table = Table(overview_data, colWidths=[2.5*inch, 3.5*inch])
    overview_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#18181b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f4f4f5')),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.HexColor('#3f3f46')),
        ('TEXTCOLOR', (1, 1), (1, -1), colors.HexColor('#18181b')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 1), (-1, -1), 12),
        ('RIGHTPADDING', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        
        # Border
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e4e4e7')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#3b82f6')),
    ]))
    
    elements.append(overview_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Safety Threshold Information
    threshold_title = Paragraph("Safety Threshold Settings", heading2_style)
    elements.append(threshold_title)
    
    threshold_data = [
        ['Parameter', 'Minimum', 'Maximum', 'Critical Max'],
        ['Flowrate', str(THRESHOLDS['flowrate']['min']), str(THRESHOLDS['flowrate']['max']), str(THRESHOLDS['flowrate']['critical_max'])],
        ['Pressure', str(THRESHOLDS['pressure']['min']), str(THRESHOLDS['pressure']['max']), str(THRESHOLDS['pressure']['critical_max'])],
        ['Temperature', str(THRESHOLDS['temperature']['min']), str(THRESHOLDS['temperature']['max']), str(THRESHOLDS['temperature']['critical_max'])],
    ]
    
    threshold_table = Table(threshold_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
    threshold_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#18181b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fafafa')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e4e4e7')),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#3b82f6')),
    ]))
    elements.append(threshold_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Bar Chart
    bar_chart_img = create_bar_chart(data)
    if bar_chart_img:
        chart_title = Paragraph("Average Parameters", heading2_style)
        elements.append(chart_title)
        img = Image(bar_chart_img, width=5*inch, height=3.33*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.3 * inch))
    
    # Pie Chart
    pie_chart_img = create_pie_chart(data)
    if pie_chart_img:
        chart_title = Paragraph("Equipment Distribution", heading2_style)
        elements.append(chart_title)
        img = Image(pie_chart_img, width=5*inch, height=3.33*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.3 * inch))
    
    elements.append(PageBreak())
    
    # Trend Chart
    trend_chart_img = create_trend_chart(data)
    if trend_chart_img:
        chart_title = Paragraph("Equipment Parameter Trends", heading2_style)
        elements.append(chart_title)
        img = Image(trend_chart_img, width=6.5*inch, height=3.25*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.3 * inch))
    
    # Safety Analysis Chart
    safety_chart_img = create_safety_chart(data)
    if safety_chart_img:
        chart_title = Paragraph("Safety Status Distribution", heading2_style)
        elements.append(chart_title)
        img = Image(safety_chart_img, width=6.5*inch, height=2.17*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.3 * inch))
    
    # Safety Warnings
    warnings = check_safety_warnings(data)
    if warnings:
        warning_title = Paragraph("⚠ Safety Warnings", heading2_style)
        elements.append(warning_title)
        
        for w in warnings:
            # Warning card
            warn_data = [[f"{w['equipment']} ({w['type']})"]]
            for warn in w['warnings']:
                warn_data.append([f"• {warn}"])
            
            warn_table = Table(warn_data, colWidths=[6.5*inch])
            warn_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fef2f2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#991b1b')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffffff')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#dc2626')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (0, 0), 8),
                ('BOTTOMPADDING', (0, 0), (0, 0), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#fca5a5')),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#dc2626')),
            ]))
            elements.append(warn_table)
            elements.append(Spacer(1, 0.15 * inch))
    else:
        # Safe status card
        safe_data = [["✓ All Systems Normal"], ["All equipment operating within safe parameters"]]
        safe_table = Table(safe_data, colWidths=[6.5*inch])
        safe_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0fdf4')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#166534')),
            ('TEXTCOLOR', (0, 1), (0, 1), colors.HexColor('#16a34a')),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, 1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (0, 0), 12),
            ('FONTSIZE', (0, 1), (0, 1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (0, 0), 12),
            ('BOTTOMPADDING', (0, 0), (0, 0), 4),
            ('TOPPADDING', (0, 1), (0, 1), 4),
            ('BOTTOMPADDING', (0, 1), (0, 1), 12),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#22c55e')),
        ]))
        elements.append(safe_table)
        elements.append(Spacer(1, 0.3 * inch))
    
    # Equipment Distribution Table
    if 'equipment_by_type' in data and data['equipment_by_type']:
        elements.append(PageBreak())
        dist_title = Paragraph("Equipment Distribution by Type", heading2_style)
        elements.append(dist_title)
        
        dist_data = [['Equipment Type', 'Count', 'Percentage']]
        total = sum(data['equipment_by_type'].values())
        for eq_type, count in data['equipment_by_type'].items():
            percentage = (count / total * 100) if total > 0 else 0
            dist_data.append([eq_type, str(count), f"{percentage:.1f}%"])
        
        dist_table = Table(dist_data, colWidths=[3 * inch, 1.5 * inch, 1.5 * inch])
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#18181b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f4f4f5')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#3f3f46')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e4e4e7')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#3b82f6')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f4f4f5'), colors.white]),
        ]))
        elements.append(dist_table)
        elements.append(Spacer(1, 0.3 * inch))
    
    # Equipment Details with Safety Status
    if 'equipment_data' in data and data['equipment_data']:
        details_title = Paragraph("Detailed Equipment Data with Safety Status", heading2_style)
        elements.append(details_title)
        
        details_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp', 'Status']]
        
        for eq in data['equipment_data']:
            # Determine status
            status = '✓ Safe'
            status_color = colors.green
            
            if (eq['flowrate'] > THRESHOLDS['flowrate']['critical_max'] or
                eq['pressure'] > THRESHOLDS['pressure']['critical_max'] or
                eq['temperature'] > THRESHOLDS['temperature']['critical_max']):
                status = '🔴 Critical'
                status_color = colors.red
            elif (eq['flowrate'] > THRESHOLDS['flowrate']['max'] or eq['flowrate'] < THRESHOLDS['flowrate']['min'] or
                  eq['pressure'] > THRESHOLDS['pressure']['max'] or eq['pressure'] < THRESHOLDS['pressure']['min'] or
                  eq['temperature'] > THRESHOLDS['temperature']['max'] or eq['temperature'] < THRESHOLDS['temperature']['min']):
                status = '⚠ Warning'
                status_color = colors.orange
            
            details_data.append([
                eq['name'][:20],
                eq['type'],
                f"{eq['flowrate']:.1f}",
                f"{eq['pressure']:.1f}",
                f"{eq['temperature']:.1f}",
                status
            ])
        
        details_table = Table(details_data, colWidths=[1.5*inch, 1.2*inch, 0.9*inch, 0.9*inch, 0.8*inch, 1*inch])
        
        # Build style with modern theme
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#18181b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e4e4e7')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#3b82f6')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f4f4f5'), colors.white]),
        ]
        
        details_table.setStyle(TableStyle(table_style))
        elements.append(details_table)
    
    # Build PDF with custom canvas
    doc.build(elements, canvasmaker=HeaderCanvas)
    buffer.seek(0)
    return buffer

