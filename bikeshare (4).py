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
    print('\nGreetings! I hear you are interested in exploring some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to explore: Chicago, New York City, or Washington? I want to explore: ').lower()
        if city not in CITY_DATA:
            print('\n\n***Oopps! There is an error with your response... Please enter the city with the exact spelling. Lets try again!***')
        if city in CITY_DATA:
            break
            
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('\n\nTime to filter by Month. Input a Month: January, Febuary, March, April, May, June OR input "all" to explore all available Months.I want to filter by: ').lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month not in months and month != "all":
                print('\n\n***Oopps! There is an error with your response...Please re-enter the month with the exact spelling. Lets try again!***')
        elif month in months or month == "all":
            break
                
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day =  input('\n\nTime to filter by Day. Input a Day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday OR input "all" to explore all Days. I want to filter by: ').lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day not in days and day != "all":
            print('\n\n***Oopps! There is an error with your response...Please re-enter the day with the exact spelling. Lets try again!***')
        elif day in days or day == "all":
            break

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
    #load
    df = pd.read_csv(CITY_DATA[city])
    
    #convert column to dt (date time)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #get month and day from starttime
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #filter by month condition if needed
    if month!='all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        #filter by month to create new df
        df = df[df['month']== month]
    
    #filter by day condition if needed
    if day!= 'all':
        #filter by day to create new df
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month: ', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day: ', popular_day)

    # TO DO: display the most common start hour
    #extract hour
    df['hour'] = df['Start Time'].dt.hour
    #find and print most common hour via mode
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour: ', popular_hour, '00 (24 hour time)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start_station = df['Start Station'].mode()
    print('The most commonly used start station: ', pop_start_station)
    
    # TO DO: display most commonly used end station
    pop_end_station = df['End Station'].mode()
    print('The most commonly used end station: ', pop_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    pop_start_end_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most frequent combination of start station and end station for a trip: ', pop_start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    #Sum up the total time for the filtered data frame and convert to days
    total_travel_time_days = df['Trip Duration'].sum() / 86400
    
    #make travel time more "readable" for program users through a function to format the amount of time
    def total_travel_time_formatting(total_travel_time_days):
        #formulas for each display of time
        weeks = total_travel_time_days // 7
        remaining_days = total_travel_time_days % 7
        hours = remaining_days * 24
        return "{} week(s) {} day(s) {} hour(s)".format(int(weeks), int(remaining_days), round(hours, 2))
    
    #this calls the results of the total travel time formatting function so it can be used in the below print function
    total_travel_time = total_travel_time_formatting(total_travel_time_days)
    
    print('The total travel time for your selected filters is ', total_travel_time)
    
    # TO DO: display mean travel time + in multiple time formats
    mean_travel_time_min = df['Trip Duration'].mean() /60
    
    # Find the longest and shortest travel times
    max_travel_time_min = df['Trip Duration'].max() /60
    min_travel_time_min = df['Trip Duration'].min() /60
    
    #Display mean, min and max travel times
    print('\nThe mean travel time is {} minute(s). \n\nThere was a user riding for only {} minute(s) and a user was out there riding for {} minute(s)!'.format(round(mean_travel_time_min, 2), round(min_travel_time_min, 2), round(max_travel_time_min, 2)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #To provide more context for the program user, display the total users for the given dataframe
    total_users = df['User Type'].count()
    print('There were {} total users based on your filters.\n\nLets break this down a bit more below!'.format(total_users))
    
    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type']).size()
    print('\nHere are the counts of user types:\n', user_types) 

    # TO DO: Display counts of gender. Washington has no gender data therefore created if statement to check if the data frame has a gender column and if not, pass on the analysis amd report no data through a message.
    if 'Gender' in df.columns:
        gender = df.groupby(['Gender']).size()
        print('\nHere are the counts of gender: ***cavet: not all users specified a gender***\n', gender)
    else:
        print('\nNo gender data available')

    # TO DO: Display earliest, most recent, and most common year of birth. Washington has no birth year data therefore created an if statement to check if the data frame has a birth year column and if not, pass on the analysis and report no data through a message.
    if 'Birth Year' in df.columns:
        earliest_by = df['Birth Year'].min()
        most_recent_by = df['Birth Year'].max()
        most_common_by = df['Birth Year'].mode()[0]
        print('\n\nThe oldest user was born in {}, the youngest user was born in {}, and the most common birth year is {}'.format(int(earliest_by), int(most_recent_by), int(most_common_by)))
    else:
        print('\nNo birth year data available')
    
    #extra analysis on the age gap between users when there is an age gap >= 50 years. Washington has no birth year data therefore created an if statement to check if the data frame has a birth year column. No "no data" nessage requeied as the age gap message is not applicable for <50year age gaps. Therefore, it just passes on to the next line of code.
    if 'Birth Year' in df.columns:
        age_gap = (df['Birth Year'].max()) - (df['Birth Year'].min())
        #see if there is a large age gap >=50
        if age_gap >=50:
            print('\nWoah there is a {} year age gap in users!'.format(int(age_gap)))
        else:
             pass
    else:
        pass       

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

        #raw data prompt
        raw_data = input('\nWould you like to see the first 5 lines of raw data? Enter Yes or No. \n').lower()
        index = 0
        while True:
            #check for valid reponses
            if raw_data != 'yes' and raw_data != 'no':
                raw_data = input('There is an error with your response, please specify Yes or No ')
            #for "yes" responses
            if raw_data == 'yes':
                print(df.head(index + 5))
                index += 5
                #ask if user wants more raw data prompt
                raw_data = input('\nWould you like to see the next  5 lines of raw data? Enter Yes or No.\n').lower()
            #for "no" responses to break raw data prompt
            elif raw_data == 'no':
                break
                
        #simple y/n prompt to ask user if they would like to hear a joke
        joke = input('\nWould you like to hear a bike joke? Enter Yes or No.\n').lower()
        if joke == 'yes':
            print('\nYAY!\n\nWhy can\'t a bicycle stand up on it\'s own?\n\n...because it\'s two-tired!')
        else:
            pass
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
