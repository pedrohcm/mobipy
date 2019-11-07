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
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    if(selector.start_date != "" and selector.end_date != ""):
        mask = (df['date'] > selector.start_date) & (df['date'] < selector.end_date)
        df = df.loc[mask]
    if(selector.week_days != ""):
        weekDays = [day for day in range(0, len(selector.week_days)) if selector.week_days[day] == "1"]
        df['weekday'] = df['date'].apply(lambda x: x.weekday())
        df = df[df['weekday'].isin(weekDays)]
    if(selector.day_hours != ""):
        dayHours = [hour for hour in range(0, len(selector.day_hours)) if selector.day_hours[hour] == "1"]
        df['dayHour'] = df['date'].apply(lambda x: x.hour)
        df = df[df['dayHour'].isin(dayHours)]  
    return df