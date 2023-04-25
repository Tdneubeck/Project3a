import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from stock_data import main


# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'hello'



@app.route('/', methods=('GET', 'POST'))
def stock():
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
            chart= main(symbol,chart_type,time_series,start_date,end_date)
            
        return render_template('stock.html', chart = chart)

    return render_template('stock.html')

app.run(host="0.0.0.0")