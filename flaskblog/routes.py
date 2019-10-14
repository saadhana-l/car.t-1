import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm,FinalForm,InputForm,NotificationForm
from flaskblog.models import Account, Car,Notification
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
from sklearn.externals import joblib

@app.route("/")
@app.route("/home")
def home():
    posts = Car.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

# @app.route("/notif")
# def view_notif():
#     notifs = Notification.query.all()
#     return render_template('notifications.html', notifs=notifs)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():   #will tell us if the form is valid on submit
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        account = Account(username=form.username.data, email=form.email.data,account_type=form.account_type.data, password=hashed_password)
        db.session.add(account)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        account = Account.query.filter_by(email=form.email.data).first()
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture_2(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/car_pics', picture_fn)

    output_size = (325, 325)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        car = Car(title=form.title.data, content=form.content.data,author=current_user,location=form.location.data,year=form.year.data,kilometers_driven=form.kilometers_driven.data,fuel_type=form.fuel_type.data,transmission=form.transmission.data,owner_type=form.owner_type.data,mileage=form.mileage.data,engine=form.engine.data,power=form.power.data,seats=form.seats.data,brand=form.brand.data)
        if form.picture.data:
            picture_file = save_picture_2(form.picture.data)
            car.image_file = picture_file
        db.session.add(car)
        db.session.commit()
        flash('Price Predicted!', 'success')
        return redirect(url_for('predictor_post',post_id=car.id))
    return render_template('create_post.html', title='New Prediction',form=form,
                                       legend='New Prediction')

@app.route("/input", methods=['GET', 'POST'])
@login_required
def input():
    form = InputForm()
    if form.validate_on_submit():
        return redirect(url_for('search',brand=form.brand.data,location=form.location.data,kilometers_driven_start=form.kilometers_driven_start.data,
            kilometers_driven_end=form.kilometers_driven_end.data,fuel_type=form.fuel_type.data,transmission=form.transmission.data,owner_type=form.owner_type.data,))
    return render_template('input.html', title='Input',form=form, legend='Input')
@app.route("/search",methods=['GET', 'POST'])
def search():
    quer=dict()
    nparr=[request.args.get('location'),request.args.get('fuel_type'),request.args.get('transmission'), request.args.get('owner_type'),
    request.args.get('brand'),request.args.get('kilometers_driven_start'),request.args.get('kilometers_driven_end')]
    l=['location','fuel_type','transmission','owner_type','brand','kilometers_driven_start','kilometers_driven_end']
    for i in range(len(nparr)-2):
        if nparr[i]!=None and nparr[i]!='None':
            quer[l[i]]=nparr[i]
    posts=Car.query.filter_by(**quer)
    if nparr[len(nparr)-2]!=None:
        posts2=Car.query.filter(Car.kilometers_driven >= int(nparr[len(nparr)-2]))
        posts=[item for item in posts if item in posts2]
    if nparr[len(nparr)-1]!=None:
        posts3=Car.query.filter(Car.kilometers_driven <= int(nparr[len(nparr)-1]))
        posts=[item for item in posts if item in posts3]
    return render_template('search.html', posts=posts)

def price_predictor(nparr):
    loaded_model = joblib.load('flaskblog/static/model/final_xgb.joblib.dat')
    y_pred = loaded_model.predict([nparr])
    return np.round(y_pred)
def data_preprocess(car):
    l=[]
    location_rank = { 'mumbai':6, 'pune':9, 'chennai':8, 'coimbatore':1, 'hyderabad':4, 'jaipur':10,'kochi':3, 'kolkata':11, 'delhi':5, 'bangalore':2, 'ahmedabad':7}
    if car.location in location_rank:
        l.append(location_rank[car.location])

    l.append(car.year)
    l.append(car.kilometers_driven)

    fuel_type_enc={ 'diesel' :1, 'cng':2,'lpg':3,'petrol':4}
    if car.fuel_type in fuel_type_enc:
        l.append(fuel_type_enc[car.fuel_type])

    if car.transmission=='manual':
        l.append(1)
    elif car.transmission=='automatic':
        l.append(0)

    owner_type_enc={'first':1,'second':2,'third':3,'fourth and above':4}
    if car.owner_type in owner_type_enc:
        l.append(owner_type_enc[car.owner_type])

    if car.fuel_type=='cng':
        l.append(float(car.mileage)*0.621*2.567)
    elif car.fuel_type=='lpg':
        l.append(float(car.mileage)*0.621*(1/(0.264*1.96))*1.247)
    elif car.fuel_type=='diesel':
        l.append(float(car.mileage)*0.621*(1/0.264)*0.88)
    elif car.fuel_type=='petrol':
        l.append(float(car.mileage)*0.621*(1/0.264))

    l.append(car.engine)

    l.append(car.power)

    l.append(car.seats)

    brand_rank={'Maruti':25, 'Hyundai':22, 'Honda':21, 'Audi':9, 'Nissan':24, 'Toyota':14,'Volkswagen':23, 'Tata':26, 'Range Rover':3, 'Land Rover':6, 'Mitsubishi':15, 'Renault':20, 'Mercedes-Benz':8, 'BMW':10, 'Mahindra':17, 'Ford':19, 'Porsche':4, 'Datsun':28, 'Jaguar':5, 'Volvo':11, 'Chevrolet':29, 'Skoda':18, 'Mini':7, 'Fiat':27, 'Jeep':12, 'Smart':30, 'Ambassador':31, 'ISUZU':13, 'Force':16, 'Bentley':2, 'Lamborghini':1}
    if car.brand in brand_rank:
        l.append(brand_rank[car.brand])
    return np.array(l,dtype='float64')

@app.route("/post/<int:post_id>/predictor",methods=['GET', 'POST'])
@login_required
def predictor_post(post_id):
    car = Car.query.get_or_404(post_id)
    form = FinalForm()
    nparr = data_preprocess(car)
    car.pred_price = price_predictor(nparr)
    db.session.commit()
    if form.validate_on_submit():
        car.price = form.final_price.data
        if abs(car.price-car.pred_price) <=0.5:
                car.deal_type='good'
        else:
                car.deal_type='bad'
        db.session.commit()
        flash('Post Added!', 'success')
        return redirect(url_for('home'))
    return render_template('predictor.html',form=form,post=car)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Car.query.get_or_404(post_id)
    image_file = url_for('static', filename='car_pics/' + post.image_file)
    return render_template('post.html', title=post.title, post=post,image_file=image_file)


@app.route("/post/<int:post_id>/interested", methods=['GET', 'POST'])
@login_required
def notify_seller(post_id):
    post = Car.query.get_or_404(post_id)
    form = NotificationForm()
    if form.validate_on_submit():
        notif=Notification(content=form.content.data,seller_id=post.author.id,buyer_id=current_user.id,car_id=post.id,
            seller_name=post.author.username,buyer_name=current_user.username,car_name=post.title)
        db.session.add(notif)
        db.session.commit()
        flash('Notification Sent', 'success')
        return redirect(url_for('home'))
    return render_template('create_notification.html', title='Send Notifictaion',
                           form=form, legend='Send Notification')


@app.route("/account_expanded/<int:id>")
def display_account(id):
    acc=Account.query.get_or_404(id)
    image_file = url_for('static', filename='profile_pics/' + acc.image_file)
    return render_template('account_expanded.html', title='Account',acc=acc,image_file=image_file)

@app.route("/notif")
def view_notif():
    notifs = Notification.query.all()
    return render_template('notifications.html', title='Send Notification',notifs=notifs)



@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Car.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        post.location=form.location.data
        post.year=form.year.data
        post.kilometers_driven=form.kilometers_driven.data
        post.fuel_type=form.fuel_type.data
        post.transmission=form.transmission.data
        post.owner_type=form.owner_type.data
        post.mileage=form.mileage.data
        post.engine=form.engine.data
        post.power=form.power.data
        post.seats=form.seats.data
        post.brand=form.brand.data
        if form.picture.data:
            picture_file = save_picture_2(form.picture.data)
            post.image_file = picture_file
        db.session.commit()
        flash('Price Predicted!', 'success')
        return redirect(url_for('predictor_post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data=post.title
        form.content.data= post.content
        form.location.data=post.location
        form.year.data=post.year
        form.kilometers_driven.data=post.kilometers_driven
        form.fuel_type.data=post.fuel_type
        form.transmission.data=post.transmission
        form.owner_type.data=post.owner_type
        form.mileage.data=post.mileage
        form.engine.data=post.engine
        form.power.data=post.power
        form.seats.data=post.seats
        form.brand.data=post.brand
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Car.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
