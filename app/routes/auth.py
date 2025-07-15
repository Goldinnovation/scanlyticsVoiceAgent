
import os 
from livekit import api 
from dotenv import load_dotenv
from fastapi import APIRouter, Request

router = APIRouter()

load_dotenv()


@router.get('/getToken')
async def create_JWT_Auth_Token(request: Request):
    token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
        .with_identity("identity") \
        .with_name("name") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room="scanlyticsRoom-room",
        )).to_jwt()


    return {"token": token}

