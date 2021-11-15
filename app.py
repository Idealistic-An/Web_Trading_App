# importing Flask and other modules  
from os import terminal_size
from re import X
from typing import List, NoReturn
from flask.helpers import url_for
import requests
import json
from flask import Flask, request, render_template
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib import rcParams  

import mysql.connector
from werkzeug.utils import redirect
 
from signin.signin import login
from signin.signup import valid
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sql@123#",
  database="stocks"
)

app = Flask(__name__) 


"""
URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete"
querystring = {"q":"tesla","region":"US"}
headers = {'x-rapidapi-key':"d7a08a194bmshe740dbe49b19340p19bcadjsn09656858a655",'x-rapidapi-host':"apidojo-yahoo-finance-v1.p.rapidapi.com"} 
response = requests.get(URL, headers=headers, params=querystring) 
status_code = response.status_code
print(status_code) 
"""
#RAPIDAPI_KEY = "66deec0ce2msh8fa540303464a2cp19719fjsn420ed24dad4b" #2nd acc
RAPIDAPI_KEY    = "3b17580dafmsh7f4f720f9633022p1390f2jsne35be8f4c1cf" #mine
#RAPIDAPI_KEY = "a0d2fdbc8fmsha5fcc65f88fcaf5p18caf8jsn6463b5483650"  #anant
 
RAPIDAPI_HOST = "yh-finance.p.rapidapi.com"

inputdata = {} 
USERNAME = ""
CURRENT_STOCK = "" 
MAINNEWS = []
BOOKMARKS = []
KEY = "MrXiipKYDYm_5mspomSAQUAaU06Sbb3ffhj7z9k1HMY="
KEY = KEY.encode()
@app.route("/")
def default():
  global MAINNEWS  
  url = "https://yh-finance.p.rapidapi.com/news/v2/list"
  querystring = {"region":"US","snippetCount":"28"}

  headers = {
    'x-rapidapi-host': RAPIDAPI_HOST,
    'x-rapidapi-key': RAPIDAPI_KEY
    }

  response = requests.request("POST", url, headers=headers, params=querystring)
  homeNews = response.json()
  MAINNEWS = homeNews["data"]["main"]["stream"]
  #print(n1[0]["content"]["title"])
  print(len(BOOKMARKS))
  if len(BOOKMARKS)>0:
   print(BOOKMARKS[0])
  if len(BOOKMARKS) == 0:
    return render_template("index.html",username = USERNAME,homeNews = MAINNEWS) 
  return render_template("index.html",username = USERNAME,homeNews = MAINNEWS,bookmarks = BOOKMARKS)   

 #LOGIN

@app.route("/login/user",methods = ["GET", "POST"])
def checkuser():
  print("before") 
  usern = request.form.get("user")
  print(usern)
  password = request.form.get("password")
  print("adsasd")
  
  if(login(usern,password)):
    global USERNAME
    global homeNews
    global BOOKMARKS
    USERNAME = usern
    BOOKMARKS = []
    # calling bmks
    mycursor = mydb.cursor() 
    current_bookmarks = f"SELECT bookmarks from Userregst WHERE Username = '{USERNAME}';" 
    mycursor.execute(current_bookmarks) 
    fetch_bms = mycursor.fetchall()
    print(fetch_bms)
    bms = fetch_bms[0][0]
    if(len(BOOKMARKS)>0):
     BOOKMARKS = toList(bms)
     if BOOKMARKS[0] == '':
      return render_template("index.html",username = USERNAME, homeNews = MAINNEWS)
    else:   
     print(BOOKMARKS)
     return render_template("index.html",username = USERNAME,bookmarks = BOOKMARKS,homeNews = MAINNEWS)  
  else:
    USERNAME = "check your login details"
    return render_template("index.html",username="check your login details",loginfail=True,homeNews = MAINNEWS)
@app.route("/login")
def renderlogin():
 return  render_template("Loginpage.html")
@app.route("/logout")
def logout():
  global USERNAME
  USERNAME = ""
  return render_template("index.html",homeNews = MAINNEWS) 

#SIGNIN

@app.route("/signup/user",methods = ["GET", "POST"])
def reguser():
  print("before") 
  usern = request.form.get("user")
  print(usern)
  password = request.form.get("password")
  print(password)
  mail_id = request.form.get("email")
  print(mail_id)
  phoneno = request.form.get("phone")
  print(phoneno)
  return valid(usern,mail_id,password,phoneno) 
@app.route("/signup")
def rendersignup():
  return render_template("Validation.html") 

@app.route("/search", methods =["GET", "POST"]) # route for searching stocks
def display():
    if request.method == "POST":  
           searchItem = request.form.get("searchfor") 
           if len(searchItem) > 3: 
             searchItem = request.form.get("searchfor") 
             mycursor = mydb.cursor()
             sql = f"SELECT symbols FROM stocknames WHERE sNames like '%{searchItem}%';"  
             print(sql)
           
             mycursor.execute(sql)

             myresult = mycursor.fetchall()
             symbols_list = []
             for x in myresult:
               symbols_list.extend(x) 
               #print(symbols_list)
             return render_template("index.html",symbols_list = symbols_list,username = USERNAME) 

           else: 
                   return render_template("index.html",username = USERNAME)

@app.route("/api/<symbol>")  # route for fetching stock data   
def fetchStockData(symbol):   
    #print(symbol)
    URL = "https://yh-finance.p.rapidapi.com/market/get-charts"  
    querystring = {"symbol":f"{symbol}","interval":"1d","range":"1mo","region":"US","comparisons":"^GDAXI,^FCHI"}

    headers={
      "X-RapidAPI-Host": RAPIDAPI_HOST,
      "X-RapidAPI-Key": RAPIDAPI_KEY,
      "Content-Type": "application/json"
    }  
    response = requests.get(URL, headers=headers, params=querystring)
    stockData = response.json()

    #print(stockData) 
       

    inputdata["Timestamp"] = parseTimestamp(stockData)

    inputdata["Values"] = parseValues(stockData)

    inputdata["Events"] = attachEvents(stockData)
    #print(inputdata)
    df = pd.DataFrame(inputdata)  # creating data frame using pandas
    #print(df)
    sns.set(style="darkgrid")
    rcParams['figure.figsize'] = 13,5
    rcParams['figure.subplot.bottom'] = 0.2

      
    ax = sns.lineplot(x="Timestamp", y="Values", hue="Events",dashes=False, markers=True, 
    data=df, sort=False)
    ax.set_title('Symbol: ' + symbol)
      
    plt.xticks(
          rotation=45, 
          horizontalalignment='right',
          fontweight='light',
          fontsize='xx-small'  
      ) 
    #plt.show() 
   
    
    # print(json.dumps(response.json()))  
   
    return fetchStockDetails(stockData)


     
def parseTimestamp(inputdata):
  timestamplist = []

  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"]) # for opening figures
  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"]) # for closing figures

  calendertime = []

  for ts in timestamplist:
     dt = datetime.fromtimestamp(ts)
     calendertime.append(dt.strftime("%m/%d/%Y"))
  return calendertime      # returns calendertime for each timestamp

#for extracting the opening and closing values
def parseValues(inputdata):

  valueList = []
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])
 #print(len(valueList))
  return valueList
    
# for defining the opening and closing values

def attachEvents(inputdata):

  eventList = []

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventList.append("open")	

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventList.append("close")
  #print(len(eventList))
  return eventList
  #update Userregst set bookmarks = '[acc,asda,asda]' where Username = 'anant';

@app.route("/delete/<symbol>", methods =["GET", "POST"])
def deletebookmark(symbol):
    global BOOKMARKS
    mycursor = mydb.cursor()  
    current_bookmarks = f"SELECT bookmarks from Userregst WHERE Username = '{USERNAME}';" 
    mycursor.execute(current_bookmarks) 
    fetch_bms = mycursor.fetchall()
    bms = fetch_bms[0][0]
    BOOKMARKS = toList(bms)  
    BOOKMARKS.remove(symbol)
    bms_string = toString(BOOKMARKS)
    pushBookmark = f"update Userregst set bookmarks = '{bms_string}' WHERE Username = '{USERNAME}';"
    print(pushBookmark)
    mycursor.execute(pushBookmark)  
    mydb.commit()
    return render_template("index.html",bookmarks = BOOKMARKS,homeNews = MAINNEWS,username = USERNAME)    
     
@app.route("/bookmarkit", methods =["GET", "POST"])
def bookmark():   
    global BOOKMARKS  
    mycursor = mydb.cursor()  
    current_bookmarks = f"SELECT bookmarks from Userregst WHERE Username = '{USERNAME}';" 
    mycursor.execute(current_bookmarks) 
    fetch_bms = mycursor.fetchall()
    bms = fetch_bms[0][0] 
    print(type(bms)) 
    if bms == None:
       if(len(BOOKMARKS)>0): 
          if BOOKMARKS[0] == '':
             BOOKMARKS.pop(0)
       first = f"update Userregst set bookmarks = '{CURRENT_STOCK}' WHERE Username = '{USERNAME}';"
       mycursor.execute(first)
       BOOKMARKS.append(CURRENT_STOCK) 
       mydb.commit()
       print("db")
    else:  
     if(CURRENT_STOCK in BOOKMARKS):
       return "Noreturn"
     else:
      if(len(BOOKMARKS)>0): 
          if BOOKMARKS[0] == '':
             BOOKMARKS.pop(0)
      BOOKMARKS.append(CURRENT_STOCK)
      print(BOOKMARKS)
      bms_string = toString(BOOKMARKS)
      print(bms_string)
      pushBookmark = f"update Userregst set bookmarks = '{bms_string}' WHERE Username = '{USERNAME}';"
      print(pushBookmark)
      mycursor.execute(pushBookmark)  
      mydb.commit()
      print("commitrun")
    #elif(fetch_bms.index(CURRENT_STOCK)):
     #    return "NULL"     
    return "NoReturn"
# route for fetching news and quotes from fetchquotes() 
def toList(string):
    li = list(string.split(" "))
    return li
def toString(list):
    stg = ' '.join([str(elem) for elem in list])
    return stg
def fetchStockDetails(stockData): 
    symbol = stockData["chart"]["result"][0]["meta"]["symbol"]
    global CURRENT_STOCK
    CURRENT_STOCK = symbol
    stockValue = stockData["chart"]["result"][0]["meta"]["regularMarketPrice"]
    url = "https://yh-finance.p.rapidapi.com/auto-complete"
    
    querystring = {"q":f"{symbol}","region":"US"}

    headers = {
    'x-rapidapi-host': RAPIDAPI_HOST,
    'x-rapidapi-key':  RAPIDAPI_KEY
    } 

    response = requests.request("GET", url, headers=headers, params=querystring) 
    quotesData = fetchQuotes(symbol) 
    recs = fetchRecs(symbol)
    print(recs["finance"]["result"][0]["quotes"][0]["symbol"])
    #newslen = len(newsdata["news"])  
    return render_template("index.html",news=response.json(),quotes=quotesData,stockValue=stockValue,symbol=symbol,recs=recs,username = USERNAME)


def fetchQuotes(symbol): # fetching quotes   
    url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes"

    querystring = {"region":"US","symbols":f"{symbol}"}

    headers = {
    'x-rapidapi-host': RAPIDAPI_HOST,
    'x-rapidapi-key':  RAPIDAPI_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #print(json.dumps(response.json())) 
   
    return response.json()

def fetchRecs(symbol):
  import requests

  url = "https://yh-finance.p.rapidapi.com/stock/v2/get-recommendations"

  querystring = {"symbol":f"{symbol}"}

  headers = {
    'x-rapidapi-host': "yh-finance.p.rapidapi.com",
    'x-rapidapi-key': RAPIDAPI_KEY
    }

  response = requests.request("GET", url, headers=headers, params=querystring)

  print(json.dumps(response.json()))
  return response.json()     
if __name__=='__main__':
  app.run()