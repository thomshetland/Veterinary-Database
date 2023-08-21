import mysql.connector as mysql
import sqlalchemy
from sqlalchemy import Integer, String


class GLOBALS:

    POST_CODE_SIZE = 6
    DESCRIPTION_SIZE = 100
    SUPPLY_ID_SIZE = 12
    SUPPLY_TYPE_SIZE = 30
    T_ID_SIZE = 15
    PHONE_SIZE = 11

    # A DICTIONARY CONTAINING INFORMATION ON
    # (Python datatype, MySQL datatype, Auto Increment)
    ID_DATATYPES = {'clinics': [int, Integer, True],
                    'pets': [int, Integer, False],
                    'supplies': [str, String, False],
                    'postcode': [str, String, False],
                    'appointments': [int, Integer, False],
                    'examinations': [int, Integer, False],
                    'invoices': [int, Integer, True],
                    'invoices_paid': [int, Integer, False],
                    'pans': [int, Integer, False],
                    'pet_owners': [int, Integer, False],
                    'pet_stay': [int, Integer, False],
                    'pet_treatments': [int, Integer, False],
                    'pharma_supplies': [str, String, False],
                    'staff': [int, Integer, True],
                    'supply_types': [str, String, False],
                    'treatments': [str, String, False],
                    'tr_requirements': [str, String, False]
                    }


class DatabaseSetup:

    ignore_warning = True

    def __init__(self):
        self.connection = mysql.connect(
            host='localhost',
            user='root',
            password='Viking2002:')

        self.cursor = self.connection.cursor()

        # Stage 0
        self.create_database()
        self.create_table_postcode()
        self.create_table_treatments()
        self.create_table_supply_type()

        # stage 1
        self.create_table_clinic()

        # Stage 2
        self.create_table_pens()
        self.create_table_staff()
        self.create_table_supplies()
        self.create_table_pharmaSupplies()
        self.create_table_treatmentRequirements()

        self.create_table_petOwners()

        # Stage 3
        self.create_table_pets()

        # Stage 4
        self.create_table_petStay()
        self.create_table_examinations()
        self.create_table_appointments()
        self.create_table_invoices()

        # Stage 5
        self.create_table_invoicesPaid()
        self.create_table_petTreatments()

    def create_database(self):
        query = "CREATE DATABASE IF NOT EXISTS emPet"

        self.cursor.execute(query)
        self.connection.commit()

        self.cursor.execute("USE emPet")
        self.connection.commit()

    def create_table_postcode(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS postcode (" \
                "postcode VARCHAR(6) NOT NULL," \
                "area VARCHAR(30) NOT NULL," \
                "PRIMARY KEY(postcode)" \
                ")"

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_clinic(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS clinics(" \
                "id INTEGER AUTO_INCREMENT," \
                "postcode VARCHAR(6)," \
                "street VARCHAR(30)," \
                "telephone VARCHAR(20)," \
                "faxNumber VARCHAR(20)," \
                "PRIMARY KEY(id)," \
                "FOREIGN KEY (postcode) REFERENCES postcode(postcode)" \
                ")"

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_staff(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS staff" \
                "(id INTEGER AUTO_INCREMENT," \
                "clinicID INTEGER," \
                "firstName VARCHAR(30)," \
                "lastName VARCHAR(30)," \
                "street VARCHAR(30)," \
                "postcode VARCHAR({})," \
                "phone VARCHAR({})," \
                "dateOfBirth DATE," \
                "gender VARCHAR(10)," \
                "position VARCHAR(30)," \
                "salary DECIMAL(10, 2)," \
                "ssn VARCHAR(12)," \
                "FOREIGN KEY(postcode) REFERENCES postcode(postcode)," \
                "PRIMARY KEY(id))".format(GLOBALS.POST_CODE_SIZE, GLOBALS.PHONE_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_supplies(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS supplies" \
                "(" \
                "id VARCHAR({}) NOT NULL, " \
                "supplyType VARCHAR({}), " \
                "clinicID INTEGER, " \
                "name VARCHAR(30), " \
                "amountInStock INTEGER, " \
                "unitsAvailable INTEGER, " \
                "price FLOAT, " \
                "description VARCHAR({}), " \
                "reorderLevel INTEGER, " \
                "reorderQuantity INTEGER, " \
                "FOREIGN KEY (clinicID) REFERENCES clinics(id), " \
                "FOREIGN KEY (supplyType) REFERENCES supply_types(supplyType), " \
                "PRIMARY KEY (id) " \
                ")".format(GLOBALS.SUPPLY_ID_SIZE, GLOBALS.SUPPLY_TYPE_SIZE,
                           GLOBALS.DESCRIPTION_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_supply_type(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS supply_types" \
                "(supplyType VARCHAR({}) NOT NULL, " \
                "PRIMARY KEY(supplyType))".format(GLOBALS.SUPPLY_TYPE_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_pharmaSupplies(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS pharma_supplies" \
                "(" \
                "id VARCHAR({}) NOT NULL, " \
                "supplyType VARCHAR({}), " \
                "clinicID INTEGER, " \
                "name VARCHAR(30), " \
                "amountInStock INTEGER, " \
                "unitsAvailable INTEGER, " \
                "price FLOAT, " \
                "description VARCHAR({}), " \
                "reorderLevel INTEGER, " \
                "reorderQuantity INTEGER, " \
                "dosage DECIMAL(8, 2), " \
                "methodOfAdministration VARCHAR({}), " \
                "FOREIGN KEY (clinicID) REFERENCES clinics(id), " \
                "FOREIGN KEY (supplyType) REFERENCES supply_types(supplyType), " \
                "PRIMARY KEY (id) " \
                ")".format(GLOBALS.SUPPLY_ID_SIZE, GLOBALS.SUPPLY_TYPE_SIZE,
                           GLOBALS.DESCRIPTION_SIZE, GLOBALS.DESCRIPTION_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_treatments(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS treatments" \
                "(id VARCHAR(10) NOT NULL," \
                "price DECIMAL(10, 2)," \
                "description VARCHAR(100)," \
                "PRIMARY KEY(id))"

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_treatmentRequirements(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS tr_requirements " \
                "(" \
                "treamentID VARCHAR({})," \
                "supplyID VARCHAR({})," \
                "supplyType VARCHAR({})," \
                "unitsRequired INTEGER," \
                "PRIMARY KEY(treamentID)," \
                "FOREIGN KEY(TreamentID) REFERENCES treatments(id)" \
                ")".format(GLOBALS.T_ID_SIZE, GLOBALS.SUPPLY_ID_SIZE, GLOBALS.SUPPLY_TYPE_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_petOwners(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS pet_owners " \
                "(" \
                "id INTEGER NOT NULL, " \
                "clinicID INTEGER NOT NULL, " \
                "firstName VARCHAR(30), " \
                "lastName VARCHAR(30), " \
                "phone VARCHAR({}), " \
                "street VARCHAR(30), " \
                "postcode VARCHAR({}), " \
                "PRIMARY KEY(id, clinicID)," \
                "FOREIGN KEY(clinicID) REFERENCES clinics(id)" \
                ")".format(GLOBALS.PHONE_SIZE, GLOBALS.POST_CODE_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_pets(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS pets" \
                "(" \
                "id INTEGER NOT NULL," \
                "clinicID INTEGER, " \
                "ownerID INTEGER, " \
                "typeOfPet VARCHAR(20), " \
                "dateOfBirth DATE, " \
                "description VARCHAR({}), " \
                "dateRegistered DATE, " \
                "currentSatus VARCHAR(20), " \
                "FOREIGN KEY(clinicID) REFERENCES clinics(id)," \
                "FOREIGN KEY (ownerID) REFERENCES pet_owners(id)," \
                "PRIMARY KEY(id, clinicID)" \
                ")".format(GLOBALS.DESCRIPTION_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_examinations(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS examinations " \
                "(" \
                "id INTEGER NOT NULL," \
                "clinicID INTEGER," \
                "datetime DATETIME," \
                "vetID INTEGER," \
                "petID INTEGER," \
                "description VARCHAR({})," \
                "FOREIGN KEY (clinicID) REFERENCES clinics(id)," \
                "FOREIGN KEY (petID) REFERENCES pets(id)," \
                "FOREIGN KEY (vetID) REFERENCES staff(id)," \
                "PRIMARY KEY(id, clinicID))" \
                "".format(GLOBALS.DESCRIPTION_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_petTreatments(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS pet_treatments (" \
                "id INTEGER NOT NULL, " \
                "clinicID INTEGER NOT NULL, " \
                "treatmentID VARCHAR(10) NOT NULL, " \
                "examinationID INTEGER NOT NULL, " \
                "petID INTEGER NOT NULL, " \
                "comments VARCHAR({}), " \
                "description VARCHAR({}), " \
                "treatmentQuantity INTEGER NOT NULL, " \
                "startDate DATE NOT NULL, " \
                "endDate DATE NOT NULL, " \
                "FOREIGN KEY (clinicID) REFERENCES clinics(id), " \
                "FOREIGN KEY (treatmentID) REFERENCES treatments(id), " \
                "FOREIGN KEY (examinationID) REFERENCES examinations(id), " \
                "FOREIGN KEY (petID) REFERENCES pets(id), " \
                "PRIMARY KEY(ID)" \
                ")".format(GLOBALS.DESCRIPTION_SIZE, GLOBALS.DESCRIPTION_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_appointments(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS appointments" \
                "(" \
                "id INTEGER NOT NULL," \
                "clinicID INTEGER, " \
                "ownerID INTEGER, " \
                "petID INTEGER, " \
                "datetime DATETIME, " \
                "FOREIGN KEY(clinicID) REFERENCES clinics(id)," \
                "FOREIGN KEY (ownerID) REFERENCES pet_owners(id)," \
                "FOREIGN KEY (petID) REFERENCES pets(id)," \
                "PRIMARY KEY(id, clinicID)" \
                ")".format(GLOBALS.DESCRIPTION_SIZE)

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_invoices(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS invoices (" \
                "id INTEGER AUTO_INCREMENT, " \
                "treatmentID VARCHAR(10), " \
                "petID INTEGER, " \
                "ownerID INTEGER, " \
                "date DATE , " \
                "FOREIGN KEY(treatmentID) REFERENCES treatments(id), " \
                "FOREIGN KEY(petID) REFERENCES pets(id), " \
                "FOREIGN KEY(ownerID) REFERENCES pet_owners(id), " \
                "PRIMARY KEY(id)" \
                ")"

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_invoicesPaid(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS invoices_paid (" \
                "id INTEGER NOT NULL, " \
                "paid BOOLEAN NOT NULL, " \
                "datePaid DATE NOT NULL, " \
                "paymentType VARCHAR(10) NOT NULL, " \
                "FOREIGN KEY (id) REFERENCES invoices(id), " \
                "PRIMARY KEY(id)" \
                ")"

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_pens(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS pens" \
                "(id INTEGER NOT NULL," \
                "clinicID INTEGER, " \
                "capacity INTEGER," \
                "availability INTEGER," \
                "closed BOOLEAN," \
                "FOREIGN KEY(clinicID) REFERENCES clinics(id)," \
                "PRIMARY KEY(id))"

        self.cursor.execute(query)
        self.connection.commit()

    def create_table_petStay(self):
        self.ignore_warning = True

        query = "CREATE TABLE IF NOT EXISTS pet_stay (" \
                "id INTEGER NOT NULL, " \
                "treatmentID VARCHAR(10), " \
                "petID INTEGER, " \
                "penID INTEGER, " \
                "date DATE, " \
                "comments VARCHAR({}), " \
                "FOREIGN KEY (petID) REFERENCES pets(id), " \
                "FOREIGN KEY (penID) REFERENCES pens(id), " \
                "FOREIGN KEY (treatmentID) REFERENCES treatments(id), " \
                "PRIMARY KEY(id)" \
                ")".format(GLOBALS.DESCRIPTION_SIZE)

        self.cursor.execute(query)
        self.connection.commit()


if __name__ == "__main__":
    database = DatabaseSetup()
