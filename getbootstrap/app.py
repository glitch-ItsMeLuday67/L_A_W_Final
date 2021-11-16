from flask import Flask, session, render_template, request, redirect, url_for
from datetime import datetime
from database import connect_db, get_db, g
import sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = "encrypted_data"

@app.route('/home', methods=['GET', 'POST'])
def home():
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/biggest_number")
def biggest_number():
    return render_template("biggest_number.html")

@app.route("/validate_biggest")
def validate_biggest():
    user = request.form.get("user")
    user1 = request.form.get("user1")
    user2 = request.form.get("user2")
    result = ""
    if user > user1 and user > user2:
        result =  str(user) + " is the biggest number"
    elif user2 > user and user2 > user1:
        result =  str(user2) + " is the biggest number"
    elif user1 > user and user1 > user2:
        result =  str(user1) + " is the biggest number"
    elif user == user1:
        if user2 == user1:
            result =  "All numbers are same"
        if user2 < user:
            result =  str(user) + " and " + str(user1) + " are bigger."
    elif user1 == user2:
        if user < user1:
            result =  str(user1) + " and " + str(user2) + " are bigger."
    elif user == user2:
        if user1 < user2:
            result =  str(user) + " and " + str(user2) + " are bigger."
    return render_template("biggest_number.html",result = result)

@app.route("/bmi",methods=["GET","POST"])
def bmi():
    if request.method == "GET":
        return render_template("bmi.html")
    weight = request.form.get("weight",type = float)
    height = request.form.get("height", type = float)
    age = request.form.get("age", type = float)
    gender = request.form.get("gender")
    resultBMI = ""
    resultFAT = ""
    resultH2O = ""
    resultHOW = ""
    totalResult = ""
    BMI = weight / (height/100) ** 2
    resultBMI = "Your BMI is %.2f"% BMI
    fat = (1.20 * BMI) + (0.23 * age) - 16.2
    resultFAT = "Fat percentage in your body is %.2f" % fat
    if gender == "f":
        TBW = -2.097 + 0.1069 * height + 0.2466 * weight
        resultH2O = "Your total body water is %.2f"% TBW
    if gender == "m":
        TBW1 =  2.447 - 0.09156 * age + 0.1074 * height + 0.3362 * weight
        resultH2O = "Your total body water is %.2f"% TBW1
    if BMI <= 18.4:
        resultHOW = "You are underweight."
    elif BMI <= 24.9:
        resultHOW = "You are healthy."
    elif BMI <= 29.9:
        resultHOW = "You are over weight."
    elif BMI <= 34.9:
        resultHOW = "You are severely over weight."
    elif BMI <= 39.9:
        resultHOW = "You are obese."
    else:
        resultHOW = "You are severely obese."
    totalResult = resultBMI + ". " + resultFAT + ". " + resultH2O + ". " + resultHOW
    return render_template("bmi.html", totalResult = totalResult)

@app.route('/leap_year', methods=['GET', 'POST'])
def leap_year():
    if request.method == "GET":
        return render_template("leap_year.html")
    year = request.form.get("year", type = int)
    result = ""
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                 result = str(year) + " is a leap year"
            else:
                result = str(year) + " is not a leap year"     
        else: 
            result = str(year) + " is a leap year"
    else:
        result = str(year) + " is not a leap year"

    return render_template("leap_year.html", result = result) 

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == "GET":
        return render_template("encrypt_decrypt.html")
    string = request.form.get("string")
    encrypt = ""
    for i in string:
        eye = ord(i) + 5
        eye1 = chr(eye)
        encrypt += eye1

    return render_template("encrypt_decrypt.html", encrypt = encrypt)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == "GET":
        return render_template("encrypt_decrypt.html")
    string = request.form.get("string1")
    decrypt = ""
    for i in string:
        eye = ord(i) - 5
        eye1 = chr(eye)
        decrypt += eye1

    return render_template("encrypt_decrypt.html", decrypt = decrypt)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form.get("username")
    session["username"] = username
    password = request.form.get("password")
    session["password"] = password
    confirmpass = request.form.get("cpassword")
    email = request.form.get("email")
    session["email"] = email
    message = ""

    conn = sqlite3.connect('getbootstrap/users.db')
    cur = conn.cursor()
    usernames = cur.execute("SELECT Username FROM registration_db").fetchall()
    print(usernames)
    users = []
    for i in usernames:
        users.append(i[0])
    print(users)
    if username in users:
        error = "Username already exists."
        return render_template("register.html", error = error)

    if confirmpass != password:
        message = "Password mismatch."
        return render_template("register.html", message = message)
    
    conn = sqlite3.connect('getbootstrap/users.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO registration_db(
        Username, Password, Email) VALUES(?,?,?)''',(username, password, email))
    print("Values Inserted")
    records1 = cur.execute("SELECT * FROM registration_db;").fetchall()
    session["records"] = records1
    print(records1)
    conn.commit()
    conn.close()

    return render_template("login.html", records = records1)
        
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method=="GET":
        return render_template("login.html")

    user_admin = "admin"
    pass_admin = "lukeanand123$"
    username = request.form.get("username")
    password = request.form.get("password")
    message_login = ""
    db_username = session.get("username", "Incorrect username or password")
    db_password = session.get("password", "Incorrect username or password")
    role = request.form.get("flexRadioDefault")

    if role == "admin":
        if username == user_admin:
            if password == pass_admin:
                message_login = "You have logged in as an admin"
                session["admin"] = True
                session["authenticated"] = True
                return render_template("index.html", message_login = message_login)
            message_login = "Username or password is incorrect."
            return render_template("login.html", message_login = message_login)
        message_login = "Username or password is incorrect."
        return render_template("login.html", message_login = message_login)
    
    if username == db_username:
        if password == db_password:
            message_login = "Successfully Logged In"
            session["authenticated"] = True
            return render_template("index.html", message_login = message_login)
        message_login = "Incorrect username or password"
        return render_template("login.html", message_login = message_login)
    message_login = "Incorrect username or password"
    return render_template("login.html", message_login = message_login)

@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = sqlite3.connect("getbootstrap/users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM registration_db")
    records = cur.fetchall()
    print(records)
    conn.commit()
    conn.close()
    if session.get("admin"):
        return render_template("user_table.html", records = records)
    else:
        return render_template("404pagenotfound.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    message = "You have successfully logged out"
    return render_template("index.html", message_login = message)

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("test.html")


#**FOOD TRACKER APP⬇️**#


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/foodtracker/', methods=['POST', 'GET'])
def foodtracker():
    db = get_db()

    if request.method == 'POST':
        date = request.form['date'] #assuming the date is in YYYY-MM-DD format
        print(date)
        food_name=request.form['food-select']
        dt = datetime.strptime(date, '%Y-%m-%d')
        database_date = datetime.strftime(dt, '%Y%m%d')
        db.execute('insert into log_date (entry_date) values (?)', [database_date])
        db.commit()

        cur=db.execute('select id from log_date where entry_date=(?)',[database_date])
        record=cur.fetchone()
        db.execute('insert into food_date (food_id, log_date_id) values (?, ?)', [food_name,record[0]])
        db.commit()

    cur = db.execute('''select log_date.entry_date, sum(food.protein) as protein, sum(food.carbohydrates) as carbohydrates, sum(food.fat) as fat, sum(food.calories) as calories 
                        from log_date 
                        join food_date on food_date.log_date_id = log_date.id 
                        join food on food.id = food_date.food_id 
                        group by log_date.id order by log_date.entry_date desc''')

    results = cur.fetchall()

    date_results = []

    for i in results:
        single_date = {}

        single_date['entry_date'] = i['entry_date']
        single_date['protein'] = i['protein']
        single_date['carbohydrates'] = i['carbohydrates']
        single_date['fat'] = i['fat']
        single_date['calories'] = i['calories']

        d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
        single_date['pretty_date'] = datetime.strftime(d, '%B %d, %Y')

        date_results.append(single_date)

    food_cur = db.execute('select id, name from food')
    food_results = food_cur.fetchall()

    return render_template('foodtracker_home.html', results=date_results,food_master_list=food_results)

@app.route('/foodtracker_view/<date>', methods=['GET', 'POST']) #date is going to be 20170520
def foodtracker_view(date):
    db = get_db()
    message=''

    cur = db.execute('select id, entry_date from log_date where entry_date = ?', [date])
    date_result = cur.fetchone()
    
    if request.method == 'POST':
        print(request.form['food-select'], date_result['id'])

        cur1=db.execute('select * from food_date where food_id=(?) and log_date_id = (?)',[request.form['food-select'], date_result['id']])
        print(cur1.rowcount)
        print(cur1.arraysize)
        record=cur1.fetchone()
        print(record)

        if record==None:
            db.execute('insert into food_date (food_id, log_date_id) values (?, ?)', [request.form['food-select'], date_result['id']])
            db.commit()
        else:
            message='Record Already Exists'

    d = datetime.strptime(str(date_result['entry_date']), '%Y%m%d')
    pretty_date = datetime.strftime(d, '%B %d, %Y')

    food_cur = db.execute('select id, name from food')
    food_results = food_cur.fetchall()

    log_cur = db.execute('''select food.name, food.protein, food.carbohydrates, food.fat, food.calories 
                            from log_date 
                            join food_date on food_date.log_date_id = log_date.id 
                            join food on food.id = food_date.food_id 
                            where log_date.entry_date = ?''', [date])

    log_results = log_cur.fetchall()

    totals = {}
    totals['protein'] = 0
    totals['carbohydrates'] = 0
    totals['fat'] = 0
    totals['calories'] = 0

    for food in log_results:
        totals['protein'] += food['protein']
        totals['carbohydrates'] += food['carbohydrates']
        totals['fat'] += food['fat']
        totals['calories'] += food['calories']

    return render_template('foodtracker_day.html', entry_date=date_result['entry_date'], pretty_date=pretty_date, \
                           food_results=food_results, log_results=log_results, totals=totals,message=message)

@app.route('/foodtracker_food', methods=['GET', 'POST'])
def foodtracker_food():
    db = get_db()

    if request.method == 'POST':
        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])

        calories = protein * 4 + carbohydrates * 4 + fat * 9
     
        db.execute('insert into food (name, protein, carbohydrates, fat, calories) values (?, ?, ?, ?, ?)', \
            [name, protein, carbohydrates, fat, calories])
        db.commit()

    cur = db.execute('select name, protein, carbohydrates, fat, calories from food')
    results = cur.fetchall()

    return render_template('foodtracker_add_food.html', results=results)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404pagenotfound.html"), 404


if __name__ == "__main__":
    app.run(debug = True)