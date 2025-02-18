import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import os, traceback
from database import VMS_DB

class Report:
    def __init__(self):
        self.current_date = datetime.now().strftime('%d-%m-%Y')
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = os.path.join(downloads_path, f"all_weapons_report_{timestamp}.xlsx")

    def generate_report(self):
        try:
            db = VMS_DB()
            weapons = db.get_all_weapons(page=None, page_size=None)

            self.groupColors = {
                "Basic Details": "FF5733",  # Red-Orange
                "T.Pod": "33A1FF",     # Blue
                "T. Unit": "28B463",    # Green
                "OS": "F1C40F",     # Yellow
                "DMGS": "8E44AD",  # Purple
                "L-Tube": "E67E22",  # Orange
                "TVPC": "7F8C8D",         # Gray
                "Bty BB-287": "2C3E50",  # Dark Blue
                "NVS": "D35400",  # Dark Orange
                "BPC": "C0392B",  # Dark Red
                "VPC": "16A085",  # Teal
                "L.Bty": "A569BD",         # Soft Purple
                "Doc": "5D6D7E",         # Slate Blue-Gray
                "Status & Creation Details": "008B8B" # Deep Cyan
            }
            
            if not weapons:
                print("No data found to export.")
                return
            
            # Map database columns to display names
            db_to_display = {
                "Wpn_No": "Wpn No",
                "T_Pod_Leg_lock_handle": "Leg lock handle",  "T_Pod_Anchor_claw": "Anchor claw",  "T_Pod_Leveling_Bubbles": "Leveling Bubbles", "T_Pod_Lubrication":"Lubrication",  
                "T_Pod_Pull_tube":"Pull tube",  "T_Pod_Detent_stop_lever":"Detent stop lever", "T_Pod_Foot_pad_legs_body_condition":"Foot pad/ legs body condition",

                "T_Unit_Traversing_Lock":"Traversing Lock",  "T_Unit_Elevation_lock_check":"Elevation lock check", "T_Unit_Elevation_lock_handle":"Elevation lock handle",  "T_Unit_Viscosity_of_Viscos_damper":"Viscosity of Viscos damper", 
                "T_Unit_Azimuth_lock_check":"Azimuth lock check", "T_Unit_Lubrication":"Lubrication", "T_Unit_Protective_cover":"Protective cover",  "T_Unit_Coil_Card":"Coil Card",

                "OS_Eye_Shield": "Eye Shield", "OS_Focusing_knob": "Focusing knob",  "OS_Sillica_gel_condition": "Sillica gel condition", "OS_Reticle_lamp": "Reticle lamp",  
                "OS_Body_condition": "Body condition", "OS_N2_purg_filling_connection": "N2 purg / filling connection", "OS_Reticle_switch": "Reticle switch",  "OS_Cable_connector": "Cable connector", 
                "OS_Locking_device": "Locking device", "OS_Lens_cover": "Lens cover", "OS_Objective_lens": "Objective lens",

                "DMGS_Meter_indicator_AZ_Elev":" Meter indicator (AZ & Elev)",  "DMGS_Sockets":" Sockets", "DMGS_MGS_DMGS_case":" MGS/ DMGS case",  
                "DMGS_Protective_cover":" Protective cover", "DMGS_Cable":" Cable", "DMGS_Bty_connector":" Bty connector",  "DMGS_Self_test":" Self/ test", 

                "L_Tube_Body_Condition":"Body Condition",
                "TVPC_Body_Condition":"Body Condition", "TVPC_Fly_Net":"Fly Net", "TVPC_On_Off_Switch":"On/Off Switch", "TVPC_Indicator_It":"Indicator It", "TVPC_Connector":"Connector", "TVPC_Voltage":"Voltage",

                "Bty_BB_287_Bty_connector": "Bty connector", "Bty_BB_287_Voltage_24V_sec": "Voltage +24 V sec",  "Bty_BB_287_Voltage_50V": "Voltage +50 V", 
                "Bty_BB_287_Voltage_50V_sec": "Voltage +50 V sec", "Bty_BB_287_Bty_condition": "Bty condition", "Bty_BB_287_Bty_Tvpc" : "TVPC", "Bty_BB_287_Power_cable_condition": "Power cable condition",
                
                "NVS_Coolant_unit": "Coolant unit", "NVS_Eye_piece": "Eye piece", "NVS_Cable_connector": "Cable connector", "NVS_Lens_assy": "Lens assy", "NVS_Power_cable_condition": "Power cable condition",
                "BPC_Body": "Body",  "BPC_Cables": "Cables",  "BPC_On_Off_Switch": "On/Off Switch",
                "VPC_Body": "Body", "VPC_Switch": "Switch", "VPC_VPC_Power_Cable": "VPC Power Cable",            
                "L_Bty_Bty_Voltage":"Bty Voltage",

                "Doc_6_Monthly_verification_record":"6 Monthly verification record", "Doc_Last_ATI_pts_has_been_killed":"Last ATI pts has been killed", "Doc_Bty_charging_record":"Bty charging record", 
                "Doc_Storage_temp_Humidity_record":"Storage temp & Humidity record", "Doc_Firing_record_check":"Firing record check", "Doc_Svc_ability_Completeness_of_tools_accy":"Svc ability & Completeness of tools & accy", 
                "Doc_Self_test_record_check":"Self test record check", "Doc_Is_eARMS_fully_func":"Is eARMS fully func and all the processes involved are being carried out through eARMS",
                "Doc_Complete_eqpt_inventory_update_on_eARMS":"Complete eqpt inventory update on eARMS", "Doc_DRWO_work_order_being_processed_on_eARMS":"DRWO/ work order being processed on eARMS", 
                "Doc_Are_Log_book_maintain_properly":"Are Log book maintain properly",

                "Status": "Status", "created_by": "Created By", "created_at": "Created At"
            }

            main_header = {
                "Basic Details": ["Wpn_No"],
                "T.Pod": [ "T_Pod_Leg_lock_handle", "T_Pod_Anchor_claw", "T_Pod_Leveling_Bubbles", "T_Pod_Lubrication", "T_Pod_Pull_tube", "T_Pod_Detent_stop_lever", "T_Pod_Foot_pad_legs_body_condition" ],
                "T. Unit": [ "T_Unit_Traversing_Lock", "T_Unit_Elevation_lock_check", "T_Unit_Elevation_lock_handle", "T_Unit_Viscosity_of_Viscos_damper", "T_Unit_Azimuth_lock_check", "T_Unit_Lubrication", "T_Unit_Protective_cover", "T_Unit_Coil_Card" ],
                "OS": [ "OS_Eye_Shield", "OS_Focusing_knob", "OS_Sillica_gel_condition","OS_Reticle_lamp","OS_Body_condition","OS_N2_purg_filling_connection","OS_Reticle_switch","OS_Cable_connector","OS_Locking_device","OS_Lens_cover","OS_Objective_lens"],

                "DMGS": [ "DMGS_Meter_indicator_AZ_Elev", "DMGS_Sockets", "DMGS_MGS_DMGS_case", "DMGS_Protective_cover", "DMGS_Cable", "DMGS_Bty_connector", "DMGS_Self_test" ],
                "L-Tube": [ "L_Tube_Body_Condition" ],
                "TVPC": [ "TVPC_Body_Condition","TVPC_Fly_Net","TVPC_On_Off_Switch","TVPC_Indicator_It","TVPC_Connector","TVPC_Voltage" ],
                "Bty BB-287": [ "Bty_BB_287_Bty_connector", "Bty_BB_287_Voltage_24V_sec", "Bty_BB_287_Voltage_50V", "Bty_BB_287_Voltage_50V_sec", "Bty_BB_287_Bty_condition", "Bty_BB_287_Bty_Tvpc", "Bty_BB_287_Power_cable_condition" ],
                "NVS": [ "NVS_Coolant_unit", "NVS_Eye_piece", "NVS_Cable_connector", "NVS_Lens_assy", "NVS_Power_cable_condition" ],
                
                "BPC": [ "BPC_Body", "BPC_Cables", "BPC_On_Off_Switch"],
                "VPC": [ "VPC_Body", "VPC_Switch", "VPC_VPC_Power_Cable" ],
                "L.Bty": ["L_Bty_Bty_Voltage"],
                "Doc": [ "Doc_6_Monthly_verification_record","Doc_Last_ATI_pts_has_been_killed","Doc_Bty_charging_record","Doc_Storage_temp_Humidity_record","Doc_Firing_record_check","Doc_Svc_ability_Completeness_of_tools_accy",
                        "Doc_Self_test_record_check","Doc_Is_eARMS_fully_func", "Doc_Complete_eqpt_inventory_update_on_eARMS","Doc_DRWO_work_order_being_processed_on_eARMS","Doc_Are_Log_book_maintain_properly",],
                "Status & Creation Details": ["Status", "created_by", "created_at"]
            }

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Weapons Report"

            # Header
            ws.merge_cells("A1:AG1")
            ws["A1"] = "44 AK HAT Battalion, Pakistan Army"
            ws["A1"].font = Font(size=14, bold=True)
            ws["A1"].alignment = Alignment(horizontal="left")
            
            ws.merge_cells("A2:AG2")
            ws["A2"] = "Weapons Maintenance Report"
            ws["A2"].font = Font(size=12, bold=True)
            ws["A2"].alignment = Alignment(horizontal="left")
            
            ws.merge_cells("A3:AG3")
            ws["A3"] = f"Date: {self.current_date}"
            ws["A3"].font = Font(size=10, italic=True)
            ws["A3"].alignment = Alignment(horizontal="left")

            # Leave 2 rows empty
            ws.append([])
            ws.append([])

            # Column Headers
            # Column Headers with Category Headers
            col_index = 1
            for category, columns in main_header.items():
                ws.merge_cells(start_row=6, start_column=col_index, end_row=6, end_column=col_index + len(columns) - 1)
                cell = ws.cell(row=6, column=col_index, value=category)
                cell.font = Font(size=14, bold=True, color="FFFFFF")
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.fill = PatternFill(start_color=self.groupColors[category], fill_type="solid")
                cell.border = Border(top=Side(style='thin'), bottom=Side(style='thin'), left=Side(style='thin'), right=Side(style='thin'))
                col_index += len(columns)
            
            # ws.append([db_to_display[col] for columns in main_header.values() for col in columns])

            # Style Column Headers
            for col_num, column_title in enumerate([col for columns in main_header.values() for col in columns], start=1):
                cell = ws.cell(row=7, column=col_num, value=db_to_display[column_title])
                cell.font = Font(size=12, bold=True)
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = Border(bottom=Side(style='thin'))

            all_columns = [col for columns in main_header.values() for col in columns]

            # Adding data
            for weapon in weapons:
                row_data = []
                for columns in main_header.values():
                    for col in columns:
                        row_data.append(weapon.get(col, ""))
                ws.append(row_data)
            
            
            # Now loop over all data rows (data starts at row 8 in this example because rows 1-7 are header)
            for row in ws.iter_rows(min_row=8, max_row=ws.max_row):
                for idx, cell in enumerate(row, start=1):
                    col_key = all_columns[idx - 1]
                    if col_key in ['issue_date_oil_filter', 'issue_date_fuel_filter', 'issue_date_air_filter', 'issue_date_transmission_filter', 'issue_date_differential_oil', 'battery_issue_date', 'flusing_issue_date', 'greasing_issue_date'] and cell.value:
                        try:
                            date_obj = datetime.strptime(str(cell.value), "%Y-%m-%d").date()
                            if col_key == 'issue_date_oil_filter':
                                self.date_rules(cell, date_obj, 6, 20)
                            elif col_key == 'issue_date_fuel_filter':
                                self.date_rules(cell, date_obj, 12, 20)
                            elif col_key in ['issue_date_air_filter', 'issue_date_transmission_filter', 'issue_date_differential_oil']:
                                self.date_rules(cell, date_obj, 18, 20)
                            elif col_key == 'battery_issue_date':
                                self.date_rules(cell, date_obj, 42, 20)
                            elif col_key == 'flusing_issue_date':
                                self.date_rules(cell, date_obj, 4, 20)
                            elif col_key == 'greasing_issue_date':
                                self.date_rules(cell, date_obj, 3, 20)
                        except ValueError:
                            print(f"Invalid date format for {cell.value} in column {col_key}")
                            continue

            # Auto-Adjust Column Widths
            for col in ws.columns:
                max_length = max((len(str(cell.value)) if cell.value else 0) for cell in col)
                col_letter = openpyxl.utils.get_column_letter(col[0].column)
                ws.column_dimensions[col_letter].width = max_length + 5

            # Save file
            wb.save(self.filename)
            print(f"Report saved at: {self.filename}")
            return True
        
        except Exception as e:
            traceback.print_exc()
            print(f"Exception in generate_report: {e}")
            return False
        
    def date_rules(self, cell, cell_value, no_of_month, no_of_days):
        # print(f"IN Rule: {type(cell_value)}, {cell_value},  {date.today()}")
        difference = relativedelta(date.today(), cell_value)
        months_diff = difference.years * 12 + difference.months
        days_diff = difference.days
        # print(f"{months_diff} : {days_diff}")

        if months_diff >= no_of_month:
            cell.fill = PatternFill(start_color="FF0000", fill_type="solid")  # Red BG
            cell.font = Font(color="FFFFFF", bold=True)  # White text for visibility
        elif months_diff >= (no_of_month-1) and days_diff >= no_of_days and days_diff <= (no_of_days+10):
            cell.fill = PatternFill(start_color="FFFF00", fill_type="solid")  # Yellow BG
            cell.font = Font(color="000000", bold=True)  # Black text for visibility

# Usage Example
if __name__ == "__main__":
    report = Report()
    report.generate_report()
