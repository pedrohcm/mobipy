import pandas as pd

def dataset_selector(f):
    def wrapper(*args, **kw):
        dataframe = kw['dataframe']
        identifier = kw['identifier']
        selector = kw['selector']
        kw['dataframe'] = select_df(dataframe, selector, identifier)
        return f(*args, **kw)
    return wrapper

def select_df(df, selector, identifier):
    df['date'] = pd.to_datetime(df['date'])
    mask = (df['date'] > selector.start_date) & (df['date'] < selector.end_date)
    df = df.loc[mask].copy()
    weekDays = [day for day in range(0, len(selector.week_days)) if selector.week_days[day] == "1"]
    dayHours = [hour for hour in range(0, len(selector.day_hours)) if selector.day_hours[hour] == "1"]
    df['weekday'] = df['date'].apply(lambda x: x.weekday())
    df['dayHour'] = df['date'].apply(lambda x: x.hour)
    weekdays_only = df[df['weekday'].isin(weekDays)]
    hours_only = weekdays_only[weekdays_only['dayHour'].isin(dayHours)] 
    #printDf(hours_only)   
    return hours_only