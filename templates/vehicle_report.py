from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime, os
from controllers.load_assets import *

class VehicleReport:
    def __init__(self):
        pass
    
    def generate_vehicle_pdf_report_updated(self, row_data):
        """
        Generates a one-page, sectioned PDF report for a vehicle record with 0.5-inch margins,
        full-width left-aligned tables, and minimal spacing between sections.
        The PDF is saved to the user's Downloads directory.
        
        Parameters:
        row_data (dict): Dictionary containing vehicle data.
        """
        # Determine Downloads folder and generate a unique filename
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(downloads_path, f"vehicle_report_{timestamp}.pdf")

        # Create document with 0.5-inch margins on all sides
        margin = 0.5 * inch
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            leftMargin=margin,
            rightMargin=margin,
            topMargin=margin,
            bottomMargin=margin
        )

        # Calculate the available width for content
        content_width = letter[0] - 2 * margin

        styles = getSampleStyleSheet()
        # Adjust header style (keep centered header items)
        header_style = ParagraphStyle(
            name='HeaderStyle',
            parent=styles['Heading1'],
            alignment=1,  # center for header title if needed
            fontSize=20,
            textColor=colors.HexColor('#007BFF'),
            spaceAfter=6
        )
        # Section (table) headings: left aligned
        subheader_style = ParagraphStyle(
            name='SubHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            alignment=0,  # left aligned
            spaceAfter=3
        )
        normal_style = styles['Normal']

        elements = []

        #*******************************************************************************************************************************
        # --- Header Section ---
        logo_path = get_asset_path('assets/images/tank.png')
        try:
            logo = Image(logo_path, width=1*inch, height=1*inch)
        except Exception:
            logo = Paragraph("Logo", normal_style)
        
        org_info = Paragraph(
            "44 AK HAT Battalion, Pakistan Army<br/><b>Vehicle Maintenance Report</b>",
            normal_style
        )

        report_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        date_para = Paragraph(
            f"Report Date: {report_date}",
            ParagraphStyle('date', parent=normal_style, alignment=2, fontSize=10, textColor=colors.gray)
        )
        
        # Header table: Use fixed colWidths that add up to the available content_width
        header_table = Table([[logo, org_info, date_para]], 
                            colWidths=[1.2*inch, content_width - (1.2*inch + 1.8*inch), 1.8*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (2,0), (2,0), 'RIGHT'),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.gray),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))  # minimal space

        #*******************************************************************************************************************************

        # --- Section: Basic Details (4-column table) ---
        elements.append(Paragraph("Basic Details", subheader_style))
        basic_details_data = [
            ['Category', 'BA No.', 'Make Type', 'Engine No.'],
            [
                row_data.get('Category', ''),
                row_data.get('BA No.', ''),
                row_data.get('Make Type', ''),
                row_data.get('Engine No.', '')
            ]
        ]
        num_cols = 4
        basic_table = Table(basic_details_data, colWidths=[content_width/num_cols]*num_cols)
        basic_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(basic_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Oil Filter (4-column table) ---
        elements.append(Paragraph("Oil Filter", subheader_style))
        oil_filter_data = [
            ['Issue Date', 'Due Date', 'Current Mileage', 'Due Mileage'],
            [
                row_data.get('Issue Date (Oil Filter)', ''),
                row_data.get('Due Date (Oil Filter)', ''),
                row_data.get('Current Mileage (Oil Filter)', ''),
                row_data.get('Due Mileage (Oil Filter)', '')
            ]
        ]
        num_cols = 4
        oil_table = Table(oil_filter_data, colWidths=[content_width/num_cols]*num_cols)
        oil_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(oil_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Fuel Filter (4-column table) ---
        elements.append(Paragraph("Fuel Filter", subheader_style))
        fuel_filter_data = [
            ['Issue Date', 'Due Date', 'Current Mileage', 'Due Mileage'],
            [
                row_data.get('Issue Date (Fuel Filter)', ''),
                row_data.get('Due Date (Fuel Filter)', ''),
                row_data.get('Current Mileage (Fuel Filter)', ''),
                row_data.get('Due Mileage (Fuel Filter)', '')
            ]
        ]
        num_cols = 4
        fuel_table = Table(fuel_filter_data, colWidths=[content_width/num_cols]*num_cols)
        fuel_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(fuel_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Air Filter (4-column table) ---
        elements.append(Paragraph("Air Filter", subheader_style))
        air_filter_data = [
            ['Issue Date', 'Due Date', 'Current Mileage', 'Due Mileage'],
            [
                row_data.get('Issue Date (Air Filter)', ''),
                row_data.get('Due Date (Air Filter)', ''),
                row_data.get('Current Mileage (Air Filter)', ''),
                row_data.get('Due Mileage (Air Filter)', '')
            ]
        ]
        num_cols = 4
        air_table = Table(air_filter_data, colWidths=[content_width/num_cols]*num_cols)
        air_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(air_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Transmission Filter (4-column table) ---
        elements.append(Paragraph("Transmission Filter", subheader_style))
        trans_filter_data = [
            ['Issue Date', 'Due Date', 'Current Mileage', 'Due Mileage'],
            [
                row_data.get('Issue Date (Transmission Filter)', ''),
                row_data.get('Due Date (Transmission Filter)', ''),
                row_data.get('Current Mileage (Transmission Filter)', ''),
                row_data.get('Due Mileage (Transmission Filter)', '')
            ]
        ]
        num_cols = 4
        trans_table = Table(trans_filter_data, colWidths=[content_width/num_cols]*num_cols)
        trans_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(trans_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Differential Oil (4-column table) ---
        elements.append(Paragraph("Differential Oil", subheader_style))
        diff_oil_data = [
            ['Issue Date', 'Due Date', 'Current Mileage', 'Due Mileage'],
            [
                row_data.get('Issue Date (Differential Oil)', ''),
                row_data.get('Due Date (Differential Oil)', ''),
                row_data.get('Current Mileage (Differential Oil)', ''),
                row_data.get('Due Mileage (Differential Oil)', '')
            ]
        ]
        num_cols = 4
        diff_table = Table(diff_oil_data, colWidths=[content_width/num_cols]*num_cols)
        diff_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(diff_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Battery Details (2-column table) ---
        elements.append(Paragraph("Battery Details", subheader_style))
        battery_data = [
            ['Issue Date', 'Due Date'],
            [
                row_data.get('Issue Date (Battery)', ''),
                row_data.get('Issue Date (Battery)', '')
            ]
        ]
        num_cols = 2
        battery_table = Table(battery_data, colWidths=[content_width/num_cols]*num_cols)
        battery_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(battery_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Flushing Details (4-column table) ---
        elements.append(Paragraph("Flushing Details", subheader_style))
        flushing_data = [
            ['Issue Date', 'Due Date', 'Fuel Tank Flush', 'Radiator Flush'],
            [
                row_data.get('Issue Date (Flushing)', ''),
                row_data.get('Due Date (Flushing)', ''),
                row_data.get('Fuel Tank Flush', ''),
                row_data.get('Radiator Flush', '')
            ]
        ]
        num_cols = 4
        flushing_table = Table(flushing_data, colWidths=[content_width/num_cols]*num_cols)
        flushing_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(flushing_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Greasing Details (5-column table) ---
        elements.append(Paragraph("Greasing Details", subheader_style))
        greasing_data = [
            ['Issue Date', 'Due Date', 'TRS and Suspension', 'Engine Part', 'Steering Lever Pts'],
            [
                row_data.get('Issue Date (Greasing)', ''),
                row_data.get('Due Date (Greasing)', ''),
                row_data.get('TRS and Suspension', ''),
                row_data.get('Engine Part', ''),
                row_data.get('Steering Lever Pts', '')
            ]
        ]
        num_cols = 5
        greasing_table = Table(greasing_data, colWidths=[content_width/num_cols]*num_cols)
        greasing_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(greasing_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: General Maintenance (7-column table) ---
        elements.append(Paragraph("General Maintenance", subheader_style))
        maintenance_data = [
            ['Wash', 'Oil Level Check', 'Lubrication of Parts', 'Air Cleaner'],
            [
                row_data.get('Wash', ''),
                row_data.get('Oil Level Check', ''),
                row_data.get('Lubrication of Parts', ''),
                row_data.get('Air Cleaner', '')
            ]
        ]
        num_cols = 4
        maintenance_table = Table(maintenance_data, colWidths=[content_width/num_cols]*num_cols)
        maintenance_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(maintenance_table)
        # elements.append(Spacer(1, 0.1*inch))

        #*****************************************

        # elements.append(Paragraph("General Maintenance", subheader_style))
        maintenance_data = [
            ['Fuel Filter', 'French Chalk', 'TR Adjustment'],
            [
                row_data.get('Fuel Filter', ''),
                row_data.get('French Chalk', ''),
                row_data.get('TR Adjustment', '')
            ]
        ]
        num_cols = 3
        maintenance_table = Table(maintenance_data, colWidths=[content_width/num_cols]*num_cols)
        maintenance_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(maintenance_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Overhaul Details (3-column table) ---
        elements.append(Paragraph("Overhaul Details", subheader_style))
        overhaul_data = [
            ['Current Milage (Overhaul)', 'Due Milage (Overhaul)', 'Remarks/Status'],
            [
                row_data.get('Current Milage (Overhaul)', ''),
                row_data.get('Due Milage (Overhaul)', ''),
                row_data.get('Status', '')
            ]
        ]
        num_cols = 3
        overhaul_table = Table(overhaul_data, colWidths=[content_width/num_cols]*num_cols)
        overhaul_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(overhaul_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Final Details (Created By and Created At) ---
        # final_details_data = [
        #     ['Created By', 'Created At'],
        #     [
        #         row_data.get('Created By', ''),
        #         row_data.get('Created At', '')
        #     ]
        # ]
        # num_cols = 2
        # final_table = Table(final_details_data, colWidths=[content_width/num_cols]*num_cols)
        # final_table.setStyle(TableStyle([
        #     ('BOX', (0,0), (-1,-1), 1, colors.black),
        #     ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
        #     ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        #     ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        # ]))
        # elements.append(final_table)

        #*******************************************************************************************************************************

        # --- Page Number Footer ---
        def add_page_number(canvas, doc):
            canvas.setFont("Helvetica", 9)
            page_num = canvas.getPageNumber()
            canvas.drawRightString(content_width + margin - 10, 10, f"Page {page_num}")

        # Build the PDF document
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

        # Show flash message (if using PyQt)
        try:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Report saved successfully to Downloads")
            msg.setWindowTitle("Report Generated")
            msg.exec_()
        except Exception:
            print("Report saved successfully to Downloads")
