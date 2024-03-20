from abc import ABC, abstractmethod
from easy_console_table.table_error import TableError

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
                        "line_separator": "_",
                        "alignment_title": "center"}
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
                raise TableError(f"Invalid {key} argument, argument should be in : "
                                 f"{', '.join(self.options.keys())}")
        if "alignment" in kwargs.keys():
            if kwargs["alignment"] not in alignment.keys():
                raise TableError(f"Invalid alignment {kwargs['alignmen']} argument,"
                                 f" it should be in : {', '.join(alignment.keys())}")
        elif "alignment_title" in kwargs.keys():
            if kwargs["alignment_title"] not in alignment.keys():
                raise TableError(f"Invalid alignment {kwargs['alignmen']} argument,"
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

    @abstractmethod
    def export_as_csv(self, file_name: str):
        """ Method to export into a CSV file with filter
            :param file_name: str -> file name to use
        """
        pass

    def __str__(self) -> str:
        """ Special method to get the str format of the table
            :return: str -> the table
        """
        pass
