import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from stock_data import main


# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'hello'

# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

## function to get a post
def get_post(post_id):
    #get a database connection
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)
    
    return post


# use the app.route() decorator to create a Flask view function called index()


#route to edit post

# route to delete a post


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