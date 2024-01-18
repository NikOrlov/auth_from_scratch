from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserCreate, UserInDB
from models.jwt import TokenInfo
from services.user_service import UserService, get_user_service
from services.jwt_service import JWTService, get_jwt_service
from schemas.entity import User


#for getting auth token: 'Authorization: Bearer token'
http_bearer = HTTPBearer()

router = APIRouter()


def generate_user_token(user: User,
                        jwt_service: JWTService = Depends(get_jwt_service),) -> TokenInfo:
    payload = {'sub': str(user.id), 'login': user.login}
    access_token = jwt_service.encode_jwt(payload)
    token = jwt_service.create_token(access_token)
    return token


@router.post('/signup/', response_model=TokenInfo)
async def signup_user(user_model: UserCreate,
                      user_service: UserService = Depends(get_user_service),
                      jwt_service: JWTService = Depends(get_jwt_service),) -> TokenInfo:
    user = await user_service.create_user(user_model)
    token = generate_user_token(user, jwt_service)
    return token


@router.post('/signin/', response_model=TokenInfo)
async def signin_user(user_model: UserCreate,
                      user_service: UserService = Depends(get_user_service),
                      jwt_service: JWTService = Depends(get_jwt_service),) -> TokenInfo:
    user = await user_service.get_user_by_login(user_model.login)
    if not user or not user.check_password(user_model.password):
        raise HTTPException(status_code=400,
                            detail="Incorrect credentials")
    token = generate_user_token(user, jwt_service)
    return token


@router.get('/me/', response_model=UserInDB)
async def auth_self_info(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
) -> UserInDB:
    jwt_token = credentials.credentials
    try:
        payload = jwt_service.decode_jwt(jwt_token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=401,
                            detail=f'invalid token error: {e}')
    user = await user_service.get_user_by_login(payload['login'])
    return user
