import time
import pandas as pd
import numpy as np
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

## Filenames
#chicago = 'chicago.csv'
#new_york_city = 'new_york_city.csv'
#washington = 'washington.csv'

def get_rawdata_asper_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    while True:
        get_city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
        if get_city.lower() in ('chicago', 'new york', 'washington'):
            if get_city.lower() == 'chicago':
                city_filename = chicago
            elif get_city.lower() == 'new york':
                city_filename = new_york_city
            elif get_city.lower() == 'washington':
                city_filename = washington
            break
        print('Enter a valid city name provided in the options')
    raw_city_data = pd.read_csv(city_filename)
    raw_city_data['Start Time'] = pd.to_datetime(raw_city_data['Start Time'])
    raw_city_data['End Time'] = pd.to_datetime(raw_city_data['End Time'])  
    raw_city_data.columns = [x.strip().replace(' ', '_') for x in raw_city_data.columns]
    city_file = get_city.lower()
    return raw_city_data, city_file


def filter_data_asper_time_period(raw_city_data):
    while True: 
        time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
        if time_period in ('month', 'day', 'none'):
            break
        print('Enter a valid input provided in the options')
    if time_period =='month':
        month_tuple = ('january', 'february', 'march', 'april', 'may', 'june')
        while True:
            get_month = input('\nWhich month? January, February, March, April, May, or June?\n')
            if get_month.lower() in month_tuple:
                month_ind = month_tuple.index(get_month.lower()) + 1
                filtered_city_data = raw_city_data[raw_city_data['Start_Time'].dt.month==month_ind]
                time_period = get_month.lower()
                break
            print('Enter a valid month name provided in the options')

    elif time_period =='day':
        list_weekdays = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
        while True:
            get_day = int(input('\nWhich day? Please type your response as an integer. E.g. Monday:0, Tuesday:1...\n'))
            if get_day in np.arange(0,6,1,'int'):
                filtered_city_data = raw_city_data[raw_city_data['Start_Time'].dt.dayofweek==get_day]
                time_period=list_weekdays[get_day]
                break
            print('Enter a valid day for the month:')

    else:
        filtered_city_data = raw_city_data

    return filtered_city_data, time_period

def popular_month(city_file,time_period,filtered_city_data):
    month_tuple = ('January', 'February', 'March', 'April', 'May', 'June')
    grouped_data = filtered_city_data['Start_Time'].groupby([filtered_city_data.Start_Time.dt.month]).agg('count')
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular month for start time is {} with {} total transactions.".format(month_tuple[grouped_data.argmax()-1], grouped_data[grouped_data.argmax()]))
    print("It's total number of transactions is {} times greater than the total transactions for the least popular month {}.".format(format(grouped_data[grouped_data.argmax()]/grouped_data[grouped_data.argmin()],'.2f'),month_tuple[grouped_data.argmin()-1]))

def popular_day(city_file,time_period,filtered_city_data):
    list_weekdays = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
    tmp_data1 = filtered_city_data.loc[:,['Start_Time','End_Time']]
    tmp_data1['weekday'] = tmp_data1['Start_Time'].dt.dayofweek
    tmp_data2 = tmp_data1.groupby(['weekday']).size().reset_index(name='counts')
    final_poplr_day_stat = tmp_data2.loc[tmp_data2['counts'].idxmax()]
    lst_poplr_day_stat = tmp_data2.loc[tmp_data2['counts'].idxmin()]
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular day of the week is {} with total transactions of {}.".format(list_weekdays[final_poplr_day_stat['weekday']], final_poplr_day_stat['counts']))
    print("{} has {} times more transaction than {} which is the least popular day.".format(list_weekdays[final_poplr_day_stat['weekday']], format(final_poplr_day_stat['counts']/lst_poplr_day_stat['counts'],'.2f'), list_weekdays[lst_poplr_day_stat['weekday']]))

def popular_hour(city_file, time_period,filtered_city_data):
grouped_data = filtered_city_data['Start_Time'].groupby([filtered_city_data.Start_Time.dt.hour]).agg('count')
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular hour of the day for start time is {}:00 with {} total transactions.".format(grouped_data.argmax(), grouped_data[grouped_data.argmax()]))
    print("It's total transactions are {} times greater than the total transactions of {}:00 which is the least popular hour.".format(format(grouped_data[grouped_data.argmax()]/grouped_data[grouped_data.argmin()],'.2f'),grouped_data.argmin()))

def trip_duration(city_file, time_period,filtered_city_data):
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The total trip duration and average trip duration are {} seconds and {} seconds".format(format(filtered_city_data['Trip_Duration'].max(),'.2f'), format(filtered_city_data['Trip_Duration'].mean(),'.2f')))

def popular_stations(city_file, time_period,filtered_city_data):
    grp_pplr_start_stn = filtered_city_data.groupby(['Start_Station']).size().reset_index(name='counts')
    pplr_start_stn=grp_pplr_start_stn.loc[grp_pplr_start_stn['counts'].idxmax()]
    lst_pplr_start_stn=grp_pplr_start_stn.loc[grp_pplr_start_stn['counts'].idxmin()]
    grp_pplr_end_stn = filtered_city_data.groupby(['End_Station']).size().reset_index(name='counts')
    pplr_end_stn=grp_pplr_end_stn.loc[grp_pplr_end_stn['counts'].idxmax()]
    lst_pplr_end_stn=grp_pplr_end_stn.loc[grp_pplr_end_stn['counts'].idxmin()]
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular start station is '{}' with {} total transactions.".format(pplr_start_stn['Start_Station'], pplr_start_stn['counts']))
    print("'{}' has {} times more transactions than the '{}' which is least popular start station.".format(pplr_start_stn['Start_Station'], format(pplr_start_stn['counts']/lst_pplr_start_stn['counts'],'.2f'), lst_pplr_start_stn['Start_Station']))
    print("The most popular end station is '{}' with {} total transactions.".format(pplr_end_stn['End_Station'], pplr_end_stn['counts']))
    print("'{}' has {} times more transactions than the '{}' which is least popular end station.".format(pplr_end_stn['End_Station'], format(pplr_end_stn['counts']/lst_pplr_end_stn['counts'],'.2f'), lst_pplr_end_stn['End_Station']))

def popular_trip(city_file, time_period,filtered_city_data):
    grp_pplr_trip = filtered_city_data.groupby(['Start_Station', 'End_Station']).size().reset_index(name='counts')
    pplr_trip=grp_pplr_trip.loc[grp_pplr_trip['counts'].idxmax()]
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular trip starts from station '{}' and ends at '{}' with {} total transactions.".format(pplr_trip['Start_Station'], pplr_trip['End_Station'], pplr_trip['counts']))

def users(city_file, time_period, filtered_city_data):
    grp_user_type = filtered_city_data.groupby(['User_Type']).size().reset_index(name='counts')
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The total counts of each user type are as follows:")
    print(grp_user_type)

def gender(city_file, time_period,filtered_city_data):
    if city_file.lower() == 'washington':
        print('Sorry! Data related to gender is not present for Washingtion.')
    else:
        grp_gender = filtered_city_data.groupby(['Gender']).size().reset_index(name='counts')
        print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
        print("The total counts of each gender type are as follows:")
        print(grp_gender)

def birth_years(city_file, time_period,filtered_city_data):
    if city_file.lower() == 'washington':
        print('Sorry! Data related to birth year is not present for Washingtion.')
    else:
        grp_birth_year = filtered_city_data.groupby(['Birth_Year']).size().reset_index(name='counts')
        print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
        print("The the earliest (i.e. oldest user) and the most recent (i.e. youngest user) birth years are {} and {}, respectively".format(int(grp_birth_year['Birth_Year'].min()), int(grp_birth_year['Birth_Year'].max())))
        print("The most popular birth year is {} with total {} counts.".format(int(grp_birth_year.loc[grp_birth_year['counts'].idxmax()]['Birth_Year']),int(grp_birth_year.loc[grp_birth_year['counts'].idxmax()]['counts'])))

def display_data(city_file,time_period, filtered_city_data):
    count=0;
    while True:
        display = input('\nWould you like to view individual trip data?'
                        'Type \'yes\' or \'no\'.\n')
        if display.lower() in ('yes', 'no'):
            if display.lower() == 'yes':
                print("This individual trip data is filtered by '{}' and belongs to {} city.".format(time_period, city_file))
                print(filtered_city_data[count:count+5])
                count +=5
            else:
                print('Display of the data ends!')
                break
        print('Enter a valid input provided in the options')

def statistics():
    raw_data, city_name = get_rawdata_asper_city()
    filtered_data, filter_method = filter_data_asper_time_period(raw_data)

    print('Calculating the first statistic...')
    if filter_method == 'none':
        start_time = time.time()
        popular_month(city_name,filter_method,filtered_data)
        print("That took %s seconds.\n" % (time.time() - start_time))
        print("Calculating the next statistic...")
    month_tuple = ('january', 'february', 'march', 'april', 'may', 'june')
    if filter_method == 'none' or filter_method in month_tuple:
        start_time = time.time()
        popular_day(city_name,filter_method,filtered_data)
        print("That took %s seconds.\n" % (time.time() - start_time))
        print("Calculating the next statistic...")

    start_time = time.time()
    popular_hour(city_name,filter_method,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    trip_duration(city_name,filter_method,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    popular_stations(city_name,filter_method,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    popular_trip(city_name,filter_method,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    users(city_name,filter_method,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    gender(city_name,filter_method,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    birth_years(city_name,filter_method,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    display_data(city_name,filter_method,filtered_data)
    while True:
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
        if restart.lower() in ('yes', 'no'):
            if restart.lower() == 'yes':
                statistics()
            else:
                print('Thanks for using this application. Hope you enjoyed the interactive session.')
            break
        print('Enter a valid input provided in the options')

if __name__ == "__main__":
    statistics()
