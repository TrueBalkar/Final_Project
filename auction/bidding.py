from auction.imports import get_money, select_by_id_price, update_price, update_money, select_by_id_name, \
    select_by_id, select_items, select_from_bidden_items, ConnectToDatabase, select_from_bidden_price, \
    update_bidden_items, update_bidden_price, update_last_bidder, delete_item_data
from flask import request, session, flash, redirect, url_for
import math
import datetime


def get_budget() -> str:
    """
    Function used to display beautiful numbers.

    :return: User current budget with beautiful comas after every thousand of thousands.
    """
    budget = "{:,}".format(get_money(session['username']))
    return budget


def bid_on_the_item(bid_price: float, link_to_return: str):
    """
    Function that do all bidding related tasks.

    :param bid_price: Amount of money user wish to add to the price of the item.
    :param link_to_return: Link to refresh page
    :return: Update data of bidden item, user, refresh page and display messages.
    """
    """
    Getting item data from <input ...></input> html tag.
    """
    bidden_item = request.form.get('bid_item')
    time_left = request.form.get('time_left')
    """
    If item exist... The fun part begin!
    """
    if bidden_item is not None:
        """
        If user at least have enough money to increase the price without the actual price of the product.
        The process will not stop, otherwise it will be stopped and corresponding message displayed.
        """
        if get_money(session['username']) >= bid_price and time_left != "Expired":
            """
            Check if user have ever bidden on this item. And how much he has bidden.
            """
            bidden_items = select_from_bidden_items(session['username'])
            bidden_price = select_from_bidden_price(session['username'])
            item = None
            iteration = 0
            for i in bidden_items:
                if i == bidden_item:
                    item = i
                    bidden_price[iteration] = float(bidden_price[iteration])
                    break
                iteration += 1
            """
            If he didn't then id of the item and new price will be inserted into the user database as well as
            new price in item database, if user has enough money to finish transaction.
            """
            if not item:
                if get_money(session['username']) >= bid_price + select_by_id_price(bidden_item):
                    update_price(bidden_item, select_by_id_price(bidden_item) + bid_price)
                    bidden_items.append(str(bidden_item))
                    bidden_price[iteration] = select_by_id_price(bidden_item)
                    bidden_price.append(str(select_by_id_price(bidden_item)))
                    update_bidden_items(session['username'], bidden_items)
                    update_bidden_price(session['username'], bidden_price)
                    update_money(session['username'], get_money(session['username'])
                                 - (select_by_id_price(bidden_item)))
                else:
                    flash(f"You don't have enough money for this bid!", category="danger")
                    """
                    Refreshing page!
                    """
                    return redirect(url_for(link_to_return))
            else:
                bid_price_2 = select_by_id_price(bidden_item) - bidden_price[iteration] + bid_price
                update_price(bidden_item, select_by_id_price(bidden_item) + bid_price)
                update_bidden_price(session['username'], bidden_price)
                update_money(session['username'], get_money(session['username']) - bid_price_2)
            """
            The last bidder will be updated to user login if transaction ended successfully,
            which will make him future owner of the item if no one else bid on it.
            """
            update_last_bidder(session['username'], bidden_item)
            flash(f"Congratulations! You bid on "
                  f"{select_by_id_name(bidden_item)} for "
                  f"{select_by_id_price(bidden_item)}$! "
                  f"If no one else bid on this item for {time_left} it will be yours! "
                  f"Good luck!", category="success")
        else:
            flash(f"You don't have enough money for this bid!", category="danger")
    """
    Refreshing page!
    """
    return redirect(url_for(link_to_return))


def update_balance(login: str, money: float, symbol: str):
    """
    Update budget of some user.

    :param login: Login of the user.
    :param money: Amount of money to transfer of deduct from account.
    :param symbol: "+" or "-". "+" is for transfering money to account and "-" to deduct them from account.
    :return: Update amount of user money and refresh page.
    """
    if symbol == "+":
        if money <= 0:
            money *= -1
        o_money = get_money(login) + money
        update_money(login, o_money)
        o_money = "{:,}".format(math.trunc(o_money * 100) / 100)
        money = "{:,}".format(math.trunc(money * 100) / 100)
        if session['username'] == login:
            flash(f"Congratulation! {money}$ was successfully transfered "
                  f"to your account! Now you have {o_money}$!", category="success")
        else:
            flash(f"Congratulation! {money}$ was successfully transfered "
                  f"to {login}`s account! Now he has {o_money}$!", category="success")
        return redirect(url_for("my_office_page"))
    if symbol == "-":
        if money <= 0:
            money *= -1
        o_money = get_money(login) - money
        if o_money < 0:
            o_money = 0
        update_money(login, o_money)
        o_money = "{:,}".format(math.trunc(o_money * 100) / 100)
        money = "{:,}".format(math.trunc(money * 100) / 100)
        if session['username'] == login:
            flash(f"Congratulation! {money}$ was successfully deducted "
                  f"from your account! Now you have {o_money}$!", category="success")
        else:
            flash(f"Congratulation! {money}$ was successfully deducted "
                  f"from {login}`s account! Now he has {o_money}$!", category="success")
        return redirect(url_for("my_office_page"))


def return_money_to_losers(last_bidder: str, item_id: int) -> None:
    """
    Return money to those who lost bid on the item.

    :param last_bidder: Name of the winner
    :param item_id: id of the won item.
    :return: Transfer money to those who lost.
    """
    ConnectToDatabase.cursor.execute("SELECT login FROM users")
    users = ConnectToDatabase.cursor.fetchall()[0]
    item_id = str(item_id)
    for i in users:
        if i != last_bidder:
            bidden_items = select_from_bidden_items(i)
            bidden_price = select_from_bidden_price(i)
            iteration = 0
            for n in bidden_items:
                if n == item_id:
                    update_balance(i, float(bidden_price[iteration]), "+")
                    bidden_price.remove(bidden_price[iteration])
                    bidden_items.remove(n)
                    update_bidden_items(i, bidden_items)
                    update_bidden_price(i, bidden_price)


def put_on_auction(price: float, date: str, time: str):
    """
    Function for putting owned item on auction.

    :param price: Starting price of the item.
    :param date: Date till end of auction for this item.
    :param time: Time till end of auction for this item.
    :return: Refresh page and post item.
    """
    item_id = request.form.get('sell_item')
    ConnectToDatabase.cursor.execute(f'UPDATE auction SET price = {price}, bid_time = "{date} {time}" '
                                     f'WHERE id = {item_id}')
    ConnectToDatabase.db_connection.commit()
    flash("Your item was successfully posted on the auction!", category="success")
    return redirect(url_for("my_bids_page"))


def get_values_for_auction(*item_id: list) -> list:
    """
    This func get item values from database to display them in a nice way.

    :param item_id: id's of items if all items not needed
    :return: Dictionary of parameters of items
    """
    items = []
    columns = []
    item = {}
    item.update({"id": None, "item": None, "owners": None, "descript": None, "price": None,
                 "time_left": None, "last_bidder": None})
    data = []
    for i in item.keys():
        """
        Filling columns of future list of dictionaries.
        """
        columns.append(i)
    if item_id:
        """
        If some id's were passed. Only those specific item's info will be used.
        """
        for i in item_id:
            for n in i:
                if select_by_id(n):
                    data.append(select_by_id(n))
        data = [data]
    else:
        """
        Else every single item's info shall be passed.
        """
        data.append(select_items())
    for i in range(len(data[0])):
        """
        Filling rows of the future list of dictionaries.
        """
        for j in range(len(columns)):
            item.update({columns[j]: data[0][i][j]})
            if columns[j] == "price":
                if data[0][i][j] < round(data[0][i][j]):
                    buff = "{:,}".format(math.trunc(data[0][i][j] * 100) / 100)
                else:
                    buff = "{:,}".format(round(data[0][i][j], 2))
                item.update({columns[j]: buff})
            if columns[j] == "time_left":
                if datetime.datetime.today() < data[0][i][j]:
                    item.update({columns[j]: str(data[0][i][j] - datetime.datetime.today())[:8]})
                else:
                    item.update({columns[j]: "Expired"})
        items.append(dict(item))
    return items


def add_new_item(item: str, description: str, price: float, bid_date: str, bid_time: str):
    """
    Add new item to auction.

    :param item: Name of the item.
    :param description: Description of the item.
    :param price: Price of the item.
    :param bid_date: Date till end of auction for this item.
    :param bid_time: Time till end of auction for this item.
    :return: Add new item to auction and refresh the page.
    """
    price = math.trunc(price * 100) / 100
    ConnectToDatabase.cursor.execute(f'SELECT MAX(id) FROM auction')
    max_id = ConnectToDatabase.cursor.fetchall()[0][0]
    if max_id is None:
        max_id = 1
    else:
        max_id += 1
    try:
        ConnectToDatabase.cursor.execute(f'INSERT INTO auction (id, item, owners, descript, '
                                         f'price, last_bidder, bid_time) VALUES ({max_id}, '
                                         f'"{item}", "{session["username"]}", "{description}", '
                                         f'{price},"" , "{bid_date} {bid_time}")')
    except:
        flash('Something went wrong! Make sure not to write "" symbols while adding new item!', category="danger")
        return redirect(url_for("my_office_page"))
    ConnectToDatabase.db_connection.commit()
    flash(f'Dear {session["username"]}, your new item {item} was successfully posted on auction! '
          f'Wish you the best of luck in selling the item with highest price! Thanks for using our '
          f'services!', category="success")
    return redirect(url_for("my_office_page"))


def delete_item(item_id: int) -> None:
    """
    Delete the item using item's id.

    :param item_id: id of the item which data you wish to erase.
    :return: Erase data if item exist.
    """
    """
    Check if item with this id exist and erase data if it does.
    """
    if delete_item_data(item_id):
        """
        Erase data of bid history on this item from users;
        """
        ConnectToDatabase.cursor.execute("SELECT login FROM users")
        users = ConnectToDatabase.cursor.fetchall()
        item_id = str(item_id)
        for i in users:
            i = i[0]
            bidden_items = select_from_bidden_items(i)
            bidden_price = select_from_bidden_price(i)
            iteration = 0
            for n in bidden_items:
                if n == item_id:
                    update_balance(i, float(bidden_price[iteration]), "+")
                    bidden_price.remove(bidden_price[iteration])
                    bidden_items.remove(n)
                    update_bidden_items(i, bidden_items)
                    update_bidden_price(i, bidden_price)
        flash(f'Item with id {item_id} was successfully deleted!', category="success")
    else:
        flash(f'It seems item with id {item_id} doesn`t exist!', category="danger")
