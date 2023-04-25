import requests
from datetime import datetime
from datetime import date
import pygal


def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()



def askTimeSeries(stockSymbol,tseries):
    stock = stockSymbol
    data = []

    try:
        timeSeries = tseries
            
        if timeSeries == 1:
            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + stock + '&interval=60min&apikey=' + 'VVYFBPRGDKHX0K93'
            r = requests.get(url)
            data = r.json()
            return data
        elif timeSeries == 2:
                url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock + '&apikey=' + 'VVYFBPRGDKHX0K93'
                r = requests.get(url)
                data = r.json()
                return data
        elif timeSeries == 3:
                url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + stock + '&apikey=' + 'VVYFBPRGDKHX0K93'
                r = requests.get(url)
                data = r.json()
                return data
        elif timeSeries == 4:
                url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + stock + '&apikey=' + 'VVYFBPRGDKHX0K93'
                data = r.json()
                return data
            
    except ValueError: 
        print(ValueError)
    return data, timeSeries

def generateGraph(stockSymbol, chartType, timeSeries, data, startDate, endDate):
    format2 = "%Y-%m-%d %H:%M:%S"
    format = "%Y-%m-%d"
    high = []
    low =[]
    close =[]
    open = []
    dateList = []
    stock = stockSymbol
    chart = chartType
    timeS = timeSeries
    sd = startDate
    ed = endDate
    datetime.strptime(sd, format)
    datetime.strptime(ed, format)
    dataList = data
    
    if timeS == 1:
        for date in dataList['Time Series (60min)']:
            datetime.strptime(date, format2)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Time Series (60min)'][date]['1. open'])
            high.append(dataList['Time Series (60min)'][date]['2. high'])
            low.append(dataList['Time Series (60min)'][date]['3. low'])
            close.append(dataList['Time Series (60min)'][date]['4. close'])

    if timeS == 2:
        for date in dataList['Daily Time Series']:
            datetime.strptime(date, format)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Daily Time Series'][date]['1. open'])
            high.append(dataList['Daily Time Series'][date]['2. high'])
            low.append(dataList['Daily Time Series'][date]['3. low'])
            close.append(dataList['Daily Time Series'][date]['4. close'])

    if timeS == 3:
        for date in dataList['Weekly Time Series']:
            datetime.strptime(date, format)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Weekly Time Series'][date]['1. open'])
            high.append(dataList['Weekly Time Series'][date]['2. high'])
            low.append(dataList['Weekly Time Series'][date]['3. low'])
            close.append(dataList['Weekly Time Series'][date]['4. close'])
            
    if timeS == 4:
        for date in dataList['Monthly Time Series']:
            datetime.strptime(date, format)
            if date > ed:
                continue 
            if date <= sd:
                break
            dateList.append(date)
            open.append(dataList['Monthly Time Series'][date]['1. open'])
            high.append(dataList['Monthly Time Series'][date]['2. high'])
            low.append(dataList['Monthly Time Series'][date]['3. low'])
            close.append(dataList['Monthly Time Series'][date]['4. close'])

    openFloat = [float(item) for item in open]
    highFloat = [float(item) for item in high]
    lowFloat = [float(item) for item in low]
    closeFloat = [float(item) for item in close]

    if chart == 1:
        chart = pygal.Bar(x_label_rotation=90)
        chart.title = stock
        chart.x_labels = map(str, dateList)
        chart.add('Open', openFloat)
        chart.add('High', highFloat)
        chart.add('Low', lowFloat)
        chart.add('Close', closeFloat)
        return chart.render_data_uri
    

    if chart == 2:
        chart = pygal.Line(x_label_rotation=90)
        chart.title = stock
        chart.x_labels = map(str, dateList)
        chart.add('Open', openFloat)
        chart.add('High', highFloat)
        chart.add('Low', lowFloat)
        chart.add('Close', closeFloat)
        chart.render_data_uri()
        return chart.render_data_uri()
    
        
def main(symbol,chart_t,tseries, startdate,enddate):

    try:
       stockSymbol = symbol
       chartType = chart_t
       data, timeSeries = askTimeSeries(stockSymbol,tseries)
       startDate, endDate = startdate, enddate
       chart = generateGraph(stockSymbol, chartType, timeSeries, data, startDate, endDate)
       return chart

    except ValueError:
        print("ERROR: Invalid Option!")

    