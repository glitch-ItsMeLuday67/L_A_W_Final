from flask import Flask, render_template, request, session
from flask_mail import Mail
import smtplib, ssl
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

app.config["SECRET_KEY"] = "asdasdasdad"
app.config["DEBUG"] = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

sender_email = "hello.luke.21.12@gmail.com"
sender_password = "Luke123$testinG"

mail = Mail(app)

@app.route("/vcode", methods = ["GET", "POST"])
def vcode():
    recipient_email = "emark4497@gmail.com"
    recipient_name = "Luke"
    subject = "verification_code"
    verification_code = str(random.randrange(100000, 999999))
    session["code"] = verification_code
    message = "Hi %s your verification code is %s"%(recipient_name, verification_code)
    #try with string format methods after class#
    sendemail(subject, recipient_email, message)
    return render_template("vcode.html", email = recipient_email)

def sendemail(subject, recipient_email, message):
    email_message = MIMEMultipart("alternative")
    email_message["Subject"] = subject
    email_message["From"] = sender_email
    email_message["To"] = recipient_email
    part_1 = MIMEText(message, "plain")
    email_message.attach(part_1)
    #create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, email_message.as_string())

@app.route("/vcode_check", methods = ["POST"])
def vcode_check():
    vcode_input = request.form.get("vcode_input")
    vcode = session.get("code")
    print(vcode)
    if vcode == vcode_input:
        return "success"
    else:
        return "failure"

if __name__ == "__main__":
    app.run(debug = True)