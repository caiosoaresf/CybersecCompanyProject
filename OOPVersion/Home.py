import sqlite3
import shutil
import json

#Implementation of Device
class Devices:
    def __init__(self,Id,Hostname,InCharge,Sector,Type,Vulnerabilities=None):
        self.Id = Id
        self.Hostname = Hostname
        self.InCharge = InCharge
        self.Sector = Sector
        self.DeviceType = Type
        self.Vulnerabilities = Vulnerabilities if Vulnerabilities is not None else []

#Implementation of Database and CRUD
class Database:
    def __init__(self,Db="Database.db"):
        self.connection = sqlite3.connect(Db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Devices(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Hostname TEXT NOT NULL,
                InCharge TEXT NOT NULL,
                Sector TEXT NOT NULL,
                Type TEXT NOT NULL,
                Vulnerabilities TEXT DEFAULT '[]'
            );
        """)
        self.connection.commit()

    def create(self,Hostname,InCharge,Sector,Type):
        query = "INSERT INTO Devices(Hostname,InCharge,Sector,Type) Values (?,?,?,?)"
        self.cursor.execute(query,(Hostname,InCharge,Sector,Type))
        self.connection.commit()
        ID = self.cursor.lastrowid
        print(f"Successfully registered the Device with ID: ({ID},)")

    def read(self, Id, Type):
        self.cursor.execute("SELECT * FROM Devices WHERE Id = ? AND Type = ?", (Id, Type))
        row = self.cursor.fetchone()
        if row:
            return Devices(row[0],row[1],row[2],row[3],row[4],json.loads(row[5]))
        return None

    def update(self, Id, NewHostname, NewInCharge, NewSector, Type, VulnerabilitiesList):
        VulnerabilitiesJson = json.dumps(VulnerabilitiesList)
        query = "UPDATE Devices SET Hostname = ?, InCharge = ?, Sector = ?, Type = ?, Vulnerabilities = ? WHERE Id = ?"
        self.cursor.execute(query,(NewHostname,NewInCharge,NewSector,Type,VulnerabilitiesJson,Id))
        self.connection.commit()
        print("Successfully updated the data")

    def delete(self, Id):
        self.cursor.execute("DELETE FROM Devices WHERE Id = ?", (Id,))
        self.connection.commit()
        print("Successfully deleted, returning to Device selection")

#Implementation of Main
class Main:
    def __init__(self):
        self.db = Database()
        self.columns = shutil.get_terminal_size().columns
        self.types = {1: "Laptop",2: "Server",3: "Router",4: "Printer"}

    def close(self):
        print("All done here. See you later".center(self.columns))
        self.db.connection.commit()
        self.db.connection.close()
        exit()

    def start(self):
        print("Welcome to Security©".center(self.columns))
        print("*We are a large company that ensures your electronical devices are safe*".center(self.columns))

        while True:
            print("""
Do you already have devices registered in our system?
Press "y" if you do
Press "n" if you don't or want to register new devices/Vulnerabilities
Press "b" if you want to leave
            """)

            choice = input().strip().lower()

            if choice == "b":
                self.close()

            elif choice == "y":
                self.check()

            elif choice == "n":
                self.register()

            else:
                print("Typing error")

    def check(self):
        while True:
            print("""
Which type of device would you like to check:
Press "1" for Laptop
Press "2" for Server
Press "3" for Router
Press "4" for Printer
Press "5" to return
            """)
            try:
                option = int(input().strip())
                if option == 5:
                    break

                elif option in [1, 2, 3, 4]:
                    while True:
                        try:
                            id = int(input("\nInsert the ID of the device you would like to check or press '0' to leave:\n").strip())
                            if id == 0:
                                break

                            device = self.db.read(id, self.types[option])

                            if device:
                                print((device.Id, device.Hostname, device.InCharge, device.Sector, device.DeviceType))

                                while True:
                                    choice = input("\nWould you like to check the Vulnerabilities list too? (y/n):\n").strip().lower()
                                    if choice == "n":
                                        break
                                    elif choice == "y":
                                        if device.Vulnerabilities:
                                            for idx, vuln in enumerate(device.Vulnerabilities, start=1):
                                                print((id, idx, vuln['Description'], vuln['Category'], vuln['Severity'], vuln['Status']))
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

                                    if choice == "r":
                                        break

                                    elif choice == "u":
                                        NewHostname = input("\nInsert the new hostname of the device: ")
                                        NewInCharge = input("Insert who is the new person in charge of the device: ")
                                        NewSector = input("Insert the new sector where the device is located: ")
                                        try:
                                            NewType = int(input("Insert the new type of device(number): "))
                                            Type = self.types[NewType]
                                            if NewType != option:
                                                print("OBS device type was changed, after operations return to device selection to select the new type")
                                        except ValueError:
                                            print("This is not a number")
                                            continue

                                        VulnerabilitiesList = device.Vulnerabilities

                                        while True:
                                            choice = input("\nWould you like to update the Vulnerabilities too? (y/n):\n").strip().lower()
                                            if choice == "n":
                                                break
                                            elif choice == "y":
                                                while True:
                                                    try:
                                                        VulnId = int(input("\nInsert the VulnId of the vulnerability you would like to change:\n").strip())
                                                        if VulnId <= 0 or VulnId > len(VulnerabilitiesList):
                                                            print("VulnId doesn't exist, returning")
                                                            continue
                                                    except ValueError:
                                                        print("This is not a number, returning to vulnerability update")
                                                        continue

                                                    NewDescription = input("\nInsert the new description of the vulnerability: ")
                                                    NewCategory = input("Insert the new category of the vulnerability: ")
                                                    NewSeverity = input("Insert the new severity of the vulnerability: ")
                                                    NewStatus = input("Insert the new status of the vulnerability: ")

                                                    VulnerabilitiesList[VulnId - 1] = {
                                                        "Description": NewDescription,
                                                        "Category": NewCategory,
                                                        "Severity": NewSeverity,
                                                        "Status": NewStatus
                                                    }
                                                    print("Successfully updated the vulnerability")
                                                    break
                                            else:
                                                print("Invalid option")

                                        self.db.update(id,NewHostname,NewInCharge,NewSector,Type,VulnerabilitiesList)
                                        break

                                    elif choice == "d":
                                        self.db.delete(id)
                                        break
                                    else:
                                        print("This option doesn't exist")
                            else:
                                print("Id not found")

                        except ValueError:
                            print("This is not a number")
                            continue
                else:
                    print("This option doesn't exist")
            except ValueError:
                print("This is not a number")

    def register(self):
        while True:
            print("""
Which type of device would you like to register:
Press "1" for Laptop
Press "2" for Server
Press "3" for Router
Press "4" for Printer
Press "5" to return
            """)
            try:
                option = int(input().strip())
                if option == 5:
                    break

                elif option in [1, 2, 3, 4]:
                    while True:
                        print("""
What would you like to insert
Press "d" for new device
Press "v" for new vulnerability
Press "r" to return
                        """)
                        choice = input().strip().lower()

                        if choice == "r":
                            break

                        elif choice == "d":
                            Hostname = input("\nInsert the hostname of the device: ")
                            InCharge = input("Insert who is in charge of the device: ")
                            Sector = input("Insert the sector where the device is located: ")
                            Type = self.types[option]

                            GeneratedId = self.db.create(Hostname,InCharge,Sector,Type)
                            VulnerabilitiesList = []

                            while True:
                                print("\nDoes the device have any vulnerability to be inserted? (y/n)\n")
                                choice = input().strip().lower()

                                if choice == "n":
                                    break
                                elif choice == "y":
                                    Description = input("\nInsert the description of the vulnerability: ")
                                    Category = input("Insert the category of the vulnerability: ")
                                    Severity = input("Insert the severity of the vulnerability: ")
                                    Status = input("Insert the status of the vulnerability: ")

                                    VulnerabilitiesList.append({
                                        "Description": Description,
                                        "Category": Category,
                                        "Severity": Severity,
                                        "Status": Status
                                    })
                                    print(f"Successfully registered the vulnerability with VulnID ({len(VulnerabilitiesList)},)")
                                else:
                                    print("This option doesn't exist")
                            
                            self.db.update(GeneratedId,Hostname,InCharge,Sector,Type,VulnerabilitiesList)

                        elif choice == "v":
                            try:
                                id = int(input("\nInsert the ID of the device you would like to add a vulnerability or '0' to leave:\n").strip())
                                if id == 0:
                                    break

                                self.db.cursor.execute("SELECT * FROM Devices WHERE Id = ?", (id,))
                                row = self.db.cursor.fetchone()

                                if not row:
                                    print("ID doesn't exist, returning")
                                    continue

                                Description = input("\nInsert the description of the vulnerability: ")
                                Category = input("Insert the category of the vulnerability: ")
                                Severity = input("Insert the severity of the vulnerability: ")
                                Status = input("Insert the status of the vulnerability: ")

                                Vulns = json.loads(row[5])
                                Vulns.append({
                                    "Description": Description,
                                    "Category": Category,
                                    "Severity": Severity,
                                    "Status": Status
                                })

                                self.db.update(row[0], row[1], row[2], row[3], row[4], Vulns)
                                print(f"Successfully registered the vulnerability with VulnID {len(Vulns)}")

                            except ValueError:
                                print("This is not a number")
                                continue
                        else:
                            print("This option doesn't exist")
                else:
                    print("This option doesn't exist")
            except ValueError:
                print("This is not a number")

app = Main()
app.start()