from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.models.user import User
from app.api.services.auth_service import create_user, authenticate_user, create_access_token
from app.api.services.auth_service import get_current_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register")
async def register(user: User):
    """
    Register a new user.

    Args:
        user (User): The user object containing username, email, and password.

    Returns:
        dict: A dictionary containing the user's information and a success message.
    """
    try:
        # Validate user input (e.g., email format, password strength)
        if not user.email or not user.password:
            raise HTTPException(status_code=400, detail="Missing email or password")
        if not user.email.endswith("@example.com"):
            raise HTTPException(status_code=400, detail="Email must end with @example.com")

        # Hash password
        user.set_password(user.password)

        # Create user in database
        created_user = create_user(user)

        # Send confirmation email or token (optional)

        return {"user": created_user, "message": "User registered successfully"}
    except Exception as e:
        print(f"Failed to register user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login")
async def login(username: str, password: str):
    """
    Login a user and generate a JWT token.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: A dictionary containing the JWT token and a success message.
    """
    try:
        # Authenticate user
        user = authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Generate JWT token
        access_token = create_access_token(data={"sub": user.username})

        return {"access_token": access_token, "token_type": "bearer", "message": "Login successful"}
    except Exception as e:
        print(f"Failed to login user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/me", dependencies=[Depends(get_current_user)])
async def get_current_user(current_user: User = Depends(get_current_user)):
    """
    Get the current logged-in user's information.

    Args:
        current_user (User): The current logged-in user object.

    Returns:
        dict: A dictionary containing the user's information.
    """
    return {"user": current_user}

