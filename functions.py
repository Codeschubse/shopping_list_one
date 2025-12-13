import sqlite3

from functools import wraps
from flask import redirect, session


# Configure SQLite database
connection = sqlite3.connect("./database_used_while_coding.db", check_same_thread=False)
db = connection.cursor()

# functions order:
# 1. app functionality
# 2. general lists
# 3. specific lists


# require user to be logged in
# code heavily inspired from cs50 problem set 9 finance
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# send user to about page if not logged in
# code heavily inspired from cs50 problem set 9 finance
def show_about(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/about")
        return f(*args, **kwargs)
    return decorated_function


# make general list of categories
def list_categories():
    # list categories if any
    rows = db.execute("SELECT * FROM categories ORDER BY category").fetchall()
    if rows:

        # create and fill dictionary-list of categories
        categorylist  = []
        for row in rows:
            categoryid = row[0]
            category = row[1]

            categorydict = {
                "categoryid": categoryid,
                "category": category
            }
            categorylist.append(categorydict)

        return categorylist
    # there aren't any categories
    else:
        pass


# make general list of used categories
def list_used_categories():
    # check which categories are used in positionings
    usedcategorylist = []
    rows = db.execute("SELECT DISTINCT category_id FROM positionings ORDER BY category_id").fetchall()
    if rows:
        for row in rows:
            used = row[0]
            usedcategorylist.append(used)

        return usedcategorylist
    # there are no categories used in positionings
    else:
        pass


# make general list of items
def list_items():
    # list items if any
    rows = db.execute("SELECT * FROM items ORDER BY description").fetchall()
    if rows:

        # create and fill dictionary-list of categories
        itemlist = []
        for row in rows:
            itemid = row[0]
            description = row[1]
            categoryid = row[2]

            # get category name also
            catname = db.execute("SELECT category FROM categories WHERE categoryid = ?", (categoryid,)).fetchall()
            category = catname[0][0]

            itemdict = {
                "itemid": itemid,
                "description": description,
                "categoryid": categoryid,
                "category": category
            }
            itemlist.append(itemdict)

        return itemlist
    # there aren't any items
    else:
        pass


# make general list of used items
def list_used_items():
    # check which items are used in lists
    useditemlist = []
    rows = db.execute("SELECT DISTINCT item_id FROM lists ORDER BY item_id").fetchall()
    if rows:
        for row in rows:
            used = row[0]
            useditemlist.append(used)

        return useditemlist
    # there are no categories used in positionings
    else:
        pass


# make general list of stores
def list_stores():
    # list stores if any
    rows = db.execute("SELECT * FROM stores ORDER BY store").fetchall()
    if rows:

        # create and fill dictionary-list of stores
        storelist  = []
        for row in rows:
            storeid = row[0]
            store = row[1]
            adress = row[2]

            if adress == "NULL":
                adress = ""
            else:
                adress = adress.replace("\r\n", "<br />")

            storedict = {
                "storeid": storeid,
                "store": store,
                "adress": adress
            }
            storelist.append(storedict)

        return storelist
    # there aren't any stores
    else:
        pass


# make specific positioning list of categories in selected store
def list_positioning(storeid):
    positionlist  = []
    # get existing category order if any
    rows = db.execute("SELECT position, category_id FROM positionings WHERE store_id = ? ORDER BY position", (storeid,)).fetchall()

    if rows:

        # create and fill dictionary-list of positions
        for row in rows:
            position = row[0]
            categoryid = row[1]

            catname = db.execute("SELECT category FROM categories WHERE categoryid = ?", (categoryid,)).fetchall()
            category = catname[0][0]

            positiondict = {
                "position": position,
                "categoryid": categoryid,
                "category": category
            }
            positionlist.append(positiondict)
    return positionlist


# make specific list of positionings on shopping list available in selected store
def list_new_positionings(storeid):

    alteredcategorylist = []
    userid = session.get("user_id")
    bar = db.execute("""SELECT category_id
                          FROM positionings
                         WHERE store_id = ?
                           AND category_id IN (SELECT DISTINCT items.category_id
                                                          FROM items
                                                          JOIN lists
                                                            ON items.itemid = lists.item_id
                                                         WHERE lists.user_id = ?)
                      ORDER BY position""", (storeid, userid)).fetchall()
    if bar:
        for foo in bar:
            bazid = foo[0]

            # get category name
            name = db.execute("SELECT category FROM categories WHERE categoryid = ?", (bazid,)).fetchall()
            bazcat = name[0][0]

            bazdict = {
                "categoryid": bazid,
                "category": bazcat
            }
            alteredcategorylist.append(bazdict)

        return alteredcategorylist
    # user has no items on their list
    else:
        pass


# make specific list of positionings on shopping list NOT available in selected store
def list_none_positionings(storeid):

    nonecategorylist = []
    userid = session.get("user_id")
    bar = db.execute("""SELECT categoryid, category
                          FROM categories
                         WHERE categoryid IN (SELECT DISTINCT items.category_id
                                                         FROM items
                                                         JOIN lists
                                                           ON items.itemid = lists.item_id
                                                        WHERE lists.user_id = ?
                                                          AND items.category_id NOT IN (SELECT DISTINCT category_id
                                                                                                   FROM positionings
                                                                                                  WHERE store_id = ?))
                      ORDER BY category""", (userid, storeid)).fetchall()
    if bar:
        for foo in bar:
            bazid = foo[0]
            bazcat = foo[1]

            bazdict = {
                "categoryid": bazid,
                "category": bazcat
            }
            nonecategorylist.append(bazdict)

        return nonecategorylist
    # user has no items on their list
    else:
        pass


# make specific shopping list of active user
def list_users_items(userid):

    shoppinglist = []
    rows = db.execute("""SELECT lists.item_id, lists.amount, lists.strike, items.description, items.category_id
                           FROM lists
                           JOIN items
                             ON lists.item_id = items.itemid
                          WHERE lists.user_id = ?
                       ORDER BY description""", (userid,)).fetchall()
    if rows:
        for row in rows:
            itemid = row[0]
            amount = row[1]
            strike = row[2]
            description = row[3]
            categoryid = row[4]

            itemdict = {
                "itemid": itemid,
                "description": description,
                "amount": amount,
                "categoryid": categoryid,
                "strike": strike
            }
            shoppinglist.append(itemdict)

        return shoppinglist
    # user has no items on their list
    else:
        pass


# make specific list of categories in users shopping list
def list_users_categories(userid):

    shoppinglistcategories = []
    bar = db.execute("""SELECT categoryid, category
                          FROM categories
                         WHERE categoryid IN (SELECT DISTINCT items.category_id
                                                         FROM items
                                                         JOIN lists
                                                           ON items.itemid = lists.item_id
                                                        WHERE lists.user_id = ?)
                      ORDER BY category""", (userid,)).fetchall()
    if bar:
        for foo in bar:
            bazid = foo[0]
            bazcat = foo[1]

            bazdict = {
                "categoryid": bazid,
                "category": bazcat
            }
            shoppinglistcategories.append(bazdict)

        return shoppinglistcategories
    # user has no items on their list
    else:
        pass
