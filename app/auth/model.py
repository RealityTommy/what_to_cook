# Import necessary modules from pydantic
from pydantic import BaseModel, EmailStr


# UserCreate model: Used for user registration
class UserCreate(BaseModel):
    """
    Pydantic model for user creation/registration.
    This defines the structure of the data required when creating a new user.
    """

    # EmailStr ensures that the email is in a valid format
    email: EmailStr

    # The password field is a simple string
    # Note: In the database, this should be hashed for security
    password: str

    # The user's first name
    first_name: str

    class Config:
        # This provides an example of what valid data looks like
        # It's useful for API documentation and testing
        json_schema_extra = {
            "example": {
                "email": "app@tommytruong.dev",
                "password": "strongpassword123",
                "first_name": "Tommy",
            }
        }


# UserLogin model: Used for user authentication
class UserLogin(BaseModel):
    """
    Pydantic model for user login.
    This defines the structure of the data required when a user attempts to log in.
    """

    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {"email": "app@tommytruong.dev", "password": "strongpassword123"}
        }


# Token model: Used for authentication responses
class Token(BaseModel):
    """
    Pydantic model for authentication token.
    This defines the structure of the response data when a user successfully authenticates.
    """

    # The access token string
    access_token: str

    # The type of token, typically "bearer"
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
