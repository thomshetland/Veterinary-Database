from queryBuilder import QueryBuilder
from database_setup import DatabaseSetup
from orm_setup import *


class DataBase:

    def __init__(self):
        self.qBuilder = QueryBuilder()
        self.setup = DatabaseSetup()

    def connect(self):
        pass

    def insertInto(self, table, exclude_ID=False, **kwargs):
        pass


