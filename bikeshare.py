import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def process_month():
    '''Requests month and continues request until data is cleanly obtained'''
    month = input('Which month ? January, February, March, April, May, or June ?\n')
    while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june']:
        month = input('\nPlease pick one of : January, February, March, April, May, or June.\n')
    return month

def process_day():
    '''Requests day and continues request until data is cleanly obtained.'''
    day = input('Which day ? Pick a whole number, i.e., Monday=0 ... Sunday=6.\n')
    while int(day) not in [0, 1, 2, 3, 4, 5, 6]:
        day = input('\nPlease pick a day by selecting a whole number, i.e., Monday=0 ... Sunday=6.\n')
    return int(day)

def get_filters():
    """
    Asks user to specify a city, month, day, or no date filter to analyze bike data.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) no_filter - none, if no date filter is required
    """
    print('\nHello ! Let\'s explore some US bikeshare data !\n')
    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington ?\n')
    while city.lower() not in ['chicago', 'new york city', 'washington']:
        city = input('\nI did not understand your answer. Please indicate one of : Chicago, New York, or Washington.\n')
    # get user input for month (all, january, february, ... , june)
    date_filter = input("\nWould you like to filter the data by month, day, both, or not at all ?\nIndicate 'none' for no date filter.\n")
    while date_filter.lower() not in ['month', 'day', 'both', 'none']:
        date_filter = input('\nI did not understand your answer. Please indicate one of : month, day, both, or none.\n')
    if date_filter.lower() == 'month':
        month = process_month()
        day = None
        no_filter = None
    if date_filter.lower() == 'day':
        month = None
        day = process_day()
        no_filter = None
    if date_filter.lower() == 'both':
        month = process_month()
        day = process_day()
        no_filter = None
    if date_filter.lower() == 'none':
        month = None
        day = None
        no_filter = None
    print('\n' + '-'*40 + '\n')
    return city, month, day, no_filter


def load_data(city, month, day, no_filter):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) no_filter - none, if no date filter is required
    Returns:
        (Dataframe) df - Pandas DataFrame containing city data filtered by month and day
    """
    month_dict = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6}
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    if (month == None) & (day == None) & (no_filter == None):
        df = df
    elif (month is not None) & (day is not None) & (no_filter == None):
        df = df[(df['month'] == month_dict[month.lower()]) & (df['day_of_week'] == day)]
    elif (month is not None) & (day == None) & (no_filter == None):
        df = df[df['month'] == month_dict[month.lower()]]
    elif (month == None) & (day is not None) & (no_filter == None):
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df, month, day, no_filter):
    """Displays statistics on the most frequent times of travel.
    Args:
        (data) df - pandas Dataframe of data filtered by city and date (if any)
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) no_filter - none, if no date filter is required
    Returns:
        (Dataframe) df - Updated pandas DataFrame with new date columns (if any)
    """
    month_dict = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June'}
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if (month == None) & (day == None) & (no_filter == None):
        print("\nUsing no data filter, here is analysis of the bike share data :\n")
        # display the most common month
        common_month_mode = df['month'].mode()[0]
        # convert to name ;
        converted_month = month_dict[str(common_month_mode)]
        print("The most common month is : {}.".format(converted_month))
        # display the most common day of week
        common_day = df['day_of_week'].mode()[0]
        print("The most common day is : {} (where Monday=0 ... Sunday=6).".format(common_day))
        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        common_hour = df['hour'].mode()[0]
        print("The most common start hour is : {} (in U.S. military time).".format(common_hour))
    elif (month is not None) & (day is not None) & (no_filter == None):
        print("\nUsing a month and day filter, here is analysis of the bike share data :\n")
        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        common_hour = df['hour'].mode()[0]
        print("The most common start hour is : {} (in U.S. military time).".format(common_hour))
    elif (month is not None) & (day == None) & (no_filter == None):
        print("\nUsing a month filter, here is analysis of the bike share data :\n")
        # display the most common day of week
        common_day = df['day_of_week'].mode()[0]
        print("The most common day is : {} (where Monday=0 ... Sunday=6).".format(common_day))
        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        common_hour = df['hour'].mode()[0]
        print("The most common start hour is : {} (in U.S. military time).".format(common_hour))
    elif (month == None) & (day is not None) & (no_filter == None):
        print("\nUsing a day filter, here is analysis of the bike share data :\n")
        # display the most common month
        common_month_mode = df['month'].mode()[0]
        # convert to name ;
        converted_month = month_dict[str(common_month_mode)]
        print("The most common month is : {}.".format(converted_month))
        # display the most common start hour
        df['hour'] = df['Start Time'].dt.hour
        common_hour = df['hour'].mode()[0]
        print("The most common start hour is : {} (in U.S. military time).".format(common_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df


def station_stats(df):
    """Displays station and trip statistics.
    Args:
        (data) df - Updated pandas Dataframe of data filtered by city and date (if any)
    Returns:
        Outputs : Displays statistics on the most popular stations and trip.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is : {}.".format(common_start_station))
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station is : {}.".format(common_end_station))
    # display most frequent combination of start station and end station tri
    frequent_combination = df.groupby(['Start Station','End Station']).size().reset_index()
    print("The most frequent combination of stations are :")
    print("Start station : {}".format(frequent_combination.max()['Start Station']))
    print("End station : {}".format(frequent_combination.max()['End Station']))
    print("This combination of stations had {} trips.".format(frequent_combination.max()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays trip length statistics.
    Args:
        (data) df - Updated pandas Dataframe of data filtered by city and date (if any)
    Returns:
        Outputs : Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    days = (60 * 60 * 24)
    hours = (60 * 60)
    minutes = 60
    total_time = df['Trip Duration'].sum()
    total_days = total_time // days
    remaining_time = total_time % days
    total_hours = remaining_time // hours
    remaining_time = remaining_time % hours
    total_minutes = remaining_time // minutes
    total_seconds = remaining_time % minutes
    print("The total travel time was :")
    print("Days : {}".format(total_days))
    print("Hours : {}".format(total_hours))
    print("Minutes : {}".format(total_minutes))
    print("Seconds : {}".format(total_seconds))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time (in seconds) is : {}".format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays user data.
    Args:
        (data) df - Updated pandas Dataframe of data filtered by city and date (if any)
    Returns:
        Outputs : Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('The breakdown in User Types is : ')
    print(count_user_type)
    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        print('\nThe breakdown by Gender is : ')
        print(count_gender)
    except KeyError:
        pass
    # Display earliest, most recent, and most common year of birth
    try:
        mask_df = df.dropna(axis=0)
        earliest_year = int(mask_df['Birth Year'].min())
        recent_year = int(mask_df['Birth Year'].max())
        common_year = int(mask_df['Birth Year'].mode()[0])
        print("\nThe earliest year is : {}".format(earliest_year))
        print("The most recent year is : {}".format(recent_year))
        print("The most common year is : {}".format(common_year))
    except KeyError:
        pass
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_data(df):
    """Displays rows of raw data upon request.
    Args:
        (data) df - Updated pandas Dataframe of data filtered by city and date (if any)
    Returns:
        Outputs : Displays chunks of the dataframe 5 rows at a time.
    """
    see_data = input('\nWould you like to see the first five rows of data ? yes or no\n')
    while see_data.lower() not in ['yes', 'no']:
        city = input('\nI did not understand your answer. Please choose : yes or no.\n')
    start = 0
    while see_data == 'yes':
        print(df.iloc[start:start+5])
        start += 5
        see_data = input('\nWould you like to see the next five rows of data ? yes or no\n')
    print('\nI hope you found this data analysis helpful. Thank you.\n')

def main():
    while True:
        city, month, day, no_filter = get_filters()
        # Dataframe is created based on city and time slection (if any)
        df = load_data(city, month, day, no_filter)
        # Dataframe is updated with new columns for time calculations
        df = time_stats(df, month, day, no_filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
