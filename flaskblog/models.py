from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_account(account_id):
    return Account.query.get(int(account_id))


class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    account_type = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Car', backref='author', lazy=True)

    def __repr__(self):
        return f"Account('{self.username}','{self.account_type}', '{self.email}', '{self.image_file}')"


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default='default_car.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    location = db.Column(db.String(20),nullable=False)
    year = db.Column(db.Integer,nullable=False)
    kilometers_driven = db.Column(db.Integer,nullable=False)
    fuel_type= db.Column(db.String(20),nullable=False)
    transmission= db.Column(db.String(20),nullable=False)
    owner_type= db.Column(db.String(20),nullable=False)
    mileage = db.Column(db.String(20),nullable=False)
    engine =  db.Column(db.Integer,nullable=False)
    power =  db.Column(db.Integer,nullable=False)
    seats =   db.Column(db.Integer,nullable=False)
    brand=  db.Column(db.String,nullable=False)
    pred_price =  db.Column(db.Float,nullable=True)
    price = db.Column(db.Float,nullable=True)
    deal_type =  db.Column(db.String,nullable=True)

    def __repr__(self):
        return f"Car({self.title}', '{self.date_posted}','{self.content}','{self.user_id}','{self.location}','{self.year}','{self.kilometers_driven}','{self.fuel_type}','{self.transmission}','{self.owner_type}','{self.mileage}','{self.engine}','{self.power}','{self.seats}','{self.brand}',, '{self.image_file}')"

class Notification(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    seller_id= db.Column(db.Integer)
    buyer_id= db.Column(db.Integer)
    car_id= db.Column(db.Integer)
    seller_name=db.Column(db.String)
    buyer_name=db.Column(db.String)
    car_name=db.Column(db.String)
    content = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f"Notification('{self.seller_id}','{self.buyer_id}', '{self.car_id}', '{self.content}','{self.seller_name}','{self.buyer_name}','{self.car_name}')"

