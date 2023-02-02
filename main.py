# This is a sample Python script.



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


from flask import Flask,render_template,request,session,url_for,redirect
from flask_mysqldb import MySQL
import MySQLdb

app=Flask(__name__)
app.config['SECRET_KEY']='-RFins9nLKTN-FHawdrPAQ'
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="Gowri"
app.config["MYSQL_PASSWORD"]="2001"
app.config["MYSQL_DB"]="notes"
#app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/")
def sample():
    return render_template("index.html")

@app.after_request    #after session pop when we click back python flask
def after_request(response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response



@app.route("/register", methods=['POST','GET'])
def register():
    if request.method=="POST":
        cursor = mysql.connection.cursor()
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        note=request.form['note']
        try:
            cursor.execute("INSERT INTO user1 (username,email,password,note) VALUES (%s,%s,%s,%s)", (username, email, password, note))
            record = cursor.fetchone()
            mysql.connection.commit()
            print("db executed")
            return redirect(url_for('login'))
        except MySQLdb.IntegrityError:
            newmsg1="You already have an account."
            newmsg2="Go to login page or Use another E-Mail and User Name."
            return render_template("register.html",msg1=newmsg1,msg2=newmsg2)
    return render_template("register.html")


@app.route("/login",methods=['POST','GET'])
def login():
    global rec
    msg=""
    if request.method=='POST':
        print("post executed")
        cursor = mysql.connection.cursor();
        username=request.form['username']
        password=request.form['password']
        cursor.execute("SELECT * FROM user1 WHERE username=%s AND password= '{}' ",(username,password))
        record=cursor.fetchone()
        print("db executed")
        if record:
            session['loggedin']=True
            session['username']=record[1]
            session['id']=record[0]
            print("username")
            print(session['username'])
            print(session['id'])
            msg="logged in successfully"
            return redirect(url_for('home'))
        else:
            msg="Incorrect username or password"
    return render_template("index.html",msg=msg)


@app.route("/home" , methods=["POST","GET"])
def home():
    try:
        if session['loggedin']==True:
            cursor = mysql.connection.cursor();
            cursor.execute("SELECT * FROM user1 WHERE username=%s", (session['username'],))
            rec = cursor.fetchall()
            if rec:
                print(rec)
                note = rec[0][4]
                id=rec[0][0]
                print(id)
            return render_template('home.html',username=session['username'],rec=note,id=id)
    except KeyError:
        return redirect(url_for('login'))

@app.route("/edit/<string:id>",methods=['GET','POST'])
def edit(id):
    try:
        if session['loggedin'] == True:
            cursor = mysql.connection.cursor();
            cursor.execute("SELECT * FROM user1 WHERE id=%s", (id,))
            rec = cursor.fetchone()
            print(rec)
            print(rec[4])
            noteForEdit=rec[4]
            if request.method=="POST":
                newNote=request.form['changed']
                cursor = mysql.connection.cursor();
                cursor.execute("UPDATE user1 SET note=%s WHERE id=%s", (newNote,id,))
                record = cursor.fetchone()
                mysql.connection.commit()
                return redirect(url_for('home'))
    except KeyError:
        return redirect(url_for('login'))


    return render_template("edit.html", nfe=noteForEdit)




@app.route("/logout", methods=['POST','GET'])
def logout():
    session.pop('loggedin',None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for("sample"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
