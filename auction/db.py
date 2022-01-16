import datetime

from flask import redirect, url_for
import mysql.connector
import math


class ConnectToDatabase:
    """
    Connecting to database class!
    """
    db_connection = mysql.connector.connect(
        host="Localhost",
        user="root",
        password="not_so_good",
        database="python_mysql"
    )
    cursor = db_connection.cursor()


def select_items() -> list:
    """
    Get data of all items.

    :return: List of data of items.
    """
    ConnectToDatabase.cursor.execute(f'SELECT id, item, owners, descript, price, bid_time, last_bidder FROM auction')
    return ConnectToDatabase.cursor.fetchall()


def select_by_id(item_id: list) -> list:
    """
    Get data of items with specified id.

    :param item_id: List of id's used for data extraction.
    :return: List of data of those items
    """
    ConnectToDatabase.cursor.execute(f'SELECT id, item, owners, descript, price, '
                                     f'bid_time, last_bidder FROM auction WHERE id = {item_id}')
    return ConnectToDatabase.cursor.fetchall()[0]


def select_by_id_owner(item_id: int) -> str:
    """
    Get data about owner of item with specified id.

    :param item_id: id of item which owner needed.
    :return: Login of the owner of item.
    """
    ConnectToDatabase.cursor.execute(f'SELECT owners FROM auction WHERE id = {item_id}')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_by_id_name(item_id: int) -> str:
    """
    Get name of the item with specified id.

    :param item_id: id of the item.
    :return: Name of the item.
    """
    ConnectToDatabase.cursor.execute(f'SELECT item FROM auction WHERE id = {item_id}')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_by_id_price(item_id: str) -> float:
    """
    Get price of the item with specified id.

    :param item_id: id of the item.
    :return: Current price of the item.
    """
    ConnectToDatabase.cursor.execute(f'SELECT price FROM auction WHERE id = {item_id}')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_by_id_bid_time(item_id: int) -> datetime.datetime:
    """
    Get time of the end of auction for item with specified id.

    :param item_id: id of the item.
    :return: Date and time of the end of auction for this item.
    """
    ConnectToDatabase.cursor.execute(f'SELECT bid_time FROM auction WHERE id = {item_id}')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_from_last_bidder(item_id: int) -> str:
    """
    Get login of the user who bidden last on item with specified id.

    :param item_id: id of the item.
    :return: Login of the user.
    """
    ConnectToDatabase.cursor.execute(f'SELECT last_bidder FROM auction WHERE id = {item_id}')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def transfer_ownership(new_owner: str, item_id: int) -> None:
    """
    Transfer ownership of item with specified id to new owner.

    :param new_owner: Login of new owner of the item.
    :param item_id: id of the item.
    :return: Update database.
    """
    ConnectToDatabase.cursor.execute(f'UPDATE auction SET owners = "{new_owner}" WHERE id = {item_id}')
    ConnectToDatabase.db_connection.commit()


def select_from_user_id(login: str) -> int:
    """
    Get id of the user with username specified by variable "login".

    :param login: Login of the user.
    :return: id of the user.
    """
    ConnectToDatabase.cursor.execute(f'SELECT id FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_from_password(login: str) -> str:
    """
    Get password of the user.

    :param login: Login of the user.
    :return: Password of the user.
    """
    ConnectToDatabase.cursor.execute(f'SELECT user_password FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_from_email(login: str) -> str:
    """
    Get email of the user.

    :param login: Login of the user.
    :return: Email of the user.
    """
    ConnectToDatabase.cursor.execute(f'SELECT email FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def get_money(login: str) -> float:
    """
    Get budget of the user from database.

    :param login: Login of the user.
    :return: Budget of the user.
    """
    ConnectToDatabase.cursor.execute(f'SELECT budget FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_from_bidden_items(login: str) -> list:
    """
    Return string of items specified user bid on.

    :param login: Login of the user.
    :return: String of items user bid on.
    """
    ConnectToDatabase.cursor.execute(f'SELECT bidden_items FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0].split()


def select_from_bidden_price(login: str) -> str:
    """
    Return string of prices of items specified user bid on.

    :param login: Login of the user.
    :return: String of prices of items user bid on.
    """
    ConnectToDatabase.cursor.execute(f'SELECT bidden_price FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0].split()


def select_from_story(login: str) -> str:
    """
    Get "About Me:" info of the user.

    :param login: Login of the user.
    :return: User personal story.
    """
    ConnectToDatabase.cursor.execute(f'SELECT story FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def select_from_privilegies(login: str) -> str:
    """
    Get level of access of the user.

    :param login: Login of the user.
    :return: Level of access.
    """
    ConnectToDatabase.cursor.execute(f'SELECT privilegies FROM users WHERE login = "{login}"')
    return ConnectToDatabase.cursor.fetchall()[0][0]


def update_story(login: str, data: str):
    """
    Update user's "About Me".

    :param login: Login of the user.
    :param data: Data to update in "About Me".
    :return: Update data and refresh page.
    """
    ConnectToDatabase.cursor.execute(f'UPDATE users SET story = "{data}" WHERE login = "{login}"')
    ConnectToDatabase.db_connection.commit()
    return redirect(url_for("my_office_page"))


def update_money(login: str, money: float) -> None:
    """
    Update user budget.

    :param login: Login of the user.
    :param money: Amount of money user should have.
    :return: Update data in database.
    """
    money = math.trunc(money * 100) / 100
    ConnectToDatabase.cursor.execute(f'UPDATE users SET budget = {money} WHERE login = "{login}"')
    ConnectToDatabase.db_connection.commit()


def update_price(item_id: str, price: float) -> None:
    """
    Update item price.

    :param item_id: id of the item.
    :param price: Price of the item.
    :return: Update data in database.
    """
    price = math.trunc(price * 100) / 100
    ConnectToDatabase.cursor.execute(f'UPDATE auction SET price = {price} WHERE id = {item_id}')
    ConnectToDatabase.db_connection.commit()


def update_bidden_items(login: str, item_id: list) -> None:
    """
    Update bidden items of the user.

    :param login: Login of the user.
    :param item_id: id's of items user bid on.
    :return: Update data in database.
    """
    ConnectToDatabase.cursor.execute(f'UPDATE users SET bidden_price = "" WHERE login = "{login}"')
    ConnectToDatabase.db_connection.commit()
    buffer = ""
    for i in item_id:
        buffer += f' {i}'
    ConnectToDatabase.cursor.execute(f'UPDATE users SET bidden_items = "{buffer}" WHERE login = "{login}"')
    ConnectToDatabase.db_connection.commit()


def update_bidden_price(login: str, price: list) -> None:
    """
    Update bidden items prices of the user.

    :param login: Login of the user.
    :param price: Prices of corresponding bidden items/
    :return: Update data in database
    """
    ConnectToDatabase.cursor.execute(f'UPDATE users SET bidden_price = "" WHERE login = "{login}"')
    ConnectToDatabase.db_connection.commit()
    buffer = ""
    for i in price:
        buffer += f' {i}'
    ConnectToDatabase.cursor.execute(f'UPDATE users SET bidden_price = "{buffer}" WHERE login = "{login}"')
    ConnectToDatabase.db_connection.commit()


def update_last_bidder(login: str, item_id: int) -> None:
    """
    Update info about the last user who bid on item with specified id.

    :param login: Login of user who bid on item last.
    :param item_id: id of the item.
    :return: Update data in database.
    """
    ConnectToDatabase.cursor.execute(f'UPDATE auction SET last_bidder = "{login}" WHERE id = {item_id}')
    ConnectToDatabase.db_connection.commit()


def delete_account_data(login: str) -> bool:
    """
    Delete all data about the user.

    :param login: Login of the user whose data needs to be deleted.
    :return: True if data of the user was successfully deleted.
    """
    ConnectToDatabase.cursor.execute(f'SELECT login FROM users WHERE login = "{login}"')
    try:
        ConnectToDatabase.cursor.fetchall()[0][0]
        ConnectToDatabase.cursor.execute(f'DELETE FROM users WHERE login = "{login}"')
        ConnectToDatabase.db_connection.commit()
        return True
    except:
        return False


def delete_item_data(item_id: int) -> bool:
    """
    Delete all data about the item.

    :param item_id: id of the item which data needs to be deleted.
    :return: True if item data was successfully deleted.
    """
    ConnectToDatabase.cursor.execute(f'SELECT id FROM auction WHERE id = "{item_id}"')
    try:
        ConnectToDatabase.cursor.fetchall()[0][0]
        ConnectToDatabase.cursor.execute(f'DELETE FROM auction WHERE id = "{item_id}"')
        ConnectToDatabase.db_connection.commit()
        return True
    except:
        return False
