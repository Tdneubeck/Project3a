import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from stock_data import main
import pygal
import getstocks
from datetime import datetime
import requests



# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'hello'

def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def askTimeSeries(stockSymbol,tseries):
    stock = stockSymbol
    data = []

    try:
        time_series = tseries
            
        if time_series == '1':
           url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=5min&apikey=VVYFBPRGDKHX0K93&datatype=csv"
                
        elif time_series == '2':
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&apikey=VVYFBPRGDKHX0K93&datatype=csv"
                
        elif time_series == '3':
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={stock}&apikey=VVYFBPRGDKHX0K93&datatype=csv"
                
        elif time_series == '4':
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={stock}&apikey=VVYFBPRGDKHX0K93&datatype=csv"
        r = requests.get(url)
        data = r.json()
        return data
    except ValueError: 
        print(ValueError)
    return data

def generateGraph(stockSymbol, chartType, timeSeries, data, startDate, endDate):
    format2 = "%Y-%m-%d %H:%M:%S"
    format = "%Y-%m-%d"
    high = []
    low =[]
    close =[]
    open = []
    dateList = []
    stock = stockSymbol
    chartt = chartType
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

    if chartt == 1:
        bar = pygal.Bar(x_label_rotation=90)
        bar.title = stock
        bar.x_labels = map(str, dateList)
        bar.add('Open', openFloat)
        bar.add('High', highFloat)
        bar.add('Low', lowFloat)
        bar.add('Close', closeFloat)
        chart = bar.render_data_uri
        return chart
    

    if chartt == 2:
        line = pygal.Line(x_label_rotation=90)
        line.title = stock
        line.x_labels = map(str, dateList)
        line.add('Open', openFloat)
        line.add('High', highFloat)
        line.add('Low', lowFloat)
        line.add('Close', closeFloat)
        chart = line.render_data_uri()
        return chart

def Stockchoice():
      import csv
      with open('stocks.csv', newline='') as f:
         reader = csv.reader(f)
         data = list(reader)
         
      n = 1
      choicelist = [] 
      for x in data:
         for w in x:
           choicelist.append(w)
      
         
      return choicelist


@app.route('/', methods=('GET', 'POST'))
def stock():
    symbol_list = Stockchoice()
    if request.method == 'POST':
        #get title and content
        symbol = request.form['symbol']
        chart_type = request.form['chart_type']
        time_series = request.form['time_series']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        #display error if title of content not submitted
        #otherwise make database connection and insert the content
        if not symbol:
            flash('Symbol is required!')
        elif not chart_type:
            flash('Chart Type is required!')
        elif not time_series:
            flash('Time Series is required!')
        elif not start_date:
            flash('Start Date is required!')
        elif not end_date:
            flash('End Date is required!')
        elif end_date <= start_date:
            flash('Please insert end date after the start date')
        else:
            data =askTimeSeries (symbol,time_series)
            chart = generateGraph(symbol,chart_type,time_series,data,start_date,end_date)

            return render_template('stock.html', chart = chart, symbol_list = symbol_list)

    return render_template('stock.html', symbol_list = symbol_list)

app.run(host="0.0.0.0")