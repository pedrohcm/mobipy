import pandas as pd
import numpy as np

def get_sample_df():
    date_rng = pd.date_range(start='2009-01-01', end='2009-02-28', freq='Min')
    df = pd.DataFrame(date_rng, columns=['date'])
    df['data'] = np.random.randint(0,100,size=(len(date_rng)))
    return df