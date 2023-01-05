from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.workout_model import Workout
from flask_app.models.exercise_model import Exercise
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)



# Read All workouts
@app.route('/workouts/view')
def read_all():
    all_workouts = Workout.get_all()
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return render_template('all_workouts.html', workouts = all_workouts, user = user, weekdays = weekdays)



# Read all your workouts
@app.route('/my_workouts/view')
def read_mine():
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    my_workouts = Workout.get_mine(data)
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return render_template('my_workouts.html', workouts = my_workouts, user = user, weekdays = weekdays)



# Read one workout
@app.route('/workouts/view/<int:id>')
def read_one(id):
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    exercises = Exercise.get_by_workout(data)
    workout = Workout.get_one(data)
    posted_by_data = {
        'id' : workout.posted_by
    }
    posted_by = User.get_by_id(posted_by_data)
    return render_template('one_workout.html', workout = workout, user = user, exercises = exercises, posted_by = posted_by)



# Create a workout
@app.route('/workouts/new', methods = ['POST'])
def new_workout():
    if not Workout.validate(request.form):
        return redirect('/dashboard')
    this_workout = Workout.create(request.form)
    return redirect(f"/workouts/view/{this_workout}")



# Delete a workout
@app.route('/workouts/delete/<int:id>')
def del_workout(id):
    data = {
        'id': id
    }
    Workout.delete_workout(data)
    return redirect('/my_workouts/view')


#Edit workouts
@app.route("/workouts/update/<int:id>", methods=["POST"])
def update_workout(id):
    if not Workout.validate(request.form):
        return redirect(f'/my_workouts/view')
    data = {
        ** request.form,
        "id": id
    }
    Workout.update(data)
    return redirect("/my_workouts/view")


# Schedule your own workouts
@app.route("/workouts/schedule/<int:id>", methods=["POST"])
def schedule_workout(id):
    if not Workout.validate(request.form):
        return redirect(f'/workouts/view/{id}')
    data = {
        ** request.form,
        "id": id
    }
    Workout.update(data)
    return redirect(f"/workouts/view/{id}")


# Add someone else's workout to your schedule
@app.route("/workouts/add_schedule/<int:id>")
def add_schedule(id):
    data = {
        'id': id
    }
    user_data = {
        'id':session['user_id']
    }
    workout = Workout.get_one(data)
    user = User.get_by_id(user_data)
    return render_template("schedule_workout.html", workout = workout, user = user)


@app.route("/workouts/add", methods=["POST"])
def add():
    data = {
        'name' : request.form['name'],
        'day' : request.form['day'],
        'user_id' : request.form['user_id'],
        'posted_by' : request.form['posted_by']
    }
    workout = Workout.create(data)
    exercise_data = {
        'id' : request.form['id']
    }
    exercises = Exercise.get_by_workout(exercise_data)
    for exercise in exercises:
        exercise_instance = {
            'name' : exercise.name,
            'muscle' : exercise.muscle,
            'sets' : exercise.sets,
            'reps' : exercise.reps,
            'description' : exercise.description,
            'workout_id': workout
        }
        Exercise.create(exercise_instance)
    return redirect(f"/workouts/view/{workout}")