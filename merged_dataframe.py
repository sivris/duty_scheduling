import pandas as pd
from process_last_names import get_names_from_json, save_last_names_to_json
from create_month import create_month_frame


def fill_shift_a(month: pd.DataFrame, names: pd.DataFrame):
    """
    Function collects the right name from names data frame to save it in the
    column name in month data frame.

    Initialize 3 indexes for looping the columns in the names data frame.

    Looping in the month and saving the correct name in the name column.
    parameters:

    1)  month: data frame with 5 columns (date, month, day, name_A,
        name_B)

    2)  names: data frame with 6 columns (weekdaysA, weekdaysB, fridaysA,
        fridaysB, weekendsA, weekendsB)
    """

    # indexes for names columns
    index_weekends_a = 0
    index_fridays_a = 0
    index_weekdays_a = 0

    # looping the month frame in column day
    for i, day in enumerate(month.loc[:, 'DAY']):

        # WEEKEND
        if day == 'Saturday' or day == 'Sunday':
            # check if index is out of bound
            if index_weekends_a == len(names):
                index_weekends_a = 0

            # save the name
            name = names.iloc[index_weekends_a, 4]
            index_weekends_a += 1  # increasing the index

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
        month.iloc[i, 3] = name  # i=current row, 3=column with names

    return month


def check_shift_a(shifts: pd.DataFrame) -> bool:
    """
    The function checks the shift A for back to back shift and corrects it.
    parameters: a data frame with the shifts.
    """

    double_shift = True  # boolean variable for the while loop

    while double_shift:

        # set the boolean variable as False. if there is no need for
        # correction in shifts, the while loop will terminate
        double_shift = False

        for i, name in enumerate(shifts.loc[:, 'A']):
            if i:  # if i is not 0

                # if name in current row is equal with the previous row name
                if shifts.iloc[i-1, 3] == name:

                    # if i+7 does not exceed the days of month(=len(month)),
                    # i swap the names below (the next same type day)
                    if (i+7 < len(shifts)):
                        shifts.iloc[i, 3], shifts.iloc[i+7, 3] =\
                            shifts.iloc[i+7, 3], shifts.iloc[i, 3]

                    # i+7 exceeds the days of month so the change completed
                    # above
                    else:
                        """the swap must become above"""
                        shifts.iloc[i, 3], shifts.iloc[i-7, 3] =\
                            shifts.iloc[i-7, 3], shifts.iloc[i, 3]

                    # found at least one double shift, while loop will run
                    # again to search for double shifts
                    double_shift = True
            else:
                """ ********** check the previous month **********"""
                pass

    return shifts


def fill_shift_b(month: pd.DataFrame, names: pd.DataFrame):

    # indexes for names columns
    index_weekends_b = 0
    index_fridays_b = 0
    index_weekdays_b = 0

    # looping the month data frame in column day
    for i, day in enumerate(month.loc[:, 'DAY']):

        # WEEKEND
        if day == 'Saturday' or day == 'Sunday':
            # check if index is out of bound
            if index_weekends_b == len(names):
                index_weekends_b = 0

            # save the name
            name = names.iloc[index_weekends_b, 5]
            index_weekends_b += 1  # increasing the index

        # FRIDAY
        elif day == 'Friday':
            # check if index is out of bound
            if index_fridays_b == len(names):
                index_fridays_b = 0

            # save the name
            name = names.iloc[index_fridays_b, 3]
            index_fridays_b += 1

        # WEEKDAY
        else:
            # check if index is out of bound
            if index_weekdays_b == len(names):
                index_weekdays_b = 0

            # save the name
            name = names.iloc[index_weekdays_b, 1]
            index_weekdays_b += 1

        # save the name that found in the row of the month data frame
        month.iloc[i, 4] = name  # i=current row, 3=column with names

    return month


def fill_n_check_b(months: pd.DataFrame, names: pd.DataFrame) -> pd.DataFrame:

    # creating lists with the names
    weekdays_b = list(names.loc[:, 'weekdays B'])
    fridays_b = list(names.loc[:, 'fridays B'])
    weekends_b = list(names.loc[:, 'weekends B'])

    # assistant lists
    weekday = []
    friday = []
    weekend = []

    # looping in the frame month
    for i, day in enumerate(months.loc[:, 'DAY']):

        while True:
            if day == 'Saturday' or day == 'Sunday':

                if i == 0:
                    break
                    if False:  # previous month check
                        pass

                elif i<len(months) - 1:
                    if weekend:
                        for name in weekend:
                            if months.iloc[i-1, 3] == name or months.iloc[i, 3] == name or months.iloc[i+1, 3] == name or months.iloc[i-1, 4] == name:
                                continue  # next name in list
                            else:
                                months.iloc[i, 4] = name
                                weekend.remove(name)
                                break  # out of the for loop

                    if months.iloc[i, 4] is None:
                        if months.iloc[i-1, 3] == weekends_b[0] or months.iloc[i, 3] == weekends_b[0] or months.iloc[i+1, 3] == weekends_b[0] or months.iloc[i-1, 4] == weekends_b[0]:
                            temp = weekends_b.pop(0)
                            weekends_b.append(temp)
                            weekend.append(temp)
                            continue  # try again in the same day

                        else:
                            months.iloc[i, 4] = weekends_b[0]  # fill the day
                            weekends_b.append(weekends_b.pop(0))  # put name at the end of list
                            break  # go to next day

                    else:
                        break  # go to next day
                
                else:
                    break  # i>=len

            elif day == 'Friday':
                if i == 0:
                    break
                    if False:  # previous month check
                        pass

                elif i<len(months) - 1:
                    if friday:
                        for name in friday:
                            if months.iloc[i-1, 3] == name or months.iloc[i, 3] == name or months.iloc[i+1, 3] == name or months.iloc[i-1, 4] == name:
                                continue  # next name in list
                            else:
                                months.iloc[i, 4] = name
                                friday.remove(name)
                                break  # out of the for loop

                    if months.iloc[i, 4] is None:
                        if months.iloc[i-1, 3] == fridays_b[0] or months.iloc[i, 3] == fridays_b[0] or months.iloc[i+1, 3] == fridays_b[0] or months.iloc[i-1, 4] == fridays_b[0]:
                            temp = fridays_b.pop(0)
                            fridays_b.append(temp)
                            friday.append(temp)
                            continue  # try again in the same day

                        else:
                            months.iloc[i, 4] = fridays_b[0]  # fill the day
                            fridays_b.append(fridays_b.pop(0))  # put name at the end of list
                            break  # go to next day

                    else:
                        break  # go to next day
                
                else:
                    break  # i>=len
            
            else:  # weekday
                if i == 0:
                    break
                    if False:  # previous month check
                        pass

                elif i<len(months) - 1:
                    if weekday:
                        for name in weekday:
                            if months.iloc[i-1, 3] == name or months.iloc[i, 3] == name or months.iloc[i+1, 3] == name or months.iloc[i-1, 4] == name:
                                continue  # next name in list
                            else:
                                months.iloc[i, 4] = name
                                weekday.remove(name)
                                break  # out of the for loop

                    if months.iloc[i, 4] is None:
                        if months.iloc[i-1, 3] == weekdays_b[0] or months.iloc[i, 3] == weekdays_b[0] or months.iloc[i+1, 3] == weekdays_b[0] or months.iloc[i-1, 4] == weekdays_b[0]:
                            temp = weekdays_b.pop(0)
                            weekdays_b.append(temp)
                            weekday.append(temp)
                            continue  # try again in the same day

                        else:
                            months.iloc[i, 4] = weekdays_b[0]  # fill the day
                            weekdays_b.append(weekdays_b.pop(0))  # put name at the end of list
                            break  # go to next day

                    else:
                        break  # go to next day

                else:
                    break  # i>=len

    # printing the leftovers
    print(f'weekday: {weekday}')
    print(f'friday: {friday}')
    print(f'weekend: {weekend}')


# creating the month data frame
month = create_month_frame()

# creating the names data frame
names = pd.read_excel(r'sort_data.xlsx')

# fill shift A
fill_shift_a(month, names)
# check shift A
check_shift_a(month)

# fill and check shift B
fill_n_check_b(month, names)

# print results
print(month)
