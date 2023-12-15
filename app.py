from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    priority = db.Column(db.Integer)
    active = db.Column(db.Boolean)


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

    ret= ''
    for v in vendors:
        ret += v.name+'<br>'

    return f"Hello<br> {ret}"


if __name__ == '__main__':
    app.run(debug=True)
