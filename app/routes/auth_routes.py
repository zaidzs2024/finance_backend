from fastapi import APIRouter, HTTPException
from app.database import users_collection
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(400, "User already exists")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["isActive"] = True

    await users_collection.insert_one(user_dict)

    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({
        "id": str(db_user["_id"]),
        "role": db_user["role"]
    })

    return {"access_token": token}