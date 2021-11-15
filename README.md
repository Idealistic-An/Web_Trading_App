# Web_Trading_App
Creating a webtrading app similar to yahoo finance with basic functionalities


************Creation of a Web Trading App that allows following functions**********

1. User creation
2. Searching of stock data
3. Displaying stocks
4. Displaying graphs of stocks
5. Displaying recommendations
6. Supplying news regading stocks
7. Showing latest news
8. Selection of bookmarks
9. Deletion of bookmarks

***********PREREQUISITS************

1. python 3
2. mysql
3. jinja
4. html/css/js
5. cryptography.fernet for encryption of user data
6. matplotlib for graphs
7. we use flask to connect backend and frontend
8. The Operating System to do it was Windows 10 & 11

**************PROCESS**************

------SEARCH BAR------

First, we create a basic search bar using html forms and linked with app.py that has search funstion using flask.
This py file extracts information  from the form and sends to py file and shows some suggestions as per the keywords entered

------SEARCH DETAILS-----


The Search details show the stock searched and provides a redirect link when clicked on stock leads to news details about that stock

------SIGNUP-----

Next we see Signup that is user creation, here we created a html file called Validation.html and use javascript(js) for validation
Then we link this html file with SignUp.py and mysql database and store the data extracting from html form into database by flask
Here we also use encryption on passwords while storing data like passwords
The user mail id was made as primary key so that a single mail id can have only 1 account

------SIGN IN-----------


Next we have Signin.py for this we created a basic login page  with html and extract information via flask and then validate it with the one in database.
If it matches we login else it shows a message saying login credentials are wrong.

--------BOOKMARKS-------


Next we have a function bookmarks in app.py this will show a button on a stock when we search about it as add to bookmarks clicking that we get an additional entry as bookmarks for a user

-------DELETION OF BOOKMARKS-------


There are cases when a user accidentaly hits a bookmarks button so to avoid this we have created a button called delete bookmarks (x)
Upon calling this function we can clear this column from the user database

------News-----


When a websurfer first opens our webpage we provide him with latest headlines of some latest news regarding stockmarket 

  
