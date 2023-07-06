import pandas as pd
from process_last_names import (get_names_from_json, save_last_names_to_json,
                                save_leftovers_json, get_leftovers,
                                get_last_day, save_last_day)
from create_month import create_month_frame
# from my_exception import AboveTwoNamesException


class Shifts:
    """
    Objects Shifts represents a data frame with a month and its shifts.
    """

    def __init__(self) -> None:
        """
        Method initializes the attributes of the object.
        Also calls the methods to fill the data frame self.month with the
        shifts.

        self.month: Data frame that consists the days and the shifts

        self.names: Data frame that consists all names

        self.last_month_names: Dictionary that consists the names of the last
            shifts of the last month

        self.last_month_names_list: List with the names of the last shifts of
            the last month

        self.backups: Dictionary that has the backup names for the current
            month
        """

        # create frame with the month
        self.month = create_month_frame()

        # get names from excel in a data frame
        self.names = pd.read_excel(r'sort_data.xlsx')

        # get last month's names from json in a dictionary
        self.last_month_names = get_names_from_json()

        # list with the last names of the last month
        self.previous_month_last_day_names = get_last_day()

        # get the leftover names from the json file
        self.prev_leftovers = get_leftovers()

        # dictionary with the backup names
        self.backups = {'A': {'weekday': [], 'friday': [], 'weekend': []},
                        'B': {'weekday': [], 'friday': [], 'weekend': []}
                        }

        # dictionary for the last names in every category
        self.last_names_to_save = {'A': {'weekday': None, 'friday': None,
                                         'weekend': None},
                                   'B': {'weekday': None, 'friday': None,
                                         'weekend': None}
                                   }

        # dictionary to save the leftovers before save it in a json file
        self.leftovers = {'weekday': None, 'friday': None, 'weekend': None}

        "---------------------------------------------------------------------"
        "              FILLING THE MONTH AND PRINTING RESULTS"
        "---------------------------------------------------------------------"

        # fill shift A
        self.fill_shift_a()

        # check shift A
        self.check_shift_a()

        # fill and check shift B
        self.fill_n_check_b()

        # saving the last names of the current month in json file
        self.save_last_names_of_month()

        # saving the names that left over in json file
        self.handle_leftovers(self.leftovers)

        # saving the last day names in json file
        save_last_day([self.month.iloc[-1, 3], self.month.iloc[-1, 4]])

        # print results
        print(self.month)

        print('---------\nBACKUPS A')
        for key, names in self.backups['A'].items():
            print(f'{key} -> {names}')

        print('---------\nBACKUPS B')
        for key, names in self.backups['B'].items():
            print(f'{key} -> {names}')

    def fill_shift_a(self) -> None:
        """
        The method fills the month with names at column A.
        """

        # creating lists with the names
        weekdays = list(self.names.loc[:, 'weekdays A'])
        fridays = list(self.names.loc[:, 'fridays A'])
        weekends = list(self.names.loc[:, 'weekends A'])

        # modify the order of the lists
        while weekdays[-1] != self.last_month_names['last_weekday_a']:
            weekdays.append(weekdays.pop(0))

        while fridays[-1] != self.last_month_names['last_friday_a']:
            fridays.append(fridays.pop(0))

        while weekends[-1] != self.last_month_names['last_weekend_a']:
            weekends.append(weekends.pop(0))

        # looping the month frame in column DAY
        for i, day in enumerate(self.month.loc[:, 'DAY']):

            # WEEKEND
            if day == 'Saturday' or day == 'Sunday':
                # save the name in a variable
                name = weekends[0]
                weekends.append(weekends.pop(0))

            # FRIDAY
            elif day == 'Friday':
                # save the name in a variable
                name = fridays[0]
                fridays.append(fridays.pop(0))

            # WEEKDAY
            else:
                # save the name in a variable
                name = weekdays[0]
                weekdays.append(weekdays.pop(0))

            # save the name that found in the row of the month data frame
            self.month.iloc[i, 3] = name  # i=current row, 3=column with names

        # saving the last names that filled the month
        self.last_names_to_save['A']['weekday'] = weekdays[-1]
        self.last_names_to_save['A']['friday'] = fridays[-1]
        self.last_names_to_save['A']['weekend'] = weekends[-1]

        # filling the backup dict for shift A
        # WEEKDAYS
        self.backups['A']['weekday'].append(weekdays[0])
        self.backups['A']['weekday'].append(weekdays[1])

        # FRIDAYS
        self.backups['A']['friday'].append(fridays[0])
        self.backups['A']['friday'].append(fridays[1])

        # WEEKENDS
        self.backups['A']['weekend'].append(weekends[0])
        self.backups['A']['weekend'].append(weekends[1])

        return None

    def check_shift_a(self) -> None:
        """
        The function checks the shift A for back to back shift and corrects it.
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
                    if name in self.previous_month_last_day_names:

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

        """
        Assistant lists that filled with the leftovers from the previous month
        or empty
        """
        # WEEKDAY
        if self.prev_leftovers['weekday']:
            weekday = self.prev_leftovers['weekday']
        else:
            weekday = []

        # FRIDAY
        if self.prev_leftovers['friday']:
            friday = self.prev_leftovers['friday']
        else:
            friday = []

        # WEEKEND
        if self.prev_leftovers['weekend']:
            weekend = self.prev_leftovers['weekend']
        else:
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
                                        name in\
                                        self.previous_month_last_day_names:

                                    continue  # next name in list

                            else:  # last day of month
                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i-1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            # if code is here
                            # filling the day with the name
                            self.month.iloc[i, 4] = name
                            weekend.remove(name)  # remove it from the list

                            # saving it as the last name for this month
                            self.last_names_to_save['B']['weekend'] = name

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
                                    self.previous_month_last_day_names:

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

                        # saving it as the last name for this month
                        self.last_names_to_save['B']['weekend'] = weekends_b[0]

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
                                        name in\
                                        self.previous_month_last_day_names:

                                    continue  # next name in list

                            else:  # last day of month
                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i-1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            # if code is here
                            # filling the day with the name
                            self.month.iloc[i, 4] = name
                            friday.remove(name)  # remove it from the list

                            # saving it as the last name for this month
                            self.last_names_to_save['B']['friday'] = name

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
                                    self.previous_month_last_day_names:

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

                        # saving it as the last name for this month
                        self.last_names_to_save['B']['friday'] = fridays_b[0]

                        # put name at end of list
                        fridays_b.append(fridays_b.pop(0))

                        break  # go to next day

                    else:  # day filled from the assistant list
                        break  # go to next day

                else:  # day == weekday

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
                                        name in\
                                        self.previous_month_last_day_names:

                                    continue  # next name in list

                            else:  # last day of month
                                if self.month.iloc[i, 3] == name or\
                                    self.month.iloc[i-1, 3] == name or\
                                        self.month.iloc[i-1, 4] == name:

                                    continue  # next name in list

                            # if code is here
                            # filling the day with the name
                            self.month.iloc[i, 4] = name
                            weekday.remove(name)  # remove it from the list

                            # saving it as the last name for this month
                            self.last_names_to_save['B']['weekday'] = name

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
                                    self.previous_month_last_day_names:

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

                        # saving it as the last name for this month
                        self.last_names_to_save['B']['weekday'] = weekdays_b[0]

                        # put name at end of list
                        weekdays_b.append(weekdays_b.pop(0))

                        break  # go to next day

                    else:  # day filled from the assistant list
                        break  # go to next day

        # printing the leftovers
        print(f'weekday: {weekday}')
        print(f'friday: {friday}')
        print(f'weekend: {weekend}')

        "---------------------------------------------------------------------"
        "                  Filling the backup dict for shift B                "
        "---------------------------------------------------------------------"

        # WEEKDAYS
        if weekday:
            if len(weekday) >= 2:
                self.backups['B']['weekday'].append(weekday[0])
                self.backups['B']['weekday'].append(weekday[1])
                self.leftovers['weekday'] = weekday

            else:  # len(weekday) == 1
                self.backups['B']['weekday'].append(weekday[0])
                self.backups['B']['weekday'].append(weekdays_b[0])
                self.leftovers['weekday'] = weekday

        else:
            self.backups['B']['weekday'].append(weekdays_b[0])
            self.backups['B']['weekday'].append(weekdays_b[1])

        # FRIDAYS
        if friday:
            if len(friday) >= 2:
                self.backups['B']['friday'].append(friday[0])
                self.backups['B']['friday'].append(friday[1])
                self.leftovers['friday'] = friday

            else:  # len(friday) == 1
                self.backups['B']['friday'].append(friday[0])
                self.backups['B']['friday'].append(fridays_b[0])
                self.leftovers['friday'] = friday

        else:
            self.backups['B']['friday'].append(fridays_b[0])
            self.backups['B']['friday'].append(fridays_b[1])

        # WEEKENDS
        if weekend:
            if len(weekend) >= 2:
                self.backups['B']['weekend'].append(weekend[0])
                self.backups['B']['weekend'].append(weekend[1])
                self.leftovers['weekend'] = weekend

            else:  # len(weekend) == 1
                self.backups['B']['weekend'].append(weekend[0])
                self.backups['B']['weekend'].append(weekends_b[0])
                self.leftovers['weekend'] = weekend

        else:
            self.backups['B']['weekend'].append(weekends_b[0])
            self.backups['B']['weekend'].append(weekends_b[1])

    def save_last_names_of_month(self) -> None:

        save_last_names_to_json(day_a=self.last_names_to_save['A']['weekday'],
                                day_b=self.last_names_to_save['B']['weekday'],
                                fri_a=self.last_names_to_save['A']['friday'],
                                fri_b=self.last_names_to_save['B']['friday'],
                                wend_a=self.last_names_to_save['A']['weekend'],
                                wend_b=self.last_names_to_save['B']['weekend']
                                )

        return None

    def handle_leftovers(self, names: dict) -> None:
        """
        This method calls the function that saves the names that left over in a
        json file.

        Parameter: list with the names.
        """

        return save_leftovers_json(names)


for x in range(100):
    print('\n\n')
    Shifts()
