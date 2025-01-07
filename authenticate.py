from database import verify_user, register_user, hash_password


class Auth:
    def __init__(self):
        self.current_user = None

    @staticmethod
    def register(username, password):
        hashed_password = hash_password(password)
        if register_user(username, hashed_password):
            return True
        return False

    def login(self, username, password):
        hashed_password = hash_password(password)
        if verify_user(username, hashed_password):
            self.current_user = username
            return True
        return False


    def logout(self):
        self.current_user = None