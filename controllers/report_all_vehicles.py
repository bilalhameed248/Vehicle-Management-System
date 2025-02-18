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
        self.filename = os.path.join(downloads_path, f"all_vehicles_report_{timestamp}.xlsx")

    def generate_report(self):
        try:
            db = VMS_DB()
            vehicles = db.get_all_vehicle(page=None, page_size=None)

            self.groupColors = {
                "Basic Details": "FF5733",  # Red-Orange
                "Oil Filter": "33A1FF",     # Blue
                "Fuel Filter": "28B463",    # Green
                "Air Filter": "F1C40F",     # Yellow
                "Transmission Filter": "8E44AD",  # Purple
                "Differential Oil": "E67E22",  # Orange
                "Battery Info": "2C3E50",  # Dark Blue
                "Flushing Info": "D35400",  # Dark Orange
                "Greasing Info": "C0392B",  # Dark Red
                "General Maint": "16A085",  # Teal
                "Overhaul": "7F8C8D",        # Gray
                "Status & Creation Details": "008B8B" # Deep Cyan
            }
            
            if not vehicles:
                print("No data found to export.")
                return
            
            # Map database columns to display names
            db_to_display = {
                "category": "Category", "ba_no_input": "BA No.", "make_type_input": "Make Type", "engine_no_input": "Engine No.",
                "issue_date_oil_filter": "Issue Date (Oil Filter)", "due_date_oil_filter": "Due Date (Oil Filter)", "current_mileage_oil_filter": "Current Mileage (Oil Filter)", "due_mileage_oil_filter": "Due Mileage (Oil Filter)",
                "issue_date_fuel_filter": "Issue Date (Fuel Filter)", "due_date_fuel_filter": "Due Date (Fuel Filter)", "current_mileage_fuel_filter": "Current Mileage (Fuel Filter)", "due_mileage_fuel_filter": "Due Mileage (Fuel Filter)",
                "issue_date_air_filter": "Issue Date (Air Filter)", "due_date_air_filter": "Due Date (Air Filter)", "current_mileage_air_filter": "Current Mileage (Air Filter)", "due_mileage_air_filter": "Due Mileage (Air Filter)",
                "issue_date_transmission_filter": "Issue Date (Transmission Filter)", "due_date_transmission_filter": "Due Date (Transmission Filter)", "current_mileage_transmission_filter": "Current Mileage (Transmission Filter)", "due_mileage_transmission_filter": "Due Mileage (Transmission Filter)",
                "issue_date_differential_oil": "Issue Date (Differential Oil)", "due_date_differential_oil": "Due Date (Differential Oil)", "current_mileage_differential_oil": "Current Mileage (Differential Oil)", "due_mileage_differential_oil": "Due Mileage (Differential Oil)",
                "battery_issue_date": "Issue Date (Battery)", "battery_due_date": "Due Date (Battery)",
                "flusing_issue_date": "Issue Date (Flushing)", "flusing_due_date": "Due Date (Flushing)", "fuel_tank_flush": "Fuel Tank Flush", "radiator_flush": "Radiator Flush",
                "greasing_issue_date": "Issue Date (Greasing)", "greasing_due_date": "Due Date (Greasing)", "trs_and_suspension": "TRS and Suspension","engine_part": "Engine Part", "steering_lever_Pts": "Steering Lever Pts", 
                "wash": "Wash", "oil_level_check": "Oil Level Check", "lubrication_of_parts": "Lubrication of Parts",
                "air_cleaner": "Air Cleaner", "fuel_filter": "Fuel Filter", "french_chalk": "French Chalk", "tr_adjustment": "TR Adjustment",
                "overhaul_current_milage": "Current Milage (Overhaul)", "overhaul_due_milage": "Due Milage (Overhaul)", 
                "overhaul_remarks_input": "Status",
                "created_by": "Created By", "created_at": "Created At"
            }

            main_header = {
                'Basic Details': ['category', 'ba_no_input', 'make_type_input', 'engine_no_input'], 
                'Oil Filter' : ["issue_date_oil_filter", "due_date_oil_filter",  "current_mileage_oil_filter", "due_mileage_oil_filter"],
                'Fuel Filter': ["issue_date_fuel_filter", "due_date_fuel_filter", "current_mileage_fuel_filter", "due_mileage_fuel_filter"],
                'Air Filter': ["issue_date_air_filter", "due_date_air_filter", "current_mileage_air_filter", "due_mileage_air_filter"],
                'Transmission Filter': ["issue_date_transmission_filter", "due_date_transmission_filter", "current_mileage_transmission_filter", "due_mileage_transmission_filter"],
                'Differential Oil': ["issue_date_differential_oil", "due_date_differential_oil", "current_mileage_differential_oil", "due_mileage_differential_oil"],
                'Battery Info': ["battery_issue_date", "battery_due_date"],
                'Flushing Info': ["flusing_issue_date", "flusing_due_date", "fuel_tank_flush", "radiator_flush"],
                'Greasing Info': ["greasing_issue_date", "greasing_due_date", "trs_and_suspension", "engine_part", "steering_lever_Pts"],
                'General Maint': ["wash", "oil_level_check", "lubrication_of_parts", "air_cleaner", "fuel_filter", "french_chalk", "tr_adjustment"],
                'Overhaul': ["overhaul_current_milage", "overhaul_due_milage"],
                'Status & Creation Details' : ["overhaul_remarks_input", "created_by", "created_at"]
            }

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Vehicle Report"

            # Header
            ws.merge_cells("A1:AG1")
            ws["A1"] = "44 AK HAT Battalion, Pakistan Army"
            ws["A1"].font = Font(size=14, bold=True)
            ws["A1"].alignment = Alignment(horizontal="left")
            
            ws.merge_cells("A2:AG2")
            ws["A2"] = "Vehicle Maintenance Report"
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
            for vehicle in vehicles:
                row_data = []
                for columns in main_header.values():
                    for col in columns:
                        row_data.append(vehicle.get(col, ""))
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
