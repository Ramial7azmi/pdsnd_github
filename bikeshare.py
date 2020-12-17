import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(' Enter a city (chicago, new york city, washington)\n')
        city = city.lower()
        if city.lower()=='chicago' or city.lower()=='new york city' or city.lower()=='washington':
            break
        else: 
            print('Error input!\n')
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(' Enter a month (all, january, february, ... , june)\n')
        month = month.lower()
        if month.lower()=='all' or month.lower()=='january' or month.lower()=='march' or\
           month.lower()=='april' or month.lower()=='june' or month.lower()=='july' or\
           month.lower()=='august' or month.lower()=='september' or month.lower()=='october' or\
           month.lower()=='november' or month.lower()=='december':
            break
        else: 
            print('Error input!\n')
            continue
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(' Enter a day of week (all, monday, tuesday, ... sunday)\n')
        day = day.lower()
        if day.lower()=='all' or day.lower()=='monday' or day.lower()=='tuesday' or\
           day.lower()=='wednsday' or day.lower()=='thursday' or day.lower()=='friday' or\
           day.lower()=='saturday' or day.lower()=='sunday':
            break
        else: 
            print('Error input!\n')
            continue

    print('-'*40)
    return city, month, day


def display_raw_data(df):
    """
    
    Display users data 5 raw at a time if user input any thing except ('no').

    """
    i = 0
    raw = input("Would you like to display 5 users Data, (input: 'no' to stop)\n") 
    
    pd.set_option('display.max_columns',200)

    while True:    
        # TO DO: convert the user input to lower case using lower() function
        if raw.lower() == 'no':
            break
        print(df[i:i+5])
        raw = input("would you like to display more? (input: 'no' to stop") 
        i += 5

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month, max( count grouped by month)
    dfCountMonth = df.groupby(['month']).count()[['Start Time']]
    dfCountMonthL=dfCountMonth.values.tolist()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',\
              'october', 'november', 'december']
    print("most common month is",months[dfCountMonthL.index(max(dfCountMonthL))])


    # TO DO: display the most common day of week, max( count grouped by day of week)
    dayOfWeek = ['monday', 'tuesday', 'wendnsday', 'thursday', 'friday',\
                 'saturday', 'sunday']
    dfCountDay = df.groupby(['day_of_week']).count()[['Start Time']]
    dfCountDayL=dfCountDay.values.tolist()
    print("most common day of week is",dayOfWeek[dfCountDayL.index(max(dfCountDayL))])


    # TO DO: display the most common start hour, max( count grouped by hours)
    df['hour'] = df['Start Time'].dt.hour
    dfCountHour = df.groupby(['hour']).count()[['Start Time']]
    dfCountHourL=dfCountHour.values.tolist()
    print("most common start hour is",dfCountHourL.index(max(dfCountHourL))+1)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station, max ( count grouped by start station) - 1
    StartStation= df['Start Station'].sort_values().unique()
    dfCountStation = df.groupby(['Start Station']).count()[['Start Time']]
    dfCountStationL=dfCountStation.values.tolist()
    print("most common start Station is",StartStation[dfCountStationL.index(max(dfCountStationL))])


    # TO DO: display most commonly used end station, max ( count grouped by end station) - 2
    EndStation= df['End Station'].sort_values().unique()
    dfCountEndStation = df.groupby(['End Station']).count()[['Start Time']]
    dfCountEndStationL=dfCountEndStation.values.tolist()
    print("most common End Station is",EndStation[dfCountEndStationL.index(max(dfCountEndStationL))])


    # TO DO: display most frequent combination of start station and end station trip, max ( 1 & 2)
    dfEndStartStation =  df[['Start Station','Start Time']].append( df[['End Station','Start Time']].\
                                                                  rename(columns={'End Station': 'Start Station'}))
    #dfEndStartStation = pd.DataFrame({'Start Station':EndStartStationL})
    EndStartStation= dfEndStartStation['Start Station'].sort_values().unique()
    dfCountEndStartStation = dfEndStartStation.groupby(['Start Station']).count()
    dfCountEndStartStationL=dfCountEndStartStation.values.tolist()
    print("most common Start & End Station is",\
          EndStartStation[dfCountEndStartStationL.index(max(dfCountEndStartStationL))])
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time, sum of duration
    print("the sum of total duration is",df['Trip Duration'].sum() , "minutes")

    # TO DO: display mean travel time, avr of duration
    print("the mean duration is",df['Trip Duration'].mean() , "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types, group by user type
    print("this is the counts of user type\n",df.groupby(['User Type']).count()[['Start Time']])

    # TO DO: Display counts of gender, group by gender
    try:
        print("\nthis is the counts of gender\n",df.groupby(['Gender']).count()[['Start Time']])
    except:
        print("\nNo gender Data!")
            
    # TO DO: Display earliest, most recent, and most common year of birth, (min, max and group by year)
    try:
        YearBirth= df['Birth Year'].sort_values().unique()
        dfCountYearBirth = df.groupby(['Birth Year']).count()[['Start Time']]
        dfCountYearBirthL= dfCountYearBirth.values.tolist()
        print("\nthese are the earliest, most recent, and most common year of birth",\
             int(df['Birth Year'].min()),',', int(df['Birth Year'].max()),'and',\
             int(YearBirth[dfCountYearBirthL.index(max(dfCountYearBirthL))]))
    except:
        print("\nNo Birth day Data!")
            
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
