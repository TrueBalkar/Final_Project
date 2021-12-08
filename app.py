from flask import Flask, render_template
from db import ConnectToDatabase, SqlStatement, get_values_from_db
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/auction')
def auction_page():
    items = get_values()
    return render_template('auction.html', items=items)


def get_values():
    return get_values_from_db(ConnectToDatabase.cursor,
                              SqlStatement.select_from_id,
                              SqlStatement.select_from_name,
                              SqlStatement.select_from_barcode,
                              SqlStatement.select_from_price)
