from columnerror import ColumnError

alignment = {"left": "<", "center": "^", "right": ">"}


class Table:
    """ Class to create a table with name as key and list as values
        :atr table: dict -> contains all the datas
        :atr options: dict -> contains all the customizable options
    """

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
                                  f"{", ".join(self.options.keys())}")
        if "alignment" in kwargs.keys():
            if kwargs["alignment"] not in alignment.keys():
                raise ColumnError(f"Invalid alignment {kwargs["alignment"]} argument,"
                                  f" it should be in : {", ".join(alignment.keys())}")

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
        self.table.pop(name)

    def get_table(self) -> dict:
        """ Method to get the table
            :return: dict -> the whole table
        """
        return self.table

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

    def _get_max_lenght_value(self) -> int:
        """ Private method to get the max lenght value to get the right to format to display
            :return: int -> max lenght value
        """
        max_value = 0
        # table values
        for val in self.table.values():
            m_values = sorted([len(str(value)) for value in val])
            if m_values[0] > max_value:
                max_value = m_values[0]

        # table keys
        for key in self.table.keys():
            if len(key) > max_value:
                max_value = len(key)

        return max_value + 1  # +1 to have a better result

    def _get_longest_column(self) -> int:
        """ Private method to get the longest list contained in the table
            :return: int -> longest column lenght
        """
        return len(max(self.table.values(), key=lambda x: len(x)))

    def __str__(self) -> str:
        """ Special method to get the str format of the table
            :return: str -> the table
        """
        if self.table == {}:
            return ""

        keys = [value for value in list(self.table.keys()) if value not in self.filter]
        align: str = alignment[self.options["alignment"]]
        title_separator: str = self.options["title_separator"]
        column_separator: str = self.options["column_separator"]
        line_separator: str = self.options["line_separator"]

        # titles display
        max_digit_value = self._get_max_lenght_value()
        # draw a column * amount of column (don't take last char)
        title_separator_line = ((title_separator * (max_digit_value + 7)) * len(keys))[:-1]
        to_return = [title_separator_line, column_separator, title_separator_line]
        for key in keys:
            to_return[1] += f" {key: ^{max_digit_value + 3}} {column_separator}"

        # values display
        # (column separator + draw a column) * amount of column + column separator
        separator_values_lines = (f"{column_separator} {line_separator * (max_digit_value + 3)} " *
                                  len(keys) + column_separator)
        longest_column = self._get_longest_column()
        for i in range(longest_column):
            to_return.append(column_separator)
            for key in keys:
                if len(self.table[key]) - 1 >= i:  # existing value
                    value = self.table[key][i]
                else:  # non-existing value
                    value = ""
                to_return[-1] += f" {value: {align}{max_digit_value + 3}} {column_separator}"

            # line separator
            to_return.append(separator_values_lines)

        return "\n".join(to_return)
