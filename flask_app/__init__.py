from flask import Flask
DATABASE = "everstrong_schema"
app = Flask(__name__)
app.secret_key = "don't tell secrets"