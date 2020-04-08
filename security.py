from werkzeug.security import safe_str_cmp
from models.user import UserModel 

# authenticate a user
def authenticate(username,password):
    user = UserModel.find_by_username(username) # default mapping to None if no user is found
    if user and safe_str_cmp(user.password, password): # safe_str_cmp safer than passwd == mypasswd for
        return user

def identity(payload):
    """
    Identity by ID
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

