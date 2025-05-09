from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta
import random

from passlib.context import CryptContext
from jose import JWTError, jwt
from config.db import db
from config.jwt import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")

collection = db.users
router = APIRouter(prefix="/api/users", tags=["Users"])


class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    email: str
    phone: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await collection.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception

    if "password" in user:
        del user["password"]
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("disabled", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/", status_code=201)
async def create_user(user: User):
    existing_user = await collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(user.password)
    background_color = "%06x" % random.randint(0, 0xFFFFFF)

    new_user = {
        "_id": str(uuid4()),
        "firstname": user.firstname,
        "lastname": user.lastname,
        "username": user.username,
        "password": hashed_password,
        "email": user.email,
        "phone": user.phone,
        "thumbnail": f"https://ui-avatars.com/api/?background={background_color}&color=fff&name={user.firstname}+{user.lastname}&size=256",
        "date_created": str(datetime.now()),
        "is_admin": False,
        "disabled": False,
    }

    try:
        await collection.insert_one(new_user)
        return {"detail": "User Created Successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=dict)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user


@router.put("/{user_id}", status_code=201)
async def update_user(
    user_id: str,
    updated_user: User,
    current_user: dict = Depends(get_current_active_user),
):
    if current_user["_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    if updated_user.username != current_user["username"]:
        existing_user = await collection.find_one({"username": updated_user.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )

    update_data = {
        "firstname": updated_user.firstname,
        "lastname": updated_user.lastname,
        "username": updated_user.username,
        "email": updated_user.email,
        "phone": updated_user.phone,
    }

    result = await collection.update_one({"_id": user_id}, {"$set": update_data})

    if not result.modified_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID: {user_id} was not found",
        )

    updated_user_data = await collection.find_one({"_id": user_id})
    if "password" in updated_user_data:
        del updated_user_data["password"]

    return updated_user_data
