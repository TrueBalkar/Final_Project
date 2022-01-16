from auction import app
from auction.page_render import home_render, auction_render, my_bids_render, my_office_render, register_render, \
    login_render, logout_render


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    return home_render()


@app.route('/auction', methods=['GET', 'POST'])
def auction_page():
    return auction_render()


@app.route('/my_bids', methods=['GET', 'POST'])
def my_bids_page():
    return my_bids_render()


@app.route('/my_office', methods=['GET', 'POST'])
def my_office_page():
    return my_office_render()


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return register_render()


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return login_render()


@app.route('/logout')
def logout_page():
    return logout_render()
