import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, String, Integer, Float, Date, Boolean, create_engine, ForeignKey, Time, DateTime

Base = declarative_base()


# Just a helper function to avoid typing primary_key = True all the time
def Primary_key(dataType, foreignKey=None, autoincrement=False):
    if autoincrement:
        if foreignKey is not None:
            return Column(dataType, foreignKey, primary_key=True, autoincrement=autoincrement)

        return Column(dataType, primary_key=True, autoincrement=autoincrement)

    if foreignKey is not None:
        return Column(dataType, foreignKey, primary_key=True)

    return Column(dataType, primary_key=True)

# engine = create_engine("sqlite:///bookplace2.sqlite", echo=False)
# Session = sessionmaker(bind=engine)


# A separate table keeping track of all postcodes and their corresponding cities and areas
class PostCode(Base):  # Stage 0 DONE
    __tablename__ = "postcode"
    post_code = Primary_key(dataType=String)
    area = Column(String)

    def __init__(self):
        super().__init__()


# A separate table keeping track of all clinics within the franchise/database
class Clinic(Base):  # Stage 1 DONE
    __tablename__ = "clinc"
    ID = Primary_key(dataType=Integer, autoincrement=True)
    postcode = Column(String, ForeignKey(PostCode.post_code))

    street = Column(String)
    telephone = Column(String)
    faxNumber = Column(String)

    def __init__(self):
        super().__init__()


# A separate table keeping track of all staff members and their related information
# for each clinic, allowing us to pinpoint a specific staff member at a specific clinic
class Staff(Base):  # Stage 2 DONE
    __tablename__ = "staff"
    ID = Primary_key(dataType=Integer, autoincrement=True)
    clinc_id = Column(Integer, ForeignKey(Clinic.ID))
    post_code = Column(String, ForeignKey(PostCode.post_code))

    first_name = Column(String)
    last_name = Column(String)
    street = Column(String)
    phone = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    position = Column(String)
    salary = Column(Float)
    ssn = Column(String)

    clinic = relationship("Clinic")

    def __init__(self):
        super().__init__()


# A separate table keeping track of the various supply types
# allowing us to expand if needed
class SupplyTypes(Base):  # Stage 1 DONE
    __tablename__ = "supplyTypes"
    supplyType = Primary_key(dataType=String)

    def __init__(self):
        super().__init__()


# A separate table that handles all the non-pharmaceutical supplies
# which does not require dosage and administration information
# We chose to do it this way to avoid empty cells within the table
# and to avoid adding unnecessary complexity in terms of
# performing queries and maintenance
class Supplies(Base):  # Stage 2 DONE
    __tablename__ = "supplies"
    ID = Primary_key(dataType=String)
    supplyType = Primary_key(dataType=String, foreignKey=ForeignKey(SupplyTypes.supplyType))
    clinic_id = Column(Integer, ForeignKey(Clinic.ID))
    name = Column(String)
    amountInStock = Column(Integer)
    units_available = Column(Integer)
    price = Column(Float)
    description = Column(String)
    reorder_level = Column(Integer)
    reorder_quantity = Column(Integer)

    def __init__(self):
        super().__init__()


# A separate table that handles all the non-pharmaceutical supplies
# which does not require dosage and administration information
# Additionally we introduced the term units available in order to convert from dosages
# to how many times that dosage can be applied in the various treatments.
# As a result we added some complexity in terms of maintenance, meaning in order to update
# the quantity and units available we'll have to subtract the units consumed from the units previously available
# and subtract the dosage multiplied by the units consumed from the quantity in stock
class PharmaSupplies(Base):  # Stage 2 DONE
    __tablename__ = "pharmaSupplies"
    ID = Primary_key(dataType=String)
    supplyType = Primary_key(dataType=String, foreignKey=ForeignKey(SupplyTypes.supplyType))

    clinic_id = Column(Integer, ForeignKey(Clinic.ID))
    name = Column(String)
    amountInStock = Column(Integer)
    price = Column(Float)
    description = Column(String)
    reorder_level = Column(Integer)
    reorder_quantity = Column(Integer)
    dosage = Column(String)
    units_available = Column(Integer)
    methodOfAdministration = Column(String)

    def __init__(self):
        super().__init__()


# A separate table that handles all the various types of treatments
# offered by the various clinics, notice that all clinics offer the same treatments
# so structuring the database in this way allows for easy maintenance
# in terms of treatments, even as the database grows
class Treatments(Base):  # Stage 0 DONE
    __tablename__ = "treatments"
    ID = Primary_key(dataType=String)
    price = Column(Float)
    description = Column(String)

    def __init__(self):
        super().__init__()


# A separate table that handles all the various types of requirements
# for a specific treatment, notice there's a many-to-many relationship
# among the various types of treatments and supplies.
# Structuring the database in this way allows us to know exactly which resources
# go into each treatment, and therefore update our inventory accordingly as the
# treatments are performed or appointed for.
# Assuring the integrity and consistency within our inventory.

# Again we to aim to maintain the density within our tables
# keeping empty cells to a minimum, and therefore structuring the table in this way

# Working in terms of units we eliminate the need to convert between measurements / dosages
# in places other than the tables concerning supplies
class TreatmentRequirements(Base):  # Stage 2 DONE
    __tablename__ = "TRRequirements"

    treatment_ID = Primary_key(dataType=String, foreignKey=ForeignKey(Treatments.ID))
    supply_ID = Primary_key(dataType=String)

    supply_type = Column(String, ForeignKey(SupplyTypes.supplyType))
    units = Column(Integer)

    """
    supply_ID = Column(String)
    pharma_supply_ID = Column(String)

    supply_quantity = Column(Integer)
    pharma_supply_quantity = Column(Integer)
    """

    def __init__(self):
        super().__init__()


# A separate table that handles all information regarding pet owners
class PetOwners(Base):  # Stage 2 DONE
    __tablename__ = "petOwners"

    # Composite keys since the owner number is unique to a particular clinic
    ID = Primary_key(dataType=Integer)
    clinic_id = Primary_key(dataType=Integer, foreignKey=ForeignKey(Clinic.ID))

    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)

    street = Column(String)
    postal_code = Column(String, ForeignKey(PostCode.post_code))

    def __init__(self):
        super().__init__()


# A separate table that handles all information regarding pets and linking it to their owners
class Pets(Base):  # Stage 3 DONE
    __tablename__ = "pets"

    # Composite keys since the pet number is unique to a particular clinic
    ID = Primary_key(dataType=Integer)
    clinic_id = Primary_key(dataType=Integer, foreignKey=ForeignKey(Clinic.ID))
    owner_id = Column(Integer, ForeignKey(PetOwners.ID))

    type_of_pet = Column(String)
    date_of_birth = Column(Date)
    description = Column(String)
    date_registered = Column(Date)
    current_status = Column(String)

    def __init__(self):
        super().__init__()


# A separate table that handles all information regarding examinations
# we chose use composite keys since that allows us
# to keep the examination numbers unique for each clinic
class Examinations(Base):  # Stage 4 DONE

    __tablename__ = "examinations"

    # Composite keys since the examination number is unique to a particular clinic
    ID = Primary_key(dataType=Integer)
    clinic_id = Primary_key(dataType=Integer, foreignKey=ForeignKey(Clinic.ID))
    dateTime = Column(DateTime)
    vet_id = Column(Integer, ForeignKey(Staff.ID))
    pet_id = Column(Integer, ForeignKey(Pets.ID))

    description = Column(String)

    vet = relationship("Staff", backref="staff.ID")
    pet = relationship("Pets", backref="pets.ID")

    # type_of_pet = None
    # pet_name = None
    # vet_name = None

    def __init__(self):
        super().__init__()


# A separate table that handles all information regarding pet treatments, this table
# has a composite key made up of 3 components allowing us to record all treatments that were
# suggested given a specific examination id
class PetTreatments(Base):  # Stage 5 DONE

    __tablename__ = "petTreatments"

    ID = Primary_key(dataType=Integer)  # pet treatment ID
    clinic_id = Primary_key(dataType=Integer, foreignKey=ForeignKey(Clinic.ID))
    treatment_id = Primary_key(dataType=String, foreignKey=ForeignKey(Treatments.ID))
    examination_id = Column(Integer, ForeignKey(Examinations.ID))

    pet_id = Column(Integer, ForeignKey(Pets.ID))

    comments = Column(String)
    description = Column(String)

    treatment_quantity = Column(Integer)

    start_date = Column(Date)
    end_date = Column(Date)

    pet = relationship("Pets", backref="Pets.ID")
    examination = relationship("Examinations", backref="Examinations.ID")
    treatment = relationship("Treatments", backref="Treatments.ID")

    def __init__(self):
        super().__init__()


# A separate table that handles all appointments, across all clinics,
# again through the use of composite keys to ensure that we keep
# certain identifiers unique for each clinic
class Appointments(Base):  # Stage 4 DONE
    __tablename__ = "appointments"
    ID = Primary_key(dataType=Integer)
    clinic_id = Primary_key(dataType=Integer, foreignKey=ForeignKey(Clinic.ID))
    pet_id = Column(Integer, ForeignKey(Pets.ID))
    owner_id = Column(Integer, ForeignKey(PetOwners.ID))

    dateTime = Column(DateTime)

    pet = relationship("Pets")
    owner = relationship("PetOwners")

    def __init__(self):
        super().__init__()


# A separate table that handles all invoices, across all clinics
class Invoices(Base):  # Stage 4 DONE
    __tablename__ = "invoices"
    ID = Primary_key(dataType=Integer, autoincrement=True)
    treatment_id = Primary_key(dataType=String, foreignKey=ForeignKey(Treatments.ID))
    pet_id = Column(Integer, ForeignKey(Pets.ID))
    owner_id = Column(Integer, ForeignKey(PetOwners.ID))
    date = Column(Date)

    pet = relationship("Pets")
    owner = relationship("PetOwners")
    treatment = relationship("Treatments")

    def __init__(self):
        super().__init__()


# A separate table that handles all invoices paid, across all clinics
class InvoicesPaid(Base):  # Stage 4 DONE
    __tablename__ = "invoicesPaid"
    ID = Primary_key(dataType=Integer, foreignKey=ForeignKey(Invoices.ID))

    paid = Column(Boolean)
    date_paid = Column(Date)
    payment_type = Column(String)

    def __init__(self):
        super().__init__()


# A separate table that handles all pens, across all clinics
class Pens(Base):  # Stage 2 DONE
    __tablename__ = "pens"
    ID = Primary_key(dataType=Integer)
    clinic_id = Primary_key(dataType=Integer, foreignKey=ForeignKey(Clinic.ID))
    capacity = Column(Integer)
    closed = Column(Boolean)
    availability = Column(Integer)

    def __init__(self):
        super().__init__()


# A separate table that handles all pens stay, across all clinics
class PetStay(Base):  # Stage 3 DONE
    __tablename__ = "petStay"

    ID = Primary_key(dataType=Integer)
    treatment_id = Primary_key(dataType=String, foreignKey=ForeignKey(Treatments.ID))
    pet_id = Column(Integer, ForeignKey(Pets.ID))
    pen_id = Column(Integer, ForeignKey(Pens.ID))
    date = Column(Date)

    comments = Column(String)
    pet = relationship("Pets")
    treatment = relationship("Treatments")
    pen = relationship("Pens")

    def __init__(self):
        super().__init__()


postcode = PostCode()
clinic = Clinic()
staff = Staff()
supplyTypes = SupplyTypes()
supplies = Supplies()
pharmaSupplies = PharmaSupplies()
treatments = Treatments()
treatmentRequirements = TreatmentRequirements()
petOwners = PetOwners()
pets = Pets()
examinations = Examinations()
petTreatments = PetTreatments()
appointments = Appointments()
invoices = Invoices()
pens = Pens()
petStay = PetStay()
