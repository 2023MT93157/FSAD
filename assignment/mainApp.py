from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MySQL@2020'
app.config['MYSQL_DB'] = 'BookBuddy'

mysql = MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ssdulam@gmail.com'
app.config['MAIL_PASSWORD'] = 'wjpx jzoc zfft uuom'

mail = Mail(app)

username = ''
result = 0

@app.route('/')
def index():
    return render_template('homePage.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/saveDetails', methods=['POST'])
def savedetails():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        command = mysql.connection.cursor()
        query = f"insert into users values('{firstname}','{lastname}', '{email}', '{password}')"
        command.execute(query)
        command.connection.commit()
        command.close()
        return render_template('successRegistration.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        command = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = """select * from users where Email='{}' and Passcode='{}'""".format(username,password)
        command.execute(query)
        result = command.fetchone()
        command.close()
        if result:
            return render_template('successLogin.html')
        else:
            return render_template('invalidLogin.html')

@app.route('/buyBook', methods=['POST', 'GET'])
def buyBook():
    command = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "select * from books"
    command.execute(query)
    records = command.fetchall()
    command.close()
    return render_template('buyBook.html', data = records)

@app.route('/sellBook')
def sellBook():
        return render_template('sellBook.html')

@app.route('/saveBook', methods=['POST'])
def saveBook():
        if request.method == 'POST':
            BookName = request.form['BookName']
            Author = request.form['Author']
            SellerName = request.form['SellerName']
            SellerEmail = request.form['SellerEmail']
            command = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = f"insert into books values ('{BookName}', '{Author}', '{SellerName}', '{SellerEmail}')"
            command.execute(query)
            command.connection.commit()
            command.close()
            return render_template('bookAddedToSell.html'), {"Refresh": "5; url=http://localhost:5000/main"}

@app.route('/main')
def main():
     return render_template('successLogin.html')

@app.route('/sendEmail', methods = ['POST'])
def sendEmail():
    data = request.get_json()
    rowData = data.get('rowData', [])
    BookName = rowData[0]
    Author = rowData[1]
    SellerName = rowData[2]
    SellerEmail = rowData[3]
    recipient = SellerEmail
    sender = 'ssdulam@gmail.com'
    subject = f'BookBuddy! {BookName} Request'
    body = f'Hello {SellerName}, I got your contact from BookBuddy! I would like to buy {BookName} by {Author}!'
    message = Message(subject=subject, sender=sender, recipients=[recipient])
    message.body = body
    mail.send(message)

    recipient = 'ssdulam@gmail.com'
    subject = f'BookBuddy! {BookName} Request Sent to Seller'
    body = f'Hello, Your request for {BookName} by {Author} sent to {SellerName} successfully.'
    message = Message(subject=subject, sender=sender, recipients=[recipient])
    message.body = body
    mail.send(message)

    return render_template('emailSuccess.html'), {"Refresh": "5; url=http://localhost:5000/main"}

app.run(debug = True)