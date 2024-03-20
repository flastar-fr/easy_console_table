from abc import abstractmethod
from easy_console_table.table_error import TableError
from table_abc import TableABC


class TableABCSEntry(TableABC):
    """ Abstract class for tables of easy-console-table package, implemented with a dict
        :atr table: dict -> contains all the datas
        :atr options: dict -> contains all the customizable options
        :atr filter: list -> contains the column's name to not show
    """

    def add_column(self, name: str, datas: list):
        """ Method to create a column to the table
            :param name: str -> column's name to create
            :param datas: list -> column's values to create
        """
        if not isinstance(datas, list):
            raise TableError("Column must be a list type")
        self.table[name] = datas

    def delete_column(self, name: str):
        """ Method to delete a column to the table
            :param name: str -> column's name to delete
        """
        if name not in self.table.keys():
            raise TableError("Column's name not in table")
        if name in self.filter:
            self.remove_filter(name)
        self.table.pop(name)

    def set_column(self, name: str, values: list):
        """ Method to set a column value
            :param name: str -> column name to set
            :param values: list -> value to set to column
        """
        if name not in self.table.keys():
            raise TableError("Column's name not in table")
        if not isinstance(values, list):
            raise TableError("Column must be a list type")
        self.table[name] = values

    def get_column(self, name: str) -> list:
        """ Method to get the column list with the name
            :param name: str -> column's name to get

            :return: list -> the column
        """
        if name not in self.table.keys():
            raise TableError("Column's name not in table")
        return self.table[name]

    def get_is_perfect(self) -> bool:
        """ Method to know if all column's lenght is the same
            :return: bool -> True if it is the same, False if it is not the same
        """
        default_len = len(list(self.table.values())[0])
        for value in self.table.values():
            if len(value) != default_len:
                return False
        return True

    def get_filter(self) -> list:
        """ Method to get the filter
            :return: list -> the filter
        """
        return self.filter

    def add_filter(self, key: str):
        """ Method to add a filter
            :param key: str -> key filtered
        """
        if key not in self.table.keys():
            raise TableError(f"Key {key} not in table keys")
        self.filter.append(key)

    def remove_filter(self, key: str):
        """ Method to remove a filter
            :param key: str -> key remove
        """
        if key not in self.filter:
            raise TableError(f"Key {key} not in filter")
        self.filter.remove(key)

    def clear_filter(self):
        """ Method to clear the filter """
        self.filter = []

    def sort_table_from_column(self, column_name: str):
        """ Method to sort the table from depending on sorting a column
            :param column_name: str -> column name use to sort all the table
        """
        if not self.get_is_perfect():
            raise TableError("Table values should have the same lenght")
        from_column = self.table[column_name]
        for key, value in self.table.items():
            self.table[key] = [x for _, x in sorted(zip(from_column, value))]

    @abstractmethod
    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        pass

    def _get_longest_column(self) -> int:
        """ Private method to get the longest list contained in the table
            :return: int -> longest column lenght
        """
        return len(max(self.table.values(), key=lambda x: len(x)))
