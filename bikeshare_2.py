import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
VALID_CITIES = ['chicago', 'new york', 'washington']
VALID_FILTER_MD = ['day', 'month', 'both', 'none']
VALID_MONTH = ['january', 'february', 'march', 'april', 'may', 'june']
VALID_WEEK_DAY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
'saturday', 'sunday']

FILTER_CRITERIA = None


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global FILTER_CRITERIA
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while True:   # to handle invalid inputs
        city = input("\nWould you like to see data for Chicago, New York, or Washington?\n").lower()
        if city in VALID_CITIES:
            break

    # Understand month or day filter
    month_day = None
    while True:   # to handle invalid inputs
        month_day = input("\nWould you like to filter the data by month, day, both or not at all? Type none for no filter. \n").lower()
        if month_day in VALID_FILTER_MD:
            break

    # get user input for month (all, january, february, ... , june)
    month = 'all'
    if month_day in ['month', 'both']:
        while True:   # to handle invlaid inputs
            month = input("\nWhich month - January, February, March, April, May, or June? \n").lower()
            if month in VALID_MONTH:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = 'all'
    if month_day in ['day', 'both']:
        while True:
            day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()
            if day in VALID_WEEK_DAY:
                break

    FILTER_CRITERIA = month_day  # Set it for leverage in other funcitons

    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # df['week_day_name'] = df['Start Time'].dt.weekday_name # Old version
    df['week_day_name'] = df['Start Time'].dt.day_name()  # New versions

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['week_day_name'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    print('Most common month:', df['month'].mode()[0],
        'Count:', df['month'].value_counts()[:1].sort_values(ascending=False).iloc[0],
        'Filter:', FILTER_CRITERIA)


    # display the most common day of week
    df['week_day_name'] = df['Start Time'].dt.day_name()
    print('Most common day of week is', df['week_day_name'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.strftime('%H')
    print('Most common start hour is', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most commonly used end station is:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['travel_trip'] = df['Start Station'] + ' - ' + df['End Station']
    print('Most frequent combination of start station and end station trip is:',
        df['travel_trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel time for given filter is:', df['Trip Duration'].sum())

    # display mean travel time
    print('\nMean Travel time for given filter is:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    if view_data in ['yes', 'ye', 'yep', 'yeah', 'y']:
        start_loc = 0
        while True:
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            if start_loc >= df.count()[0]:   # If start_loc exceeds record count, exit loop
                break
            view_data = input("Do you wish to continue?: ").lower()
            if view_data not in ['yes', 'ye', 'yep', 'yeah', 'y']:
                break


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    try:
        print('\nTypes of Users:\n', df['User Type'].value_counts())
    except KeyError as e:
        print('\nNote: Unable to find', str(e), 'data for the selected city')

    # Display counts of gender
    try:
        print('\nGender types and counts:\n', df['Gender'].value_counts())
    except KeyError as e:
        print('\nNote: Unable to find', str(e), 'data for the selected city')

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nEarliest year of birth:', df['Birth Year'].sort_values(ascending=True).iloc[0],
            'Recent year of birth', df['Birth Year'].sort_values(ascending=False).iloc[0],
            'Most common year of birth:', df['Birth Year'].value_counts().sort_values(ascending=False).index[0])
    except KeyError as e:
        print('\nNote: Unable to find', str(e), 'data for the selected city')

    # Display data
    display_data(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print('Filter Criteria:', city.title(), month.title(), day.title())
        df = load_data(city, month, day)
        if df.empty == True:
            print('No data found for this filter criteria', FILTER_CRITERIA)
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        FILTER_CRITERIA = None


if __name__ == "__main__":
    main()
