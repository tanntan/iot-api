from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from app.api.config.config import BaseConfig 
from app.api.resx.v1 import auth_routes
from app.api.resx.v1 import rpm_routes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

from app.api.resx.v1 import device_routes


# from api.resx.routes.v1 import products
from app.api.schemas.validator import BadRequestException, UnauthorizedException, ForbiddenException, NotFoundException, \
    CustomRequestValidationError

app = FastAPI(title="IOT API")


#
origins = [
    "*.ltlabs.co/*",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Middleware to check authentication
# @app.middleware("http")
# async def auth_middleware(request, call_next):
#     if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json") or request.url.path.startswith("/api/v1/auth/verifyToken"):
#         return await call_next(request)
#     if "authorization" in request.headers:
#         auth_method, auth_token = request.headers["authorization"].split(" ")
#         lang = request.headers.get("lang", "en")
#         if auth_method == "Bearer" and auth_token:
#             decrypted = verify_token(auth_token)
#             if decrypted["success"]:
#                 request.scope["lang"] = lang
#                 request.scope["userData"] = decrypted["data"]
#                 await next()
#             else:
                
#                 raise HTTPException(status_code=401, detail=f"Invalid authorization token {BaseConfig.APP_NAME} {BaseConfig.APP_MODE}")
#         else:
#             raise HTTPException(status_code=401, detail=f"Invalid authorization token {BaseConfig.APP_NAME} {BaseConfig.APP_MODE}")
#     else:
#         raise HTTPException(status_code=401, detail=f"Authorization header missing {BaseConfig.APP_NAME} {BaseConfig.APP_MODE}")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# @app.get('/protected', dependencies=[Depends(auth_middleware)])
# async def protected_route():
#     return {"message": "This is a protected route"}

# def verify_token(token):
#     try:
#         print(BaseConfig.SECRET_KEY)
#         payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
#         # Perform additional token verification logic if needed
#         return {"success": True, "data": payload}
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
   

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=CustomRequestValidationError().status_code,
                        content={"detail": CustomRequestValidationError().detail})
app.include_router(device_routes.router)
app.include_router(auth_routes.router)
app.include_router(rpm_routes.router)
# app.include_router(products.router)


if __name__ == '__main__':
    # uvicorn.run(app)
    uvicorn.run(app, host=BaseConfig.HOST or "127.0.0.1", port=BaseConfig.APP_PORT or 8882)