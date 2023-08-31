from fastapi import APIRouter
from src.drive.utils import book_drive, confirm_drive

router = APIRouter(
    prefix='/Drives',
    tags=['Drives']
)


@router.post("/book_drive/{drive_id}")
async def book_drive_endpoint(drive_id: int, user_id: int):
    return book_drive(drive_id, user_id)


@router.post("/confirm_drive/{drive_id}")
async def confirm_drive_endpoint(drive_id: int, user_id: int):
    return confirm_drive(drive_id, user_id)
