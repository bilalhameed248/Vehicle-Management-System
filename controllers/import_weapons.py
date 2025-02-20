import pandas as pd
from collections import defaultdict
from database import VMS_DB

class ImportWeapons:

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
        df.columns = df.columns.str.replace(r'\s+', ' ', regex=True)
        df.columns = df.columns.str.strip()

        # Reverse mapping to handle duplicate column names
        reverse_mapping = defaultdict(list)
        for db_col, excel_col in self.db_to_display.items():
            reverse_mapping[excel_col].append(db_col)

        for index, row in df.iterrows():
            data = {}
            # Map Excel columns to database columns using db_to_display dictionary
            for excel_col, db_cols in reverse_mapping.items():
                excel_value = row.get(excel_col, None)
                for db_col in db_cols:
                    if db_col == "created_by":
                        data[db_col] = 1
                    else:
                        data[db_col] = excel_value  # Assign the same value to multiple columns

            if 'created_at' in data:
                del data['created_at']

            # Insert the data into the database
            success = self.db_obj.insert_weapon(data)
            if not success:
                is_successfully_import = False
                print(f"Failed to insert row {index}")
        return is_successfully_import