from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id =db.column (db.integer, primary_key=True)
    username = db.column(db.String(80), unique=True, nullable=False)