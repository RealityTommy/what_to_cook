# Function to serialize a single user object
def individual_serial(user) -> dict:
    # Convert a user object into a dictionary
    # This is useful for converting database objects to JSON-serializable format
    return {
        # Convert the database '_id' to a string 'id'
        "id": str(user["_id"]),
        # Use the unique identifier
        "uid": str(user["_uid"]),
        # Include the user's first name
        "first_name": user["first_name"],
        # Use the user's email address
        "email": user["email"],
        # Include the admin status
        "is_admin": user["is_admin"],
    }


# Function to serialize a list of user objects
def list_serial(users) -> list:
    # Convert a list of user objects into a list of dictionaries
    # This is useful when you need to return multiple users, like in a 'get all users' endpoint
    return [individual_serial(user) for user in users]
