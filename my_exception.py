class AboveTwoNamesException(Exception):
    def __init__(self, number_of_names) -> None:
        self.number_of_names = number_of_names
        self.msg = f'More than 2 names left: List has {self.number_of_names}.'

    def __str__(self) -> str:
        return self.msg
