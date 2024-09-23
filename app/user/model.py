# Import necessary modules
from pydantic import BaseModel


# Define the UserModel
class UserModel(BaseModel):
    # Unique identifier for the user
    uid: str
    # User's first name
    first_name: str
    # User's email address
    email: str
    # Boolean flag indicating whether the user has admin privileges
    is_admin: bool
