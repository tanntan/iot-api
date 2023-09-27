from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
import uvicorn as uvicorn
from fastapi import FastAPI
from app.api.config import config as Config


app = FastAPI()


from app.api.resx.v1 import device_routes


# from api.resx.routes.v1 import products
from app.api.schemas.validator import BadRequestException, UnauthorizedException, ForbiddenException, NotFoundException, \
    CustomRequestValidationError

app = FastAPI(title="IOT API")


#
# origins = [
#     "*.ltlabs.co/*",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


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

# app.include_router(products.router)


if __name__ == '__main__':
    # uvicorn.run(app)
    uvicorn.run(app, host=Config.HOST or "127.0.0.1", port=Config.APP_PORT or 8882)