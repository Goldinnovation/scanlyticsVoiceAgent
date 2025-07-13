
from livekit import api 
from dotenv import load_dotenv
import os 




load_dotenv()


def create_JWT_Auth_Token():
    token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
        .with_identity("identity") \
        .with_name("name") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room="scanlyticsRoom-room",
        )).to_jwt()


    return token


if __name__ == "__main__":
    token = create_JWT_Auth_Token()
    print('token', token)
    