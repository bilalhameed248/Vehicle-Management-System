from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import datetime, os
from controllers.load_assets import *

class WeaponReport:
    def __init__(self):
        pass
    
    def generate_weapons_pdf_report_updated(self, row_data):
        """
        Generates a one-page, sectioned PDF report for a weapon record with 0.5-inch margins,
        full-width left-aligned tables, and minimal spacing between sections.
        The PDF is saved to the user's Downloads directory.
        
        Parameters:
        row_data (dict): Dictionary containing weapon data.
        """
        # Determine Downloads folder and generate a unique filename
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(downloads_path, f"weapon_report_{timestamp}.pdf")

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
            spaceAfter=2
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
            "44 AK HAT Battalion, Pakistan Army<br/><b>Weapon Maintenance Report</b>",
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

        # --- Section: Basic Details (1-column table) ---
        elements.append(Paragraph("Basic Details", subheader_style))
        basic_details_data = [
            ['Wpn No'],
            [
                row_data.get('Wpn No', '')
            ]
        ]
        num_cols = 1
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

        # --- Section: T.Pod (7-column table) ---
        elements.append(Paragraph("T.Pod", subheader_style))
        T_Pod_data = [
            [ "Leg lock \nhandle", "Anchor \nclaw", "Leveling \nBubbles", "Lubrication", "Pull \ntube", "Detent \nstop lever", "Foot pad/ \nlegs body \ncondition"],
            [
                row_data.get('Leg lock handle', ''),
                row_data.get('Anchor claw', ''),
                row_data.get('Leveling Bubbles', ''),
                row_data.get('Lubrication', ''),
                row_data.get('Pull tube', ''),
                row_data.get('Detent stop lever', ''),
                row_data.get('Foot pad/ legs body condition', '')
            ]
        ]
        num_cols = 7
        T_Pod_table = Table(T_Pod_data, colWidths=[content_width/num_cols]*num_cols)
        T_Pod_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(T_Pod_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: T. Unit (4-column table) ---
        elements.append(Paragraph("T. Unit", subheader_style))
        T_Unit_data = [
            [ "Traversing \nLock", "Elevation \nlock \ncheck", "Elevation \nlock \nhandle", "Viscosity of \nViscos \ndamper", "Azimuth \nlock \ncheck", "Lubrication", "Protective \ncover", "Coil \nCard"],
            [
                row_data.get('Traversing Lock', ''),
                row_data.get('Elevation lock check', ''),
                row_data.get('Elevation lock handle', ''),
                row_data.get('Viscosity of Viscos damper', ''),
                row_data.get('Azimuth lock check', ''),
                row_data.get('Lubrication', ''),
                row_data.get('Protective cover', ''),
                row_data.get('Coil Card', '')
            ]
        ]
        num_cols = 8
        T_Unit_table = Table(T_Unit_data, colWidths=[content_width/num_cols]*num_cols)
        T_Unit_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(T_Unit_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: OS (11-column table) ---
        elements.append(Paragraph("OS", subheader_style))
        OS_data = [
            [ "Eye Shield", "Focusing knob", "Sillica gel \ncondition", "Reticle lamp", "Body condition", "N2 purg / filling \nconnection"],
            [
                row_data.get('Eye Shield', ''),
                row_data.get('Focusing knob', ''),
                row_data.get('Sillica gel condition', ''),
                row_data.get('Reticle lamp', ''),
                row_data.get('Body condition', ''),
                row_data.get('N2 purg / filling connection', ''),
            ]
        ]
        num_cols = 6
        OS_table = Table(OS_data, colWidths=[content_width/num_cols]*num_cols)
        OS_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(OS_table)

        OS_data = [
            [ "Reticle switch", "Cable connector" , "Locking device", "Lens cover", "Objective lens" ],
            [
                row_data.get('Reticle switch', ''),
                row_data.get('Cable connector', ''),
                row_data.get('Locking device', ''),
                row_data.get('Lens cover', ''),
                row_data.get('Objective lens', '')
            ]
        ]
        num_cols = 5
        OS_table = Table(OS_data, colWidths=[content_width/num_cols]*num_cols)
        OS_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(OS_table)
        elements.append(Spacer(1, 0.1*inch))


        #*******************************************************************************************************************************

        # --- Section: DMGS (7-column table) ---
        elements.append(Paragraph("DMGS", subheader_style))
        DMGS_data = [
            [ "Meter indicator \n(AZ & Elev)", "Sockets", "MGS/ DMGS \ncase", "Protective \ncover", "Cable", "Bty \nconnector", "Self/ test"],
            [
                row_data.get('Meter indicator (AZ & Elev))', ''),
                row_data.get('Sockets', ''),
                row_data.get('MGS/ DMGS case', ''),
                row_data.get('Protective cover', ''),
                row_data.get('Cable', ''),
                row_data.get('Bty connector', ''),
                row_data.get('Self/ test', '')
            ]
        ]
        num_cols = 7
        DMGS_table = Table(DMGS_data, colWidths=[content_width/num_cols]*num_cols)
        DMGS_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(DMGS_table)
        elements.append(Spacer(1, 0.1*inch))
        #*******************************************************************************************************************************

        # --- Section: Differential Oil (4-column table) ---
        L_Tube_Title = Paragraph("L-Tube", subheader_style)
        L_Tube_data = [
            [ "Body \nCondition" ],
            [
                row_data.get('Body Condition', '')
            ]
        ]
        num_cols = 1
        L_Tube_table = Table(L_Tube_data, colWidths=[(content_width * 0.2)])
        # L_Tube_table = Table(L_Tube_data, colWidths=[content_width/num_cols]*num_cols)
        L_Tube_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))

        #*******************************************************************************************************************************

        # --- Section: TVPC (6-column table) ---
        TVPC_Title = Paragraph("TVPC", subheader_style)
        TVPC_data = [
            [ "Body \nCondition", "Fly \nNet", "On/Off \nSwitch", "Indicator \nIt", "Connector", "Voltage" ],
            [
                row_data.get('Body Condition', ''),
                row_data.get('Fly Net', ''),
                row_data.get('On/Off Switch', ''),
                row_data.get('Indicator It', ''),
                row_data.get('Connector', ''),
                row_data.get('Voltage', '')
            ]
        ]
        num_cols_TVPC = 6
        TVPC_table = Table(TVPC_data, colWidths=[(content_width*0.8)/num_cols_TVPC]*num_cols_TVPC)
        TVPC_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))

        combined_table = Table([
            [[L_Tube_Title, L_Tube_table], [TVPC_Title, TVPC_table]]  # Titles and tables in one row
        ], colWidths=[content_width * 0.2, content_width * 0.8])  # L-Tube gets 30%, TVPC gets 70%

        combined_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),  # Align content to the top
            ('ALIGN', (0,0), (-1,-1), 'CENTER')  # Center align the inner tables
        ]))

        # Append the combined table to elements
        elements.append(combined_table)
        elements.append(Spacer(1, 0.1*inch))

        elements.append(PageBreak())  # Adds a page break
        #*******************************************************************************************************************************

        # --- Section: Bty BB-287 (7-column table) ---
        elements.append(Paragraph("Bty BB-287", subheader_style))
        Bty_BB_287_data = [
            [ "Bty \nconnector", "Voltage \n+24 V \nsec", "Voltage \n+50 V", "Voltage \n+50 V \nsec", "Bty \ncondition", "Tvpc", "Power \ncable \ncondition" ],
            [
                row_data.get('Bty connector', ''),
                row_data.get('Voltage +24 V sec', ''),
                row_data.get('Voltage +50 V', ''),
                row_data.get('Voltage +50 V sec', ''),
                row_data.get('Bty condition', ''),
                row_data.get('Tvpc', ''),
                row_data.get('Power cable condition', '')
            ]
        ]
        num_cols = 7
        Bty_BB_287_table = Table(Bty_BB_287_data, colWidths=[content_width/num_cols]*num_cols)
        Bty_BB_287_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(Bty_BB_287_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: NVS (5-column table) ---
        elements.append(Paragraph("NVS", subheader_style))
        NVS_data = [
            [ "Coolant unit", "Eye piece", "Cable connector", "Lens assy", "Power cable condition"],
            [
                row_data.get('Coolant unit', ''),
                row_data.get('Eye piece"', ''),
                row_data.get('Cable connector', ''),
                row_data.get('Lens assy', ''),
                row_data.get('Power cable condition', '')
            ]
        ]
        num_cols = 5
        NVS_table = Table(NVS_data, colWidths=[content_width/num_cols]*num_cols)
        NVS_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(NVS_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: BPC (5-column table) ---
        BPC_title = Paragraph("BPC", subheader_style)
        BPC_data = [
            ["Body", "Cables", "On/Off \nSwitch"],
            [
                row_data.get('Body', ''),
                row_data.get('Cables', ''),
                row_data.get('On/Off Switch', '')
            ]
        ]
        num_cols_BPC = 3
        
        BPC_table = Table(BPC_data, colWidths=[(content_width*0.4)/num_cols_BPC]*num_cols_BPC)
        BPC_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))

        #*******************************************************************************************************************************

        # --- Section: Greasing Details (5-column table) ---
        VPC_title = Paragraph("VPC", subheader_style)
        VPC_data = [
            ["Body", "Switch", "VPC Power \nCable"],
            [
                row_data.get('Body', ''),
                row_data.get('Switch', ''),
                row_data.get('VPC Power Cable', '')
            ]
        ]
        VPC_num_cols = 3
        VPC_table = Table(VPC_data, colWidths=[(content_width*0.4)/VPC_num_cols]*VPC_num_cols)
        VPC_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))

        #*******************************************************************************************************************************

        # --- Section: L.Bty (1-column table) ---
        L_Tube_Title = Paragraph("L.Bty", subheader_style)
        L_Bty_data = [
            ["Bty \nVoltage"],
            [
                row_data.get('Bty Voltage', '')
            ]
        ]
        num_cols = 1
        L_Bty_table = Table(L_Bty_data, colWidths=[(content_width * 0.2)])
        L_Bty_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))

        combined_table = Table([
            [[BPC_title, BPC_table], [VPC_title, VPC_table], [L_Tube_Title, L_Bty_table]]  # Titles and tables in the same row
        ], colWidths=[content_width * 0.4, content_width * 0.4, content_width * 0.2])  # Leave some space for margins

        combined_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),  # Align content to the top
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),  # Center align the inner tables
        ]))

        elements.append(combined_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Doc (9-column table) ---
        elements.append(Paragraph("Doc", subheader_style))
        Doc_data = [
            [ "6 Monthly \nverification \nrecord", "Last ATI \npts has \nbeen killed", "Bty charging \nrecord", "Storage temp & \nHumidity record", "Firing \nrecord \ncheck", "Svc ability \n& Completeness\n of tools & accy", ],
            [
                row_data.get('6 Monthly verification record', ''),
                row_data.get('Last ATI pts has been killed', ''),
                row_data.get('Bty charging record', ''),
                row_data.get('Storage temp & Humidity record', ''),
                row_data.get('Firing record check', ''),
                row_data.get('Svc ability & Completeness of tools & accy', '')
            ]
        ]
        num_cols = 6
        Doc_table = Table(Doc_data, colWidths=[content_width/num_cols]*num_cols)
        Doc_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(Doc_table)

        Doc_data = [
            [ "Self test \nrecord check", "Is eARMS fully \nfunc and all \nthe processes involved \nare being carried \nout through eARMS", "Complete eqpt \ninventory update \non eARMS", "DRWO/ work \norder being \nprocessed on \neARMS", "Are Log \nbook maintain \nproperly"],
            [
                row_data.get('Self test record check', ''),
                row_data.get('Is eARMS fully func and all the processes involved are being carried out through eARMS', ''),
                row_data.get('Complete eqpt inventory update on eARMS', ''),
                row_data.get('DRWO/ work order being processed on eARMS', ''),
                row_data.get('Are Log book maintain properly', '')
            ]
        ]
        num_cols = 5
        Doc_table = Table(Doc_data, colWidths=[content_width/num_cols]*num_cols)
        Doc_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(Doc_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Overhaul Details (3-column table) ---
        elements.append(Paragraph("Status", subheader_style))
        Status_data = [
            ["Status"],
            [
                row_data.get('Status', '')
            ]
        ]
        num_cols = 1
        overhaul_table = Table(Status_data, colWidths=[content_width/num_cols]*num_cols)
        overhaul_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(overhaul_table)
        elements.append(Spacer(1, 0.1*inch))

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


# Usage Example
if __name__ == "__main__":
    report = WeaponReport()
    report.generate_weapons_pdf_report_updated()