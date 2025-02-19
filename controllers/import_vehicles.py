import pandas as pd
from database import VMS_DB
class ImportVehicles:

    def __init__(self, db_to_display = None):
        self.db_to_display = db_to_display
        self.db_obj = VMS_DB()

    def read_and_insert_excel(self, file_path):
        """
        Reads an Excel report starting at row 8 (skipping introductory rows)
        and inserts each vehicle record into the database.
        """
        # Skip the first 7 rows so that row 8 is treated as header
        df = pd.read_excel(file_path, skiprows=7)
        
        # Iterate over each row in the dataframe
        for index, row in df.iterrows():
            data = {}
            # Map Excel columns to database columns using db_to_display dictionary
            for db_col, excel_col in self.db_to_display.items():
                data[db_col] = row.get(excel_col, None)
            # Insert the data into the database
            success = self.db_obj.insert_vehicle(data)
            if not success:
                print(f"Failed to insert row {index}")

if __name__ == "__main__":
    imp_vhl_obj = ImportVehicles()
    file_path = "path_to_your_excel_report.xlsx"
    imp_vhl_obj.read_and_insert_excel(file_path)