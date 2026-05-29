import sqlite3
import shutil

#Creating the Database
connection = sqlite3.connect("Database.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

#Can be removed if a permanent database is required
cursor.execute("DROP TABLE IF EXISTS Devices")
cursor.execute("DROP TABLE IF EXISTS Vulnerabilities")

cursor.execute("""
CREATE TABLE Devices(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Hostname TEXT NOT NULL,
    InCharge TEXT NOT NULL,
    Sector TEXT NOT NULL,
    Type TEXT NOT NULL);     
""")

cursor.execute("""
CREATE TABLE Vulnerabilities(
    DeviceId INT,
    VulnId INTEGER PRIMARY KEY AUTOINCREMENT,
    Description TEXT NOT NULL,
    Category TEXT NOT NULL,
    Severity TEXT NOT NULL,
    Status TEXT NOT NULL,
    FOREIGN KEY(DeviceId) REFERENCES Devices(Id) ON DELETE CASCADE ON UPDATE NO ACTION);
""")

columns = shutil.get_terminal_size().columns

#Main user interface
def close_program():
    print("All done here. See you later".center(columns))
    connection.commit()
    connection.close()
    exit()

print("Welcome to Security©".center(columns))
print("*We are a large company that ensures your electronical devices are safe*".center(columns))

while True:
    print("""
Do you already have devices registered in our system?
Press "y" if you do
Press "n" if you don't or want to register new devices/vulnerabilities
Press "b" if you want to leave
    """)

    choice = input().strip().lower()

    if (choice == "b"):
        close_program()

    elif (choice == "y"):
        while True:
            print("""
Which type of device would you like to check:
Press 1 for Laptop
Press 2 for Server
Press 3 for Router
Press 4 for Printer
Press 5 to return
            """)

#Implementation of dictionary since SQL makes them useless here
            types = {1: "Laptop", 2: "Server", 3: "Router", 4: "Printer"}
            
            try:
                option = int(input().strip())
                if option == 5:
                    break

#Implementation of Read
                elif (option == 1 or option == 2 or option == 3 or option == 4):
                    while True:
                        try: 
                            id = int(input("\nInsert the ID of the device you would like to check or press '0' to leave:\n").strip())
                            cursor.execute("SELECT * FROM Devices WHERE Id = ? AND Type = ?" , (id,types[option]))
                            rows = cursor.fetchall()
                            
                            if (id == 0):
                                break

                            elif rows:
                                for row in rows:
                                    print(row)
                            
                                while True:
                                    choice = input("\nWould you like to check the vulnerabilities list too? (y/n):\n").strip().lower()

                                    if (choice == "n"):
                                        break

                                    elif (choice == "y"):
                                        cursor.execute("SELECT * FROM Vulnerabilities WHERE DeviceId = ?", (id,))
                                        rows = cursor.fetchall()
                                        if rows:
                                            for row in rows:
                                                print(row)
                                        else:
                                            print("There are no vulnerabilites registered for this ID")

                                    else:
                                        print("Invalid option")

                                while True:
                                    print("""
Would you like to do any operation with this data?
Press "u" to update the data
Press "d" to delete the data
Press "r" to return to device selection
                                                """)
                                    choice = input().strip().lower()

                                    if (choice == "r"):
                                        break
                                    
#Implementation of Update
                                    elif (choice == "u"):
                                        NewHostname = input("\nInsert the new hostname of the device: ")
                                        NewInCharge = input("Insert who is the new person in charge of the device: ")
                                        NewSector = input("Insert the new sector where the device is located: ")
                                        try: 
                                            NewType = int(input("Insert the new type of device(number): "))
                                            Type = types[NewType]
                                            if (NewType != option):
                                                print("OBS device type was changed, after operations return to device selection to select the new type")
                                        
                                        except ValueError:
                                            print("This is not a number")
                                            continue
                                        
                                        query = "UPDATE Devices SET Hostname = ?, InCharge = ?, Sector = ?, Type = ? WHERE Id = ?"
                                        cursor.execute(query, (NewHostname,NewInCharge,NewSector,Type,id))
                                        connection.commit()
                                        print("Successfully updated the data")

                                        while True:
                                            choice = input("\nWould you like to update the vulnerabilities too? (y/n):\n").strip().lower()
                                            
                                            if(choice == "n"):
                                                break
                                            
                                            elif (choice == "y"):
                                                while True:
                                                    try:
                                                        VulnId = int(input("\nInsert the VulnId of the vulnerability you would like to change:\n").strip())
                                                        cursor.execute("SELECT 1 FROM Vulnerabilities WHERE VulnId = ?", (VulnId,))
                                                        
                                                        if not cursor.fetchone():
                                                            print("VulnId doesn't exist, returning")
                                                            continue

                                                    except ValueError:
                                                        print("This is not a number, returning to vulnerability update")
                                                        continue

                                                    NewDescription = input("\nInsert the new description of the vulnerability: ")
                                                    NewCategory = input("Insert the new category of the vulnerability: ")
                                                    NewSeverity = input("Insert the new severity of the vulnerability: ")
                                                    NewStatus = input("Insert the new status of the vulnerability: ")

                                                    query = "UPDATE Vulnerabilities SET Description = ?, Category = ?, Severity = ?, Status = ? WHERE VulnId = ?"
                                                    cursor.execute(query, (NewDescription,NewCategory,NewSeverity,NewStatus,VulnId))
                                                    connection.commit()
                                                    print("Successfully updated the vulnerability")
                                                    break
                                            
                                            else:
                                                print("Invalid option")

#Implementation of Delete
                                    elif (choice == "d"):
                                        cursor.execute("DELETE FROM Devices WHERE Id = ?", (id,))
                                        connection.commit()
                                        print("Successfully deleted, returning to Device selection")
                                        break

                                    else:
                                        print(("This option doesn't exist"))
                            
                            else:
                                print("Id not found")
                        
                        except ValueError:
                            print("This is not a number")
                            continue
            
            except ValueError:
                print("This is not a number")       

    elif (choice == "n"):
        while True:
            print("""
Which type of device would you like to register:
Press 1 for Laptop
Press 2 for Server
Press 3 for Router
Press 4 for Printer
Press 5 to return
            """)
#Implementation of dictionary since SQL makes them useless here
            types = {1: "Laptop", 2: "Server", 3: "Router", 4: "Printer"}

            try:
                option = int(input().strip()) 
                
                if option == 5:
                    break

#Implementation of Create
                elif (option == 1 or option == 2 or option == 3 or option == 4):
                    
                    while True:
                        print("""
What would you like to insert
Press d for new device
Press v for new vulnerability
Press r to return
                        """)

                        choice = input().strip().lower()

                        if (choice == "r"):
                            break

                        elif (choice == "d"):
                            Hostname = input("\nInsert the hostname of the device: ")
                            InCharge = input("Insert who is in charge of the device: ")
                            Sector = input("Insert the sector where the device is located: ")
                            Type = types[option]

                            query = "INSERT INTO Devices(Hostname,InCharge,Sector,Type) Values (?,?,?,?)"
                            cursor.execute(query, (Hostname,InCharge,Sector,Type))
                            connection.commit()
                            cursor.execute("SELECT Id FROM Devices WHERE Type = ?", (types[option],))
                            ID = cursor.fetchone()
                            print(f"Successfully registered the Device with ID: {ID}")

                            while True:
                                print("\nDoes the device have any vulnerability to be inserted? (y/n)\n")
                                choice = input().strip().lower()

                                if (choice == "n"):
                                    break

                                elif (choice == "y"):
                                    GeneratedId = cursor.lastrowid
                                    Description = input("\nInsert the description of the vulnerability: ")
                                    Category = input("Insert the category of the vulnerability: ")
                                    Severity = input("Insert the severity of the vulnerability: ")
                                    Status = input("Insert the status of the vulnerability: ")

                                    query = "INSERT INTO Vulnerabilities(DeviceId,Description,Category,Severity,Status) VALUES (?,?,?,?,?)"
                                    cursor.execute(query, (GeneratedId,Description,Category,Severity,Status))
                                    connection.commit()
                                    cursor.execute("SELECT VulnId FROM Vulnerabilities WHERE DeviceId = ?", (ID[0],))
                                    VulnID = cursor.fetchone()
                                    print(f"Successfully registered the vulnerability with VulnID {VulnID}")
                                
                                else:
                                    print("This option doesn't exist")
                            
                        elif (choice == "v"):
                            try:
                                id = int(input("\nInsert the ID of the device you would like to add a vulnerability or '0' to leave: \n").strip())
                                cursor.execute("SELECT 1 FROM Devices WHERE Id = ?" , (id,))

                                if (id == 0):
                                    break

                                if not cursor.fetchone():
                                    print("ID doesn't exist, returning")
                                    continue

                                Description = input("\nInsert the description of the vulnerability: ")
                                Category = input("Insert the category of the vulnerability: ")
                                Severity = input("Insert the severity of the vulnerability: ")
                                Status = input("Insert the status of the vulnerability: ")

                                query = "INSERT INTO Vulnerabilities(DeviceId,Description,Category,Severity,Status) VALUES (?,?,?,?,?)"
                                cursor.execute(query, (id,Description,Category,Severity,Status))
                                connection.commit()
                                cursor.execute("SELECT VulnId FROM Vulnerabilities WHERE DeviceId = ?", (id,))
                                VulnID = cursor.lastrowid
                                print(f"Successfully registered the vulnerability with VulnID {VulnID}")    

                            except ValueError:
                                print("This is not a number")
                                continue

                        else:
                            print("This option doesn't exist")
                else:
                    print("This option doesn't exist")

            except ValueError:
                print("This is not a number")  

    else:
        print("Typing error")
