from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash, session #part of data validation
from flask_app.models import user_model
import re #regex access



class Workout:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.day = data['day']
        self.user_id = data['user_id']
        self.posted_by = data['posted_by']
        self.author = {}
        self.exercises = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    #Create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO workouts (name, day, user_id, posted_by) VALUES (%(name)s, %(day)s, %(user_id)s, %(posted_by)s);"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results


    #Workout edit
    @classmethod
    def update(cls, data):
        query = "UPDATE workouts SET name = %(name)s, day = %(day)s" \
        " WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


    #Get Workout id
    @classmethod
    def get_workout(cls, data):
        query = "SELECT * FROM workouts LEFT JOIN users ON users.id = user_id WHERE workouts.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        return cls(results[0])


    # Delete Workout
    @classmethod
    def delete_workout(cls, data):
        query2 = "DELETE FROM exercises WHERE workout_id = %(id)s;"
        results2 = connectToMySQL(DATABASE).query_db(query2, data)
        query = "DELETE FROM workouts WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        if not results2:
            return False
        return results


    # Get all of user signed in
    @classmethod
    def get_mine(cls, data):
        query = "SELECT * FROM workouts WHERE user_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        my_workouts = []
        for row in results:
            workout_instance = cls(row)
            data = {
                'id' : row['posted_by']
            }
            this_user = user_model.User.get_by_id(data)
            workout_instance.author = this_user
            my_workouts.append(workout_instance)
        return my_workouts


    #Get all with users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_workouts = []
        for row in results:
            workout_instance = cls(row)
            data = {
                'id': row['posted_by'],
            }
            this_user = user_model.User.get_by_id(data)
            workout_instance.author = this_user
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
        if len(workout_data['name']) < 2:
            flash("Workout must have a name","name")
            is_valid = False
        data = {
            'id' : workout_data['user_id']
        }
        my_workouts = Workout.get_mine(data)
        count = 0
        if workout_data['day'] == "no_schedule":
            is_valid = True
            return is_valid
        for workout in my_workouts:
            if workout_data['day'] == workout.day:
                count += 1
            if count >= 1:
                flash(f"There is already a workout assigned to {workout_data['day']}", "day")
                is_valid = False
                return is_valid
        return is_valid