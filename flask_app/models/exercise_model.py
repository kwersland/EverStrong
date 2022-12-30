from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Exercise:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.muscle = data['muscle']
        self.sets = data['sets']
        self.reps = data['reps']
        self.workout = data['workout_id']
        self.description = data['description']


    #Create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO exercises (name, muscle, sets, reps, description, workout_id) VALUES (%(name)s, %(muscle)s, %(sets)s, %(reps)s, %(description)s, %(workout_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    #Workout edit
    @classmethod
    def update(cls, data):
        query = "UPDATE exercises SET name = %(name)s, muscle = %(muscle)s, sets = %(sets)s, reps = %(reps)s, description = %(description)s, workout_id = %(workout_id)s;" \
        " WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    #Get Workout id
    @classmethod
    def get_by_workout(cls, data):
        query = "SELECT * FROM exercises LEFT JOIN workouts ON workouts.id = exercises.workout_id WHERE workouts.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        exercises = []
        if results:
            for row in results:
                exercise_instance = cls(row)
                exercises.append(exercise_instance)
        return exercises


    # Delete Exercise
    @classmethod
    def delete_exercise(cls, data):
        query = "DELETE FROM exercises WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        return results


    # Get all of user signed in
    @classmethod
    def get_mine(cls, data):
        query = "SELECT * FROM exercises WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        my_workouts = []
        for row in results:
            workout_instance = cls(row)
            my_workouts.append(workout_instance)
        return my_workouts


    #Get all with users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts LEFT JOIN users ON users.id = user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_workouts = []
        for row in results:
            workout_instance = cls(row)
            all_workouts.append(workout_instance)
        return all_workouts


    #Get one with user
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM workouts LEFT JOIN users ON users.id = user_id WHERE workouts.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])


    # validations
    @staticmethod
    def validate(workout_data):
        is_valid = True
        if len(workout_data['name']) < 3:
            flash("Name cannot be empty", "name")
            is_valid = False
        if len(workout_data['muscle']) < 3:
            flash("Muscle group cannot be empty", "muscle")
            is_valid = False
        if len(workout_data['description']) < 3:
            flash("Descripition cannot be blank", "description")
            is_valid = False
        if len(workout_data['day']) < 1:
            flash("You must assign workout to a day", "day")
            is_valid = False
        return is_valid