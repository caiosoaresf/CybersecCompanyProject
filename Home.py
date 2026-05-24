import sqlite3
import shutil

#Creating the Database
connection = sqlite3.connect("Database.db")
cursor = connection.cursor()


cursor.execute("PRAGMA foreign_keys = ON;")

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
    Description TEXT NOT NULL,
    Category TEXT NOT NULL,
    Severity TEXT NOT NULL,
    Status TEXT NOT NULL,
    FOREIGN KEY(DeviceId) REFERENCES Devices(Id) ON DELETE CASCADE ON UPDATE NO ACTION);
""")

#First user interface
columns = shutil.get_terminal_size().columns

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
Press "Y/y" if you Do
Press "N/n" if you Don't
Press "B/b" if you want to leave
    """)

    choice = input().strip().lower()

    if (choice == "b"):
        close_program()

    elif (choice == "y"):
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
            choice = int(input().strip())
        except Exception:
            print("Hi")        

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
                choice = int(input().strip()) 
                if choice == 5:
                    break

                elif (choice == 1 or choice == 2 or choice == 3 or choice == 4):
                    
                    Hostname = input("Insert the hostname of the device: ")
                    InCharge = input("Insert who is in charge of the device: ")
                    Sector = input("Insert the sector where the device is located: ")
                    Type = types[choice]

                    query = "INSERT INTO Devices(Hostname,InCharge,Sector,Type) Values (?,?,?,?)"
                    cursor.execute(query, (Hostname,InCharge,Sector,Type))
                    print("Successfully registered the Device")

                    while True:
                        print("""
Does the device have any vulnerability to be inserted?
Press "Y" or "y" for yes
Press "N" or "n" for no
                            """)

                        choice = input().strip().lower()

                        if (choice == "n"):
                            break

                        elif (choice == "y"):
                            GeneratedId = cursor.lastrowid
                            Description = input("Insert the description of the vulnerability: ")
                            Category = input("Insert the category of the vulnerability: ")
                            Severity = input("Insert the severity of the vulnerability: ")
                            Status = input("Insert the status of the vulnerability: ")

                            query = "INSERT INTO Vulnerabilities(DeviceId,Description,Category,Severity,Status) VALUES (?,?,?,?,?)"
                            cursor.execute(query, (GeneratedId,Description,Category,Severity,Status))
                            print("Successfully registered the vulnerability")
                        
                        else:
                            print("This option doesn't exist")
                else:
                    print("This option doesn't exist")
            except ValueError:
                print("This option doesn't exist")     
    else:
        print("Typing error")