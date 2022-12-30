from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.workout_model import Workout
from flask_app.models.exercise_model import Exercise
from flask_bcrypt import Bcrypt


# New Exercise
@app.route('/exercise/new', methods = ["POST"])
def create_exercise():
    data = {
        'id': request.form['workout_id']
    }
    workout = Workout.get_workout(data)
    exercise = Exercise.create(request.form)
    return redirect(f'/workouts/view/{workout.id}')

# Delete Exercise
@app.route('/exercises/delete/<int:workout>/<int:exercise>')
def delete_exercise(workout, exercise):
    exercise_data = {
        'id' : exercise
    }

    Exercise.delete_exercise(exercise_data)
    return redirect(f'/workouts/view/{workout}')