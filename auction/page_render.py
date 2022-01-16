from flask import render_template, redirect, url_for

from auction.imports import UpdateBalanceForm, DeleteAccountForm, AddItemForm, ChangeStoryForm, \
    AdminRightsDeleteUserForm, AdminRightsUpdateUserBalanceForm, AdminRightsDeleteItemForm, update_story, session, \
    update_balance, delete_account, add_new_item, delete_item, login_required, get_budget, \
    select_from_privilegies, select_from_story, select_from_email, get_values_for_auction, BidOnItemForm, \
    bid_on_the_item, select_from_last_bidder, select_by_id_owner, select_by_id_price, transfer_ownership, \
    update_last_bidder, return_money_to_losers, select_from_bidden_items, RegisterForm, register, logout, LoginForm, \
    login, check_logged_in, SellItemForm, put_on_auction


def home_render():
    """
    Function used to get all related to home page data to render on html page.

    :return: render template of the home page.
    """
    check_logged_in()
    try:
        if session['loggedin']:
            budget = get_budget()
            return render_template('home.html', budget=budget)
    except:
        session['loggedin'] = False
    return render_template('home.html')


def register_render():
    """
    Function used to get all related to register page data to render on html page.

    :return: render template of the registration page..
    """
    form = RegisterForm()
    if register(form) is True:
        return redirect(url_for('auction_page'))
    return render_template('register.html', form=form)


def login_render():
    """
    Function used to get all related to login page data to render on html page.

    :return: render template of the login page.
    """
    form = LoginForm()
    if login(form):
        return redirect(url_for("home_page"))
    return render_template('login.html', form=form)


def logout_render():
    """
    Just a logout function.
    """
    logout()
    return redirect(url_for("home_page"))


def auction_render():
    """
    Function used to get all related to auction page data to render on html page.

    :return: render template of the auction page.
    """
    check_logged_in()
    if not session['loggedin']:
        return login_required()

    items = get_values_for_auction()
    budget = get_budget()
    bid_on_item_form = BidOnItemForm()

    if bid_on_item_form.validate_on_submit():
        return bid_on_the_item(bid_on_item_form.bid.data, "auction_page")

    for i in items:
        if i["time_left"] == "Expired":
            if select_from_last_bidder(i["id"]) != "":
                update_balance(select_by_id_owner(i["id"]), select_by_id_price(i["id"]), "+")
                transfer_ownership(select_from_last_bidder(i["id"]), i["id"])
                update_last_bidder("", i["id"])
                return_money_to_losers(select_from_last_bidder(i["id"]), i["id"])

    return render_template('auction.html', items=items, budget=budget, bid_on_item_form=bid_on_item_form)


def my_bids_render():
    """
    Function used to get all related to my bids page data to render on html page.

    :return: render template of the my bids page.
    """
    check_logged_in()
    if not session['loggedin']:
        return login_required()

    my_bids = get_values_for_auction(select_from_bidden_items(session['username']))
    items = get_values_for_auction()
    budget = get_budget()
    bid_on_item_form = BidOnItemForm()
    sell_item_form = SellItemForm()

    if bid_on_item_form.validate_on_submit():
        return bid_on_the_item(bid_on_item_form.bid.data, "my_bids_page")

    if sell_item_form.submit.data:
        return put_on_auction(sell_item_form.price.data, sell_item_form.date_until_purchase.data,
                              sell_item_form.time_until_purchase.data)

    for i in items:
        if i["time_left"] == "Expired":
            if select_from_last_bidder(i["id"]) != "":
                update_balance(select_by_id_owner(i["id"]), select_by_id_price(i["id"]), "+")
                transfer_ownership(select_from_last_bidder(i["id"]), i["id"])
                update_last_bidder("", i["id"])
                return_money_to_losers(select_from_last_bidder(i["id"]), i["id"])

    return render_template('my_bids.html', items=items, my_bids=my_bids, budget=budget,
                           bid_on_item_form=bid_on_item_form, sell_item_form=sell_item_form)


def my_office_render():
    """
    Function used to get all related to my office page data to render on html page.

    :return: render template of the my office page.
    """
    check_logged_in()
    if not session['loggedin']:
        return login_required()

    budget = get_budget()
    privilegies = select_from_privilegies(session['username'])

    update_balance_form = UpdateBalanceForm()
    delete_form = DeleteAccountForm()
    add_item_form = AddItemForm()
    change_story_form = ChangeStoryForm()
    admin_rights_delete_user_form = AdminRightsDeleteUserForm()
    admin_rights_delete_item_form = AdminRightsDeleteItemForm()
    admin_rights_update_user_balance_form = AdminRightsUpdateUserBalanceForm()
    story = select_from_story(session['username'])
    my_email = select_from_email(session['username'])

    if change_story_form.validate_on_submit():
        if change_story_form.submit.data:
            return update_story(session['username'], change_story_form.story.data)

    if update_balance_form.validate_on_submit():
        if update_balance_form.update.data:
            return update_balance(session['username'], update_balance_form.balance.data, "+")

    if delete_form.validate_on_submit():
        if delete_form.delete.data:
            return delete_account(session['username'])

    if add_item_form.validate_on_submit():
        if add_item_form.submit.data:
            return add_new_item(add_item_form.name.data, add_item_form.description.data,
                                add_item_form.price.data, add_item_form.date_until_purchase.data,
                                add_item_form.time_until_purchase.data)

    if admin_rights_delete_user_form.validate_on_submit():
        if admin_rights_delete_user_form.submit_delete_user.data:
            delete_account(admin_rights_delete_user_form.delete_user.data)

    if admin_rights_delete_item_form.validate_on_submit():
        if admin_rights_delete_item_form.submit_delete_item.data:
            delete_item(admin_rights_delete_item_form.delete_item.data)

    if admin_rights_update_user_balance_form.validate_on_submit():
        if admin_rights_update_user_balance_form.submit_update_balance_plus.data:
            update_balance(admin_rights_update_user_balance_form.update_user_balance.data,
                           admin_rights_update_user_balance_form.update_balance.data, "+")
        if admin_rights_update_user_balance_form.submit_update_balance_minus.data:
            update_balance(admin_rights_update_user_balance_form.update_user_balance.data,
                           admin_rights_update_user_balance_form.update_balance.data, "-")

    return render_template('my_office.html', budget=budget, privilegies=privilegies,
                           update_balance_form=update_balance_form, delete_form=delete_form,
                           add_item_form=add_item_form, my_email=my_email, story=story,
                           change_story_form=change_story_form,
                           admin_rights_delete_user_form=admin_rights_delete_user_form,
                           admin_rights_delete_item_form=admin_rights_delete_item_form,
                           admin_rights_update_user_balance_form=admin_rights_update_user_balance_form)
