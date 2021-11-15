# importing Flask and other modules
from flask.templating import render_template
import mysql.connector 
from cryptography.fernet import Fernet
# Flask constructor 
  
# A decorator used to tell the application
# which URL is associated function
KEY = "MrXiipKYDYm_5mspomSAQUAaU06Sbb3ffhj7z9k1HMY="
KEY = KEY.encode()
f = Fernet(KEY)
def valid(usern,mail_id,password,phoneno):
    #if request.method == "POST":
       # getting input with name = fname in HTML form
       #usern = request.form.get("user")
       #print(usern)
       # getting input with name = lname in HTML form 
       #mail_id = request.form.get("email")
       #getting mail id of user
      # password = request.form.get("pswrd")
       #getting password of account
      # phoneno = request.form.get("phone")
       #getting phone number
       print("Your regst is "+usern + mail_id + password + phoneno)
       
       #now connecting to database
       mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sql@123#",
  database="stocks"
)
       mycursor = mydb.cursor()
       #mycursor.execute("CREATE TABLE Userregst (Username VARCHAR(255), mail_id VARCHAR(255), pswrd VARCHAR(255), phoneno VARCHAR(100),PRIMARY KEY (`mail_id`))")
       #We have a database created, so we now insert data into columns using Insert into command 
       sql = "INSERT INTO Userregst (Username,mail_id,pswrd,phoneno ) VALUES (%s, %s, %s, %s)" 
       hashed = f.encrypt(password.encode())
       print(hashed)
       val = (usern, mail_id,hashed,phoneno)
       mycursor.execute(sql, val)
       mydb.commit()
       #We stored the data as list and inserted in a go
       #Now lets check if the user entered all data if there's anything missing we need to throw a message stating data is missed
       if all([usern, mail_id, password,phoneno]):
           print(mycursor.rowcount, "record inserted.")
       else:
           print("u missed data")
       #Now we check if all data is inserted or not
       print(mycursor.rowcount, "record inserted.")
       return render_template("index.html") 