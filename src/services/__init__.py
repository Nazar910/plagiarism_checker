import bcrypt
import os

class Service:
    def __init__(self, collection):
        self.coll = collection

class UserService(Service):
    def find_by_email_and_password(self, email, password):
        user = self.coll.find_one({'email': email})
        expected_pass = password.encode('utf-8')
        actual_pass = user['password'].encode('utf-8')
        if bcrypt.checkpw(expected_pass, actual_pass):
            return user

    def ensure_admin_user(self, email, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        admin = {
            'first_name': 'Admin',
            'last_name': 'Admin',
            'email': email,
            'password': hashed.decode('utf-8'),
            'role': 'admin'
        }
        self.coll.update_one({'email': email}, {'$set': admin}, upsert=True)
