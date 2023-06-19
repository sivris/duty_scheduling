import pandas as pd
from process_last_names import *
from create_month import create_month_frame
import datetime as dt

# creating the month data frame
month = create_month_frame()

# creating the names data frame
names = pd.read_excel(r'sort_data.xlsx')

def fill_shift_a(month:pd.DataFrame, names:pd.DataFrame):
    """
    Function collects the right name from names data frame to save it in the column name in month data frame.
    Initialize 3 indexes for looping the columns in the names data frame.
    Looping in the month and saving the correct name in the name column.
    parameters: month: data frame with 5 columns (date, month, day, name_A, name_B)
                names: data frame with 6 columns (weekdaysA, weekdaysB, fridaysA, fridaysB, weekendsA, weekendsB)    
    """

    # indexes for names columns
    index_weekends_a = 0
    index_fridays_a = 0
    index_weekdays_a = 0

    # looping the month data frame in column day
    for i, day in enumerate(month.loc[:, 'day']):

        # WEEKEND
        if day == 'Saturday' or day == 'Sunday':
            # check if index is out of bound
            if index_weekends_a == len(names):
                index_weekends_a = 0

            # save the name
            name = names.iloc[index_weekends_a, 4]
            index_weekends_a += 1 # increasing the index
        

        # FRIDAY
        elif day == 'Friday':
            # check if index is out of bound
            if index_fridays_a == len(names):
                index_fridays_a = 0

            # save the name
            name = names.iloc[index_fridays_a, 2]
            index_fridays_a += 1


        # WEEKDAY
        else:
            # check if index is out of bound
            if index_weekdays_a == len(names):
                index_weekdays_a = 0

            # save the name
            name = names.iloc[index_weekdays_a, 0]
            index_weekdays_a += 1

        # save the name that found in the row of the month data frame
        month.iloc[i, 3] = name # i=current row, 3=column with names
    print(month)






fill_shift_a(month, names)










'''must become function'''




"""                      ------------checking the names for double shift---------------                """
double_shift = True # boolean variable for the while loop
while(double_shift):  
    
    # set the boolean variable as False. if there is no need for change, the while loop will terminate
    double_shift = False

    for i, name in enumerate(month.loc[:, 'name_A']):
        if i: # if i is not 0
            if month.iloc[i-1, 3] == name: # if name in current row is equal with the previous row name
                
                # if i+7 does not exceed the days of month(=len(month)), i swap the names below (the next same type day)
                if (i+7 < len(month)):
                    month.iloc[i, 3], month.iloc[i+7, 3] = month.iloc[i+7, 3], month.iloc[i, 3]

                # i+7 exceeds the days of month so the change completed above
                else:
                    """the swap must become above"""
                    month.iloc[i, 3], month.iloc[i-7, 3] = month.iloc[i-7, 3], month.iloc[i, 3]

                # found at least one double shift, while loop will run again to search for double shifts
                double_shift = True
        else:
            """ ********** check the previous month **********"""
            pass
print(month)


