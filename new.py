from flask import Flask,render_template,request,flash,redirect
from flask_mail import Mail,Message
import csv
import os

app = Flask(__name__)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'grupali645@gmail.com'
app.config['MAIL_PASSWORD'] = '123456@@'

mail = Mail(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/send_message',methods=['GET','POST'])
def send_message():
    if request.method == 'POST':
        smtp=request.form['smtp_email']
        port=request.form['port']
        sender=request.form['sender_email']
        password=request.form['password']

        subject = request.form['subject']
        msg = request.form['message']

        if request.form["submit_button"] == 'test':
            email=request.form['email']
            email=email.splitlines() #convert into list
            print(email)
            message = Message(subject,sender=sender,recipients=email)
            message.body = msg
            if not (mail.send(message)):
                flash("Mail sent Successful","success")
                return redirect(request.url)
            flash("Mail send Failed","danger")
            return redirect(request.url)


        if request.form["submit_button"] == 'bulk':
            target=os.path.join(APP_ROOT,'csv_file/')
            print("target:\t",target)

            if not os.path.isdir(target):
                os.mkdir(target)
            for file in request.files.getlist("file"):
                print(file)
                filename=file.filename
                print(filename) #file name
                des="/".join([target,filename])
                print("des\t:",des)
                file.save(des)
            try:
                with open(r'C:\Users\Harsh arora\Desktop\selenium\csv_file\{}'.format(filename), newline='') as f:
                    print("hey")
                    reader = csv.reader(f)
                    list1 = list(reader)
                print(list1) 
                flat_list = []
                for sublist in list1:
                    for item in sublist:
                        flat_list.append(item)
                print(flat_list)
                if not flat_list:
                    flash("you did not load properly","danger")
                else:
                    message=Message(subject,sender=sender,recipients=flat_list)  #passing list of receipents
                    message.body=msg

                    if not (mail.send(message)):
                        flash("Mail sent Successful","success")
                        return redirect(request.url)
                    flash("Mail send Failed","danger")
                    return redirect(request.url)
            except:
                flash("you did not load properly","danger")
                return redirect(request.url)
    return render_template("home.html")

if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)