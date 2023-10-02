from fastapi import APIRouter

from app.api.schemas.auth import User, UserLogin

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    '/verifyToken',
    response_description="Returns user access token",
    summary="Authenticate API user",
    description="Authenticate an API user and return a token for subsequent requests"
)
async def get_token(user: UserLogin):
    # authenticated_user = default.all()
    return {"message": "Login successful", "user": 'ura'}