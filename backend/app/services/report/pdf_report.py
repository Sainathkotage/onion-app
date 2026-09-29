import os
from pathlib import Path
from typing import Dict, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from app.config import BASE_DIR, UPLOAD_DIR

REPORTS_DIR = UPLOAD_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class PDFReportGenerator:
    """
    Generates downloadable PDF Quality Reports using ReportLab.
    """
    @staticmethod
    def generate_pdf(
        grading_data: Dict,
        classifications: List[Dict],
        annotated_image_url: str,
        upload_id: str
    ) -> str:
        pdf_filename = f"report_{upload_id}.pdf"
        pdf_path = REPORTS_DIR / pdf_filename

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Palette & Styles
        primary_color = colors.HexColor('#065f46')   # Emerald 800
        secondary_color = colors.HexColor('#d97706') # Amber 600
        dark_text = colors.HexColor('#0f172a')       # Slate 900
        light_bg = colors.HexColor('#f8fafc')        # Slate 50

        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=primary_color,
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#475569'),
            spaceAfter=12
        )

        heading2_style = ParagraphStyle(
            'Heading2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            textColor=primary_color,
            spaceBefore=8,
            spaceAfter=6
        )

        normal_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=dark_text,
            leading=12
        )

        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=colors.white,
            alignment=1
        )

        table_cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=dark_text,
            alignment=1
        )

        elements = []

        # Header Title
        elements.append(Paragraph("ONION QUALITY ASSESSMENT REPORT", title_style))
        elements.append(Paragraph("Procurement Center Automated AI Grading Certificate • Problem ID: 26031", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceAfter=12))

        # Batch Info Table
        batch_info_data = [
            [
                Paragraph(f"<b>Batch ID:</b> {grading_data['batch_id']}", normal_style),
                Paragraph(f"<b>Assessment Date:</b> {grading_data['timestamp']}", normal_style),
            ],
            [
                Paragraph(f"<b>Total Onions Analyzed:</b> {grading_data['total_onions']}", normal_style),
                Paragraph(f"<b>Recommendation:</b> <font color='{primary_color.hexval()}'><b>{grading_data['recommendation']}</b></font>", normal_style),
            ]
        ]
        info_table = Table(batch_info_data, colWidths=[270, 270])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), light_bg),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 12))

        # Key Executive Metrics Cards
        elements.append(Paragraph("Grading Overview Summary", heading2_style))
        grade_a_pct = grading_data['grade_a']['percentage']
        urs_pct = grading_data['urs']['percentage']

        summary_data = [
            [
                Paragraph("<b>Grade A (Healthy) Rate</b>", table_header_style),
                Paragraph("<b>URS (Defect / Rejected) Rate</b>", table_header_style)
            ],
            [
                Paragraph(f"<font size=16 color='#065f46'><b>{grade_a_pct}%</b></font><br/>({grading_data['grade_a']['count']} onions)", table_cell_style),
                Paragraph(f"<font size=16 color='#dc2626'><b>{urs_pct}%</b></font><br/>({grading_data['urs']['count']} onions)", table_cell_style)
            ]
        ]
        summary_table = Table(summary_data, colWidths=[270, 270])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), primary_color),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#991b1b')),
            ('BACKGROUND', (0, 1), (-1, 1), light_bg),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 14))

        # Defect Breakdown Table
        elements.append(Paragraph("Detailed Defect Category Breakdown", heading2_style))
        bd = grading_data['breakdown']
        breakdown_table_data = [
            [
                Paragraph("Quality / Defect Class", table_header_style),
                Paragraph("Count", table_header_style),
                Paragraph("Percentage", table_header_style),
                Paragraph("Classification Status", table_header_style),
            ],
            [Paragraph("Healthy / Grade A", normal_style), Paragraph(str(bd['healthy']['count']), table_cell_style), Paragraph(f"{bd['healthy']['percentage']}%", table_cell_style), Paragraph("<font color='#065f46'><b>Passed (Grade A)</b></font>", table_cell_style)],
            [Paragraph("Damaged (Cuts / Cracks)", normal_style), Paragraph(str(bd['damaged']['count']), table_cell_style), Paragraph(f"{bd['damaged']['percentage']}%", table_cell_style), Paragraph("<font color='#d97706'>Defective (URS)</font>", table_cell_style)],
            [Paragraph("Rotten (Decay / Fungal)", normal_style), Paragraph(str(bd['rotten']['count']), table_cell_style), Paragraph(f"{bd['rotten']['percentage']}%", table_cell_style), Paragraph("<font color='#dc2626'>Defective (URS)</font>", table_cell_style)],
            [Paragraph("Sprouted (Green Shoots)", normal_style), Paragraph(str(bd['sprouted']['count']), table_cell_style), Paragraph(f"{bd['sprouted']['percentage']}%", table_cell_style), Paragraph("<font color='#65a30d'>Defective (URS)</font>", table_cell_style)],
            [Paragraph("Undersized (<65% Median)", normal_style), Paragraph(str(bd['undersized']['count']), table_cell_style), Paragraph(f"{bd['undersized']['percentage']}%", table_cell_style), Paragraph("<font color='#7c3aed'>Defective (URS)</font>", table_cell_style)],
            [Paragraph("<b>Total Batch</b>", normal_style), Paragraph(f"<b>{grading_data['total_onions']}</b>", table_cell_style), Paragraph("<b>100.0%</b>", table_cell_style), Paragraph("<b>Evaluated</b>", table_cell_style)],
        ]

        bd_table = Table(breakdown_table_data, colWidths=[180, 100, 120, 140])
        bd_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e2e8f0')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(bd_table)
        elements.append(Spacer(1, 14))

        # Visual Evidence Section
        elements.append(Paragraph("Visual Evidence & Computer Vision Detection", heading2_style))
        ann_path = BASE_DIR / annotated_image_url.lstrip("/")
        if not ann_path.exists():
            ann_path = UPLOAD_DIR / Path(annotated_image_url).name

        if ann_path.exists():
            try:
                # Add resized image to fit report width nicely
                img = RLImage(str(ann_path), width=480, height=270)
                elements.append(img)
            except Exception as e:
                elements.append(Paragraph(f"Annotated image file located at: {annotated_image_url}", normal_style))
        
        elements.append(Spacer(1, 14))

        # Flagged Defective Thumbnails
        flagged_onions = [item for item in classifications if item.get("is_defective", False)]
        if flagged_onions:
            elements.append(Paragraph(f"Flagged Defective Onion Samples ({len(flagged_onions)} flagged)", heading2_style))
            flagged_rows = []
            for item in flagged_onions[:6]:  # Show up to 6 flagged samples
                crop_rel = item.get("crop_path", "")
                crop_abs = BASE_DIR / crop_rel.lstrip("/")
                if not crop_abs.exists():
                    crop_abs = UPLOAD_DIR / "crops" / Path(crop_rel).name

                label_p = Paragraph(f"<b>{item.get('label')}</b><br/>Class: <b>{item.get('class_label')}</b><br/>{item.get('defect_reason', '')}", normal_style)
                
                if crop_abs.exists():
                    try:
                        crop_img = RLImage(str(crop_abs), width=65, height=65)
                        flagged_rows.append([crop_img, label_p])
                    except Exception:
                        flagged_rows.append([Paragraph("No Image", normal_style), label_p])
                else:
                    flagged_rows.append([Paragraph("No Image", normal_style), label_p])

            if flagged_rows:
                # Format into 2-column table
                grid_cells = []
                for i in range(0, len(flagged_rows), 2):
                    row1 = flagged_rows[i]
                    if i + 1 < len(flagged_rows):
                        row2 = flagged_rows[i+1]
                        grid_cells.append([row1[0], row1[1], row2[0], row2[1]])
                    else:
                        grid_cells.append([row1[0], row1[1], Paragraph("", normal_style), Paragraph("", normal_style)])
                
                flagged_table = Table(grid_cells, colWidths=[75, 195, 75, 195])
                flagged_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), light_bg),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('PADDING', (0, 0), (-1, -1), 5),
                ]))
                elements.append(flagged_table)

        elements.append(Spacer(1, 16))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=8))
        elements.append(Paragraph(
            "<b>Notice:</b> This report was generated automatically by the OnionIQ Computer Vision & ML Procurement Quality Assessor Prototype. Results are intended for rapid procurement center decision support.",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#64748b'), alignment=1)
        ))

        doc.build(elements)
        return f"/uploads/reports/{pdf_filename}"
