class QueryBuilder:
    ignore_warning = True

    ILLEGAL_KEYWORDS = ['select', 'insert', 'delete']

    def __init__(self):
        pass

    def select(self, *, table: str, orderby: bool | tuple[bool, str, str] = False, multiTable: bool = False,
               **conditions) -> str:

        query = "" if multiTable else "SELECT * FROM {} WHERE".format(table)

        xor_arguments, conditions = self._extract_xor_arguments(**conditions)
        conditions = self._format_string(**conditions)
        query += self._format_and_arguments(**conditions) if conditions else ""
        if conditions:
            query += " AND"
        query += self._format_xor_arguments(**xor_arguments) if xor_arguments else ""
        query += self._format_order_by(orderby=orderby)

        return query

    def select_multiple_tables(self, joins, columns=None, include_groupBy=False,
                               orderby: bool | tuple[bool, str, str] = False,
                               having=None, **tables):

        self.ignore_warning = True

        query, group_by = self._format_multi_table_columns_group_by(tables=tables, columns=columns)

        query += " AND ".join([_ for idx, _ in enumerate(joins)])
        query += " AND" if sum([1 for _ in tables if tables[_] not in [None, ""]]) == len(tables) else ""
        query += " AND ".join([tables[_] for _ in tables if tables[_] not in ["", None]])

        if group_by and include_groupBy:
            group_by = " GROUP BY " + group_by
            query += group_by

        order_by = self._format_order_by(orderby=orderby)
        having = self._format_having(having=having)
        query += having if having is not None else ""
        query += order_by

        query = query.replace("  ", " ")
        print("\n")
        print(query)
        return query

    def insert(self, table, **kwargs) -> tuple[str, list]:
        self.ignore_warning = True
        query = "INSERT INTO {} ({}) VALUES ({})".format(table, ", ".join(list(kwargs)),
                                                         ", ".join(['?'] * len(kwargs)))

        values = list(self._format_string(**kwargs).values())

        return query, values

    def update(self):
        pass

    def delete(self):
        pass

    def create_table(self):
        pass

    def create_database(self):
        pass

    def _format_order_by(self, orderby: bool | tuple[bool, str, str] = False):
        self.ignore_warning = True
        temp = ""
        if orderby:
            temp = " ORDER BY {} {}".format(*list(orderby[1:]))

        return temp

    def _format_date(self):
        pass

    def _format_string(self, **kwargs) -> dict:
        self.ignore_warning = True

        for _ in kwargs:
            if type(kwargs[_]) == str:
                kwargs[_] = f"'{kwargs[_]}'"

        return kwargs

    def _extract_xor_arguments(self, **kwargs) -> tuple[dict, dict]:
        self.ignore_warning = True

        xor_arguments = {}
        for _ in kwargs:
            if type(kwargs[_]) in [list, tuple]:
                xor_arguments[_] = kwargs[_]

        for _ in xor_arguments:
            kwargs.pop(_)

        return xor_arguments, kwargs

    def _format_xor_arguments(self, **kwargs) -> str:
        self.ignore_warning = True

        string = " "

        for idx, _ in enumerate(kwargs):
            if idx > 0:
                string += " AND "
            temp = "{} = (".format(_)
            temp += " OR ".join([_ for _ in kwargs[_]])
            temp += ")"
            string += temp

        return string

    def _format_and_arguments(self, **kwargs) -> str:
        self.ignore_warning = True
        extension = " "
        extension += " = {} AND ".join(_ for _ in kwargs)
        extension += " = {}"
        extension = extension.format(*[kwargs[_] for _ in kwargs])

        return extension

    def _no_illegals(self, **kwargs) -> bool:
        for _ in kwargs:
            if type(kwargs[_]) == str:
                if kwargs[_].lower() in self.ILLEGAL_KEYWORDS:
                    return False

        return True

    def _format_condition_multi_table(self, *, table: str, **conditions) -> str:
        self.ignore_warning = True
        temp = {"{}.".format(table) + _: conditions[_] for _ in conditions}
        return self.select(table=table, orderby=False, multiTable=True, **temp)

    def format_table_conditions(self, *, table: str, **conditions) -> str:

        condition = self._format_condition_multi_table(table=table, **conditions)
        print(condition)
        return condition

    def _format_multi_table_columns_group_by(self, tables, columns) -> tuple[str, str]:
        self.ignore_warning = True
        group_by = ""
        query = ""

        if columns is None:
            query = "SELECT * FROM {} WHERE ".format(", ".join([_ for _ in tables]))
        else:
            query = "SELECT "

            for idx, _ in enumerate(tables):
                if idx > 0:
                    query += ", "
                    group_by += ", "
                query += ", ".join([f"{_}." + column for column in columns[_]])
                group_by += ", ".join([f"{_}." + column for column in columns[_]])

        query += " FROM {} WHERE ".format(", ".join([_ for _ in tables]))

        return query, group_by

    def _format_having(self, having):
        self.ignore_warning = True

        if having:
            having = " HAVING " + having
            return having

        return ""


qBuilder = QueryBuilder()
"""
condition_1 = qBuilder.format_table_conditions(table='abz', color=['Red', 'Blue', 'Brown'],
                                               peep=['Red', 'Blue', 'Brown'], job=['Pilot', 'Blue', 'Brown'])

condition_2 = qBuilder.format_table_conditions(table='banana', color=['Red', 'Blue', 'Brown'],
                                               peep=['Red', 'Blue', 'Brown'], job=['Red', 'Blue', 'Brown'])

qBuilder.select_multiple_tables(joins=['abz.ID = banana.abzID', 'abz.name = banana.abzName'],
                                columns={'abz': ['1', '2', '3'], 'banana': ['1', '2']},
                                having="sum > 10",
                                orderby=(True, 'name', 'DESC'),
                                include_groupBy=True, abz=condition_1, banana=condition_2)
"""

print(qBuilder.insert(table='postcode', postcode=2302, area=23043, sumo="Hadda", id=10))
