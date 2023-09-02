from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from fastapi import FastAPI
from src.auth.routers import router as auth_router
from src.drive.routers import router as drive_router
from src.regions.routers import router as regions_router


app = FastAPI(
    title='Ride Sharing Service'
)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


app.include_router(auth_router)
app.include_router(drive_router)
app.include_router(regions_router)
