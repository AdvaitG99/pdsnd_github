import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'all']

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city's data would you like to access, Chicago, New York City or Washington? \n").lower()
    while city not in (CITY_DATA.keys()):
        print("Incorrect name entered. Please retry")
        city = input(
            "Input the name of the city whose data you would like to access again. Chicago, New York City or Washington. \n").lower()
    # get user filter for month or both(month and day)
    filter_input = input(
        "Would you like to filter the data by month, day, both or none at all? Type 'none' for no time filtering.\n").lower()

    if filter_input == 'month' or filter_input == 'both':
        month = input(
            "Which month would you like to choose? January, February, March, April, May, June or all? Please type the full name of the month.\n").lower()
        while month not in months:
            print("Please enter the name of the month correctly from the given options or type 'all'.")
            month = input(
                "Which month would you like to choose? January, February, March, April, May, June or all? Please type the full name of the month.\n").lower()
    else:
        month = 'all'
    # get user filter for day or both(Month and day)
    if filter_input == 'day' or filter_input == 'both':
        day = input(
            "Which day would you like to choose? mon = Monday, tue = Tuesday, wed = Wednesday, thu = Thursday, fri = Friday, sat = Saturday, sun = Sunday or all?\n").lower()
        while day not in days:
            print("Please enter correct day or type 'all'.")
            day = input(
                "Which day would you like to choose? mon = Monday, tue = Tuesday, wed = Wednesday, thu = Thursday, fri = Friday, sat = Saturday, sun = Sunday or all?\n").lower()
    else:
        day = 'all'
    # code for handling incorrect user input
    while filter_input not in (['month', 'day', 'both', 'none']):
        print("Input not recognized. Please type 'month', 'day' or 'none'.")
        filter_input = input(
            "Would you like to filter the data by month, day, both or none at all? Type 'none' for no time filtering.\n").lower()

    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # loading the  data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filtering by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filtering by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0]
    print("The most common month is: {}".format(month))

    # display the most common day of week
    day = df['day_of_week'].mode()[0]
    print("The most common day of the week is: {}".format(day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("The most common start hour is: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    combined_common_station = df['Start Station'] + " to " + df['End Station']
    print("The most common trip Starting and ending stations are {}".format(combined_common_station.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    print("Total travel time is: {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    print("The average travel time was: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print(user_type_count)

    # Display counts of gender
    if 'Gender' in (df.columns):
        gender_count = df['Gender'].value_counts()
        print(gender_count)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in (df.columns):
        year_born = df['Birth Year'].fillna(0).astype('int64')
        print('The earliest birth year is {}\n Most recent birth year is {}\n Most common year of birth is {}'.format(
            year_born.min(), year_born.max(), year_born.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays the raw data upon request of the user"""
    # https://knowledge.udacity.com/questions/740371
    view_raw_data = input("Would you like to see 5 rows of raw data? Type 'Yes' or 'No'.\n").lower()
    if view_raw_data == 'yes':
        count = 0
        while True:
            print(df.iloc[count: count + 5])
            ask = input("Do you want 5 more rows?\n")
            count += 5
            if ask != 'yes':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()