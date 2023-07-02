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


def get_names_from_json() -> dict:
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


"""
last_weekdays_a = 'ΣΙΑΜΕΤΗΣ'
last_weekdays_b = 'ΤΟΠΑΛΙΔΗΣ'
last_fridays_a = 'ΒΑΒΒΑΣ'
last_fridays_b = 'ΠΑΠΟΥΤΣΑΚΗ'
last_weekends_a = 'ΓΙΑΧΑΛΗ'
last_weekends_b = 'ΚΑΤΣΑΡΟΣ'
"""
