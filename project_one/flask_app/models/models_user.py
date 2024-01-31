from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
db = 'users'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Users:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, created_at, updated_at)
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, NOW(), NOW());
                """
        
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT id, first_name, last_name, email, MONTHNAME(created_at) FROM users"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(user)
        return users
    
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update(cls, form_data, user_id):
        query = f"UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at= NOW()  WHERE id = {user_id} ;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        return connectToMySQL(db).query_db(query, form_data)
        # Create an empty list to append our instances of friends
        
    @classmethod
    def delete(cls, data, user_id):
        query = f"delete FROM users where id = {user_id}"
        return connectToMySQL(db).query_db(query, data)
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid