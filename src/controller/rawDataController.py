from fastapi import APIRouter, Depends, Request
from services import RawData
router = APIRouter()

@router.post('/raw')
async def chat(message: Request):
    try:
        RawData.raw_service()
    except ValueError as e:
        print('we will not catch exception: Exception')

        
    return {
        "message": "Thanhf coong"
    } 