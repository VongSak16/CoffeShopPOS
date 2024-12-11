from database.auth_dao import AuthDAO


class AuthChecker:
    @staticmethod
    def authenticate(username, password):
        """Authenticate the user and return user details if successful."""
        user = AuthDAO.validate_user(username, password)
        if user:
            print("User authenticated successfully.")
            return user
        else:
            print("\033[91mInvalid username or password.\033[0m")
            return None
