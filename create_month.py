import pandas as pd

def create_month_frame(start='7/1/2023', end='7/31/2023'):
    """
    function creates a data frame which contains a whole month.
    the data frame has 5 columns:
        1) date (number)
        2) month (string)
        3) day (string)
        4) name for shift A (None)
        5) name for shift B (None)
    parameters: the start and end date of the month.
    """
    df_month = pd.DataFrame({'date': pd.date_range(start=start, end=end, freq='D').day,
                             'month': pd.date_range(start=start, end=end, freq='D').month_name(),
                             'day': pd.date_range(start=start, end=end, freq='D').day_name(),
                             'name_A': None,
                             'name_B': None})
    return df_month
