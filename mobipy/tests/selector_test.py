from classes.identifier import Identifier
from classes.selector import Selector
from helpers import dataset_filter, get_sample_df

@dataset_filter
def get_all_values(dataframe, identifier, selector):
    printDf(dataframe)

def printDf(df):
    print(df)


startDate = "2009-01-25"
endDate = "2009-02-14"
weekdays = "0010001"
dayHours = "001010011111011100001110"

identifier = Identifier("lat", "lon", "timestamp", "start_time", "end_time", "user_id")
selector = Selector(startDate, endDate, weekdays, dayHours)

get_all_values(dataframe=get_sample_df(), identifier=identifier, selector=selector)