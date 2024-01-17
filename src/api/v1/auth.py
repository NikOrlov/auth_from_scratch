from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from models.entity import UserCreate, UserInDB
from schemas.entity import User
from services.user_service import UserService, get_user_service


router = APIRouter()


@router.post('/signup/', response_model=UserInDB)
async def signup_user(user_model: UserCreate,
                      user_service: UserService = Depends(get_user_service),) -> UserInDB:
    user = await user_service.create_user(user_model)
    return user


@router.post('/signin/', response_model=UserInDB)
async def signin_user(user_model: UserCreate,
                      user_service: UserService = Depends(get_user_service),) -> UserInDB:
    user = await user_service.get_user_by_login(user_model.login)
    if not user or not user.check_password(user_model.password):
        raise HTTPException(status_code=400,
                            detail="Incorrect credentials")
    return user
