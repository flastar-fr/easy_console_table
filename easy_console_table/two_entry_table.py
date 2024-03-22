from easy_console_table.table_abc import TableABC
from easy_console_table.table_error import TableError


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


def _get_max_lenght_key(keys: list[str]) -> int:
    """ Private function to get the longest line name value
        :param keys: list[str] -> line values

        :return: int -> lenght
    """
    max_digit_key = 0
    splitted_lines = []
    for key in keys:
        if "\n" in key:
            splitted_lines.append(key.split("\n"))
        else:
            splitted_lines.append([key])

    for line in splitted_lines:
        max_line_length = len(max(line, key=lambda x: len(x)))
        if max_line_length > max_digit_key:
            max_digit_key = max_line_length

    return max_digit_key + 1


class TwoEntryTable(TableABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.columns: list[str] = []
        self.lines: list[str] = []
        self.options = {"alignment": "right",
                        "title_separator": "#",
                        "column_separator": "|",
                        "line_separator": "-",
                        "alignment_title": "center"}
        self.title = ""

    def get_line_names(self) -> list[str]:
        """ Method to get all the lines
            :return: list[str] -> all the lines
        """
        return self.lines

    def get_column_names(self) -> list[str]:
        """ Method to get all the columns
            :return: list[str] -> all the columns
        """
        return self.columns

    def add_column_names(self, *args: str):
        """ Method to add line keys to the table
            :param args: list[str]
        """
        for key in args:
            if not isinstance(key, str):
                raise TableError("Key name needs to be a str")
            if key in self.lines or key in self.columns:
                raise TableError("Key already exists")
            self.columns.append(key)

    def add_line_names(self, *args: str):
        """ Method to add line keys to the table
            :param args: list[str]
        """
        for key in args:
            if not isinstance(key, str):
                raise TableError("Key name needs to be a str")
            if key in self.lines or key in self.columns:
                raise TableError("Key already exists")
            self.lines.append(key)

    def add_column_values(self, key: str, values: list):
        """ Method to add values from a column
            :param key: str -> column key to add
            :param values: list -> values to add
        """
        if key not in self.columns:
            raise TableError("Key doesn't exist")
        if not len(values) <= len(self.lines):
            raise TableError("Not enought lines to store the values")
        for i in range(len(values)):
            self.table[(key, self.lines[i])] = values[i]

    def add_line_values(self, key: str, values: list):
        """ Method to add values from a line
            :param key: str -> line key to add
            :param values: list -> values to add
        """
        if key not in self.lines:
            raise TableError("Key doesn't exist")
        if not len(values) <= len(self.columns):
            raise TableError("Not enought columns to store the values")
        for i in range(len(values)):
            self.table[(self.columns[i]), key] = values[i]

    def get_line_values(self, key: str) -> list:
        """ Method to get values from a line name
            :param key: str -> line name

            :return: list -> values to get
        """
        values = []
        columns = [key for key in self.columns if key not in self.filter]
        for column in columns:
            try:
                values.append(self.table[(column, key)])
            except KeyError:
                break

        return values

    def get_column_values(self, key: str) -> list:
        """ Method to get values from a column name
            :param key: str -> column name

            :return: list -> values to get
        """
        values = []
        lines = [key for key in self.lines if key not in self.filter]
        for line in lines:
            try:
                values.append(self.table[(key, line)])
            except KeyError:
                break

        return values

    def remove_line(self, key: str):
        """ Method to remove a whole line
            :param key: str -> line to remove
        """
        columns = [key for key in self.columns if key not in self.filter]
        for column in columns:
            try:
                self.table.pop((column, key))
            except KeyError:
                continue

        self.lines.remove(key)

        if key in self.filter:
            self.filter.remove(key)

    def remove_column(self, key: str):
        """ Method to remove a whole column
            :param key: str -> column to remove
        """
        lines = [key for key in self.lines if key not in self.filter]
        for column in lines:
            try:
                self.table.pop((key, column))
            except KeyError:
                continue

        self.columns.remove(key)

        if key in self.filter:
            self.filter.remove(key)

    def get_filter(self) -> list:
        """ Method to get the filter
            :return: list -> the filter
        """
        return self.filter

    def add_filter(self, key: str):
        """ Method to add a filter
            :param key: str -> key filtered
        """
        if key not in self.columns or key not in self.lines:
            raise TableError("You can't filter something that is not in columns or lines keys")
        self.filter.append(key)

    def remove_filter(self, key: str):
        """ Method to remove a filter
            :param key: str -> key remove
        """
        if key not in self.filter:
            raise TableError("You can only remove a filter that is filtered")
        self.filter.remove(key)

    def clear_filter(self):
        """ Method to clear the filter """
        self.filter = []

    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        lines = [key for key in self.lines if key not in self.filter]
        columns = [key.replace("\n", " ") for key in self.columns if key not in self.filter]
        with open(f"{file_name}.csv", "w", encoding="utf-8") as f:
            f.write("," + ",".replace("\n", " ").join(columns) + "\n")
            for line in lines:
                values = [val.replace("\n", " ") for val in self.get_line_values(line)]
                f.write(str(line).replace("\n", " ") + "," + ",".join(values) + "\n")

    def get_max_lenght_value_column(self, column_name: str) -> int:
        """ Private method to get the max lenght value to get the right format to display
            :return: int -> max lenght value
        """
        if column_name not in self.columns:
            raise TableError("Key doesn't exist")

        max_value = max(_get_lenght_key(column_name), _get_lenght_key(self.title))
        for val in self.lines:
            try:
                lines = str(self.table[(column_name, val)]).split('\n')
                max_line_length = max(len(line) for line in lines)
                if max_line_length > max_value:
                    max_value = max_line_length
            except KeyError:
                break

        return max_value + 1  # +1 to have a better result

    def _get_max_lenght_value_line(self, line_name: str) -> int:
        """ Private method to get the max lenght value to get the right format to display
            :return: int -> max lenght value
        """
        if line_name not in self.columns:
            raise TableError("Key doesn't exist")

        max_value = max(_get_lenght_key(line_name), _get_lenght_key(self.title))
        for val in self.lines:
            try:
                lines = str(self.table[(line_name, val)]).split('\n')
                max_line_length = max(len(line) for line in lines)
                if max_line_length > max_value:
                    max_value = max_line_length
            except KeyError:
                break

        return max_value + 1  # +1 to have a better result

    def _draw_titles(self,
                     keys: list[str],
                     line_names: list[str],
                     column_separator: str,
                     title_separator: str,
                     align_title: str) -> list[str]:
        """ Private method to draw the titles of the table
            :param keys: list[str] -> keys to draw
            :param line_names: list[str] -> make possible to draw the gap at the beginning
            :param column_separator: str -> char to separate columns

            :return: list[str] -> a list that contains the lines
        """
        # get datas
        splitted_lines = []
        for key in keys:
            if "\n" in key:
                splitted_lines.append(key.split("\n"))
            else:
                splitted_lines.append([key])

        splitted_title = self.title.split("\n")

        # uniformize datas
        max_line = len(max(splitted_lines, key=lambda x: len(x)))
        max_line = max(len(splitted_title), max_line)
        for column in splitted_lines:
            while len(column) != max_line:
                column.append("")

        # draw lines
        lines: list[str] = [title_separator for _ in range(max_line)]

        for i in range(len(splitted_lines)):
            max_lenght = self.get_max_lenght_value_column(keys[i])

            for j in range(max_line):
                value = splitted_lines[i][j]
                lines[j] += f" {value: {align_title}{max_lenght + 3}} {column_separator}"

        # align to a Two Entry format (puting space for lines keys drawing)
        max_digits = _get_max_lenght_key(line_names + [self.title])
        while len(splitted_title) != max_line:
            splitted_title.append("")
        for i, val in enumerate(splitted_title):
            lines[i] = f"{title_separator} {val: ^{max_digits + 3}} " + lines[i]

        return lines

    def _draw_line(self,
                   lines: list[str],
                   columns: list[str],
                   key: str,
                   title_separator: str,
                   column_separator: str,
                   align: str,
                   align_title: str) -> list[str]:
        """ Private method to draw a line (supports multi-line)
            :param lines: list[str] -> lines
            :param columns: list[str] -> columns
            :param key: str -> key to draw
            :param title_separator: str -> separator of title
            :param column_separator: str -> character use to separate columns
            :param align: str -> character use to align (<, ^, >)

            :return: str -> multi-lines
        """
        # get datas
        splitted_lines = []
        if "\n" in key:
            splitted_lines.append(key.split("\n"))
        else:
            splitted_lines.append([key])

        for column in columns:
            try:
                splitted_lines.append(str(self.table[column, key]).split("\n"))
            except KeyError:
                break

        while len(splitted_lines) - 1 != len(columns):
            splitted_lines.append([""])

        # uniformize datas
        max_line = len(max(splitted_lines, key=lambda x: len(x)))
        for column in splitted_lines:
            while len(column) != max_line:
                column.append("")

        # draw lines
        to_return: list[str] = ["" for _ in range(max_line)]

        # key
        max_digit_key = _get_max_lenght_key(lines + [self.title])
        for i, val in enumerate(splitted_lines[0]):
            to_return[i] += f"{title_separator} {val: {align_title}{max_digit_key + 3}} {title_separator}"

        # values
        for i in range(1, len(splitted_lines)):
            max_digit_value = self._get_max_lenght_value_line(columns[i-1])

            for j in range(max_line):
                value = splitted_lines[i][j]
                to_return[j] += f" {value: {align}{max_digit_value + 3}} {column_separator}"

        return to_return

    def __str__(self) -> str:
        """ Special method to get the str format of the table
                    :return: str -> the table
                """
        # get datas
        columns = [value for value in list(self.columns) if value not in self.filter]
        lines = [value for value in list(self.lines) if value not in self.filter]
        align: str = alignment[self.options["alignment"]]
        title_separator: str = self.options["title_separator"]
        column_separator: str = self.options["column_separator"]
        line_separator: str = self.options["line_separator"]
        alignment_title: str = alignment[self.options["alignment_title"]]

        # titles display
        # draw a column * amount of column (don't take last chars depending of amount of columns)
        # separators construct
        to_return: list[str] = []
        max_digits = _get_max_lenght_key(lines + [self.title])
        title_separator_line = title_separator * (max_digits+6)
        separator_values_lines = f"{title_separator} {((max_digits + 3) * title_separator)} {title_separator}"
        for key in columns:
            max_digit_value = self.get_max_lenght_value_column(key)
            title_separator_line += (title_separator * (max_digit_value + 7))
            separator_values_lines += f" {line_separator * (max_digit_value + 3)} {column_separator}"

        if len(columns) > 1:
            title_separator_line = title_separator_line[:-len(columns) + 1]
        to_return.append(title_separator_line)

        # draw titles
        title = self._draw_titles(columns, lines, column_separator, title_separator, alignment_title)
        for line in title:
            to_return.append(line)

        to_return.append(title_separator_line)

        # display values
        for key in lines:
            to_print = self._draw_line(lines, columns, key, title_separator, column_separator, align, alignment_title)
            for line in to_print:
                to_return.append(line)

            to_return.append(separator_values_lines)

        return "\n".join(to_return)
