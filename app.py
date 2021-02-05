from flask import (Flask, render_template, jsonify, request, flash, redirect, session)
import mysql.connector
import os

#create the app
app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    #return "hello world"


@app.route('/users', methods=['GET'])
def users():
    #return "this is the user"

    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="points_tracker")
	
    mycursor = cnx.cursor()
    mycursor.execute("SELECT * From points_tracker.users ORDER BY LastName")
    myresult = mycursor.fetchall()

    userList = []
    content = {}

    for x in myresult:
        print(x)
        content = {'PersonID': x[0], 'FirstName': x[1], 'LastName': x[2], 'Picture': x[3]}
        userList.append(content)
        content = {}
    cnx.close()

    return jsonify(userList)


@app.route('/userpoints', methods=['GET'])
def userpoints():

    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="points_tracker")
	
    mycursor = cnx.cursor()
    mycursor.execute("SELECT * From points_tracker.user_points ORDER BY PersonID")
    myresult = mycursor.fetchall()

    userPointsList = []
    content = {}

    for x in myresult:
        print(x)
        content = {'PersonID': x[0], 'MinTotal': x[1], 'WorkPoints': x[2], 'SchoolPoints': x[3], 'TotalPoints': x[4]}
        userPointsList.append(content)
        content = {}
    cnx.close()

    return jsonify(userPointsList)


@app.route('/totaluserpoints/<personID>', methods=['GET'])
def totaluserpoints(personID):

    cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="points_tracker")
	
    mycursor = cnx.cursor()
    #theSelector = "SELECT * From points_tracker.user_points WHERE PersonID =" + personID
    theSelector = "SELECT PersonID, SUM(MinTotal), SUM(WorkPoints), SUM(SchoolPoints), SUM(TotalPoints) FROM points_tracker.user_points WHERE PersonID =" + personID
    mycursor.execute(theSelector)
    myresult = mycursor.fetchall()

    userTotalPointsList = []
    content = {}

    for x in myresult:
        print(x)
        #content = {'PersonID': x[0], 'TheDate': x[1], 'MinTotal': x[2], 'WorkPoints': x[3], 'SchoolPoints': x[4], 'TotalPoints': x[5]}
        content = {'PersonID': x[0], 'MinTotal': int(x[1]), 'WorkPointsTotal': int(x[2]), 'SchoolPointsTotal': int(x[3]), 'TotalPointsTotal': int(x[4])}
        userTotalPointsList.append(content)
        content = {}
    cnx.close()

    return jsonify(userTotalPointsList)
    



if __name__=="__main__":
    app.run()