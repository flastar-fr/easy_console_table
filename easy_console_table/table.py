class Table:
    def __init__(self):
        self.table = {}

    def add_column(self, name: str, datas):
        assert name not in self.table.keys(), "Column already exists"
        self.table[name] = datas

    def delete_column(self, name: str):
        assert name in self.table.keys(), "Column's name doesn't exist"
        self.table.pop(name)

    def _max_lenght_value(self) -> int:
        max_value = 0
        for val in self.table.values():
            m_values = sorted([len(str(value)) for value in val])
            if m_values[0] > max_value:
                max_value = m_values[0]

        for key in self.table.keys():
            if len(key) > max_value:
                max_value = len(key)

        return max_value+1

    def __str__(self) -> str:
        if self.table == {}:
            return ""

        keys = list(self.table.keys())

        # titles display
        max_digit_value = self._max_lenght_value()
        title_separator_line = ("-" * (max_digit_value + 7)) * len(self.table.keys())
        to_return = [title_separator_line, "|", title_separator_line]
        for key in keys:
            to_return[1] += f" {key: ^{max_digit_value+3}} |"

        # values display
        for i in range(len(self.table[keys[0]])):
            to_return.append("|")
            for key in keys:
                value = self.table[key][i]
                to_return[-1] += f" {value: >{max_digit_value+3}} |"

            # line separator
            line = f"| {"-" * (max_digit_value+3)} " * len(keys) + "|"
            to_return.append(line)

        return "\n".join(to_return)
