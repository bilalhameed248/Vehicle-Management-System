import pandas as pd
from database import VMS_DB

class ImportVehicles:

    def __init__(self, user_session=None, parent=None, db_to_display = None):
        # super().__init__(parent)
        self.user_session = user_session if user_session else {}
        self.user_id = self.user_session.get('user_id')
        self.username = self.user_session.get('username') 
        self.db_to_display = db_to_display
        self.db_obj = VMS_DB()

    def read_and_insert_excel(self, file_path):
        """
        Reads an Excel report starting at row 8 (skipping introductory rows)
        and inserts each vehicle record into the database.
        """
        # Skip the first 7 rows so that row 8 is treated as header
        is_successfully_import = True
        df = pd.read_excel(file_path, skiprows=6)
        # Iterate over each row in the dataframe
        for index, row in df.iterrows():
            data = {}
            # Map Excel columns to database columns using db_to_display dictionary
            for db_col, excel_col in self.db_to_display.items():
                if db_col == "created_by":
                    data[db_col] = self.user_id
                else:
                    data[db_col] = row.get(excel_col, None)

            del data['created_at']

            # Insert the data into the database
            success = self.db_obj.insert_vehicle(data)
            if not success:
                is_successfully_import = False
                print(f"Failed to insert row {index}")
        return is_successfully_import