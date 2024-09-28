# Import necessary modules from FastAPI
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# Import Supabase client
from supabase import create_client, Client
import os

# Import the Pydantic models from our auth_models.py file
from app.auth.model import UserCreate, UserLogin, Token

# Import the create_user function from user.py
from app.user.user import create_user, get_user_by_email

# Create a router object. This allows us to organize our routes.
router = APIRouter(prefix="/auth", tags=["authentication"])

# Initialize Supabase client
# This client will be used to interact with Supabase services
supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),  # URL of your Supabase project
    os.environ.get("SUPABASE_KEY"),  # API key for your Supabase project
)

# OAuth2 scheme for token authentication
# This will be used to extract the token from incoming requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Helper function to create a user after OAuth sign-in
async def create_oauth_user(user_data):
    try:
        # Check if the user already exists in our database
        existing_user = await get_user_by_email(user_data.email)
        if existing_user:
            return existing_user

        # Extract first name from user metadata
        full_name = user_data.user_metadata.get("full_name", "")
        first_name = full_name.split()[0] if full_name else ""

        # If first_name is still empty, try to get it from other fields
        if not first_name:
            first_name = user_data.user_metadata.get("name", "").split()[0]
        if not first_name:
            first_name = user_data.user_metadata.get("given_name", "")

        # If we still don't have a first name, use a default value
        if not first_name:
            first_name = "Joe Schmo"  # Or you could use part of the email address

        # Create a new user
        new_user = await create_user(
            auth_id=user_data.id, email=user_data.email, first_name=first_name
        )
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create user: {str(e)}")


# Sign-up endpoint
@router.post("/signup", response_model=dict)
async def sign_up(user: UserCreate):
    """
    Endpoint for user registration.
    It takes UserCreate data and creates a new user in Supabase.
    """
    try:
        # Attempt to sign up the user using Supabase auth
        auth_response = supabase.auth.sign_up(
            {"email": user.email, "password": user.password}
        )

        if auth_response.user and auth_response.user.id:
            # If sign-up is successful, create a user in our database
            db_user = await create_user(
                auth_id=auth_response.user.id,
                email=user.email,
                first_name=user.first_name,
            )

        else:
            raise HTTPException(
                status_code=400, detail="Failed to create user in Supabase Auth"
            )

        return {"message": "User created successfully", "user": db_user}
    except Exception as e:
        # If there's an error (e.g., email already exists), raise an HTTP exception
        raise HTTPException(status_code=400, detail=str(e))


# Login endpoint
@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """
    Endpoint for user login.
    It takes UserLogin data and returns a Token if credentials are correct.
    """
    try:
        # Attempt to sign in the user using Supabase auth
        response = supabase.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        # Return the access token which will be used for authenticated requests
        return {"access_token": response.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Google Sign-In endpoint
@router.post("/google-signin")
async def google_sign_in():
    """
    Endpoint to initiate Google Sign-In.
    It returns a URL that the client should redirect to for Google authentication.
    """
    try:
        # Initiate the OAuth flow with Google as the provider
        response = supabase.auth.sign_in_with_oauth({"provider": "google"})
        return {"url": response.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Microsoft Sign-In endpoint
@router.post("/microsoft-signin")
async def microsoft_sign_in():
    """
    Endpoint to initiate Microsoft Sign-In.
    It returns a URL that the client should redirect to for Microsoft authentication.
    """
    try:
        # Initiate the OAuth flow with Microsoft Azure as the provider
        response = supabase.auth.sign_in_with_oauth({"provider": "azure"})
        return {"url": response.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Logout endpoint
@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Endpoint for user logout.
    It invalidates the provided access token.
    The token is automatically extracted from the Authorization header by the oauth2_scheme.
    """
    try:
        # Sign out the user using the provided token
        supabase.auth.sign_out(token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        # If there's any error during the logout process, return a 400 Bad Request error
        raise HTTPException(status_code=400, detail=f"Logout failed: {str(e)}")


# OAuth callback endpoint
@router.get("/callback")
async def oauth_callback(code: str):
    try:
        # Exchange the code for a session
        session = supabase.auth.exchange_code_for_session(code)

        # Get the user data
        user_data = session.user

        # Create or get the user in our database
        db_user = await create_oauth_user(user_data)

        return {"message": "Authentication successful", "user": db_user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Dependency to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    A dependency that can be used in other endpoints to get the current authenticated user.
    It validates the provided token and returns the user information.
    """
    try:
        # Get the user information from the token
        user = supabase.auth.get_user(token)
        return user
    except Exception as e:
        # If the token is invalid, raise an HTTP 401 Unauthorized exception
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
