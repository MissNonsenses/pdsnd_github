import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months_filter = ['January', 'February', 'March', 'April', 'May', 'June']
days_filter = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

"""Converts trip duration (seconds) into days, hours, minuts and seconds and print the convertion"""
def convert_time (trip_duration):
     
        day = trip_duration // 86400
        rest = trip_duration % 86400
        hour = rest // 3600
        rest %= 3600
        minut = rest // 60
        second =rest %60

        print ("{} days {} hours {} minuts {} seconds.\n".format(day, hour, minut, second))
        


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city= input('\n1. Would you like to see data for Chicago, New York City, or Washington?\n').lower()
    
    while city not in CITY_DATA:
        
        print('\nSorry, {} is not a city available in database.'. format(city))
        city= input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
    
    # get user input for month (all, january, february, ... , june)
    filter_date = input('\n2. Would you like to filter the data by month, day, both or not at all? (type \"all\" for raw data)\n').lower()
    
    while filter_date not in ('month', 'day', 'both', 'all'):
        # if filter no in correct format asks user again
        print('\nSorry, filter not recognized. Try again.')
        filter_date = input('\n2. Would you like to filter the data by month, day, both or not at all? (type \"all\" for raw data)\n').lower()
    

    if filter_date == 'month' or filter_date == 'both':
        month = input('\n3. Which month - January, February, March, April, May, or June?\n').title()
        #if month is not in list asks user again
        while month not in months_filter:
            print('\nSorry, {} is not a valid filter for month.'.format(month))
            month = input('\n3. Which month - January, February, March, April, May, or June?\n').title()
    else:
        month = 'all'       

    if filter_date == 'day' or filter_date == 'both': 
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('\n4. Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
        # if day is not correct asks the user again
        while day not in days_filter:
            print('\nSorry, {} is not a valid filter for day.'.format(day))
            day = input('\n4. Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()    
    else:
         day = 'all'
       
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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
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

    # display the most common month
    df_month = df['month'].mode()[0]
    print('\nMost common month: {}'.format(months_filter[df_month-1]))

    # display the most common day of week
    df_day = df['day_of_week'].mode()[0]
    print('\nMost common day of week: {}'.format(df_day))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    df_hour = df['Hour'].mode()[0]
    print('\nMost common start hour: {}'.format(df_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df_Start_St = df['Start Station'].mode()[0]
    print('\nMost commonly used start station is {}.'.format(df_Start_St))

    # display most commonly used end station
    df_End_St = df['End Station'].mode()[0]
    print('\nMost commonly used end station is {}.'.format(df_End_St))

    # display most frequent combination of start station and end station trip
    df_Combi_St = df['Start Station'] +"  &  " +df['End Station']
    df_Combi_St = df_Combi_St.mode()[0]
    print('\nMost frequent combination of start station and end station trip is {}.'.format(df_Combi_St))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df_Total_Time = df['Trip Duration'].sum()
    print('Total travel time:')
    # call convert_time function in order to print data in day, hour, minut, second format.
    convert_time(df_Total_Time)
    
    # display mean travel time
    df_Avg_Time = df['Trip Duration'].mean()
    print('Average travel time:')
    # call convert_time function in order to print data in day, hour, minut, second format.
    convert_time(df_Avg_Time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    df_User_Type = df['User Type'].value_counts()
        
    print('Number of users per type:\n{}'.format(df_User_Type.to_string()))

    try: 
        # Display counts of gender
        df_Gender = df['Gender'].value_counts()
        print('\nNumber of users per gender:\n{}'.format(df_Gender.to_string()))

        # Display earliest, most recent, and most common year of birth
        df_Min_BirthYear = int(df['Birth Year'].min())
        print('\nMin year of birth: {}'.format(df_Min_BirthYear))

        df_Max_BirthYear = int(df['Birth Year'].max())
        print('Max year of birth: {}'.format(df_Max_BirthYear))

        df_Mode_BirthYear = int(df['Birth Year'].mode()[0])
        print('Most common year of birth: {}'.format(df_Mode_BirthYear))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
    #If Washington is selected jumps to except.
    except: 

        print('\nThis city has no information recorded about Gender or Birth Year user details.')


""" Print 5 rows of the data at a time while user's answer is 'yes'.
    If user's answer is 'not' stop printing data"""
    
def display_data(df):
    lines = 5
    while True:
        show = input('\nDo you want to see the raw data? (yes/no)\n')
        if show.lower() == 'no':
            break
        # shows 5 rows of data.
        elif show.lower() == 'yes': 
            print(df.head(lines))
            lines +=5
        else: # Controls invalid answer, asks the user again.
            print('\nSorry, invalid answer. Type yes or no.')
            continue 
            


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
