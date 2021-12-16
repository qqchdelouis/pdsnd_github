import time
import pandas as pd
import numpy as np

CITY_DATA = { "chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }

city_message = """For which city would you like to see bike share data for :\n
Chicago, New York City, or Washington ?\n
"""

city_correction_message = """\nI did not understand your answer.\n
Please indicate one of : Chicago, New York, or Washington.\n
"""

date_message = """\nWould you like to filter the data by month, day, both, or not at all ?\n
Indicate 'none' for no date filter.\n
"""

date_correction_message = """\nI did not understand your answer.\n
Please indicate one of : month, day, both, or none.\n
"""

def process_month():
    month = input("Which month ? January, February, March, April, May, or June ?\n")
    while month.lower() not in ["january", "february", "march", "april", "may", "june"]:
        month = input("\nPlease pick one of : January, February, March, April, May, or June.\n")
    return month


def process_day():
    day = input("Which day ? Pick a whole number, i.e., Monday=0 ... Sunday=6.\n")
    while int(day) not in [0, 1, 2, 3, 4, 5, 6]:
        day = input("\nPlease pick a day by selecting a whole number, i.e., Monday=0 ... Sunday=6.\n")
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
    print("\nHello ! Let's explore some US bikeshare data !\n")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(city_message)
    while city.lower() not in ["chicago", "new york city", "washington"]:
        city = input(city_correction_message)
    # get user input for month (all, january, february, ... , june)
    date_filter = input(date_message)
    while date_filter.lower() not in ["month", "day", "both", "none"]:
        date_filter = input(date_correction_message)
    if date_filter.lower() == "month":
        month = process_month()
        day = None
        no_filter = None
    if date_filter.lower() == "day":
        month = None
        day = process_day()
        no_filter = None
    if date_filter.lower() == "both":
        month = process_month()
        day = process_day()
        no_filter = None
    if date_filter.lower() == "none":
        month = None
        day = None
        no_filter = None
    print("\n" + "-"*40 + "\n")
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    month_dict = {"january":1, "february":2, "march":3, "april":4, "may":5, "june":6}
    df = pd.read_csv(CITY_DATA[city.lower()])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = pd.DatetimeIndex(df["Start Time"]).month
    df["day_of_week"] = pd.DatetimeIndex(df["Start Time"]).dayofweek
    if (month == None) & (day == None) & (no_filter == None):
        df = df
    elif (month is not None) & (day is not None) & (no_filter == None):
        df = df[(df["month"] == month_dict[month.lower()]) & (df["day_of_week"] == day)]
    elif (month is not None) & (day == None) & (no_filter == None):
        df = df[df["month"] == month_dict[month.lower()]]
    elif (month == None) & (day is not None) & (no_filter == None):
        df = df[df["day_of_week"] == day]
    return df


def month_stats(x):
    # display the most common month
    month_dict = {"1":"January", "2":"February", "3":"March", "4":"April", "5":"May", "6":"June"}
    converted_month = month_dict[str(x)]
    print("The most common month is : {}.".format(converted_month))


def day_stats(x):
    # display the most common day of week
    print("The most common day is : {} (where Monday=0 ... Sunday=6).".format(x))


def hour_stats(x):
    # display the most common start hour
    print("The most common start hour is : {} (in U.S. military time).".format(x))




def time_stats(df, month, day, no_filter):
    """Displays statistics on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    # calculate the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    if (month == None) & (day == None) & (no_filter == None):
        print("\nUsing no data filter, here is analysis of the bike share data :\n")
        # display the most common month
        month_stats(df["month"].mode()[0])
        # display the most common day of week
        day_stats(df["day_of_week"].mode()[0])
        # display the most common start hour
        hour_stats(common_hour)
    elif (month is not None) & (day is not None) & (no_filter == None):
        print("\nUsing a month and day filter, here is analysis of the bike share data :\n")
        # display the most common start hour
        hour_stats(common_hour)
    elif (month is not None) & (day == None) & (no_filter == None):
        print("\nUsing a month filter, here is analysis of the bike share data :\n")
        # display the most common day of week
        day_stats(df["day_of_week"].mode()[0])
        # display the most common start hour
        hour_stats(common_hour)
    elif (month == None) & (day is not None) & (no_filter == None):
        print("\nUsing a day filter, here is analysis of the bike share data :\n")
        # display the most common month
        month_stats(df["month"].mode()[0])
        # display the most common start hour
        hour_stats(common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)
    return df


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()
    # display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print("The most common start station is : {}.".format(common_start_station))
    # display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print("The most common end station is : {}.".format(common_end_station))
    # display most frequent combination of start station and end station tri
    frequent_combination = df.groupby(["Start Station","End Station"]).size().reset_index()
    print("\nThe most frequent combination of stations are :")
    print("Start station : {}".format(frequent_combination.max()["Start Station"]))
    print("End station : {}".format(frequent_combination.max()["End Station"]))
    print("This combination of stations had {} trips.".format(frequent_combination.max()[0]))
    least_combination = df.groupby(["Start Station","End Station"]).size().sort_values(ascending=True).reset_index()
    print("\nAn example of a station combination with the least trips :")
    print("Start station : {}".format(least_combination.min()["Start Station"]))
    print("End station : {}".format(least_combination.min()["End Station"]))
    if least_combination.min()[0] == 1:
        print("This combination of stations had {} trip.".format(least_combination.min()[0]))
    else:
        print("This combination of stations had {} trips.".format(least_combination.min()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()
    # display total travel time
    days = (60 * 60 * 24)
    hours = (60 * 60)
    minutes = 60
    total_time = df["Trip Duration"].sum()
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
    pandas_mean_travel_time = df["Trip Duration"].mean()
    print("\nUsing pandas, the mean travel time (in seconds) is : {}".format(pandas_mean_travel_time))
    travel_time_array = np.array(df["Trip Duration"])
    numpy_mean_travel_time = travel_time_array.mean()
    print("Using numpy, the mean travel time (in seconds) is : {}".format(numpy_mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()
    # Display counts of user types
    try:
        count_user_type = df["User Type"].value_counts()
        print("The breakdown in User Types is : ")
        print("\nThe number of Subscriber Users is : {}".format(count_user_type["Subscriber"]))
        print("The number of Customer Users is : {}".format(count_user_type["Customer"]))
    except KeyError:
        pass    
    # Display counts of gender
    try:
        count_gender = df["Gender"].value_counts()
        print("\nThe breakdown by Gender is : ")
        print("\nThe number of Male Users is : {}".format(count_gender["Male"]))
        print("The number of Female Users is : {}".format(count_gender["Female"]))
    except KeyError:
        pass
    # Display earliest, most recent, and most common year of birth
    try:
        mask_df = df.dropna(axis=0)
        earliest_year = int(mask_df["Birth Year"].min())
        recent_year = int(mask_df["Birth Year"].max())
        common_year = int(mask_df["Birth Year"].mode()[0])
        print("\nAn inspection of Users' years of birth is : ")
        print("\nThe earliest year is : {}".format(earliest_year))
        print("The most recent year is : {}".format(recent_year))
        print("The most common year is : {}".format(common_year))
    except KeyError:
        pass
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def show_data(df):
    """Displays checks of the dataframe 5 rows at a time."""
    see_data = input("\nWould you like to see the first five rows of data ? yes or no\n")
    while see_data.lower() not in ["yes", "no"]:
        city = input("\nI did not understand your answer. Please choose : yes or no.\n")
    start = 0
    while see_data == "yes":
        print(df.iloc[start:start+5])
        start += 5
        see_data = input("\nWould you like to see the next five rows of data ? yes or no\n")
    print("\nI hope you found this data analysis helpful. Thank you.\n")

def main():
    while True:
        city, month, day, no_filter = get_filters()
        df = load_data(city, month, day, no_filter)
        df = time_stats(df, month, day, no_filter)
        # time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
	main()
