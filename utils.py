import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime

# Function used to convert a string date into a timestamp
def to_datetime(x):
    return  datetime.strptime(x, '%Y-%m-%d').timestamp() # convert to timestamp


# Function organizing the data

def get_Data(): 

    info =  pd.read_csv("./data/info_charact.csv",index_col=0)
    file_names = info.index.values
    charact_names = info.iloc[:, 0]

    data_size = pd.read_csv("./data/1.csv",index_col=0)
    dates = data_size.index
    stocks = data_size.columns

    monthly_returns = pd.read_csv("data/44.csv", index_col=0)
    monthReturns = monthly_returns.T

    feat1 = data_size.T

    Glob_data = None

    for date in dates: 
        A = feat1[date]
        B = monthly_returns.loc[date]
        C = pd.concat([A, B], ignore_index=False, axis = 1)
        C["Date"] = date
        C.columns = [charact_names[1], "Returns", "Date"]
        if Glob_data is None:
            Glob_data = C
        else: 
            Glob_data = pd.concat([Glob_data, C], ignore_index=False)

    for k in file_names:
        if k != 44 and k != 1: 
            file_path = "data/" + str(k) + ".csv"
            data = pd.read_csv(file_path, index_col=0)
            data = data.T
            loc_data = None
            for date in dates: 
                A = data[date]
                A = pd.DataFrame(A)
                #A["Date"] = date
                A.columns = [charact_names[k]]
                if loc_data is None:
                    loc_data = A
                else: 
                    loc_data = pd.concat([loc_data, A], ignore_index=False)
            file_data = loc_data.loc[:, charact_names[k]]
            Glob_data[charact_names[k]] = file_data
    Glob_data["Date"] = Glob_data["Date"].apply(to_datetime)

    # Dealing with NaNs
    newGlob = None
    for stock in stocks:
        data_stock = Glob_data.loc[stock]
        # Looking backwards if there is an avalaible value
        data_stock = data_stock.fillna(method='ffill')
        ''' # If there is still an NaN value, delete the ligne: 
        data_stock = data_stock.dropna() '''
        # If no avalaibles values back fill the columns with 0
        if data_stock.isnull().sum().sum() !=  0: 
            #print(str(data_stock.isnull().sum().sum()) + "-" + str(stock))
            data_stock = data_stock.fillna(0)
        if newGlob is None: 
            newGlob = data_stock
        else: 
            newGlob = pd.concat([newGlob, data_stock], ignore_index=False)

    return newGlob