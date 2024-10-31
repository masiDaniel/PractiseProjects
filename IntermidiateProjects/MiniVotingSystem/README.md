1. Understanding and Extending the User Model
The default User model in Django provides basic fields for authentication, such as:

username: Unique identifier for each user.
password: Hashed password (use Django’s set_password method to save passwords securely).
email: Optional field that you can use for email-based login.
first_name and last_name: Basic fields for the user's full name.
is_staff, is_active, is_superuser: Fields to control user access levels.


Abstract user 
