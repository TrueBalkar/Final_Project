from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, \
                    TextAreaField, TimeField, DateField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired


class RegisterForm(FlaskForm):
    """
    Registration form. Used to register new users.
    """
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    """
    Login form. Used to log users in.
    """
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class BidOnItemForm(FlaskForm):
    """
    Form for making bids on the item.
    """
    bid = FloatField(label='Your bid:', validators=[DataRequired()])
    submit = SubmitField(label='Submit!')


class AdminRightsDeleteUserForm(FlaskForm):
    """
    Form of admin rights. Used to delete users.
    """
    delete_user = StringField(label='Username:', validators=[DataRequired()])
    submit_delete_user = SubmitField(label='Submit!')


class AdminRightsDeleteItemForm(FlaskForm):
    """
    Form of admin rights. Used to delete items.
    """
    delete_item = IntegerField(label='Item id:', validators=[DataRequired()])
    submit_delete_item = SubmitField(label='Submit!')


class AdminRightsUpdateUserBalanceForm(FlaskForm):
    """
    Form of admin rights. Used to update user balance.
    """
    update_user_balance = StringField(label='Username:', validators=[DataRequired()])
    update_balance = FloatField(label='Money to transfer:', validators=[DataRequired()])
    submit_update_balance_plus = SubmitField(label='Transfer money!')
    submit_update_balance_minus = SubmitField(label='Deduct money!')


class SellItemForm(FlaskForm):
    """
    Form for putting items on auction.
    """
    price = FloatField(label='Starting Price:', validators=[DataRequired()])
    date_until_purchase = DateField(label='Date until end of bidding:', validators=[DataRequired()])
    time_until_purchase = TimeField(label='Time until end of bidding:', validators=[DataRequired()])
    submit = SubmitField(label='Post item on auction!')


class DeleteAccountForm(FlaskForm):
    """
    Form to delete current session user account.
    """
    delete = SubmitField(label='Delete Account!')


class UpdateBalanceForm(FlaskForm):
    """
    Form for transferring money to current session user account.
    """
    balance = FloatField(label='Update Balance:', validators=[DataRequired()])
    update = SubmitField(label='Submit')


class AddItemForm(FlaskForm):
    """
    Form for adding new items in database.
    """
    name = StringField(label='Name of the item:', validators=[DataRequired()])
    description = TextAreaField(label='Item Description:', validators=[DataRequired()])
    price = FloatField(label='Starting Price:', validators=[DataRequired()])
    date_until_purchase = DateField(label='Date until end of bidding:', validators=[DataRequired()])
    time_until_purchase = TimeField(label='Time until end of bidding:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class ChangeStoryForm(FlaskForm):
    """
    Form used to get user story and send it to server.
    """
    story = TextAreaField(label='About me:', validators=[DataRequired()])
    submit = SubmitField(label='Submit', validators=[DataRequired()])
