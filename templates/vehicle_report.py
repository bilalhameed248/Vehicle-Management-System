from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime, os

class VehicleReport:
    def __init__(self):
        pass
    def generate_vehicle_pdf_report(self, row_data, filename):
        """
        Generates a one-page PDF report for a vehicle record.
        
        Parameters:
        row_data (dict): A dictionary containing all the vehicle record fields.
        filename (str): The output PDF file path.
        """

        # Create a document with 1-inch margins on all sides
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            leftMargin=inch,
            rightMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )

        styles = getSampleStyleSheet()
        # Custom styles for the report
        title_style = ParagraphStyle(
            name='Title',
            parent=styles['Heading1'],
            alignment=1,
            fontSize=20,
            spaceAfter=20,
            textColor=colors.HexColor('#007BFF')
        )
        org_style = ParagraphStyle(
            name='Org',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=10
        )
        date_style = ParagraphStyle(
            name='Date',
            parent=styles['Normal'],
            fontSize=10,
            alignment=2,  # right aligned
            textColor=colors.gray
        )

        elements = []

        # --- Header: Organization Logo, Info, and Report Date ---
        logo_path = 'assets/images/tank.png'
        try:
            logo = Image(logo_path, width=1*inch, height=1*inch)
        except Exception:
            # Fallback if logo is not found
            logo = Paragraph("Logo", styles['Normal'])
        
        # Organization information (improved English)
        org_info = Paragraph("44 AK HAT Battalion, Pakistan Army<br/><b>Vehicle Maintenance Report</b>", org_style)
        # Report date (displayed on the right)
        report_date = datetime.datetime.now().strftime("%B %d, %Y")
        date_para = Paragraph(f"Report Date: {report_date}", date_style)
        
        # Arrange header items in a table (logo on left, org info center, date on right)
        header_data = [[logo, org_info, date_para]]
        header_table = Table(header_data, colWidths=[1.2*inch, 4*inch, 1.8*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (2,0), (2,0), 'RIGHT'),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.gray)
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.2*inch))

        # --- Title ---
        title = Paragraph("Vehicle Maintenance Detailed Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))

        # --- Vehicle Data Section ---
        # Create a two-column table (Field, Value) for the row data
        table_data = []
        for key, value in row_data.items():
            table_data.append([Paragraph(f"<b>{key}</b>", styles['Normal']),
                            Paragraph(str(value), styles['Normal'])])
        
        data_table = Table(table_data, colWidths=[2.5*inch, 4.5*inch])
        data_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica')
        ]))
        elements.append(data_table)

        # --- Page Number Footer ---
        def add_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            canvas.setFont("Helvetica", 9)
            # Draw page number at the bottom right
            canvas.drawRightString(letter[0] - inch, 0.75 * inch, f"Page {page_num}")

        # Build the PDF
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)


    def generate_vehicle_pdf_report_updated(self, row_data):
        """
        Generates a one-page PDF report for a vehicle record with multiple sections,
        saves it in the user's Downloads directory, and shows a flash message.

        Parameters:
        row_data (dict): Dictionary containing vehicle data.
        """

        # Determine Downloads folder and generate a unique filename
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(downloads_path, f"vehicle_report_{timestamp}.pdf")

        # Create document with 1-inch margins on all sides
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            leftMargin=inch,
            rightMargin=inch,
            topMargin=inch,
            bottomMargin=inch
        )

        styles = getSampleStyleSheet()
        # Define custom styles
        header_style = ParagraphStyle(
            name='HeaderStyle',
            parent=styles['Heading1'],
            alignment=1,
            fontSize=20,
            textColor=colors.HexColor('#007BFF'),
            spaceAfter=12
        )
        subheader_style = ParagraphStyle(
            name='SubHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6
        )
        normal_style = styles['Normal']

        elements = []

        #***************************************************************************************************************************************

        # --- Header Section ---

        # Organization logo (top left)
        logo_path = 'assets/images/tank.png'
        try:
            logo = Image(logo_path, width=1*inch, height=1*inch)
        except Exception:
            logo = Paragraph("Logo", normal_style)
        
        # Organization information (center)
        org_info = Paragraph(
            "44 AK HAT Battalion, Pakistan Army<br/><b>Vehicle Maintenance Report</b>",
            normal_style
        )
        # Report date (top right)
        report_date = datetime.datetime.now().strftime("%B %d, %Y")
        date_para = Paragraph(
            f"Report Date: {report_date}",
            ParagraphStyle('date', parent=normal_style, alignment=2, fontSize=10, textColor=colors.gray)
        )
        # Arrange header items in a table
        header_table_data = [[logo, org_info, date_para]]
        header_table = Table(header_table_data, colWidths=[1.2*inch, 4*inch, 1.8*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (2,0), (2,0), 'RIGHT'),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.gray),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

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
        basic_table = Table(basic_details_data, colWidths=[1.5*inch]*4)
        basic_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(basic_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

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
        oil_table = Table(oil_filter_data, colWidths=[1.5*inch]*4)
        oil_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(oil_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

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
        fuel_table = Table(fuel_filter_data, colWidths=[1.5*inch]*4)
        fuel_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(fuel_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

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
        air_table = Table(air_filter_data, colWidths=[1.5*inch]*4)
        air_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(air_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

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
        trans_table = Table(trans_filter_data, colWidths=[1.5*inch]*4)
        trans_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(trans_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

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
        diff_table = Table(diff_oil_data, colWidths=[1.5*inch]*4)
        diff_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(diff_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

        # --- Section: Battery Details (2-column table) ---
        elements.append(Paragraph("Battery Details", subheader_style))
        battery_data = [
            ['Battery Issue Date', 'Battery Due Date'],
            [
                row_data.get('Battery Issue Date', ''),
                row_data.get('Battery Due Date', '')
            ]
        ]
        battery_table = Table(battery_data, colWidths=[2*inch]*2)
        battery_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(battery_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

        # --- Section: Flushing Details (4-column table) ---
        elements.append(Paragraph("Flushing Details", subheader_style))
        flushing_data = [
            ['Flushing Issue Date', 'Flushing Due Date', 'Fuel Tank Flush', 'Radiator Flush'],
            [
                row_data.get('Flushing Issue Date', ''),
                row_data.get('Flushing Due Date', ''),
                row_data.get('Fuel Tank Flush', ''),
                row_data.get('Radiator Flush', '')
            ]
        ]
        flushing_table = Table(flushing_data, colWidths=[1.5*inch]*4)
        flushing_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(flushing_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

        # --- Section: Greasing Details (5-column table) ---
        elements.append(Paragraph("Greasing Details", subheader_style))
        greasing_data = [
            ['Greasing Issue Date', 'Greasing Due Date', 'TRS and Suspension', 'Engine Part', 'Steering Lever Pts'],
            [
                row_data.get('Greasing Issue Date', ''),
                row_data.get('Greasing Due Date', ''),
                row_data.get('TRS and Suspension', ''),
                row_data.get('Engine Part', ''),
                row_data.get('Steering Lever Pts', '')
            ]
        ]
        greasing_table = Table(greasing_data, colWidths=[1.2*inch]*5)
        greasing_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(greasing_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

        # --- Section: General Maintenance (7-column table) ---
        elements.append(Paragraph("General Maintenance", subheader_style))
        maintenance_data = [
            ['Wash', 'Oil Level Check', 'Lubrication of Parts', 'Air Cleaner', 'Fuel Filter', 'French Chalk', 'TR Adjustment'],
            [
                row_data.get('Wash', ''),
                row_data.get('Oil Level Check', ''),
                row_data.get('Lubrication of Parts', ''),
                row_data.get('Air Cleaner', ''),
                row_data.get('Fuel Filter', ''),
                row_data.get('French Chalk', ''),
                row_data.get('TR Adjustment', '')
            ]
        ]
        maintenance_table = Table(maintenance_data, colWidths=[1.0*inch]*7)
        maintenance_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(maintenance_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

        # --- Section: Overhaul Details (3-column table) ---
        elements.append(Paragraph("Overhaul Details", subheader_style))
        overhaul_data = [
            ['Current Milage (Overhaul)', 'Due Milage (Overhaul)', 'Remarks'],
            [
                row_data.get('Current Milage (Overhaul)', ''),
                row_data.get('Due Milage  (Overhaul)', ''),
                row_data.get('Remarks', '')
            ]
        ]
        overhaul_table = Table(overhaul_data, colWidths=[2*inch, 2*inch, 3*inch])
        overhaul_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(overhaul_table)
        elements.append(Spacer(1, 0.2*inch))

        #***************************************************************************************************************************************

        # --- Section: Final Details (Created By and Created At) ---
        final_details_data = [
            ['Created By', 'Created At'],
            [
                row_data.get('Created By', ''),
                row_data.get('Created At', '')
            ]
        ]
        final_table = Table(final_details_data, colWidths=[3*inch, 3*inch])
        final_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(final_table)

        #***************************************************************************************************************************************

        # --- Page Number Footer ---
        def add_page_number(canvas, doc):
            canvas.setFont("Helvetica", 9)
            page_num = canvas.getPageNumber()
            canvas.drawRightString(letter[0]-inch, 0.75*inch, f"Page {page_num}")

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
