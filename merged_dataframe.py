import pandas as pd
from process_last_names import get_names_from_json, save_last_names_to_json
from create_month import create_month_frame


class Shifts:
    """
    Objects Shifts represents a data frame with a month and its shifts.
    """

    def __init__(self) -> None:

        # create frame with the month
        self.month = create_month_frame()

        # get names from excel in a data frame
        self.names = pd.read_excel(r'sort_data.xlsx')

        # get last month's names from json in a dictionary
        self.last_month_names = get_names_from_json()

        # list with the last names of the last month
        self.last_month_names_list = list(self.last_month_names.values())

        "***************FILLING THE MONTH AND PRINTING RESULTS****************"

        # fill shift A
        self.fill_shift_a()
        # check shift A
        self.check_shift_a()

        # fill and check shift B
        self.fill_n_check_b()

        # print results
        print(self.month)

    def fill_shift_a(self) -> None:
        """
        """

        # creating lists with the names
        weekdays = list(self.names.loc[:, 'weekdays A'])
        fridays = list(self.names.loc[:, 'fridays A'])
        weekends = list(self.names.loc[:, 'weekends A'])

        """indexes for names columns"""

        # using the names from the json file to find the indexes in the list
        # and start filling the shifts from the next one
        index_weekends =\
            weekends.index(self.last_month_names['last_weekend_a']) + 1

        index_fridays =\
            fridays.index(self.last_month_names['last_friday_a']) + 1

        index_weekdays =\
            weekdays.index(self.last_month_names['last_weekday_a']) + 1

        # looping the month frame in column DAY
        for i, day in enumerate(self.month.loc[:, 'DAY']):

            # WEEKEND
            if day == 'Saturday' or day == 'Sunday':
                # check if index is out of bound
                if index_weekends == len(self.names):
                    index_weekends = 0

                # save the name
                name = self.names.iloc[index_weekends, 4]
                index_weekends += 1  # increasing the index

            # FRIDAY
            elif day == 'Friday':
                # check if index is out of bound
                if index_fridays == len(self.names):
                    index_fridays = 0

                # save the name
                name = self.names.iloc[index_fridays, 2]
                index_fridays += 1

            # WEEKDAY
            else:
                # check if index is out of bound
                if index_weekdays == len(self.names):
                    index_weekdays = 0

                # save the name
                name = self.names.iloc[index_weekdays, 0]
                index_weekdays += 1

            # save the name that found in the row of the month data frame
            self.month.iloc[i, 3] = name  # i=current row, 3=column with names

        return None

    def check_shift_a(self) -> None:
        """
        The function checks the shift A for back to back shift and corrects it.
        parameters: a data frame with the shifts.
        """

        double_shift = True  # boolean variable for the while loop

        while double_shift:

            # set the boolean variable as False. if there is no need for
            # correction in shifts, the while loop will terminate
            double_shift = False

            for i, name in enumerate(self.month.loc[:, 'A']):
                if i:  # if i is not 0

                    # if name in current row is equal with the previous name
                    if self.month.iloc[i-1, 3] == name:

                        # if i+7 does not exceed the days of
                        # month(=len(month)), i swap the names below
                        # (the next same type day)
                        if (i+7 < len(self.month)):
                            self.month.iloc[i, 3], self.month.iloc[i+7, 3] =\
                                self.month.iloc[i+7, 3], self.month.iloc[i, 3]

                        # i+7 exceeds the days of month so the change will be
                        # completed above
                        else:
                            """the change must become in the above same day"""
                            self.month.iloc[i, 3], self.month.iloc[i-7, 3] =\
                                self.month.iloc[i-7, 3], self.month.iloc[i, 3]

                        # found at least one double shift, while loop will run
                        # again to search for double shifts
                        double_shift = True

                    """***** check previous month for the first day *****"""
                else:
                    # if first name in current month had a shift the last day
                    # of the previous month
                    if name in self.last_month_names_list:

                        # doing the swap
                        self.month.iloc[i, 3], self.month.iloc[i+7, 3] =\
                            self.month.iloc[i+7, 3], self.month.iloc[i, 3]

                        # found at least one double shift, while loop will run
                        # again to search for double shifts
                        double_shift = True
        return None

    def fill_n_check_b(self) -> None:

        # creating lists with the names
        weekdays_b = list(self.names.loc[:, 'weekdays B'])
        fridays_b = list(self.names.loc[:, 'fridays B'])
        weekends_b = list(self.names.loc[:, 'weekends B'])

        # modify the order of the lists
        while weekdays_b[-1] != self.last_month_names['last_weekday_b']:
            weekdays_b.append(weekdays_b.pop(0))

        while fridays_b[-1] != self.last_month_names['last_friday_b']:
            fridays_b.append(fridays_b.pop(0))

        while weekends_b[-1] != self.last_month_names['last_weekend_b']:
            weekends_b.append(weekends_b.pop(0))

        # assistant lists
        weekday = []
        friday = []
        weekend = []

        # looping in the frame month
        for i, day in enumerate(self.month.loc[:, 'DAY']):

            while True:
                if day == 'Saturday' or day == 'Sunday':

                    # first checking if the assistant list has names
                    if weekend:
                        # looping in the names of the list and checking if
                        # there is any suitable for filling the day
                        for name in weekend:
                            if i > 0 and i < len(self.month) - 1:
                                if self.month.iloc[i-1, 3] == name or\
                                    self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i+1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            elif i == 0:
                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i+1, 3] == name or\
                                        name in self.last_month_names_list:

                                    continue  # next name in list

                            else:  # last day of month
                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i-1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            # if code is here
                            # filling the day with the name
                            self.month.iloc[i, 4] = name
                            weekend.remove(name)
                            break  # out of the for loop

                    # if day has not filled from above
                    if self.month.iloc[i, 4] is None:

                        if i > 0 and i < len(self.month) - 1:

                            # checking if the first available name in the
                            # original list is suitable to fill the day
                            if self.month.iloc[i-1, 3] == weekends_b[0] or\
                                self.month.iloc[i, 3] == weekends_b[0] or\
                                self.month.iloc[i+1, 3] == weekends_b[0] or\
                                    self.month.iloc[i-1, 4] == weekends_b[0]:

                                # putting the name at the end of the original
                                # list and adding it at the assistant list
                                temp = weekends_b.pop(0)
                                weekends_b.append(temp)
                                weekend.append(temp)
                                continue  # try again in the same day

                        elif i == 0:

                            if self.month.iloc[i, 3] == weekends_b[0] or\
                                self.month.iloc[i+1, 3] == weekdays_b[0]\
                                    or weekends_b[0] in\
                                    self.last_month_names_list:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = weekends_b.pop(0)
                                weekends_b.append(temp)
                                weekend.append(temp)
                                continue  # try again in the same day

                        else:  # last day of month
                            if self.month.iloc[i, 3] == weekdays_b[0] or\
                                self.month.iloc[i-1, 3] == weekends_b[0]\
                                    or self.month.iloc[i-1, 4] ==\
                                    weekends_b[0]:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = weekends_b.pop(0)
                                weekends_b.append(temp)
                                weekend.append(temp)
                                continue  # try again in the same day

                        # fill the day
                        self.month.iloc[i, 4] = weekends_b[0]

                        # put name at the end of list
                        weekends_b.append(weekends_b.pop(0))

                        break  # go to next day

                    else:  # day filled from the assistant list
                        break  # go to next day

                elif day == 'Friday':
                    if friday:
                        for name in friday:

                            if i > 0 and i < len(self.month) - 1:
                                if self.month.iloc[i-1, 3] == name or\
                                    self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i+1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            elif i == 0:

                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i+1, 3] == name or\
                                        name in self.last_month_names_list:

                                    continue  # next name in list

                            else:  # last day of month
                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i-1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            self.month.iloc[i, 4] = name
                            friday.remove(name)
                            break  # out of the for loop

                    if self.month.iloc[i, 4] is None:

                        if i > 0 and i < len(self.month) - 1:
                            if self.month.iloc[i-1, 3] == fridays_b[0] or\
                                self.month.iloc[i, 3] == fridays_b[0] or\
                                self.month.iloc[i+1, 3] == fridays_b[0] or\
                                    self.month.iloc[i-1, 4] == fridays_b[0]:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = fridays_b.pop(0)
                                fridays_b.append(temp)
                                friday.append(temp)
                                continue  # try again in the same day

                        elif i == 0:

                            if self.month.iloc[i, 3] == fridays_b[0] or\
                                self.month.iloc[i+1, 3] == fridays_b[0]\
                                    or weekends_b[0] in\
                                    self.last_month_names_list:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = fridays_b.pop(0)
                                fridays_b.append(temp)
                                friday.append(temp)
                                continue  # try again in the same day

                        else:  # last day of month

                            if self.month.iloc[i, 3] == fridays_b[0] or\
                                self.month.iloc[i-1, 3] == fridays_b[0]\
                                    or self.month.iloc[i-1, 4] ==\
                                    fridays_b[0]:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = fridays_b.pop(0)
                                fridays_b.append(temp)
                                friday.append(temp)
                                continue  # try again in the same day

                        # fill the day
                        self.month.iloc[i, 4] = fridays_b[0]

                        # put name at end of list
                        fridays_b.append(fridays_b.pop(0))

                        break  # go to next day

                    else:  # day filled from the assistant list
                        break  # go to next day

                else:  # weekday

                    if weekday:
                        for name in weekday:

                            if i > 0 and i < len(self.month) - 1:
                                if self.month.iloc[i-1, 3] == name or\
                                    self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i+1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            elif i == 0:

                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i+1, 3] == name or\
                                        name in self.last_month_names_list:

                                    continue  # next name in list

                            else:  # last day of month
                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i-1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            self.month.iloc[i, 4] = name
                            weekday.remove(name)
                            break  # out of the for loop

                    if self.month.iloc[i, 4] is None:

                        if i > 0 and i < len(self.month) - 1:
                            if self.month.iloc[i-1, 3] == weekdays_b[0] or\
                                self.month.iloc[i, 3] == weekdays_b[0] or\
                                self.month.iloc[i+1, 3] == weekdays_b[0] or\
                                    self.month.iloc[i-1, 4] == weekdays_b[0]:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = weekdays_b.pop(0)
                                weekdays_b.append(temp)
                                weekday.append(temp)
                                continue  # try again in the same day

                        elif i == 0:

                            if self.month.iloc[i, 3] == weekdays_b[0] or\
                                self.month.iloc[i+1, 3] == weekdays_b[0]\
                                    or weekdays_b[0] in\
                                    self.last_month_names_list:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = weekdays_b.pop(0)
                                weekdays_b.append(temp)
                                weekday.append(temp)
                                continue  # try again in the same day

                        else:  # last day of month

                            if self.month.iloc[i, 3] == weekdays_b[0] or\
                                self.month.iloc[i-1, 3] == weekdays_b[0]\
                                    or self.month.iloc[i-1, 4] ==\
                                    weekdays_b[0]:

                                # putting the name at the end of the
                                # original list and adding it at the
                                # assistant list
                                temp = weekdays_b.pop(0)
                                weekdays_b.append(temp)
                                weekday.append(temp)
                                continue  # try again in the same day

                        # fill the day
                        self.month.iloc[i, 4] = weekdays_b[0]

                        # put name at end of list
                        weekdays_b.append(weekdays_b.pop(0))

                        break  # go to next day

                    else:  # day filled from the assistant list
                        break  # go to next day

        # printing the leftovers
        print(f'weekday: {weekday}')
        print(f'friday: {friday}')
        print(f'weekend: {weekend}')


x = Shifts()
