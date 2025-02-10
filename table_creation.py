import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect("vms44AKDB.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE "all_vehicles" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "category" TEXT DEFAULT NULL,
  "ba_no_input" TEXT DEFAULT NULL,
  "make_type_input" TEXT DEFAULT NULL,
  "engine_no_input" TEXT DEFAULT NULL,
  "issue_date_oil_filter" DATE DEFAULT NULL,
  "due_date_oil_filter" DATE DEFAULT NULL,
  "current_mileage_oil_filter" TEXT DEFAULT NULL,
  "due_mileage_oil_filter" TEXT DEFAULT NULL,
  "issue_date_fuel_filter" DATE DEFAULT NULL,
  "due_date_fuel_filter" DATE DEFAULT NULL,
  "current_mileage_fuel_filter" TEXT DEFAULT NULL,
  "due_mileage_fuel_filter" TEXT DEFAULT NULL,
  "issue_date_air_filter" DATE DEFAULT NULL,
  "due_date_air_filter" DATE DEFAULT NULL,
  "current_mileage_air_filter" TEXT DEFAULT NULL,
  "due_mileage_air_filter" TEXT DEFAULT NULL,
  "issue_date_transmission_filter" DATE DEFAULT NULL,
  "due_date_transmission_filter" DATE DEFAULT NULL,
  "current_mileage_transmission_filter" TEXT DEFAULT NULL,
  "due_mileage_transmission_filter" TEXT DEFAULT NULL,
  "issue_date_differential_oil" DATE DEFAULT NULL,
  "due_date_differential_oil" DATE DEFAULT NULL,
  "current_mileage_differential_oil" TEXT DEFAULT NULL,
  "due_mileage_differential_oil" TEXT DEFAULT NULL,
  "battery_issue_date" DATE DEFAULT NULL,
  "battery_due_date" DATE DEFAULT NULL,
  "flusing_issue_date" DATE DEFAULT NULL,
  "flusing_due_date" DATE DEFAULT NULL,
  "fuel_tank_flush" TEXT DEFAULT NULL,
  "radiator_flush" TEXT DEFAULT NULL,
  "greasing_issue_date" DATE DEFAULT NULL,
  "greasing_due_date" DATE DEFAULT NULL,
  "trs_and_suspension" TEXT DEFAULT NULL,
  "engine_part" TEXT DEFAULT NULL,
  "steering_lever_Pts" TEXT DEFAULT NULL,
  "wash" TEXT DEFAULT NULL,
  "oil_level_check" TEXT DEFAULT NULL,
  "lubrication_of_parts" TEXT DEFAULT NULL,
  "air_cleaner" TEXT DEFAULT NULL,
  "fuel_filter" TEXT DEFAULT NULL,
  "french_chalk" TEXT DEFAULT NULL,
  "tr_adjustment" TEXT DEFAULT NULL,
  "overhaul_current_milage" TEXT DEFAULT NULL,
  "overhaul_due_milage" TEXT DEFAULT NULL,
  "overhaul_remarks_input" TEXT DEFAULT NULL,
  "created_by" TEXT DEFAULT NULL,
  "updated_by" TEXT DEFAULT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "deleted_at" TIMESTAMP DEFAULT NULL,
  "is_deleted" INTEGER DEFAULT 0
);
""")

# # Commit changes and close the connection
# conn.commit()
# conn.close()

# print("Users table created successfully!")


def insert_user(name, email, username, password, is_blocked=0):
    conn = sqlite3.connect("vms44AKDB.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (?, ?, ?, ?, ?)", 
                   (name, email, username, password, is_blocked))
    conn.commit()
    conn.close()

# insert_user("Zia Shahid", "zia@outlook.com", "ziashahid", "Zia", 1)
# print("User inserted successfully!")


def insert_vehicle():
    conn = sqlite3.connect("vms44AKDB.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO all_vehicles (
            category, ba_no_input, make_type_input, engine_no_input,
            issue_date_oil_filter, due_date_oil_filter, current_mileage_oil_filter, due_mileage_oil_filter,
            issue_date_fuel_filter, due_date_fuel_filter, current_mileage_fuel_filter, due_mileage_fuel_filter,
            issue_date_air_filter, due_date_air_filter, current_mileage_air_filter, due_mileage_air_filter,
            issue_date_transmission_filter, due_date_transmission_filter, current_mileage_transmission_filter, due_mileage_transmission_filter,
            issue_date_differential_oil, due_date_differential_oil, current_mileage_differential_oil, due_mileage_differential_oil,
            battery_issue_date, battery_due_date, flusing_issue_date, flusing_due_date,
            fuel_tank_flush, radiator_flush, greasing_issue_date, greasing_due_date,
            trs_and_suspension, engine_part, steering_lever_Pts, wash,
            oil_level_check, lubrication_of_parts, air_cleaner, fuel_filter,
            french_chalk, tr_adjustment, overhaul_current_milage, overhaul_due_milage,
            overhaul_remarks_input, created_by, updated_by, created_at, updated_at, deleted_at, is_deleted
        ) VALUES (
            'SUV', 'BA123', 'Toyota', 'ENG456',
            '2024-02-01', '2025-02-01', '15000', '30000',
            '2024-03-01', '2025-03-01', '16000', '32000',
            '2024-04-01', '2025-04-01', '17000', '34000',
            '2024-05-01', '2025-05-01', '18000', '36000',
            '2024-06-01', '2025-06-01', '19000', '38000',
            '2024-07-01', '2025-07-01', '20000', '40000',
            '2024-08-01', '2025-08-01', '2024-09-01', '2025-09-01',
            'Yes', 'No', '2024-10-01', '2025-10-01',
            'Good', 'Operational', 'Stable', 'Yes',
            'Checked', 'Lubricated', 'Clean', 'Changed',
            'Applied', 'Adjusted', '25000', '50000',
            'No remarks', '1', 'Admin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, 0
        )
    """)
    conn.commit()
    conn.close()
    print("User inserted successfully!")

insert_vehicle()

