from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash #part of data validation
import re #regex access

ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.weight = data['weight']
        self.goal_weight = data['goal_weight']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, weight, goal_weight, email, password) VALUES (%(first_name)s, %(last_name)s, %(weight)s, %(goal_weight)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


#Workout edit
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s,  weight = %(weight)s,  goal_weight = %(goal_weight)s, email = %(email)s" \
        " WHERE users.id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)


# Get by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        return cls(results[0])


# Get by id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return False
        return cls(results[0])


# validations
    @staticmethod
    def validate(user_data):
        is_valid = True
        if len(user_data['first_name']) < 2:
            flash("First name is required", "first_name")
            is_valid = False
        if len(user_data['last_name']) < 2:
            flash("Last name is required", "last_name")
            is_valid = False
        if len(user_data['email']) < 1:
            flash("Please provide email", "email")
            is_valid = False
        elif not EMAIL_REGEX.match(user_data['email']):
            flash("Invalid email", "reg")
            is_valid = False
        else:
            potential_user = User.get_by_email(user_data['email'])
            if potential_user:
                is_valid = False
                flash("Email already has account, login?", "email")
        if len(user_data['password']) < 8:
            flash("Password must be at least 8 characters", "password")
            is_valid = False
        elif not user_data['password'] == user_data['confirm_pass']:
            flash("Passwords don't match", "confirm_pass")
            is_valid = False
        return is_valid