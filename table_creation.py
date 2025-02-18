import sqlite3

# # Connect to the database (or create it if it doesn't exist)
# conn = sqlite3.connect("vms44AKDB.db")

# # Create a cursor object to execute SQL commands
# cursor = conn.cursor()

# # Create users table
# cursor.execute("""
# Select count (*) from all_vehicles where is_deleted = 0;
# """)

# # Commit changes and close the connection
# conn.commit()
# conn.close()

# print("Users table created successfully!")


# def insert_user(name, email, username, password, is_blocked=0):
#     conn = sqlite3.connect("vms44AKDB.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (name, email, username, password, is_blocked) VALUES (?, ?, ?, ?, ?)", 
#                    (name, email, username, password, is_blocked))
#     conn.commit()
#     conn.close()

# # insert_user("Zia Shahid", "zia@outlook.com", "ziashahid", "Zia", 1)
# # print("User inserted successfully!")


# def insert_vehicle():
#     conn = sqlite3.connect("vms44AKDB.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO all_vehicles (
#             category, ba_no_input, make_type_input, engine_no_input,
#             issue_date_oil_filter, due_date_oil_filter, current_mileage_oil_filter, due_mileage_oil_filter,
#             issue_date_fuel_filter, due_date_fuel_filter, current_mileage_fuel_filter, due_mileage_fuel_filter,
#             issue_date_air_filter, due_date_air_filter, current_mileage_air_filter, due_mileage_air_filter,
#             issue_date_transmission_filter, due_date_transmission_filter, current_mileage_transmission_filter, due_mileage_transmission_filter,
#             issue_date_differential_oil, due_date_differential_oil, current_mileage_differential_oil, due_mileage_differential_oil,
#             battery_issue_date, battery_due_date, flusing_issue_date, flusing_due_date,
#             fuel_tank_flush, radiator_flush, greasing_issue_date, greasing_due_date,
#             trs_and_suspension, engine_part, steering_lever_Pts, wash,
#             oil_level_check, lubrication_of_parts, air_cleaner, fuel_filter,
#             french_chalk, tr_adjustment, overhaul_current_milage, overhaul_due_milage,
#             overhaul_remarks_input, created_by, updated_by, created_at, updated_at, deleted_at, is_deleted
#         ) VALUES (
#             'SUV', 'BA123', 'Toyota', 'ENG456',
#             '2024-02-01', '2025-02-01', '15000', '30000',
#             '2024-03-01', '2025-03-01', '16000', '32000',
#             '2024-04-01', '2025-04-01', '17000', '34000',
#             '2024-05-01', '2025-05-01', '18000', '36000',
#             '2024-06-01', '2025-06-01', '19000', '38000',
#             '2024-07-01', '2025-07-01', '20000', '40000',
#             '2024-08-01', '2025-08-01', '2024-09-01', '2025-09-01',
#             'Yes', 'No', '2024-10-01', '2025-10-01',
#             'Good', 'Operational', 'Stable', 'Yes',
#             'Checked', 'Lubricated', 'Clean', 'Changed',
#             'Applied', 'Adjusted', '25000', '50000',
#             'No remarks', '1', 'Admin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, 0
#         )
#     """)
#     conn.commit()
#     conn.close()
#     print("User inserted successfully!")

# insert_vehicle()

# pyinstaller --onefile --windowed --icon=app_icon.ico --add-data "assets;assets" --add-data "vms44AKDB.db;." main.py



{
    "Wpn No": 
      ["Wpn No"],
    
    "T.Pod": 
      [ 
          "Leg lock handle", 
          "Leg lock handle", 
          "Leg lock handle", 
          "Lubrication", 
          "Pull tube", 
          "Detent stop lever", 
          "Foot pad/ legs body condition" ],
    "T. Unit": [ "Traversing Lock", "Elevation lock check", "Elevation lock handle", "Viscosity of Viscos damper", "Azimuth lock check", "Lubrication", "Protective cover", "Coil Card" ],
    "OS": [ "Eye Shield", "Focusing knob", "Sillica gel condition", "Reticle lamp", "Body condition", "N2 purg / filling connection", "Reticle switch", "Cable connector", "Locking device", 
           "Lens cover", "Objective lens" ],

    "DMGS": [ "Meter indicator (AZ & Elev)", "Sockets", "MGS/ DMGS case", "Protective cover", "Cable", "Bty connector", "Self/ test" ],
    "L-Tube": [ "Body Condition" ],
    "TVPC": [ "Body Condition", "Fly Net", "On/Off Switch", "Indicator It", "Connector", "Voltage"],
    "Bty BB-287": [ "Bty connector", "Voltage +24 V sec", "Voltage +50 V", "Voltage +50 V sec", "Bty condition", "Tvpc", "Power cable condition" ],

    "NVS": [ "Coolant unit", "Eye piece", "Cable connector", "Lens assy", "Power cable condition"],
    
    "BPC": ["Body", "Cables", "On/Off Switch"],
    "VPC": ["Body", "Switch", "VPC Power Cable"],
    "L.Bty": ["Bty Voltage"],
    "Doc": [ "6 Monthly verification record", "Last ATI pts has been killed", "Bty charging record", "Storage temp & Humidity record", "Firing record check",
      "Svc ability & Completeness of tools & accy", "Self test record check", "Is eARMS fully func and all the processes involved are being carried out through eARMS",
      "Complete eqpt inventory update on eARMS", "DRWO/ work order being processed on eARMS", "Are Log book maintain properly" ],
    "Status": ["Status"]
}


# CREATE TABLE all_weapons (
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     Wpn_No TEXT,
#     T_Pod_Leg_lock_handle TEXT,
#     T_Pod_Anchor_claw TEXT,
#     T_Pod_Leveling_Bubbles TEXT,
#     T_Pod_Lubrication TEXT,
#     T_Pod_Pull_tube TEXT,
#     T_Pod_Detent_stop_lever TEXT,
#     T_Pod_Foot_pad_legs_body_condition TEXT,
#     T_Unit_Traversing_Lock TEXT,
#     T_Unit_Elevation_lock_check TEXT,
#     T_Unit_Elevation_lock_handle TEXT,
#     T_Unit_Viscosity_of_Viscos_damper TEXT,
#     T_Unit_Azimuth_lock_check TEXT,
#     T_Unit_Lubrication TEXT,
#     T_Unit_Protective_cover TEXT,
#     T_Unit_Coil_Card TEXT,
#     OS_Eye_Shield TEXT,
#     OS_Focusing_knob TEXT,
#     OS_Sillica_gel_condition TEXT,
#     OS_Reticle_lamp TEXT,
#     OS_Body_condition TEXT,
#     OS_N2_purg_filling_connection TEXT,
#     OS_Reticle_switch TEXT,
#     OS_Cable_connector TEXT,
#     OS_Locking_device TEXT,
#     OS_Lens_cover TEXT,
#     OS_Objective_lens TEXT,
#     DMGS_Meter_indicator_AZ_Elev TEXT,
#     DMGS_Sockets TEXT,
#     DMGS_MGS_DMGS_case TEXT,
#     DMGS_Protective_cover TEXT,
#     DMGS_Cable TEXT,
#     DMGS_Bty_connector TEXT,
#     DMGS_Self_test TEXT,
#     L_Tube_Body_Condition TEXT,
#     TVPC_Body_Condition TEXT,
#     TVPC_Fly_Net TEXT,
#     TVPC_On_Off_Switch TEXT,
#     TVPC_Indicator_It TEXT,
#     TVPC_Connector TEXT,
#     TVPC_Voltage TEXT,
#     Bty_BB_287_Bty_connector TEXT,
#     Bty_BB_287_Voltage_24V_sec TEXT,
#     Bty_BB_287_Voltage_50V TEXT,
#     Bty_BB_287_Voltage_50V_sec TEXT,
#     Bty_BB_287_Bty_condition TEXT,
#     Bty_BB_287_Bty_Tvpc TEXT,
#     Bty_BB_287_Power_cable_condition TEXT,
#     NVS_Coolant_unit TEXT,
#     NVS_Eye_piece TEXT,
#     NVS_Cable_connector TEXT,
#     NVS_Lens_assy TEXT,
#     NVS_Power_cable_condition TEXT,
#     BPC_Body TEXT,
#     BPC_Cables TEXT,
#     BPC_On_Off_Switch TEXT,
#     VPC_Body TEXT,
#     VPC_Switch TEXT,
#     VPC_VPC_Power_Cable TEXT,
#     L_Bty_Bty_Voltage TEXT,
#     Doc_6_Monthly_verification_record TEXT,
#     Doc_Last_ATI_pts_has_been_killed TEXT,
#     Doc_Bty_charging_record TEXT,
#     Doc_Storage_temp_Humidity_record TEXT,
#     Doc_Firing_record_check TEXT,
#     Doc_Svc_ability_Completeness_of_tools_accy TEXT,
#     Doc_Self_test_record_check TEXT,
#     Doc_Is_eARMS_fully_func TEXT,
#     Doc_Complete_eqpt_inventory_update_on_eARMS TEXT,
#     Doc_DRWO_work_order_being_processed_on_eARMS TEXT,
#     Doc_Are_Log_book_maintain_properly TEXT,
#     Status TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     created_by TEXT,
#     updated_by TEXT,
#     is_deleted INTEGER DEFAULT 0 CHECK (is_deleted IN (0, 1))
# );


