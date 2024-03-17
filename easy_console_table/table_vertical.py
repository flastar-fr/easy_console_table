from easy_console_table.table_abc import TableABC

alignment = {"left": "<", "center": "^", "right": ">"}


def _get_lenght_key(key: str) -> int:
    """ Function to get the lenght of a title if it was on multi line
        :param key: str -> the key to verif

        :return: int -> the lenght
    """
    if "\n" in key:
        splitted_list = key.split("\n")
    else:
        splitted_list = [key]

    return len(max(splitted_list, key=lambda x: len(x)))


class TableVertical(TableABC):
    """ Class to create a vertical table with name as key and list as values
        :atr table: dict -> contains all the datas
        :atr options: dict -> contains all the customizable options
        :atr filter: list -> contains the column's name to not show
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.options = {"alignment": "right",
                        "title_separator": "-",
                        "column_separator": "|",
                        "line_separator": "_"}
        self.config(**kwargs)

    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        keys = [key for key in self.table.keys() if key not in self.filter]
        longest_column = self._get_longest_column()
        with open(f"{file_name}.csv", "w") as f:
            f.write(",".join(keys) + "\n")  # titles
            # values
            for i in range(longest_column):
                values = []
                for key in keys:
                    if len(self.table[key]) - 1 >= i:  # existing value
                        values.append(str(self.table[key][i]))
                    else:  # non-existing value
                        values.append("")
                f.write(",".join(values) + "\n")

    def _get_max_lenght_value(self, column_name: str) -> int:
        """ Private method to get the max lenght value to get the right format to display
            :return: int -> max lenght value
        """
        max_value = _get_lenght_key(column_name)
        for val in self.table[column_name]:
            lines = val.split('\n')
            max_line_length = max(len(line) for line in lines)
            if max_line_length > max_value:
                max_value = max_line_length

        return max_value + 1  # +1 to have a better result

    def _search_value_in_columns_index(self, index: int, value: str) -> bool:
        """ Private method to search a value in all columns at a specific index
            :param index: int -> index to search on
            :param value: str -> value to search

            :return: bool -> True if value in, otherwise False
        """
        for column in self.table.values():
            if len(column) - 1 >= index:
                if value in column[index]:
                    return True
        return False

    def draw_titles(self, keys: list[str], column_separator: str) -> list[str]:
        # get datas
        splitted_lines = []
        for key in keys:
            if "\n" in key:
                splitted_lines.append(key.split("\n"))
            else:
                splitted_lines.append([key])

        # uniformize datas
        max_line = len(max(splitted_lines, key=lambda x: len(x)))
        for column in splitted_lines:
            while len(column) != max_line:
                column.append("")

        # draw lines
        lines: list[str] = ["|" for _ in range(max_line)]

        for i in range(len(splitted_lines)):
            max_lenght = self._get_max_lenght_value(keys[i])

            for j in range(max_line):
                value = splitted_lines[i][j]
                lines[j] += f" {value: ^{max_lenght + 3}} {column_separator}"

        return lines

    def _draw_line_single(self, index: int, keys: list[str], column_separator: str, align: str) -> str:
        """ Private method to draw a full line on a single line
            :param index: int -> line to draw
            :param keys: list[str] -> all the keys
            :param column_separator: str -> character use to separate columns
            :param align: str -> character use to align (<, ^, >)

            :return: str -> the full line
        """
        line = ""

        for key in keys:
            if len(self.table[key]) - 1 >= index:  # existing value
                value = self.table[key][index]
            else:  # non-existing value
                value = ""
            max_digit_value = self._get_max_lenght_value(key)
            line += f" {value: {align}{max_digit_value + 3}} {column_separator}"

        return line

    def _draw_multiline(self, index: int, keys: list[str], column_separator: str, align: str) -> list[str]:
        """ Private method to draw a multi-line line
            :param index: int -> line to draw
            :param keys: list[str] -> all the keys
            :param column_separator: str -> character use to separate columns
            :param align: str -> character use to align (<, ^, >)

            :return: str -> multi-lines
        """
        assert self._search_value_in_columns_index(index, "\n"), "Method must be used for multi-line purposes"

        # get datas
        splitted_lines = []
        for column in [val for key, val in self.table.items() if key not in self.filter]:
            if len(column) - 1 >= index:
                if "\n" in column[index]:
                    splitted_lines.append(column[index].split("\n"))
                else:
                    splitted_lines.append([column[index]])
            else:
                splitted_lines.append([])

        # uniformize datas
        max_line = len(max(splitted_lines, key=lambda x: len(x)))
        for column in splitted_lines:
            while len(column) != max_line:
                column.append("")

        # draw line
        lines: list[str] = ["" for _ in range(max_line)]

        for i in range(len(splitted_lines)):
            max_digit_value = self._get_max_lenght_value(keys[i])

            for j in range(len(splitted_lines[0])):
                value = splitted_lines[i][j]
                lines[j] += f" {value: {align}{max_digit_value + 3}} {column_separator}"

        return lines

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
        # draw a column * amount of column (don't take last chars depending of amount of columns)
        # separators construct
        to_return: list[str] = []
        title_separator_line = ""
        separator_values_lines = column_separator
        for key in keys:
            max_digit_value = self._get_max_lenght_value(key)
            title_separator_line += (title_separator * (max_digit_value + 7))
            separator_values_lines += f" {line_separator * (max_digit_value + 3)} {column_separator}"

        if len(keys) > 1:
            title_separator_line = title_separator_line[:-len(keys)+1]
        to_return.append(title_separator_line)

        # draw titles
        for line in self.draw_titles(keys, column_separator):
            to_return.append(line)

        to_return.append(title_separator_line)

        # values display
        # (column separator + draw a column) * amount of column + column separator
        longest_column = self._get_longest_column()
        for i in range(longest_column):
            # multi-line
            if self._search_value_in_columns_index(i, "\n"):
                lines = self._draw_multiline(i, keys, column_separator, align)
                for index in range(len(lines)):
                    to_return.append(column_separator)
                    to_return[-1] += lines[index]
            else:   # single line
                to_return.append(column_separator)
                to_return[-1] += self._draw_line_single(i, keys, column_separator, align)

            # line separator
            to_return.append(separator_values_lines)

        return "\n".join(to_return)
