import sqlite3

# Connect to the database (or create it if it doesn't exist)
# conn = sqlite3.connect("vms44AKDB.db")

# # Create a cursor object to execute SQL commands
# cursor = conn.cursor()

# # Create users table
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT UNIQUE NOT NULL,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL,
#     is_blocked INTEGER DEFAULT 0,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )
# """)

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

insert_user("Zia Shahid", "zia@outlook.com", "ziashahid", "Zia", 1)
print("User inserted successfully!")
