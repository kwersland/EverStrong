from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.workout_model import Workout
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)
# bcrypt.generate_password_hash(password_string) #Generates hash for password
# bcrypt.check_password_hash(hashed_password, password_string) #checks for current hashed password


# home/index route
@app.route('/')
def index():
    return render_template('index.html')


# Login page
@app.route('/users/login')
def login_page():
    if 'user_id' in session:
        user = session['user_id']
        return redirect('/dashboard')
    return render_template('login.html')


# Register page
@app.route('/users/register')
def register_page():
    if 'user_id' in session:
        user = session['user_id']
        return redirect('/dashboard')
    return render_template('register.html')


# Login successful
@app.route('/dashboard')
def welcome():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    my_workouts = Workout.get_mine(data)
    workouts = Workout.get_all()
    user = User.get_by_id(data)
    return render_template('dashboard.html', user = user, my_workouts = my_workouts, workouts = workouts)


# Register
@app.route('/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/users/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "weight": request.form['weight'],
        "goal_weight": request.form['goal_weight'],
        "password" : pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect("/dashboard")


# logout
@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')


# login
@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Credentials", "log")
        return redirect('/users/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Credentials", "log")
        return redirect('/users/login')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


# Profile
@app.route('/profile')
def profile():
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('profile.html', user = user)


#Update Profile
@app.route('/users/update', methods= ['POST'])
def update():
    data = {
        **request.form
    }
    User.update(data)
    return redirect('/profile')