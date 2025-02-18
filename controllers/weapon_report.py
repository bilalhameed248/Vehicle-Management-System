from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
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

        # --- Section: T.Pod (7-column table) ---
        elements.append(Paragraph("T.Pod", subheader_style))
        T_Pod_data = [
            [ "Leg lock handle", "Anchor claw", "Leveling Bubbles", "Lubrication", ],
            [
                row_data.get('Leg lock handle', ''),
                row_data.get('Anchor claw', ''),
                row_data.get('Leveling Bubbles', ''),
                row_data.get('Lubrication', '')
            ]
        ]
        num_cols = 4
        T_Pod_table = Table(T_Pod_data, colWidths=[content_width/num_cols]*num_cols)
        T_Pod_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(T_Pod_table)

        T_Pod_data = [
            ["Pull tube", "Detent stop lever", "Foot pad/ legs body condition" ],
            [
                row_data.get('Pull tube', ''),
                row_data.get('Detent stop lever', ''),
                row_data.get('Foot pad/ legs body condition', '')
            ]
        ]
        num_cols = 3
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
            [ "Traversing Lock", "Elevation lock check", "Elevation lock handle", "Viscosity of Viscos damper"],
            [
                row_data.get('Traversing Lock', ''),
                row_data.get('Elevation lock check', ''),
                row_data.get('Elevation lock handle', ''),
                row_data.get('Viscosity of Viscos damper', '')
            ]
        ]
        num_cols = 4
        T_Unit_table = Table(T_Unit_data, colWidths=[content_width/num_cols]*num_cols)
        T_Unit_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(T_Unit_table)
        
        T_Unit_data = [
            ["Azimuth lock check", "Lubrication", "Protective cover", "Coil Card" ],
            [
                row_data.get('Azimuth lock check', ''),
                row_data.get('Lubrication', ''),
                row_data.get('Protective cover', ''),
                row_data.get('Coil Card', '')
            ]
        ]
        num_cols = 4
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
            [ "Eye Shield", "Focusing knob", "Sillica gel condition", "Reticle lamp"],
            [
                row_data.get('Eye Shield', ''),
                row_data.get('Focusing knob', ''),
                row_data.get('Sillica gel condition', ''),
                row_data.get('Reticle lamp', '')
            ]
        ]
        num_cols = 4
        OS_table = Table(OS_data, colWidths=[content_width/num_cols]*num_cols)
        OS_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(OS_table)

        OS_data = [
            [ "Body condition", "N2 purg / filling connection", "Reticle switch", "Cable connector"],
            [
                row_data.get('Body condition', ''),
                row_data.get('N2 purg / filling connection', ''),
                row_data.get('Reticle switch', ''),
                row_data.get('Cable connector', '')
            ]
        ]
        num_cols = 4
        OS_table = Table(OS_data, colWidths=[content_width/num_cols]*num_cols)
        OS_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(OS_table)

        OS_data = [
            [ "Locking device", "Lens cover", "Objective lens"  ],
            [
                row_data.get('Locking device', ''),
                row_data.get('Lens cover', ''),
                row_data.get('Objective lens', '')
            ]
        ]
        num_cols = 3
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
            [ "Meter indicator (AZ & Elev)", "Sockets", "MGS/ DMGS case"],
            [
                row_data.get('Meter indicator (AZ & Elev))', ''),
                row_data.get('Sockets', ''),
                row_data.get('MGS/ DMGS case', '')
            ]
        ]
        num_cols = 3
        DMGS_table = Table(DMGS_data, colWidths=[content_width/num_cols]*num_cols)
        DMGS_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(DMGS_table)

        DMGS_data = [
            [ "Protective cover", "Cable", "Bty connector", "Self/ test" ],
            [
                row_data.get('Protective cover', ''),
                row_data.get('Cable', ''),
                row_data.get('Bty connector', ''),
                row_data.get('Self/ test', '')
            ]
        ]
        num_cols = 4
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
        elements.append(Paragraph("L-Tube", subheader_style))
        L_Tube_data = [
            [ "Body Condition" ],
            [
                row_data.get('Body Condition', '')
            ]
        ]
        num_cols = 1
        L_Tube_table = Table(L_Tube_data, colWidths=[content_width/num_cols]*num_cols)
        L_Tube_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(L_Tube_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: TVPC (6-column table) ---
        elements.append(Paragraph("TVPC", subheader_style))
        TVPC_data = [
            [ "Body Condition", "Fly Net", "On/Off Switch", ],
            [
                row_data.get('Body Condition', ''),
                row_data.get('Fly Net', ''),
                row_data.get('On/Off Switch', '')
            ]
        ]
        num_cols = 3
        TVPC_table = Table(TVPC_data, colWidths=[content_width/num_cols]*num_cols)
        TVPC_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(TVPC_table)

        TVPC_data = [
            [ "Indicator It", "Connector", "Voltage"],
            [
                row_data.get('Indicator It', ''),
                row_data.get('Connector', ''),
                row_data.get('Voltage', '')
            ]
        ]
        num_cols = 3
        TVPC_table = Table(TVPC_data, colWidths=[content_width/num_cols]*num_cols)
        TVPC_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(TVPC_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Bty BB-287 (7-column table) ---
        elements.append(Paragraph("Bty BB-287", subheader_style))
        Bty_BB_287_data = [
            [ "Bty connector", "Voltage +24 V sec", "Voltage +50 V", "Voltage +50 V sec" ],
            [
                row_data.get('Bty connector', ''),
                row_data.get('Voltage +24 V sec', ''),
                row_data.get('Voltage +50 V', ''),
                row_data.get('Voltage +50 V sec', '')
            ]
        ]
        num_cols = 4
        Bty_BB_287_table = Table(Bty_BB_287_data, colWidths=[content_width/num_cols]*num_cols)
        Bty_BB_287_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(Bty_BB_287_table)

        Bty_BB_287_data = [
            [ "Bty condition", "Tvpc", "Power cable condition" ],
            [
                row_data.get('Bty condition', ''),
                row_data.get('Tvpc', ''),
                row_data.get('Power cable condition', '')
            ]
        ]
        num_cols = 3
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
        elements.append(Paragraph("BPC", subheader_style))
        BPC_data = [
            ["Body", "Cables", "On/Off Switch"],
            [
                row_data.get('Body', ''),
                row_data.get('Cables', ''),
                row_data.get('On/Off Switch', '')
            ]
        ]
        num_cols = 3
        BPC_table = Table(BPC_data, colWidths=[content_width/num_cols]*num_cols)
        BPC_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(BPC_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Greasing Details (5-column table) ---
        elements.append(Paragraph("VPC", subheader_style))
        VPC_data = [
            ["Body", "Switch", "VPC Power Cable"],
            [
                row_data.get('Body', ''),
                row_data.get('Switch', ''),
                row_data.get('VPC Power Cable', '')
            ]
        ]
        num_cols = 3
        VPC_table = Table(VPC_data, colWidths=[content_width/num_cols]*num_cols)
        VPC_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(VPC_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: L.Bty (1-column table) ---
        elements.append(Paragraph("L.Bty", subheader_style))
        L_Bty_data = [
            ["Bty Voltage"],
            [
                row_data.get('Bty Voltage', '')
            ]
        ]
        num_cols = 5
        L_Bty_table = Table(L_Bty_data, colWidths=[content_width/num_cols]*num_cols)
        L_Bty_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(L_Bty_table)
        elements.append(Spacer(1, 0.1*inch))

        #*******************************************************************************************************************************

        # --- Section: Doc (9-column table) ---
        elements.append(Paragraph("Doc", subheader_style))
        Doc_data = [
            [ "6 Monthly verification record", "Last ATI pts has been killed", "Bty charging record" ],
            [
                row_data.get('6 Monthly verification record', ''),
                row_data.get('Last ATI pts has been killed', ''),
                row_data.get('Bty charging record', '')
            ]
        ]
        num_cols = 3
        Doc_table = Table(Doc_data, colWidths=[content_width/num_cols]*num_cols)
        Doc_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(Doc_table)

        Doc_data = [
            [ "Storage temp & Humidity record", "Firing record check", "Svc ability & Completeness of tools & accy", ],
            [
                row_data.get('Storage temp & Humidity record', ''),
                row_data.get('Firing record check', ''),
                row_data.get('Svc ability & Completeness of tools & accy', '')
            ]
        ]
        num_cols = 3
        Doc_table = Table(Doc_data, colWidths=[content_width/num_cols]*num_cols)
        Doc_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(Doc_table)

        Doc_data = [
            [ "Self test record check", "Is eARMS fully func \n and all the processes involved are \n being carried out through eARMS", "Complete eqpt inventory \n update on eARMS", ],
            [
                row_data.get('Self test record check', ''),
                row_data.get('Is eARMS fully func and all the processes involved are being carried out through eARMS', ''),
                row_data.get('Complete eqpt inventory update on eARMS', '')
            ]
        ]
        num_cols = 3
        Doc_table = Table(Doc_data, colWidths=[content_width/num_cols]*num_cols)
        Doc_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dceefc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.gray)
        ]))
        elements.append(Doc_table)

        Doc_data = [
            [ "DRWO/ work order being processed on eARMS", "Are Log book maintain properly"],
            [
                row_data.get('DRWO/ work order being processed on eARMS', ''),
                row_data.get('Are Log book maintain properly', '')
            ]
        ]
        num_cols = 2
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
