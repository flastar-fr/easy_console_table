from columnerror import ColumnError


alignment = {"left": "<", "center": "^", "right": ">"}


class Table:
    """ Class to create a table with name as key and list as values
        :atr table: dict -> contains all the datas
        :atr options: dict -> contains all the customizable options
    """
    def __init__(self):
        self.table = {}
        self.options = {"alignment": alignment["right"],
                        "title_separator": "-",
                        "column_separator": "|",
                        "line_separator": "_"}

    def config(self, **kwargs):
        # assertion tests
        for key in kwargs.keys():
            assert key in self.options.keys(), (f"Invalid {key} argument, argument should be in : "
                                                f"{", ".join(self.options.keys())}")
        if "alignment" in kwargs.keys():
            assert kwargs["alignment"] in alignment.keys(), (f"Invalid alignment {kwargs["alignment"]} argument,"
                                                             f" it should be in : {", ".join(alignment.keys())}")

        # config
        for key in kwargs.keys():
            if key != "alignment":
                self.options[key] = kwargs[key]
            else:
                self.options[key] = alignment[kwargs[key]]

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

        return max_value+1

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

        keys = list(self.table.keys())
        align = self.options["alignment"]
        title_separator = self.options["title_separator"]
        column_separator = self.options["column_separator"]
        line_separator = self.options["line_separator"]

        # titles display
        max_digit_value = self._get_max_lenght_value()
        title_separator_line = (title_separator * (max_digit_value + 7)) * len(self.table.keys())
        to_return = [title_separator_line, column_separator, title_separator_line]
        for key in keys:
            to_return[1] += f" {key: ^{max_digit_value+3}} {column_separator}"

        # values display
        longest_column = self._get_longest_column()
        for i in range(longest_column):
            to_return.append(column_separator)
            for key in keys:
                if len(self.table[key]) - 1 >= i:   # existing value
                    value = self.table[key][i]
                else:   # non-existing value
                    value = ""
                to_return[-1] += f" {value: {align}{max_digit_value+3}} {column_separator}"

            # line separator
            line = (f"{column_separator} {line_separator * (max_digit_value+3)} " *
                    len(keys) + column_separator)
            to_return.append(line)

        return "\n".join(to_return)
