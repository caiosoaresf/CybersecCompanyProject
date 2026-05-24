import sqlite3
import shutil

# 1. Setup Database Connection
connection = sqlite3.connect("Database.db")
cursor = connection.cursor()

# Ensure Foreign Keys are active
cursor.execute("PRAGMA foreign_keys = ON;")

# 2. Recreate Tables (Uncommented and safe)
cursor.execute("DROP TABLE IF EXISTS Vulnerabilities")
cursor.execute("DROP TABLE IF EXISTS Devices")

cursor.execute("""
CREATE TABLE Devices(
    Id INTEGER NOT NULL PRIMARY KEY UNIQUE,
    Hostname TEXT NOT NULL,
    InCharge TEXT NOT NULL,
    Sector TEXT NOT NULL,
    Type TEXT NOT NULL);     
""")

cursor.execute("""
CREATE TABLE Vulnerabilities(
    DeviceId INT,
    Description TEXT NOT NULL,
    Category TEXT NOT NULL,
    Severity TEXT NOT NULL,
    Status TEXT NOT NULL,
    FOREIGN KEY(DeviceId) REFERENCES Devices(Id) ON DELETE CASCADE ON UPDATE NO ACTION);
""")
connection.commit()  # Save table schemas


# Helper function to clear and handle exit cleanly
def close_program():
    print("Saving changes and exiting...")
    connection.commit()
    connection.close()
    exit()


# 3. User Interface
columns = shutil.get_terminal_size().columns
print("Welcome to Security©".center(columns))
print("*We are a large company that ensures your electronical devices are safe*".center(columns))

print("\nWould you like to proceed?\nPress y if yes\nPress n if no")
if input().strip().lower() != "y":
    close_program()

# Using a Main Loop instead of nested functions prevents stack overflow/bugs
while True:
    print("""
======================================================
Do you already have devices registered in our system?
======================================================
Press "Y" if you Do
Press "N" if you Don't
Press "B" if you want to leave
    """)
    
    choice = input().strip().lower()

    if choice == "b":
        close_program()

    elif choice == "y":
        print("""
Which type of device would you like to check:
Press 1 for Laptop
Press 2 for Server
Press 3 for Router
Press 4 for Printer
Press 5 to return
        """)
        try:
            device_choice = int(input().strip())
            if device_choice in [1, 2, 3, 4]:
                device_id = int(input("Insert the Id of the device: "))
                
                # Fetching the device details safely
                cursor.execute("SELECT * FROM Devices WHERE Id = ?", (device_id,))
                device = cursor.fetchone()
                if device:
                    print(f"\nDevice Found: ID: {device[0]} | Hostname: {device[1]} | Owner: {device[2]} | Sector: {device[3]} | Type: {device[4]}")
                    
                    # Fetching related vulnerabilities
                    cursor.execute("SELECT * FROM Vulnerabilities WHERE DeviceId = ?", (device_id,))
                    vulns = cursor.fetchall()
                    if vulns:
                        print("Vulnerabilities found:")
                        for v in vulns:
                            print(f" -> [{v[2].upper()}] {v[1]} (Severity: {v[3]} | Status: {v[4]})")
                    else:
                        print(" -> No vulnerabilities recorded for this device.")
                else:
                    print("No device found with that ID.")
            elif device_choice == 5:
                continue
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

    elif choice == "n":
        print("""
Which type of device would you like to register:
Press 1 for Laptop
Press 2 for Server
Press 3 for Router
Press 4 for Printer
Press 5 to return
        """)
        
        device_types = {1: "Laptop", 2: "Server", 3: "Router", 4: "Printer"}
        try:
            reg_choice = int(input().strip())
            if reg_choice == 5:
                continue
            elif reg_choice in device_types:
                device_type = device_types[reg_choice]
                
                # Gather device input
                device_id = int(input("Insert the Id of the device: "))
                hostname = input("Insert the hostname of the device: ")
                in_charge = input("Insert who is in charge of the device: ")
                sector = input("Insert the sector where the device is located: ")
                
                # Insert Device
                query = "INSERT INTO Devices(Id, Hostname, InCharge, Sector, Type) Values (?,?,?,?,?)"
                cursor.execute(query, (device_id, hostname, in_charge, sector, device_type))
                connection.commit()  # <-- CRITICAL: Save data right after execution
                print(f"Successfully registered the {device_type}!")

                # Vulnerability registration loop
                while True:
                    print("\nDoes the device have any vulnerability to be inserted?\nPress 'Y' for yes\nPress 'N' for no")
                    has_vuln = input().strip().lower()
                    
                    if has_vuln == "y":
                        description = input("Insert the description of the vulnerability: ")
                        category = input("Insert the category of the vulnerability: ")
                        severity = input("Insert the severity of the vulnerability: ")
                        status = input("Insert the status of the vulnerability: ")

                        vuln_query = "INSERT INTO Vulnerabilities(DeviceId, Description, Category, Severity, Status) VALUES (?,?,?,?,?)"
                        cursor.execute(vuln_query, (device_id, description, category, severity, status))
                        connection.commit()  # <-- CRITICAL: Save data right after execution
                        print("Successfully registered the Vulnerability!")
                    elif has_vuln == "n":
                        break
                    else:
                        print("Invalid choice, type Y or N.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please input valid configuration data.")
        except sqlite3.IntegrityError:
            print("Database Error: This Device ID already exists or violates database rules.")
    
    else:
        print("No option selected, try again!")