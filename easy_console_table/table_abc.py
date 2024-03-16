from abc import ABC, abstractmethod
from easy_console_table.columnerror import ColumnError


alignment = {"left": "<", "center": "^", "right": ">"}


class TableABC(ABC):
    def __init__(self, **kwargs):
        self.table = {}
        self.options = {"alignment": "right",
                        "title_separator": "-",
                        "column_separator": "|",
                        "line_separator": "_"}
        self.config(**kwargs)
        self.filter = []

    def config(self, **kwargs):
        """ Method to configure the options for the table to show
            :param kwargs: dict -> Valid options :
             alignment=str, title_separator=str, column_separator=str, line_separator=str
        """
        # exception tests
        for key in kwargs.keys():
            if key not in self.options.keys():
                raise ColumnError(f"Invalid {key} argument, argument should be in : "
                                  f"{', '.join(self.options.keys())}")
        if "alignment" in kwargs.keys():
            if kwargs["alignment"] not in alignment.keys():
                raise ColumnError(f"Invalid alignment {kwargs['alignmen']} argument,"
                                  f" it should be in : {', '.join(alignment.keys())}")

        # config
        for key, value in kwargs.items():
            self.options[key] = value

    def add_column(self, name: str, datas: list):
        """ Method to create a column to the table
            :param name: str -> column's name to create
            :param datas: list -> column's values to create
        """
        if not isinstance(datas, list):
            raise ColumnError("Column must be a list type")
        self.table[name] = datas

    def delete_column(self, name: str):
        """ Method to delete a column to the table
            :param name: str -> column's name to delete
        """
        if name not in self.table.keys():
            raise ColumnError("Column's name not in table")
        if name in self.filter:
            self.remove_filter(name)
        self.table.pop(name)

    def get_table(self) -> dict:
        """ Method to get the table
            :return: dict -> the whole table
        """
        return self.table

    def set_column(self, name: str, values: list):
        """ Method to set a column value
            :param name: str -> column name to set
            :param values: list -> value to set to column
        """
        if name not in self.table.keys():
            raise ColumnError("Column's name not in table")
        if not isinstance(values, list):
            raise ColumnError("Column must be a list type")
        self.table[name] = values

    def get_column(self, name: str) -> list:
        """ Method to get the column list with the name
            :param name: str -> column's name to get

            :return: list -> the column
        """
        if name not in self.table.keys():
            raise ColumnError("Column's name not in table")
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
            raise ColumnError(f"Key {key} not in table keys")
        self.filter.append(key)

    def remove_filter(self, key: str):
        """ Method to remove a filter
            :param key: str -> key remove
        """
        if key not in self.filter:
            raise ColumnError(f"Key {key} not in filter")
        self.filter.remove(key)

    def clear_filter(self):
        """ Method to clear the filter """
        self.filter = []

    def sort_table_from_column(self, column_name: str):
        """ Method to sort the table from depending on sorting a column
            :param column_name: str -> column name use to sort all the table
        """
        if not self.get_is_perfect():
            raise ColumnError("Table values should have the same lenght")
        from_column = self.table[column_name]
        for key, value in self.table.items():
            self.table[key] = [x for _, x in sorted(zip(from_column, value))]

    @abstractmethod
    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        pass
