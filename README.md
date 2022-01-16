# Auction website written using flask
# Project Overview 
This is a simple flask project that was created in the proccess of learning python and flask in particular. It has basic functional of an auction website such as: registration and login of the user, biding system, selling system, user balance, account deletion and some other smaller functions.
# Configuration instructions 
Before you start using it you need to install and configure MySQL on your machine or just connect it to existing database. Then in file auction\db.py change connection data in class ConnectToDatabase to yours. After that import sql tables from my_sql_tables directory to your database. And you are pretty much ready to go.
# Installation instructions 
Download, configure and be ready to run website.
# Operating instructions
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
# Copyright and licensing information
In order to let others know what they can and cannot do with your code, it is important to include a software license in your project. If you opt out of using a license then the default copyright laws will apply and you will retain all rights to your source code and no one may reproduce, distribute, or create derivative works from your work. Hence the reason licenses are critical and highly recommended for open source projects.
# Contact information for the distributor or programmer
Name, email, social media links, and any other helpful ways of getting in contact with you or members of your team.
# Known bugs 
This is the perfect place to put tickets of known issues that you are actively working on or have on backlog. Speaking of backlog, if your project is open source, this is will allow potential contributors an opportunity to review incomplete features.
# Troubleshooting 
In this section you will be able to highlight how your users can become troubleshooting masters for common issues encountered on your project.
# Credits and acknowledgments 
Who were the contributing authors on the project, whose code did you reference, which tutorials did you watch that help you bring this project to fruition? Sharing is caring and all praises are due for those that have helped no matter how small the contribution.
# A changelog (usually for programmers) 
A changelog is a chronological list of all notable changes made to a project such as: records of changes such as bug fixes, new features, improvements, new frameworks or libraries used, and etc.
# A news section (usually for users) 
If your project is live and in production and you are receiving feedback from users, this is a great place to let them know, “Hey, we hear you, we appreciate you, and because of your feedback here are the most recent changes, updates, and new features made.”
