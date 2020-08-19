import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
def clean_dataset():

    Hourly = pd.read_csv('Hourly.csv', sep=';')
    Hourly['date-time'] = pd.to_datetime(Hourly['date-time'], format='%Y.%m.%d %H:%M:%S')
    Hourly.set_index("date-time", inplace=True)


    Monthly = pd.read_csv('Monthly.csv', sep=';')
    Monthly['date-time'] = pd.to_datetime(Monthly['date-time'], format='%Y.%m.%d %H:%M:%S')
    Monthly.set_index("date-time", inplace=True)


    Weekly = pd.read_csv('Weekly.csv', sep=';')
    Weekly['date-time'] = pd.to_datetime(Weekly['date-time'], format='%Y.%m.%d %H:%M:%S')
    Weekly.set_index("date-time", inplace=True)


    Business_Day = pd.read_csv('Business_Day.csv', sep=';')
    Business_Day['date-time'] = pd.to_datetime(Business_Day['date-time'], format='%Y.%m.%d %H:%M:%S')
    Business_Day.set_index("date-time", inplace=True)


    return  Hourly,Monthly,Weekly,Business_Day

def resample_data():
    path = '1002_processed_single_datetime.csv'

    data = pd.read_csv(path)
    data['date-time'] = pd.to_datetime(data['date_time'], format='%Y.%m.%d %H:%M:%S')
    data.set_index("date-time", inplace=True)
    data.drop("date_time", axis=1, inplace=True)

    # hourly resample

    hourly = data.resample('H')

    min = hourly.min()
    indexs = min.index

    max = hourly.max()

    median = hourly.median()
    mean = hourly.mean()
    std = hourly.std()
    sum = hourly.sum()

    hourly_final = pd.DataFrame({'min': min['messwert_kwh'],
                                 'max': max['messwert_kwh'],
                                 'median': median['messwert_kwh'],
                                 'mean': mean['messwert_kwh'],
                                 'std': std['messwert_kwh'],
                                 'sum': sum['messwert_kwh']},
                                index=indexs)

    hourly_final.to_csv('Hourly.csv', sep=';')

    weekly = data.resample('W')

    min = weekly.min()
    indexs = min.index

    max = weekly.max()

    median = weekly.median()
    mean = weekly.mean()
    std = weekly.std()
    sum = weekly.sum()

    weekly_final = pd.DataFrame({'min': min['messwert_kwh'],
                                 'max': max['messwert_kwh'],
                                 'median': median['messwert_kwh'],
                                 'mean': mean['messwert_kwh'],
                                 'std': std['messwert_kwh'],
                                 'sum': sum['messwert_kwh']},
                                index=indexs)
    weekly_final.to_csv('Weekly.csv', sep=';')

    Monthy = data.resample('M')

    min = Monthy.min()
    indexs = min.index

    max = Monthy.max()

    median = Monthy.median()
    mean = Monthy.mean()
    std = Monthy.std()
    sum = Monthy.sum()

    Monthly_final = pd.DataFrame({'min': min['messwert_kwh'],
                                  'max': max['messwert_kwh'],
                                  'median': median['messwert_kwh'],
                                  'mean': mean['messwert_kwh'],
                                  'std': std['messwert_kwh'],
                                  'sum': sum['messwert_kwh']},
                                 index=indexs)
    Monthly_final.to_csv('Monthly.csv', sep=';')

    Business_day = data.resample('B')

    min = Business_day.min()
    indexs = min.index

    max = Business_day.max()

    median = Business_day.median()
    mean = Business_day.mean()
    std = Business_day.std()
    sum = Business_day.sum()

    BD_final = pd.DataFrame({'min': min['messwert_kwh'],
                             'max': max['messwert_kwh'],
                             'median': median['messwert_kwh'],
                             'mean': mean['messwert_kwh'],
                             'std': std['messwert_kwh'],
                             'sum': sum['messwert_kwh']},
                            index=indexs)
    BD_final.to_csv('Business_Day.csv', sep=';')

def what(years,resampler,Hourly,Weekly,Monthly,Business_Day):


    if years == "all":
        if resampler == "hourly":
            datas = Hourly.copy()

            return datas
        elif resampler == "weekly":
            datas = Weekly.copy()

            return datas
        elif resampler == "monthly":
            datas = Monthly.copy()

            return datas
        elif resampler == "Business_Day":
            datas = Business_Day.copy()
            return datas

    elif years == "2016":

        if resampler == "hourly":
            datas = Hourly.copy()
            datas = datas[datas.index.year == 2016]
            return datas
        elif resampler == "weekly":
            datas = Weekly.copy()
            datas = datas[datas.index.year == 2016]
            return datas

        elif resampler == "monthly":
            datas = Monthly.copy()
            datas = datas[datas.index.year == 2016]
            return datas
        elif resampler == "Business_Day":

            datas = Business_Day.copy()
            datas = datas[datas.index.year == 2016]
            return datas

    elif years == "2017":

        if resampler == "hourly":
            datas = Hourly.copy()
            datas = datas[datas.index.year == 2017]
            return datas
        elif resampler == "weekly":
            datas = Weekly.copy()
            datas = datas[datas.index.year == 2017]
            return datas

        elif resampler == "monthly":
            datas = Monthly.copy()
            datas = datas[datas.index.year == 2017]
            return datas
        elif resampler == "Business_Day":

            datas = Business_Day.copy()
            datas = datas[datas.index.year == 2017]
            return datas

    elif years == "2018":

        if resampler == "hourly":
            datas = Hourly.copy()
            datas = datas[datas.index.year == 2018]
            return datas
        elif resampler == "weekly":
            datas = Weekly.copy()
            datas = datas[datas.index.year == 2018]
            return datas

        elif resampler == "monthly":
            datas = Monthly.copy()
            datas = datas[datas.index.year == 2018]
            return datas
        elif resampler == "Business_Day":

            datas = Business_Day.copy()
            datas = datas[datas.index.year == 2018]
            return datas

def give_decomposer(decomp,datas,stat_dec):

    if decomp == "additve":

        result = seasonal_decompose(datas[stat_dec],
                                    model='additive',
                                    extrapolate_trend='freq')
        return result

    elif decomp == "multiplicative":
        result = seasonal_decompose(datas[stat_dec],
                                    model='multiplicative',
                                    extrapolate_trend='freq')
        return result




