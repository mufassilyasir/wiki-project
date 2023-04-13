from flask_login import current_user
import re

def get_header_variables():
    logged_in = False
    name = False
    admin = False

    if current_user.is_authenticated:
        logged_in = True
        name = current_user.name
        if current_user.has_role(1): #ADMIN ROLE
            admin = True
    
    return name, logged_in, admin

def convert_to_slug(string, separator='-'):
    string = re.sub(r'[^a-zA-Z0-9_ ]', '', string)
    string = string.replace(' ', separator)
    string = string.lower()

    return string