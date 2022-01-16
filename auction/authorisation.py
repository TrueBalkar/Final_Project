from auction.imports import flash, redirect, url_for, session, ConnectToDatabase, select_from_user_id, \
    delete_account_data
from auction import bcrypt


def check_logged_in() -> None:
    """
    Checks whether user is logged in.
    """
    try:
        select_from_user_id(session['username'])
    except:
        session['loggedin'] = False


def login_required():
    """
    If user is not logged in. This function will not let him to get access to any pages that require him
    to be logged in.

    :return: redirect user to login page.
    """
    if session['loggedin'] == False:
        logout()
    flash("You need to log in in order to get access to this page!", category="info")
    return redirect(url_for("login_page"))


def logout() -> None:
    """
    Log out user!

    :return: Nothing.
    """
    session['loggedin'] = False
    flash("You have been logged out!", category='info')


def login(form):
    """
    Login function. Login user and redirect them to home page.

    :param form: Inherited class from forms.py used to make beautiful and usable fields for getting data from user.
    :return: Login user and redirect him to home page.
    """
    if form.validate_on_submit():
        """
        Check if submit button was pressed.
        """
        if check_registration_of_user(ConnectToDatabase.cursor, form.username.data, form.password.data):
            """
            Check whether user was registered or not. If such user exist and password is correct, 
            login him and redirect to home page.
            """
            session['loggedin'] = True
            session['id'] = select_from_user_id(form.username.data)
            session['username'] = form.username.data
            flash(f'You logged in successfully! Welcome {form.username.data}.', category='success')
            return redirect(url_for('auction_page'))
        else:
            flash('Username and password do not match! Please try again!', category='danger')


def check_registration_of_user(cursor, login: str, password: str) -> bool:
    """
    Checks user login and password.

    :param cursor: Database cursor.
    :param login: User login.
    :param password: User password.
    :return: True if user and password correct. False otherwise.
    """
    try:
        cursor.execute(f'SELECT user_password FROM users WHERE login="{login}"')
        buffer = cursor.fetchall()[0][0]
        if bcrypt.check_password_hash(buffer, password):
            return True
    except:
        return False


def register(form) -> bool:
    """
    Function used to register new user.

    :param form: Inherited class from forms.py used to make beautiful and usable fields for getting data from user.
    :return: Return True if all data is correct.
    """
    if form.validate_on_submit():
        """
        Check if submit button was pressed
        """
        buffer = register_users(ConnectToDatabase.cursor,
                                ConnectToDatabase.db_connection,
                                str(form.username.data),
                                str(form.password1.data),
                                str(form.email_address.data))
        """
        Check whether user with same data exist and return '' if there are no user with same username or email.
        If there is some data that is not unique to new user, it will be returned.
        """
        if buffer == '':
            flash(f'Your account was successfully registered! '
                  f'You are now logged in as "{form.username.data}".', category='success')
            session['loggedin'] = True
            session['id'] = select_from_user_id(form.username.data)
            session['username'] = form.username.data
            return True
        elif buffer == str(form.username.data):
            """
            Check if returned non unique data is username or email. Then corresponding message will be flashed.
            """
            flash(f'User with User Name: "{form.username.data}" already exist.', category='danger')
        else:
            flash(f'User with Email Address: "{form.email_address.data}" already exist.', category='danger')
    if form.errors != {}:
        """
        If there was some errors from form validation, it will be displayed in a nice message.
        """
        for err_msg in form.errors.values():
            flash(f'There was an error while creating a user: {err_msg}.', category='danger')


def register_users(cursor, conn, login: str, password: str, email: str) -> str:
    """
    Function that insert user data in database.

    :param cursor: Database cursor.
    :param conn: Database connection.
    :param login: User login.
    :param password: User password.
    :param email: User email
    :return: User login or email if it was already taken by someone else. Otherwise return '' ( empty string ).
    """
    buffer = register_user_check(cursor, login, email)
    """
    Check whether user with same data exist and return '' if there are no user with same username or email.
    If there is some data that is not unique to new user, it will be returned.
    """
    if buffer == '':
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        """
        Generating crypted password for maximum security!
        """
        cursor.execute("SELECT MAX(id) FROM users")
        user_id = cursor.fetchall()[0][0]
        if user_id is None:
            """
            Check whether it is a first user to be registered.
            """
            user_id = 0
        user_id += 1
        if login == "admin":
            privilegies = "admin"
        else:
            privilegies = "member"
        cursor.execute(f"INSERT INTO users (id, login, user_password, "
                       f"email, budget, bidden_items, bidden_price, story, privilegies) "
                       f"VALUES ({user_id}, '{login}', '{password}', '{email}', 0, '', '', '', '{privilegies}')")
        conn.commit()
        """
        Insert and commit changes in database.
        """
        return buffer
    return buffer


def register_user_check(cursor, login: str, email: str) -> str:
    """
    Check if input user data was taken by somebody else already.

    :param cursor: Database cursor.
    :param login: User login.
    :param email: User email.
    :return: User login or email if it was already taken by someone else. Otherwise return '' ( empty string ).
    """
    cursor.execute(f'SELECT login FROM users WHERE login = "{login}"')
    """
    Looking up for the same username in database.
    """
    try:
        """
        Check whether there is data from previous search. If there is None, it will return error which will be
        caught and redirected to the next search for identical email. Otherwise login shall be returned.
        """
        buffer = cursor.fetchall()[0][0]
        return buffer
    except:
        cursor.execute(f'SELECT email FROM users WHERE email = "{email}"')
        try:
            """
            Check whether there is data from email search. If there is None, it will return error which will be
            caught and '' will be returned, which means that login and email are unique and may be used for 
            registration. Otherwise email shall be returned to show da wae.
            """
            buffer = cursor.fetchall()[0][0]
            return buffer
        except:
            return ''


def delete_account(login: str):
    """
    Delete user info from database and log him out.

    :param login: User login.
    :return: Log out and redirect to home page user whose account was deleted.
    """
    if delete_account_data(login):
        """
        Check if account with such username exist. If it doesn't display corresponding message and refresh the page.
        """
        if login == session['username']:
            """
            If it is the account of user who called this func he will be logged out, stripped of account and
            throwen to home page.
            """
            logout()
            flash(f'Your account was deleted!', category="danger")
            return redirect(url_for("home_page"))
        else:
            """
            Otherwise it will happen to other user.
            """
            flash(f'{login} account was successfully deleted!', category="success")
            return redirect(url_for('my_office_page'))
    flash(f'It seems {login} account doesn`t exist!', category="danger")
    return redirect(url_for('my_office_page'))
