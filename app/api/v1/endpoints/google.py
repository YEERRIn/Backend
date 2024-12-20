# 구글 콘솔과 상호작용 관련
from fastapi import APIRouter, HTTPException, Depends, Request
import httpx
import json
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

### Access Token 받아오는 함수
# parameter - authorization code
# return - json type의 token_info 를 반환함
async def get_access_token(code):
    token_url = "https://oauth2.googleapis.com/token"

        # 클라이언트 구성 읽기
    with open("client_secret_639048076528-0mqbo91cf5t0fq5604u0tblqnaka8thp.apps.googleusercontent.com.json", "r") as f:
        client_config = json.load(f)["web"]

    token_data = {
        "code": code,
        "client_id": client_config["client_id"],
        "client_secret": client_config["client_secret"],
        "redirect_uri": "postmessage",  # 등록된 redirect_uri와 일치해야 함
        "grant_type": "authorization_code",
    }

    # 액세스 토큰 요청
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=token_data)  # 데이터는 body로 전송
        # response.raise_for_status()
        print("responose: ", response)
        print("Full Response Text: ", response.text)  # 서버에서 반환한 원본 데이터 출력
        return response.json()  # Access Token 포함된 응답 반환

    


### 캘린더 리스트 요청(캘린더 id 리스트를 받아야 함)
# parameter - authorization code
# return - json type의 calendar data
@router.get("/calendar-list")
async def get_calendar_data(token_info):
    # calendar list 요청
    client = httpx.AsyncClient()
    try:
        response = await client.get(
            "https://www.googleapis.com/calendar/v3/users/me/calendarList",
            headers={"Authorization": f"Bearer {token_info['access_token']}"}
        )
        response.raise_for_status()
        calender_list = response.json()
    finally:
        await client.aclose()  # 명시적으로 닫기

    return calender_list



@router.get("/events")
async def get_events_data(token_info, cal_id):
    # calendar events 데이터 요청
    client = httpx.AsyncClient()
    try:    
        response = await client.get(
            f"https://www.googleapis.com/calendar/v3/calendars/{cal_id}",
            headers={"Authorization": f"Bearer {token_info['access_token']}"}
        )
        response.raise_for_status()
        events_info = response.json()
    finally:
        await client.aclose()  # 명시적으로 닫기

    return events_info