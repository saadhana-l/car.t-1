from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField,IntegerField,FloatField,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,AnyOf
from flaskblog.models import Account,Car



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    #account_type=StringField('AccountType',validators=[DataRequired(),AnyOf(['Seller','Buyer'],message='Enter either Buyer or Seller')])
    account_type = SelectField('Account Type',choices=[('Seller','Seller'),('Buyer','Buyer')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        account = Account.query.filter_by(username=username.data).first()
        if account:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        account = Account.query.filter_by(email=email.data).first()
        if account:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class FinalForm(FlaskForm):
    final_price = FloatField('Enter Final Price',validators=[DataRequired()])
    submit = SubmitField('Add Listing!')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    brand = SelectField('Brand',choices=[('Maruti','Maruti'), ('Toyota','Toyota'), ('Hyundai','Hyundai'), ('Mahindra','Mahindra'), ('Honda','Honda'), ('Audi','Audi'),
       ('Nissan','Nissan'), ('BMW','BMW'), ('Ford','Ford'), ('Skoda','Skoda'), ('Volkswagen','Volkswagen'), ('Mitsubishi','Mitsibhishi'),
       ('Mercedes-Benz','Mercedes-Benz'), ('Tata','Tata'), ('Chevrolet','Chevrolet'), ('Datsun','Datsun'), ('Jaguar','Jaguar'), ('Fiat','Fiat'),
       ('Hindustan','Hindustan'), ('Renault','Renault'), ('Mini','Mini'), ('Bentley','Bentley'), ('Land Rover','Land Rover'), ('Volvo','Volvo'),
       ('Range Rover','Range Rover'), ('ISUZU','ISUZU'), ('Jeep','Jeep'), ('Porsche','Porsche'), ('Opel','Opel')])
    location = SelectField('Location',choices=[('coimbatore','Coimbatore'),('bangalore','Bangalore'),('kochi','Kochi'),('hyderabad','Hyderabad'),('delhi','Delhi'),('mumbai','Mumbai'),('ahmedabad','Ahmedabad'),('chennai','Chennai'),('pune','Pune'),('jaipur','Jaipur'),('kolkata','Kolkata')])
    year = IntegerField('Year of Model', validators=[DataRequired()])
    kilometers_driven= IntegerField('Kilometers Driven',validators=[DataRequired()])
    fuel_type = SelectField('Fuel Type',choices=[('diesel','Diesel'),('petrol','Petrol'),('cng','CNG'),('lpg','LPG')])
    transmission = SelectField('Transmission',choices=[('manual','Manual'),('automatic','Automatic')])
    owner_type = SelectField('Owner Type',choices=[('first','First'),('second','Second'),('third','Third'),('fourth and above','Fourth and above')])
    mileage = StringField('Mileage(km/l or km/kg)', validators=[DataRequired()])
    engine = IntegerField('Engine(CC)', validators=[DataRequired()])
    power = IntegerField('Power(bhp)', validators=[DataRequired()])
    seats = IntegerField('Number of seats', validators=[DataRequired()])
    picture = FileField('Upload photo of car', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('View Predicted Price')
    def validate_pic(self,picture):
        if picture.data==None:
            raise ValidationError('Please choose a picture')


class InputForm(FlaskForm):
    brand = SelectField('Brand',choices=[('Maruti','Maruti'), ('Toyota','Toyota'), ('Hyundai','Hyundai'), ('Mahindra','Mahindra'), ('Honda','Honda'), ('Audi','Audi'),
       ('Nissan','Nissan'), ('BMW','BMW'), ('Ford','Ford'), ('Skoda','Skoda'), ('Volkswagen','Volkswagen'), ('Mitsubishi','Mitsibhishi'),
       ('Mercedes-Benz','Mercedes-Benz'), ('Tata','Tata'), ('Chevrolet','Chevrolet'), ('Datsun','Datsun'), ('Jaguar','Jaguar'), ('Fiat','Fiat'),
       ('Hindustan','Hindustan'), ('Renault','Renault'), ('Mini','Mini'), ('Bentley','Bentley'), ('Land Rover','Land Rover'), ('Volvo','Volvo'),
       ('Range Rover','Range Rover'), ('ISUZU','ISUZU'), ('Jeep','Jeep'), ('Porsche','Porsche'), ('Opel','Opel'),('None','None')])
    location = SelectField('Location',choices=[('Coimbatore','Coimbatore'),('Bangalore','Bangalore'),('Kochi','Kochi'),('Hyderabad','Hyderabad'),('Delhi','Delhi'),('Mumbai','Mumbai'),('Ahmedabad','Ahmedabad'),('Chennai','Chennai'),('Pune','Pune'),('Jaipur','Jaipur'),('Kolkata','Kolkata'),('None','None')])
    kilometers_driven_start= IntegerField('Kilometers Min Range',validators=[validators.Optional(strip_whitespace=True)])
    kilometers_driven_end= IntegerField('Kilometers Max Range',validators=[validators.Optional(strip_whitespace=True)])
    fuel_type = SelectField('Fuel Type',choices=[('Diesel','Diesel'),('Petrol','Petrol'),('CNG','CNG'),('LPG','LPG'),('None','None')])
    transmission = SelectField('Transmission',choices=[('Manual','Manual'),('Automatic','Automatic'),('None','None')])
    owner_type = SelectField('Owner Type',choices=[('First','First'),('Second','Second'),('Third','Third'),('Fourth and above','Fourth and above'),('None','None')])
    submit = SubmitField('Search')

class NotificationForm(FlaskForm):
    content=StringField( validators=[DataRequired()])
    submit = SubmitField('Submit')
