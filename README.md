# car.t
used car resale with ML!

#Build

1. create a new environment

   run the following command:

>$pip install -r requirements.txt

2. Create new sqlLite Database

   Open the cmd in the main project directory and open the python command line interpreter by typing
   >$python

   Then type the following and call exit()
   >$from flaskblog import db
   >$db.create_all()
   >$exit()

3. To deploy the server run

   >python run.py

4. Basic use of the website
   Use Login to create a new account [Buyer/Seller]
   Buyers can view cars, search and send notifications to Sellers
   Sellers can add, delete and modify listings as well as view notifications from Buyers
#Model Creation Information

The model_creation directory holds all the work that lead to model creation. It holds the data visualization used to create the numeric form of the data. Since this was initially part of a competition I am unsure if I can release the original data.

The numeric version that that was created is present. The grid search used to create the final model that can be found in car_grid_search.ipynb.
