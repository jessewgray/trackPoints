from flask import (Flask, render_template, jsonify, request, flash, redirect, session)
import mysql.connector
import os
from flask_cors import CORS


#create the app
app = Flask(__name__, template_folder="templates")
CORS(app)

app.config["IMAGE_UPLOADS"] = "./static/pics"


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
    #return "hello world"


# adding users to database with python
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    return render_template('newUser.html', methods=['GET', 'POST'])
    #return "working"

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():

    if request.method == "POST":
        if request.files:
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            image = request.files["image"]

            userList = []
            params = {
                "first_name": firstName,
                "last_name": lastName,
                "image": image.filename
            }

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            print(image.filename + firstName)

            cnx = mysql.connector.connect(user="root", password="snowboarding", host="127.0.0.1", database="points_tracker")
            mycursor = cnx.cursor()

            insertStatement = ('INSERT INTO points_tracker.users (FirstName, LastName, Picture) VALUES (%s, %s, %s)')
            insertData = (firstName, lastName, image.filename)
            mycursor.execute(insertStatement, insertData)
            cnx.commit()

            userList.append(params)
            return jsonify(userList)



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