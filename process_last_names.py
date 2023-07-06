import json


def save_last_names_to_json(day_a: str, day_b: str, fri_a: str, fri_b: str,
                            wend_a: str, wend_b: str) -> bool:
    """
    function for saving the last names of the order in a json file
    parameters: strings with the names
    """
    # save the names in a dictionary
    last = {"last_weekday_a": day_a, "last_weekday_b": day_b,
            "last_friday_a": fri_a, "last_friday_b": fri_b,
            "last_weekend_a": wend_a, "last_weekend_b": wend_b}

    try:
        # open the file for writing
        with open("last_names.json", "w", encoding="utf-8") as file:
            # dumping the new json
            json.dump(last, file, ensure_ascii=False)
            return True
    # catch the exception
    except Exception as e:
        print(e)
        return False


def get_names_from_json() -> dict | bool:
    """
    function for getting the names from json file and returns a dictionary.
    """
    try:
        # open the file
        with open("last_names.json", "r", encoding="utf-8") as file:

            # load the contents as dictionary
            dictionary = json.load(file)

            # return the dictionary
            return dictionary
    # catch the exception
    except Exception as e:
        print(e)
        return False


def save_leftovers_json(names: dict) -> bool:
    """
    function for saving the names that left over in a json file
    """
    try:
        # open file for writing
        with open("leftovers.json", "w", encoding="utf-8") as file:
            json.dump(obj=names, fp=file, ensure_ascii=False)
            return True
    # catch any exception
    except Exception as e:
        print(e)
        return False


def get_leftovers() -> dict | bool:
    """
    function to get the names that left over from the previous month.
    """
    try:
        # open file
        with open("leftovers.json", "r", encoding="utf-8") as file:

            # load the contents as dictionary
            dictionary = json.load(file)

            # return the dictionary
            return dictionary
    except Exception as e:
        print(e)
        return False


def save_last_day(names: list) -> bool:
    """
    function for saving the names from the last day of the previous month
    """
    try:
        # open file
        with open("last_day.json", "w", encoding="utf-8") as file:
            json.dump(names, file, ensure_ascii=False)
            return True
    # catch any exception
    except Exception as e:
        print(e)
        return False


def get_last_day() -> list | bool:
    """
    function for getting the names from the last day of the previous month in
    a list.
    """
    try:
        with open("last_day.json", "r", encoding="utf-8") as file:

            # load the content
            names = json.load(file)

            # return the list
            return names
    except Exception as e:
        print(e)
        return False


"""
last_weekdays_a = 'ΣΙΑΜΕΤΗΣ'
last_weekdays_b = 'ΤΟΠΑΛΙΔΗΣ'
last_fridays_a = 'ΒΑΒΒΑΣ'
last_fridays_b = 'ΠΑΠΟΥΤΣΑΚΗ'
last_weekends_a = 'ΓΙΑΧΑΛΗ'
last_weekends_b = 'ΚΑΤΣΑΡΟΣ'
"""
