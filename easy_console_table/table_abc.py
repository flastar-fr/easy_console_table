from abc import ABC, abstractmethod
from easy_console_table.columnerror import ColumnError


alignment = {"left": "<", "center": "^", "right": ">"}


class TableABC(ABC):
    """ Abstract class for tables of easy-console-table package, implemented with a dict
        :atr table: dict -> contains all the datas
        :atr options: dict -> contains all the customizable options
        :atr filter: list -> contains the column's name to not show
    """
    def __init__(self, **kwargs):
        self.table = {}
        self.options = {"alignment": "right",
                        "title_separator": "-",
                        "column_separator": "|",
                        "line_separator": "_"}
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

    def get_table(self) -> dict:
        """ Method to get the table
            :return: dict -> the whole table
        """
        return self.table

    @abstractmethod
    def get_filter(self) -> list:
        """ Method to get the filter
            :return: list -> the filter
        """
        pass

    @abstractmethod
    def add_filter(self, key: str):
        """ Method to add a filter
            :param key: str -> key filtered
        """
        pass

    @abstractmethod
    def remove_filter(self, key: str):
        """ Method to remove a filter
            :param key: str -> key remove
        """
        pass

    @abstractmethod
    def clear_filter(self):
        """ Method to clear the filter """
        pass

    def __str__(self) -> str:
        """ Special method to get the str format of the table
            :return: str -> the table
        """
        pass
