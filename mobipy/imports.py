import pandas as pd
import numpy as np
import datetime as dt

def my_decorator(func):
    def my_wrapper(*args):
        filteredData = filterDf(*args)


@my_decorator
def get_all_values(df, startDate, endDate, weekdays, dayHours):
    "vou chamar o decorator"

def printDf(df):
    print(df)

def get_sample_df():
    date_rng = pd.date_range(start='2009-01-01', end='2009-02-28', freq='Min')
    df = pd.DataFrame(date_rng, columns=['date'])
    df['data'] = np.random.randint(0,100,size=(len(date_rng)))
    return df

def filterDf(df, startDate, endDate, weekDaysIndex, dayHoursIndex):
    df['date'] = pd.to_datetime(df['date'])
    mask = (df['date'] > startDate) & (df['date'] <= endDate)
    df = df.loc[mask]
    weekDays = [day for day in range(0, len(weekDaysIndex)) if weekDaysIndex[day] == "1"]
    dayHours = [hour for hour in range(0, len(dayHoursIndex)) if dayHoursIndex[hour] == "1"]
    df['weekday'] = df['date'].apply(lambda x: x.weekday())
    df['dayHour'] = df['date'].apply(lambda x: x.hour)
    weekdays_only = df[df['weekday'].isin(weekDays)]
    hours_only = weekdays_only[weekdays_only['dayHour'].isin(dayHours)]    
    return hours_only

startDate = "2009-01-25"
endDate = "2009-02-14"
weekdays = "0010101"
dayHours = "001010011111011100001111"

get_all_values(get_sample_df(), startDate, endDate, weekdays, dayHours)


