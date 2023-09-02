from src.drive.models import Trips

def book_drive(drive_id: int, user_id: int):
    drive = Trips.get_by_id(drive_id)
    if drive.driver.id == user_id:
        return {"status": "You can't book your own drive"}
    return {"status": "Successfully booked"}

def confirm_drive(drive_id: int, user_id: int):
    drive = Trips.get_by_id(drive_id)
    if drive.driver.id != user_id:
        return {"status": "You can't confirm this drive"}
    drive.is_confirmed = True
    drive.save()
    return {"status": "Successfully confirmed"}
