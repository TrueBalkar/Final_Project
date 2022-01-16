# Auction website written using flask
# Project Overview 
This is a simple flask project that was created in the proccess of learning python and flask in particular. It has basic functional of an auction website such as: registration and login of the user, biding system, selling system, user balance, account deletion and some other smaller functions.
# Configuration instructions 
Before you start using it you need to install and configure MySQL on your machine or just connect it to existing database. Then in file auction\db.py change connection data in class ConnectToDatabase to yours. After that import sql tables from my_sql_tables directory to your database. And you are pretty much ready to go.
# Installation instructions 
Download, configure and be ready to run website.
# Operating instructions
        Some testing
Execute run.py file via console and go to the adress of the server that will be displayed afterwards (usually it is 192.0.0.1).
# A list of files included 
        run.py
        auction\
                __init.py__
                authorisation.py
                bidding.py
                db.py
                forms.py
                imports.py
                page_render.py
                routes.py
                        templates\
                                auction.html
                                base.html
                                home.html
                                login.html
                                my_bids.html
                                my_office.html
                                register.html
                                        includes\
                                                delete_account_modal.html
                                                items_modals.html
                                                sell_item_modal.html
                                                VIP_functions.html
                        documentaion\
                                authorisation.html
                                bidding.html
                                db.html
                                forms.html
                                imports.html
                                index.html
                                page_render.html
                                routes.html
                                run.html
