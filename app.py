import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from functions import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
connection = sqlite3.connect("./database_used_while_coding.db", check_same_thread=False)
db = connection.cursor()


# Startpage is shopping list
@app.route("/", methods=["GET", "POST"])
@show_about
def index():

    # user reached route via GET
    if request.method == "GET":

        userid = session.get("user_id")
        name = db.execute("SELECT name FROM users WHERE id = ?", (userid,)).fetchall()
        username = name[0][0]

        # Get list of stores
        storelist = list_stores()
        if not storelist:
            storelist = []

        # Get list of known items
        itemlist = list_items()
        if not itemlist:
            itemlist = []

        # Get shopping list if any
        shoppinglisttrial = list_users_items(userid)
        if shoppinglisttrial:
            shoppinglist = shoppinglisttrial

            # Get list of categories in said shopping list
            shoppinglistcategories = list_users_categories(userid)
            if not shoppinglistcategories:
                shoppinglistcategories = []

            # define empty list for optional use and otherwise to avoid error message if not used
            nonelistcategories = []

            # If store was chosen, the list has to be altered
            storeid = request.args.get("storeid")
            if storeid:
                storeid = int(storeid)
                shoppinglistcategories = list_new_positionings(storeid)
                if not shoppinglistcategories:
                    shoppinglistcategories = []
                nonelistcategories = list_none_positionings(storeid)
                if not nonelistcategories:
                    nonelistcategories = []

            return render_template("index.html", username=username, storelist=storelist, itemlist=itemlist, shoppinglist=shoppinglist, shoppinglistcategories=shoppinglistcategories, nonelistcategories=nonelistcategories, storeid=storeid)

        # there isn't any shopping list yet
        return render_template("index.html", username=username, storelist=storelist, itemlist=itemlist)

    # User reached route via POST
    storeid = request.form.get("storeid")
    itemid = str(request.form.get("itemid"))
    if not itemid:
        flash(u'Missing item.', 'warning')
        if storeid is None or storeid == 'None':
            return redirect("/")
        return redirect("/?storeid="+storeid)

    userid = str(session.get("user_id"))
    amount = str(request.form.get("amount"))

    db.execute("INSERT INTO lists (user_id, item_id, amount) VALUES (?, ?, ?)", (userid, itemid, amount))
    connection.commit()

    flash(u'Added item to list', 'success')
    if storeid is None or storeid == 'None':
        return redirect("/")

    return redirect("/?storeid="+storeid)


# delete something from shopping list
@app.route("/abolish", methods=["POST"])
@login_required
def abolish():
    userid = session.get("user_id")
    itemid = request.form.get("itemid")
    storeid = request.form.get("storeid")

    # delete item from users shopping list (but not from items)
    db.execute("DELETE FROM lists WHERE user_id = ? AND item_id = ?", (userid, itemid))
    connection.commit()

    # inform user about success
    flash(u'Deleted item from your shopping list.', 'success')

    # back to shopping list page
    if storeid is None or storeid == 'None':
        return redirect("/")

    return redirect("/?storeid="+storeid)


# about me and manual page
@app.route("/about")
def about():
    return render_template("about.html")


# strike or unstrike item on shopping list
@app.route("/alterstrike", methods=["GET"])
@login_required
def alterstrike():
    userid = session.get("user_id")
    itemid = request.args.get("itemid")
    strike = request.args.get("strike")
    storeid = request.args.get("storeid")

    # strike or unstrike, that is the question
    if strike == 'y':
        strike = 'n'
    else:
        strike = 'y'

    # now strike the unstricken but unstrike the struck
    db.execute("UPDATE lists SET strike = ? WHERE user_id = ? AND item_id = ?", (strike, userid, itemid))
    connection.commit()

    # no need to flash the user a message since they will see the strike gone or struck
    if storeid is None or storeid == 'None':
        return redirect("/")

    return redirect("/?storeid="+storeid)


# change amount of something on shopping list
@app.route("/amount", methods=["POST"])
@login_required
def amount():

    userid = session.get("user_id")
    itemid = request.form.get("itemid")
    amount = request.form.get("amount")
    storeid = request.form.get("storeid")

     # change item's amount in user's shopping list
    db.execute("UPDATE lists SET amount = ? WHERE user_id = ? AND item_id = ?", (amount, userid, itemid))
    connection.commit()

    # inform user about success
    flash(u'Changed amount of selected item.', 'success')

    # back to shopping list page
    if storeid is None or storeid == 'None':
        return redirect("/")

    return redirect("/?storeid="+storeid)


# category page
@app.route("/category", methods=["GET", "POST"])
@login_required
def category():

    # User reached route via GET
    if request.method == "GET":
        # get list of categories
        categorylist = list_categories()
        if categorylist:

            # get list of categories used in positionings
            usedcategorylist = list_used_categories()
            if not usedcategorylist:
                usedcategorylist = []

            # send categorylist to pagetemplate
            return render_template("category.html", categorylist=categorylist, usedcategorylist=usedcategorylist)

        # there are no categories yet
        return render_template("category.html")

    # user reached route via POST
    # would user make up their mind please. if no category is submitted, I cannot stuff it into the database
    if not request.form.get("category"):
        flash(u'Missing category.', 'warning')
        return redirect("/category")

    # Enter new category into database
    category = request.form.get("category")
    db.execute("INSERT INTO categories (category) VALUES (?)", (category,))
    connection.commit()

    # Always give feedback because we care about users. :)
    flash(u'New category recorded.', 'success')

    # Redirect user to home page
    return redirect("/category")


# change category
@app.route("/categorychange", methods=["POST"])
@login_required
def categorychange():

    # if categoryname was deleted, the user might have used the wrong button
    if not request.form.get("modalInput"):
        flash(u'Category missing. If you want to delete a category, please use the delete button.', 'warning')
        return redirect("/category")

    category = request.form.get("modalInput")
    categoryid = str(request.form.get("hiddenInput"))

    db.execute("UPDATE categories SET category = ? WHERE categoryid = ?", (category, categoryid))
    connection.commit()

    # Always give feedback because we care about users. :)
    flash(u'Changed category.', 'success')

    # Redirect user to store page
    return redirect("/category")


# delete category
@app.route("/categorydelete", methods=["POST"])
@login_required
def categorydelete():

    categoryid = str(request.form.get("hiddenInput"))

    # delete store from database
    db.execute("DELETE FROM categories WHERE categoryid = ?", (categoryid,))
    connection.commit()

    # Tell user to look what they've done
    flash(u'Deleted category.', 'success')

    # Redirect user to store page
    return redirect("/category")


# item page
@app.route("/item", methods=["GET", "POST"])
@login_required
def item():

    # User reached route via GET
    if request.method == "GET":

        # get category list first
        categorylist = list_categories()
        if categorylist:

            # list items if any
            itemlist = list_items()
            if itemlist:

                # check which items are used in lists
                useditemlist = list_used_items()
                if not useditemlist:
                    useditemlist =[]

                return render_template("item.html", categorylist=categorylist, itemlist=itemlist, useditemlist=useditemlist)

            # there are no items yet but we already have categories
            return render_template("item.html", categorylist=categorylist)

        # there are no categories, hence there cannot be any items
        return render_template("item.html")

    # User reached route via POST
    # no item submitted nothing to do here
    if not request.form.get("item"):
        flash(u'Missing item.', 'warning')
        return redirect("/item")

    # prepare data for insertion into database
    item = request.form.get("item")

    if not request.form.get("categoryid"):
        flash(u'Missing category.', 'warning')
        return redirect("/item")

    categoryid = request.form.get("categoryid")

    db.execute("INSERT INTO items (description, category_id) VALUES (?, ?)", (item, categoryid))
    connection.commit()

    # let user have a sense of achievement
    flash(u'New item recorded.', 'success')

    return redirect("/item")


# change item
@app.route("/itemchange", methods=["POST"])
@login_required
def itemchange():

    # if itemname was deleted, the user might have used the wrong button
    if not request.form.get("modalInput"):
        flash(u'Item missing. If you want to delete an item, please use the delete button.', 'warning')
        return redirect("/item")
    else:
        description = request.form.get("modalInput")
        itemid = str(request.form.get("hiddenInput"))
        categoryid = str(request.form.get("modalSelect"))

        db.execute("UPDATE items SET description = ?, category_id = ? WHERE itemid = ?", (description, categoryid, itemid))
        connection.commit()

        # Always give feedback because we care about users. :)
        flash(u'Changed item.', 'success')

        # Redirect user to store page
        return redirect("/item")


@app.route("/itemdelete", methods=["POST"])
@login_required
def itemdelete():

    itemid = str(request.form.get("hiddenInput"))

    # delete store from database
    db.execute("DELETE FROM items WHERE itemid = ?", (itemid,))
    connection.commit()

    # Tell user to look what they've done
    flash(u'Deleted item.', 'success')

    # Redirect user to store page
    return redirect("/item")


# login page
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via GET
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST
    # Ensure username was submitted
    if not request.form.get("username"):
        flash(u'Missing username.', 'warning')
        return render_template("login.html")

    # Ensure password was submitted
    if not request.form.get("password"):
        flash(u'Missing password.', 'warning')
        return render_template("login.html")

    # Query database for username
    username = request.form.get("username")
    password = request.form.get("password")
    rows = db.execute("SELECT * FROM users WHERE name = ?", (username,)).fetchall()

    # Ensure username exists and password is correct
    if len(rows) != 1:
        flash(u'Wrong username.', 'warning')
        return render_template("login.html")

    # Ensure username exists and password is correct
    if not check_password_hash(rows[0][2], password):
        flash(u'Wrong password.', 'warning')
        return render_template("login.html")

    # Remember which user has logged in
    session["user_id"] = rows[0][0]

    # Let them know
    flash(u'You were successfully logged in.', 'success')

    # Redirect user to home page
    return redirect("/")


# logout
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Confirm logout to user
    flash(u'Session closed, you are logged out.', 'success')

    # Redirect user to login form
    return render_template("login.html")


# category order in store page
@app.route("/order", methods=["GET", "POST"])
@login_required
def order():

    # User reached route via GET
    if request.method == "GET":

        # prepare the dropdownlist of categories
        categorylist = list_categories()
        if not categorylist:

            # Cannot make positioning without categories
            flash(u'There are no categories yet. Please record some in Categories first.', 'warning')

            # Redirect user to positioning form
            return redirect("/category")

        # which store's categories does the user wish to edit
        storeid = str(request.args.get("storeid"))

        # get storename
        rows = db.execute("SELECT store FROM stores WHERE storeid = ?", (storeid,)).fetchall()
        store = rows[0][0]

        positionlist = list_positioning(storeid)

        # send categorylist to pagetemplate
        return render_template("order.html", categorylist=categorylist, storeid=storeid, store=store, positionlist=positionlist)

    # User reached route via POST
    # get storeid
    storeid = str(request.form.get("storeid"))

    # If user didn't enter a category we can't do stuff with the database
    if not request.form.get("categoryid"):

        # Tell user what went wrong
        flash(u'Category missing. If you want to delete a category please use the delete button.', 'warning')

        # Redirect user to positioning form
        return redirect("/order?storeid=" + storeid)

    # add category to positioning
    # prepare category for entering database
    categoryid = request.form.get("categoryid")

    # find out at what position the next category is to place
    posEnd = db.execute("SELECT MAX(position) FROM positionings WHERE store_id = ?", (storeid,)).fetchall()
    nextPos = 1
    if posEnd[0][0] is not None:
        nextPos = posEnd[0][0] + 1

    # do more stuff with the database
    db.execute("INSERT INTO positionings (store_id, category_id, position) VALUES (?, ?, ?)", (storeid, categoryid, nextPos))
    connection.commit()

    # flash the success
    flash(u'Added category.', 'success')

    # show category in store list
    return redirect("/order?storeid=" + storeid)


# delete category from positioning
@app.route("/orderdelete", methods=["POST"])
@login_required
def orderdelete():

    storeid = request.form.get("storeid")
    position = request.form.get("position")

    # delete position from database
    db.execute("DELETE FROM positionings WHERE store_id = ? and position = ?", (storeid, position))
    connection.commit()

    # subtract 1 from all the positions higher than the one to be deleted
    rows = db.execute("SELECT position FROM positionings WHERE store_id = ? AND position > ? ORDER BY position", (storeid, position)).fetchall()
    if rows:
        for row in rows:
            positionold = row[0]
            positionnew = positionold - 1
            db.execute("UPDATE positionings SET position = ? WHERE store_id = ? AND position = ?", (positionnew, storeid, positionold))
            connection.commit()

    # Tell user to look what they've done
    flash(u'Deleted position ' + position + '.', 'success')

    # Redirect user to positioning page
    return redirect("/order?storeid=" + storeid)


# move category up one row
@app.route("/ordermovedown", methods=["GET"])
@login_required
def ordermovedown():

    storeid = request.args.get("storeid")
    categoryid = request.args.get("categoryid")
    position = int(request.args.get("position"))
    positionafter = position + 1

    # only move stuff, if it's not the end of the list already
    nextPos = db.execute("SELECT category_id, position FROM positionings WHERE store_id = ? AND position = ?", (storeid, positionafter)).fetchall()
    if nextPos:

        # first delete entry to be moved
        db.execute("DELETE FROM positionings WHERE store_id = ? AND position = ?", (storeid, position))
        connection.commit()

        # then move next entry up to make way
        db.execute("UPDATE positionings SET position = ? WHERE store_id = ? AND position = ?", (position, storeid, positionafter))
        connection.commit()

        # finally re-insert entry at it's new position
        db.execute("INSERT INTO positionings (store_id, category_id, position) VALUES (?, ?, ?)", (storeid, categoryid, positionafter))
        connection.commit()

    # return user without flash message
    return redirect("/order?storeid=" + storeid)


# move category down one row
@app.route("/ordermoveup", methods=["GET"])
@login_required
def ordermoveup():

    storeid = request.args.get("storeid")
    categoryid = request.args.get("categoryid")
    position = int(request.args.get("position"))
    positionbefore = position - 1

    # only move stuff, if it's not the beginning of the list already
    previousPos = db.execute("SELECT category_id, position FROM positionings WHERE store_id = ? AND position = ?", (storeid, positionbefore)).fetchall()
    if previousPos:

        # first delete entry to be moved
        db.execute("DELETE FROM positionings WHERE store_id = ? AND position = ?", (storeid, position))
        connection.commit()

        # then move previous entry up to make way
        db.execute("UPDATE positionings SET position = ? WHERE store_id = ? AND position = ?", (position, storeid, positionbefore))
        connection.commit()

        # finally re-insert entry at it's new position
        db.execute("INSERT INTO positionings (store_id, category_id, position) VALUES (?, ?, ?)", (storeid, categoryid, positionbefore))
        connection.commit()

    # return user without flash message
    return redirect("/order?storeid=" + storeid)


# register new user
@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST
    # Ensure username was submitted
    if not request.form.get("username"):
        flash(u'Missing username.', 'warning')
        return render_template("register.html")

    # Ensure password was submitted
    if not request.form.get("password"):
        flash(u'Missing password.', 'warning')
        return render_template("register.html")

    # Ensure password was confirmed
    if not request.form.get("confirmation"):
        flash(u'Missing password confirmation.', 'warning')
        return render_template("register.html")

    # Ensure both password and it's confirmation match
    if request.form.get("password") != request.form.get("confirmation"):
        flash(u'Confirmation must match password.', 'warning')
        return render_template("register.html")

    # Ensure password fulfills requirements
    if not any(map(str.isdigit, request.form.get("password"))) or not any(map(str.isupper, request.form.get("password"))):
        flash(u'Password must fulfill requirements.', 'warning')
        return render_template("register.html")

    # Everything was entered but there's still one last check to make
    # Query database for username
    username = request.form.get("username")
    rows = db.execute("SELECT name FROM users WHERE name = ?", (username,)).fetchall()

    # Ensure username is not already taken
    if rows:
        flash(u'Username is already taken. Choose another.', 'warning')
        return render_template("register.html")

    # Everything finally seems fine
    # never eat your hash brown without a pinch of salt
    hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

    # Enter new user into database
    username = request.form.get("username")
    db.execute("INSERT INTO users (name, hash) VALUES (?, ?)", (username, hash))

    # Forget any user_id
    session.clear()

    # Query database for username
    #username = request.form.get("username") #why do I need this twice?
    rows = db.execute("SELECT * FROM users WHERE name = ?", (username,)).fetchall()

    # Remember which user has logged in
    session["user_id"] = rows[0][0]

    # Persist database changes
    connection.commit()

    # Let user know about successfully registering
    flash(u'You are now a registered user.', 'success')

    # Redirect user to home page
    return redirect("/")


# store page
@app.route("/store", methods=["GET", "POST"])
@login_required
def store():

    # User reached route via GET
    if request.method == "GET":
        storelist = list_stores()
        if not storelist:
            storelist = []

        # send storelist to pagetemplate
        return render_template("store.html", storelist=storelist)

    # User reached route via POST
    # the adress is not mandatory but I can't record a store if none was entered
    if not request.form.get("storename"):
        flash(u'Missing storename.', 'warning')
        return render_template("store.html")

    # Enter new store into database
    store = request.form.get("storename")
    adress = "NULL"
    if request.form.get("adress"):
        adress = request.form.get("adress")

    db.execute("INSERT INTO stores (store, adress) VALUES (?, ?)", (store, adress))
    connection.commit()

    # Always give feedback because we care about users. :)
    flash(u'New store recorded.', 'success')

    # Redirect user to home page
    return redirect("/store")


# change store
@app.route("/storechange", methods=["POST"])
@login_required
def storechange():

    # if storename was deleted, the user might have used the wrong button
    if not request.form.get("modalInput"):
        flash(u'Store name missing. If you want to delete a store, please use the delete button.', 'warning')
        return redirect("/store")

    store = request.form.get("modalInput")
    storeid = str(request.form.get("hiddenInput"))
    adress = "NULL"
    if request.form.get("modalArea"):
        adress = request.form.get("modalArea")

    db.execute("UPDATE stores SET store = ?, adress = ? WHERE storeid = ?", (store, adress, storeid))
    connection.commit()

    # Always give feedback because we care about users. :)
    flash(u'Changed store.', 'success')

    # Redirect user to store page
    return redirect("/store")


# delete store
@app.route("/storedelete", methods=["POST"])
@login_required
def storedelete():

    storeid = str(request.form.get("hiddenInput"))

    # delete store from database
    db.execute("DELETE FROM stores WHERE storeid = ?", (storeid,))
    db.execute("DELETE FROM positionings WHERE store_id = ?", (storeid,))
    connection.commit()

    # Tell user to look what they've done
    flash(u'Deleted store.', 'success')

    # Redirect user to store page
    return redirect("/store")
