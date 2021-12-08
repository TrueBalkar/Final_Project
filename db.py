import mysql.connector


class ConnectToDatabase:
    db_connection = mysql.connector.connect(
        host="Localhost",
        user="root",
        password="not_so_good",
        database="python_mysql"
    )
    cursor = db_connection.cursor()


class SqlStatement:
    select_from_id = "SELECT id FROM auction"
    select_from_name = "SELECT name FROM auction"
    select_from_barcode = "SELECT barcode FROM auction"
    select_from_price = "SELECT price FROM auction"


def get_values_from_db(cursor, *statements):
    items = []
    columns = []
    item = {}
    data = []
    for i in statements:
        stt = i.split()
        columns.append(stt[1])
        item.update({stt[1]: None})
    for i in statements:
        cursor.execute(i)
        data.append(cursor.fetchall())
    for i in range(len(data)):
        for j in range(len(columns)):
            item.update({columns[j]: data[j][i][0]})
        items.append(dict(item))
    return items
