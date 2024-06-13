from flask import Flask, request, redirect, render_template, session
app = Flask(__name__)
from bson import objectid, ObjectId
import os
import pymongo
import re
from datetime import datetime
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["Modern_agriculture"]
machinery_provider_col = my_db['Machinery_provider']
labour_provider_col = my_db['Labour_provider']
farmer_col = my_db['Farmer']
machinery_col = my_db['Machinery']
driver_col = my_db['Driver']
booking_col = my_db['Booking']
review_col= my_db['Review']
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT + "/static/files"
app.secret_key = 'key'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin_login")
def admin():
    return render_template("alogin.html")


@app.route("/admin_login1", methods=['post'])
def alogin1():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "admin" and password == 'admin':
        session['role'] = 'admin'
        return render_template("ahome.html")
    return render_template("msg.html", msg="Invaild Details", color='bg-danger text-white')


@app.route('/ahome')
def ahome():
    return render_template('ahome.html')


@app.route("/view_machinery_provider")
def view_machinery_provider():
    machinery_providers = machinery_provider_col.find()
    return render_template("view_machinery_provider.html", machinery_providers=machinery_providers)




@app.route("/machinery_reg")
def machinery_reg():
    return render_template("machinery_reg.html")


@app.route("/machinery_reg1", methods=['post'])
def machinery_reg1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    id_proof = request.files.get("id_proof")
    path = APP_ROOT+"/" + str(id_proof.filename)
    id_proof.save(path)
    query = {"email": email, "phone": phone}
    count = machinery_provider_col.count_documents(query)
    if count > 0:
        return render_template("msg.html", msg="User Exits", color='bg-danger')
    query = {"name": name, "email": email, "phone": phone, "password": password, "id_proof": id_proof.filename, 'status': 'Deactivate'}
    machinery_provider_col.insert_one(query)
    return render_template("msg.html", msg="Registration Successful", color='bg-success')


@app.route("/machinery_login")
def machinery_login():
    return render_template("machinery_login.html")


@app.route("/machinery_login1", methods=['post'])
def machinery_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {'email': email, 'password': password}
    count = machinery_provider_col.count_documents(query)
    if count > 0:
        machinery = machinery_provider_col.find_one(query)
        if machinery['status'] == "activate":
            session['machinery_provider_id'] = str(machinery['_id'])
            session['role'] = 'machinery_provider'
            return redirect("/machinery_home")
        else:
            return render_template("msg.html", msg="Your Account is Under Activation", color="bg-danger text-white")
    else:
        return render_template("msg.html", msg="InValid Details", color='bg-danger')


@app.route("/labour_reg")
def labour_reg():
    return render_template("labour_reg.html")


@app.route("/labour_reg1", methods=['post'])
def labour_reg1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    id_proof = request.files.get("id_proof")
    path = APP_ROOT + "/" + str(id_proof.filename)
    id_proof.save(path)
    price = request.form.get('price')
    licence = request.files.get("licence")
    path1 = APP_ROOT + "/" + str(licence.filename)
    licence.save(path1)
    query = {"email": email, "phone": phone}
    count = labour_provider_col.count_documents(query)
    if count > 0:
        return render_template("msg.html", msg="User Exits", color='bg-danger')
    query = {"name": name, "email": email, "phone": phone, "password": password, "id_proof": id_proof.filename, "licence": licence.filename, 'price':price, 'status': 'Deactivate'}
    labour_provider_col.insert_one(query)
    return render_template("msg.html", msg="Registration Successful", color='bg-success')


@app.route("/labour_login")
def labour_login():
    return render_template("labour_login.html")


@app.route("/labour_login1", methods=['post'])
def labour_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {'email': email, 'password': password}
    count = labour_provider_col.count_documents(query)
    if count > 0:
        labour = labour_provider_col.find_one(query)
        if labour['status'] == "Activate":
            session['labour_provider_id'] = str(labour['_id'])
            session['role'] = 'labour_provider'
            return redirect("/labour_home")
        else:
            return render_template("msg.html", msg="Your Account is Under Activation", color="bg-danger text-white")
    else:
        return render_template("msg.html", msg="Invalid Details", color='bg-danger')


@app.route("/view_labour_provider")
def view_labour_provider():
    labour_providers = labour_provider_col.find()
    return render_template("view_labour_provider.html", labour_providers=labour_providers)


@app.route('/Set_activate')
def Set_activate():
    labour_provider_id = request.args.get('labour_provider_id')
    query = {'_id': ObjectId(labour_provider_id)}
    query1 = {"$set": {'status': 'Activate'}}
    labour_provider_col.update_one(query,query1)
    return redirect('/view_labour_provider')


@app.route('/Set_deactivate')
def Set_deactivate():
    labour_provider_id = request.args.get('labour_provider_id')
    query = {'_id': ObjectId(labour_provider_id)}
    query1 = {"$set": {'status': 'Deactivate'}}
    labour_provider_col.update_one(query,query1)
    return redirect('/view_labour_provider')


@app.route('/labour_home')
def labour_home():
    labour_provider_id = session['labour_provider_id']
    query = {'_id': ObjectId(labour_provider_id)}
    labour_provider = labour_provider_col.find_one(query)
    return render_template('labour_home.html', labour_provider=labour_provider)


@app.route("/farmer_reg")
def farmer_reg():
    return render_template("farmer_reg.html")


@app.route("/farmer_reg1", methods=['post'])
def farmer_reg1():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    age = request.form.get("age")
    query = {"email": email, "phone": phone}
    count = farmer_col.count_documents(query)
    if count > 0:
        return render_template("msg.html", msg="User Exits", color='bg-danger')
    query = {"name": name, "email": email, "phone": phone, "password": password, 'age': age}
    farmer_col.insert_one(query)
    return render_template("msg.html", msg="Registration Successful", color='bg-success')


@app.route("/farmer_login")
def farmer_login():
    return render_template("farmer_login.html")


@app.route("/farmer_login1", methods=['post'])
def farmer_login1():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {'email': email, 'password': password}
    count = farmer_col.count_documents(query)
    if count > 0:
        farmer = farmer_col.find_one(query)
        session['farmer_id'] = str(farmer['_id'])
        session['role'] = 'farmer'
        return redirect("/farmer_home")
    return render_template("msg.html", msg="Invalid Details")

@app.route('/farmer_home')
def farmer_home():
    farmer_id = session['farmer_id']
    query = {'_id': ObjectId(farmer_id)}
    farmer = farmer_col.find_one(query)
    return render_template('farmer_home.html', farmer=farmer)


@app.route('/set_deactivate')
def set_deactivate():
    machinery_provider_id = request.args.get("machinery_provider_id")
    query = {"_id": ObjectId(machinery_provider_id)}
    query1 = {'$set': {'status': "Deactivate"}}
    machinery_provider_col.update_one(query, query1)
    return redirect("/view_machinery_provider")


@app.route('/set_activate')
def set_activate():
    machinery_provider_id = request.args.get("machinery_provider_id")
    query = {'$set': {'status': "activate"}}
    machinery_provider_col.update_one({'_id': ObjectId(machinery_provider_id)}, query)
    return redirect("/view_machinery_provider")


@app.route('/machinery_home')
def machinery_home():
    machinery_provider_id = session['machinery_provider_id']
    query = {'_id': ObjectId(machinery_provider_id)}
    machinery_provider = machinery_provider_col.find_one(query)
    return render_template('machinery_home.html', machinery_provider=machinery_provider)


@app.route('/add_machinery')
def add_machinery():
    return render_template('add_machinery.html')


@app.route('/add_machinery1', methods=['post'])
def add_machinery1():
    machinery_name = request.form.get('machinery_name')
    insurance = request.files.get('insurance')
    path = APP_ROOT+'/'+str(insurance.filename)
    insurance.save(path)
    driver_per_hour = request.form.get('driver_per_hour')
    driver_per_day = request.form.get('driver_per_day')
    machinery_per_hour = request.form.get('machinery_per_hour')
    machinery_per_day = request.form.get('machinery_per_day')
    about_machinery = request.form.get('about_machinery')
    image = request.files.get('image')
    path1 = APP_ROOT+'/'+str(image.filename)
    image.save(path1)
    query = {'machinery_name': machinery_name, 'machinery_provider_id':ObjectId(session['machinery_provider_id'])}
    count = machinery_col.count_documents(query)
    if count>0:
        return render_template('msg.html', msg='Machinery Exists' , color='bg-danger')
    query1 = {'machinery_name': machinery_name, 'insurance': insurance.filename, 'driver_per_hour': driver_per_hour, 'driver_per_day': driver_per_day, 'machinery_per_hour': machinery_per_hour, 'machinery_per_day': machinery_per_day, 'about_machinery': about_machinery, 'image': image.filename, 'machinery_provider_id': ObjectId(session['machinery_provider_id'])}
    machinery_col.insert_one(query1)
    return render_template('msg.html', msg='Machinery Added Successfully', color='bg-success')






@app.route('/add_driver')
def add_driver():
    return render_template('add_driver.html')


@app.route('/add_driver1', methods=['post'])
def add_driver1():
    name = request.form.get('name')
    age = request.form.get('age')
    experience = request.form.get('experience')
    licence = request.files.get('licence')
    path = APP_ROOT+'/'+str(licence.filename)
    licence.save(path)
    insurance = request.files.get('insurance')
    path1 = APP_ROOT+'/'+str(insurance.filename)
    insurance.save(path1)
    query = {'name': name, 'age': age, 'experience': experience, 'licence': licence.filename, 'insurance': insurance.filename, 'machinery_provider_id': ObjectId(session['machinery_provider_id'])}
    driver_col.insert_one(query)
    return render_template('msg.html', msg='Driver Added Successfully')


@app.route('/view_machinery')
def view_machinery():
    machinery_provider_id = request.args.get('machinery_provider_id')
    machinery_name = request.args.get('machinery_name')
    query ={}
    if session['role'] =='farmer' :
        if (machinery_provider_id ==None and machinery_name== None) or (machinery_provider_id =='' and machinery_name== ''):
            query = {}
        elif machinery_provider_id == '' and machinery_name !='':
            rgx = re.compile(".*" + machinery_name + ".*", re.IGNORECASE)
            query = {'machinery_name':rgx}
        elif machinery_provider_id !='' and machinery_name == '':
            query = {'machinery_provider_id': ObjectId(machinery_provider_id)}
        elif machinery_provider_id !='' and machinery_name!= '':
            rgx = re.compile(".*" + machinery_name + ".*", re.IGNORECASE)
            query ={'machinery_name': rgx, 'machinery_provider_id': ObjectId(machinery_provider_id)}
    if session['role'] =='machinery_provider':
        query = {'machinery_provider_id': ObjectId(session['machinery_provider_id'])}
    machineries = machinery_col.find(query)
    if session['role'] == 'machinery_provider':
        query = {'_id': ObjectId(session['machinery_provider_id'])}
    machinery_providers = machinery_provider_col.find(query)
    if machinery_name == None:
        machinery_name = ''
    return render_template('view_machinery.html', machineries=machineries, machinery_providers=machinery_providers,machinery_provider_id=machinery_provider_id,machinery_name=machinery_name,str=str, get_machinery_reviews=get_machinery_reviews)




def get_machinery_reviews(machinery_id):
    query = {'machinery_id': ObjectId(machinery_id)}
    bookings = booking_col.find(query)
    booking_ids = []
    for booking in bookings:
        booking_ids.append({'booking_id': booking['_id']})
    if len(booking_ids)==0:
        return 'No_Rating'
    query = {'$or': booking_ids}
    reviews = review_col.find(query)
    total_rating = 0
    number_of_ratings = 0
    for review in reviews:
        number_of_ratings = number_of_ratings+ 1
        total_rating = total_rating+int(review['rating'])
    if number_of_ratings == 0:
        return 'No_Rating'
    rating =total_rating/number_of_ratings
    return rating




@app.route('/view_driver')
def view_driver():
    drivers = driver_col.find()
    return render_template('view_driver.html',drivers=drivers)


@app.route('/view_labour_provider_farmer')
def view_labour_provider_farmer():
    query = {}
    if session['role'] == 'farmer':
        query = {}
    if session['role'] == 'labour_provider':
        query = {'_id': ObjectId(session['labour_provider_id'])}
    labour_providers = labour_provider_col.find(query)
    return render_template('view_labour_provider_farmer.html', labour_providers=labour_providers,get_labour_provider_reviews=get_labour_provider_reviews)

@app.route('/book_labour')
def book_labour():
    labour_provider_id = request.args.get('labour_provider_id')
    return render_template('book_labour.html', labour_provider_id=labour_provider_id)

@app.route('/book_labour1')
def book_labour1():
    labour_provider_id = request.args.get('labour_provider_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    male_count = request.args.get('male_count')
    female_count = request.args.get('female_count')
    query ={'_id': ObjectId(labour_provider_id)}
    labour_provider = labour_provider_col.find_one(query)
    price = int(labour_provider['price'])*(int(male_count)+int(female_count))
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')
    delta =(to_date-from_date)
    days = delta.days + 1
    price = days * price
    return render_template('View_booking_request.html', labour_provider_id=labour_provider_id, male_count=male_count, female_count=female_count, days=days, price=price, from_date=from_date, to_date=to_date, int=int)


@app.route('/confirm_request', methods=['post'])
def confirm_request():
    labour_provider_id = request.form.get('labour_provider_id')
    male_count = request.form.get('male_count')
    female_count = request.form.get('female_count')
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    days = request.form.get('days')
    price = request.form.get('price')
    query = {'farmer_id': ObjectId(session['farmer_id']), 'labour_provider_id': ObjectId(labour_provider_id), 'from_date': from_date, 'to_date': to_date, 'Booking_type': 'Only Labour', 'status': 'Requested', 'Price': price, 'male_count': male_count, 'female_count': female_count, 'days': days, 'booking_date': datetime.now()}
    booking_col.insert_one(query)
    return render_template('msg.html', msg='Booking Request Sent', color='bg-success')





@app.route('/Book_machinery')
def Book_machinery():
    machinery_id = request.args.get('machinery_id')
    return render_template('Book_machinery.html', machinery_id=machinery_id, get_machinery_by_id=get_machinery_by_id)

def get_machinery_by_id(machinery_id):
    query = {'_id': ObjectId(machinery_id)}
    machinery = machinery_col.find_one(query)
    return machinery



@app.route('/Book_machinery1')
def Book_machinery1():
    machinery_id = request.args.get('machinery_id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    from_date = from_date.replace("T"," ")
    to_date = to_date.replace("T"," ")
    is_driver_required = request.args.get('is_driver_required')
    from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M')
    to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M')
    delta = (to_date - from_date)
    days = delta.days
    seconds = delta.seconds
    hours_diff = int(delta.seconds / 3600)
    query = {"_id": ObjectId(machinery_id)}
    machinary = machinery_col.find_one(query)
    Booking_type = None
    if is_driver_required == 'yes':
        Booking_type = 'machinery_with_driver'
        total_driver_amount = days * float(machinary['driver_per_day']) + hours_diff * float(machinary['driver_per_hour'])
    else:
        Booking_type = 'only_machinery'
        total_driver_amount = 0
    total_machine_amount = days*float(machinary['machinery_per_day'])+hours_diff*float(machinary['machinery_per_hour'])
    total_amount = total_machine_amount + total_driver_amount
    return render_template('Book_machinery1.html', total_driver_amount=total_driver_amount,total_machine_amount=total_machine_amount,total_amount=total_amount, machinery_id=machinery_id, from_date=from_date, to_date=to_date,is_driver_required=is_driver_required, days=days,hours_diff=hours_diff, Booking_type=Booking_type)

@app.route('/confirm_booking')
def confirm_booking():
    machinery_id = request.args.get('machinery_id')
    driver_per_hour = request.args.get('driver_per_hour')
    total_amount = request.args.get('total_amount')
    machinery_per_hour = request.args.get('machinery_per_hour')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    is_driver_required = request.args.get('is_driver_required')
    days = request.args.get('days')
    total_machine_amount = request.args.get('total_machine_amount')
    total_driver_amount = request.args.get('total_driver_amount')
    Booking_type = request.args.get('Booking_type')
    query = {'farmer_id': ObjectId(session['farmer_id']), 'machinery_id': ObjectId(machinery_id),   'from_date': from_date, 'to_date': to_date, 'is_driver_required': is_driver_required, 'days': days, 'total_machine_amount': total_machine_amount, 'total_driver_amount': total_driver_amount, 'Booking_type': Booking_type, 'booking_date':datetime.now(), 'status': 'Requested', 'total_amount':total_amount, 'days': days}
    booking_col.insert_one(query)
    return render_template("msg.html", msg='Booking Request Sent', color='bg-success')





@app.route('/view_farmer_booking')
def view_farmer_booking():
    query = {'farmer_id': ObjectId(session['farmer_id'])}
    bookings = booking_col.find(query)
    return render_template('view_farmer_booking.html', bookings=bookings, get_farmer_by_id=get_farmer_by_id, get_machinery_by_machinery_id=get_machinery_by_machinery_id, get_machinery_provider_by_id=get_machinery_provider_by_id, get_labour_by_labour_id=get_labour_by_labour_id, get_driver_id=get_driver_id)


def get_labour_by_labour_id(labour_provider_id):
    query = {'_id': ObjectId(labour_provider_id)}
    labour_provider = labour_provider_col.find_one(query)
    return labour_provider


def get_farmer_by_id(farmer_id):
    query = {'_id': ObjectId(farmer_id)}
    farmer = farmer_col.find_one(query)
    return farmer

def get_machinery_by_machinery_id(machinery_id):
    query = {'_id': ObjectId(machinery_id)}
    machinery = machinery_col.find_one(query)
    return machinery

def get_machinery_provider_by_id(machinery_provider_id):
    query = {'_id': ObjectId(machinery_provider_id)}
    machinery_provider = machinery_provider_col.find_one(query)
    return machinery_provider

def get_labour_provider_reviews(labour_provider_id):
    query = {'labour_provider_id': ObjectId(labour_provider_id)}
    bookings = booking_col.find(query)
    booking_ids = []
    for booking in bookings:
        booking_ids.append({'booking_id': booking['_id']})
    if len(booking_ids)==0:
        return 'No_Rating'
    query = {'$or': booking_ids}
    reviews = review_col.find(query)
    total_rating = 0
    number_of_ratings = 0
    for review in reviews:
        number_of_ratings = number_of_ratings+ 1
        total_rating = total_rating+int(review['rating'])
    if number_of_ratings == 0:
        return 'No_Rating'

    rating =total_rating/number_of_ratings
    return rating




@app.route('/view_machinery_bookings')
def view_machinery_bookings():
    machinery_provider_id = ObjectId(session['machinery_provider_id'])
    query = {'machinery_provider_id': ObjectId(machinery_provider_id)}
    machineries = machinery_col.find(query)
    machinery_ids =[]
    for machinery in machineries:
        machinery_id = machinery['_id']
        machinery_ids.append({'machinery_id': machinery_id})
        query = {'$or': machinery_ids}
        bookings = booking_col.find(query)
        if len(machinery_ids) > 0:
            return render_template('view_machinery_bookings.html', bookings=bookings, get_farmer_by_id=get_farmer_by_id,
                                   get_machinery_by_machinery_id=get_machinery_by_machinery_id,
                                   get_machinery_provider_by_id=get_machinery_provider_by_id, get_driver_id=get_driver_id)
        else:
            return render_template('msg.html', msg='No available Bookings', color='bg-success text-white')


def get_driver_id(machinery_provider_id):
    query = {'machinery_provider_id': ObjectId(machinery_provider_id)}
    print(query)
    driver = driver_col.find_one(query)
    print(driver)
    return driver




@app.route('/view_labour_bookings')
def view_labour_bookings():
    labour_provider_id = session['labour_provider_id']
    type = request.args.get('type')
    if type =='history':
        query = {"$or":[{'labour_provider_id': ObjectId(labour_provider_id), 'status': 'Service_Provided'}, {'labour_provider_id': ObjectId(labour_provider_id), 'status': 'Booking_Rejected'},{'labour_provider_id': ObjectId(labour_provider_id), 'status': 'Cancel_bookings'}]}
    else:
        query = {'$or':[{'labour_provider_id': ObjectId(labour_provider_id), 'status': 'Requested'}, {'labour_provider_id': ObjectId(labour_provider_id), 'status': 'Booking_Approved'}]}

    bookings = booking_col.find(query)
    return render_template('view_labour_bookings.html', bookings=bookings, get_farmer_by_id=get_farmer_by_id, get_labour_by_labour_id=get_labour_by_labour_id, get_labour_provider_reviews=get_labour_provider_reviews)


def get_labour_by_labour_id(labour_provider_id):
    query = {'_id': ObjectId(labour_provider_id)}
    labour_provider = labour_provider_col.find_one(query)
    return labour_provider


@app.route('/set_status')
def set_status():
    booking_id = request.args.get('booking_id')
    status = request.args.get('status')
    query = {'_id': ObjectId(booking_id)}
    query1 = {'$set': {'status': status}}
    booking_col.update_one(query, query1)
    return render_template('msg.html', msg=status, color='bg-secondary')

@app.route('/review')
def review():
    booking_id = request.args.get('booking_id')
    return render_template('review.html', booking_id=booking_id)


@app.route('/review1', methods=['post'])
def review1():
    booking_id = request.form.get('booking_id')
    rating = request.form.get('rating')
    review = request.form.get('review')
    query = {'booking_id': ObjectId(booking_id), 'rating': rating, 'review': review, 'date': datetime.now()}
    review_col.insert_one(query)
    return render_template('msg.html', msg='Review Added', color='bg-success')

@app.route("/viewReviewLabor")
def viewReviewLabor():
    labour_provider_id = request.args.get('labour_provider_id')
    query = {'labour_provider_id': ObjectId(labour_provider_id)}
    bookings = booking_col.find(query)
    booking_ids = []
    for booking in bookings:
        booking_ids.append({'booking_id': booking['_id']})
    if len(booking_ids) == 0:
        return render_template('msg.html', msg='No Review Available', color='bg-success')
    query = {'$or': booking_ids}
    reviews = review_col.find(query)
    return render_template("viewReviewLabor.html",reviews=reviews, get_farmer_id=get_farmer_id,get_booking_by_id=get_booking_by_id)

def get_booking_by_id(booking_id):
   query = {'_id': ObjectId(booking_id)}
   booking = booking_col.find_one(query)
   return booking


def get_farmer_id(farmer_id):
    query = {'_id': farmer_id}
    farmer = farmer_col.find_one(query)
    return farmer


@app.route('/view_machinery_review')
def view_machinery_review():
    machinery_id = request.args.get('machinery_id')
    query = {'machinery_id': ObjectId(machinery_id)}
    bookings = booking_col.find(query)
    booking_ids = []
    for booking in bookings:
        booking_ids.append({'booking_id': booking['_id']})
    if len(booking_ids) == 0:
        return render_template('msg.html', msg='No Review Available', color='bg-success')
    query = {'$or': booking_ids}
    reviews = review_col.find(query)
    return render_template("view_machinery_review.html", reviews=reviews, get_farmer_id=get_farmer_id,
                           get_booking_by_id=get_booking_by_id)


@app.route('/set_status2')
def set_status2():
    booking_id = request.args.get('booking_id')
    query = {'machinery_provider_id': ObjectId(session['machinery_provider_id'])}
    drivers = driver_col.find(query)
    return render_template('set_status2.html', drivers=drivers, booking_id=booking_id)

@app.route('/set_status3')
def set_status3():
    booking_id = request.args.get('booking_id')
    driver_id = request.args.get('driver_id')
    query = {'_id': ObjectId(booking_id)}
    query1 = {'$set': {'status': 'Booking_Approved', 'driver_id': ObjectId(driver_id)}}
    booking_col.update_one(query,query1)
    return render_template('msg.html', msg='Driver Assignmed', color='bg-success')










@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")





app.run(debug=True)