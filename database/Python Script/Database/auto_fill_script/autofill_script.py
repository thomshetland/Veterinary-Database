
import random
import string
import datetime
import numpy as np
import pandas as pd

fNames = pd.read_csv("first-names.txt", names=['names'])
lNames = pd.read_csv("last-names.txt", names=['names'])
postcodes = pd.read_csv("postcodes.csv", index_col=0)
ge_care = pd.read_csv("ge_care.csv", index_col=0)
em_care = pd.read_csv("em_care.csv", index_col=0)
supplies = pd.read_csv("all_supplies.csv", index_col=0)
petTypes = pd.read_csv("pet_types.csv", index_col=0)
streetNames = pd.read_csv("street_names.csv", index_col=0)

pharmaSupply = supplies[supplies['supplyType'] == 'Pharmaceutical']
surgicalSupply = supplies[supplies['supplyType'] == 'Surgical']
non_surgicalSupply = supplies[supplies['supplyType'] == 'Non-Surgical']

print(f"Loaded {len(postcodes)} postcodes")
print(f"Loaded {len(em_care)} emergency treatments")
print(f"Loaded {len(ge_care)} general treatments")
print(f"Loaded {len(petTypes)} pet types")
print(f"Loaded {len(streetNames)} streets")
print("\n")
print(f"Loaded {len(supplies)} supplies")
print(f"{len(supplies[supplies['supplyType'] == 'Pharmaceutical'])} - Pharmaceutical Supplies")
print(f"{len(supplies[supplies['supplyType'] == 'Surgical'])} - Surgical Supplies")
print(f"{len(supplies[supplies['supplyType'] == 'Non-Surgical'])} - Non-Surgical Supplies")


# GOT SUPPLY DATA
# GOT TREATMENT DATA
# GOT POST CODE DATA
# GOT NAME DATA


class AutoFill:

    ignore_warning = True

    def __init__(self):
        self.cAddresses = ['Fjellveien', 'Fjellvegen',
                         'Industriveien', 'Industrivegen',
                         'Skoleveien', 'Skolevegen',
                         'Kirkeveien', 'Kyrkjevegen',
                         'Åsveien', 'Åsvegen',
                         'Strandveien', 'Strandvegen',
                         'Parkveien', 'Parkvegen',
                         'Storgata', 'Storgaten',
                         'Markveien', 'Markvegen',
                         'Nygaten', 'Ekornveien',
                         'Lillesandsveien', 'Solveien']


        self.carBrand = ['Volvo',
                         'BMW',
                         'Mercedes',
                         'Ferrari',
                         'Alpha Romeo',
                         'Bugatti',
                         'Mazda',
                         'Jaguar',
                         'Audi',
                         'Nissan',
                         'Pole Star',
                         'Porsche',
                         'Tela']
        self.carModel = [_ for _ in range(2015, 2024)]
        self.carTransmission = ['Auto', 'Manual']
        self.carEngine = ['Electric', 'Gas', 'Diesel', 'Hybrid']
        self.carType = ['SUV', 'Off Road', 'Sedan', 'Coupe', 'Sports Car', 'Crossover', 'Convertible']

    def auto_fill_postcodes_table(self, amount):
        pass

    def auto_fill_treatments_table(self, amount):
        pass

    def auto_fill_supply_types_table(self, amount):
        pass

    def auto_fill_clinics_table(self, amount):
        pass

    def auto_fill_pens_table(self, amount):
        pass

    def auto_fill_staffs_table(self, amount):
        pass

    def auto_fill_supplies_table(self, amount):
        pass

    def auto_fill_pharma_supplies_table(self, amount):
        pass

    def auto_fill_tr_requirements_table(self, amount):
        pass

    def auto_fill_pet_owners_table(self, amount):
        pass

    def auto_fill_pets_table(self, amount):
        pass

    def auto_fill_pet_stay_table(self, amount):
        pass

    def auto_fill_examinations_table(self, amount):
        pass

    def auto_fill_appointments_table(self, amount):
        pass

    def auto_fill_invoices_table(self, amount):
        pass

    def auto_fill_invoices_paid_table(self, amount):
        pass

    def auto_fill_pet_treatments_table(self, amount):
        pass

    def ssn(self):
        self.ignore_warning = True

        ssn = [str(random.randint(0, 9)) for _ in range(11)]

        return "".join(ssn)

    def fax(self):
        self.ignore_warning = True

        fax = [str(random.randint(0, 9)) for _ in range(random.randint(7, 15))]

        return "".join(fax)

    def phone(self):
        self.ignore_warning = True

        phone_number = [str(random.randint(0, 9)) for _ in range(7)]
        phone_number.insert(0, random.choice(["4", "9"]))

        return "".join(phone_number)

    def name(self):
        self.ignore_warning = True
        f_name = fNames.values[[random.randint(0, len(fNames))]].flatten()[0].capitalize()
        l_name = lNames.values[[random.randint(0, len(lNames))]].flatten()[0].capitalize()
        name = " ".join([f_name, l_name])

        return name

    def save_to_csv(self, data, fileName):
        self.ignore_warning = True

        pass


autoFill = AutoFill()
