import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from dotenv import load_dotenv
# pip install python-dotenv
from flask_mail import Mail, Message

#  pip install flask_mail

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config["FLASKY_MAIL_SUBJECT"] = '[Apka]'
app.config["FLASKY_MAIL_SENDER"] = os.getenv('MAIL_USERNAME')

mail = Mail(app)
db = SQLAlchemy(app)


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    priority = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    def __repr__(self):
        return f"Vendor {self.id}/{self.name}"


@app.route('/')
def index():
    db.create_all()

    # v1 = Vendor(id=1, name="Microsoft", priority=0, active=True)
    # db.session.add(v1)
    # db.session.commit()

    # v2 = Vendor(id=2, name='Samsung', priority=5, active=True)
    # db.session.add(v2)
    # db.session.commit()

    vendors = Vendor.query.all()
    print(Vendor.query.filter(Vendor.active == True).all())  # [Vendor 1/Microsoft, Vendor 2/Samsung]
    print(Vendor.query.filter(Vendor.name.like('%t%')).all())  # [Vendor 1/Microsoft, Vendor 2/Samsung]

    ret = ''
    for v in vendors:
        ret += str(v) + '<br>'

    return f"Hello<br> {ret}"


@app.route('/send')
def send():
    send_mail('rajkonkret660@gmail.com', "Nowy user", 'mail/new_user', user='Admin')
    return "Hallo mail"


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT'] + subject,
                  sender=app.config["FLASKY_MAIL_SENDER"], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)



if __name__ == '__main__':
    app.run(debug=True)
