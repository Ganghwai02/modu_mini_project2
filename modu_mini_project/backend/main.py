import json
import re
import requests
import uvicorn
import traceback
import os
from fastapi import FastAPI, status, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid

app = FastAPI()

# Pydantic 모델 정의
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

class Message(BaseModel):
    role: str
    content: str

class InterviewRequest(BaseModel):
    chatHistory: List[Message]
    jobTitle: str = None

class FeedbackRequest(BaseModel):
    chatHistory: List[Message]

class ChatRequest(BaseModel):
    chatHistory: List[Message]

class SaveInterviewRequest(BaseModel):
    jobTitle: str
    chatHistory: List[Message]
    
# 면접 기록 삭제를 위한 고유 ID를 포함하는 모델
class InterviewRecord(BaseModel):
    id: str
    jobTitle: str
    chatHistory: List[Message]

class DeleteInterviewRequest(BaseModel):
    id: str

# CORS 설정: 프론트엔드 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI API URL
OPENAI_API_URL = "https://dev.wenivops.co.kr/services/openai-api"

# 파일 기반 데이터베이스 경로
DB_FILE = "interviews.json"

@app.post("/api/auth/login")
async def login(login_request: LoginRequest):
    try:
        return JSONResponse(
            content={"message": "로그인 성공", "token": "fake-jwt-token"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print("로그인 엔드포인트에서 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={"message": f"서버 오류: {e}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/api/auth/register")
async def register(register_request: RegisterRequest):
    try:
        return JSONResponse(
            content={"message": "회원가입 성공", "email": register_request.email},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        print("회원가입 엔드포인트에서 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={"message": f"서버 오류: {e}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/api/interview/question")
async def get_interview_question(interview_request: InterviewRequest):
    try:
        chat_history = interview_request.chatHistory
        job_title = interview_request.jobTitle
        messages_to_send = [msg.dict() for msg in chat_history]

        if job_title:
            system_prompt = {
                "role": "system",
                "content": f"당신은 {job_title} 역할에 대한 전문 면접관입니다. 한 번에 하나의 면접 질문만 하세요. 답변이나 피드백은 제공하지 마세요. {job_title}에 대한 관련 질문만 하세요. 모든 응답은 한국어로 해주세요."
            }
            messages_to_send = [system_prompt] + messages_to_send
        
        response = requests.post(
            OPENAI_API_URL,
            json=messages_to_send,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        response.raise_for_status()
        api_response = response.json()
        
        if not api_response.get('choices'):
            raise HTTPException(status_code=500, detail='API 응답 형식이 올바르지 않습니다.')

        question = api_response['choices'][0]['message']['content']
        return JSONResponse(
            content={'question': question},
            status_code=status.HTTP_200_OK
        )

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
        return JSONResponse(
            content={'message': '외부 API에서 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'},
            status_code=http_err.response.status_code if http_err.response is not None else 500
        )
    except requests.exceptions.ConnectionError as conn_err:
        print(f"연결 오류 발생: {conn_err}")
        return JSONResponse(
            content={'message': '네트워크 연결 상태를 확인해주세요.'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except requests.exceptions.Timeout as timeout_err:
        print(f"시간 초과 오류 발생: {timeout_err}")
        return JSONResponse(
            content={'message': '요청 시간이 초과되었습니다. 다시 시도해 주세요.'},
            status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except Exception as e:
        print("질문 엔드포인트에서 예기치 않은 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={'message': f'서버 오류: {e}'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/api/interview/feedback")
async def get_feedback(feedback_request: FeedbackRequest):
    try:
        chat_history = feedback_request.chatHistory
        messages_to_send = [msg.dict() for msg in chat_history]

        # AI에게 JSON 형식으로 응답을 요청하는 시스템 프롬프트
        system_prompt = {
            "role": "system",
            "content": "당신은 전문 면접관입니다. 사용자의 마지막 답변에 대한 피드백을 JSON 형식으로만 제공해주세요. 형식은 엄격하게 지켜주세요. 예를 들어, {\"feedback\": \"피드백 내용\", \"score\": 85, \"status\": \"통과\"} 또는 {\"feedback\": \"피드백 내용\", \"score\": 50, \"status\": \"실패\"}와 같이 응답하세요. score는 0에서 100 사이의 정수여야 합니다. feedback은 답변의 명확성, 관련성, 깊이에 대해 설명해주세요."
        }
        updated_chat_history = [system_prompt] + messages_to_send

        response = requests.post(
            OPENAI_API_URL,
            json=updated_chat_history,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        response.raise_for_status()
        api_response = response.json()
        
        if not api_response.get('choices'):
            raise HTTPException(status_code=500, detail='API 응답 형식이 올바르지 않습니다.')

        full_content = api_response['choices'][0]['message']['content']
        
        try:
            feedback_data = json.loads(full_content)
            feedback = feedback_data.get('feedback', '')
            score = feedback_data.get('score', 0)
            status_text = feedback_data.get('status', '실패')

            return JSONResponse(
                content={'feedback': feedback, 'score': score, 'status': status_text},
                status_code=status.HTTP_200_OK
            )
        except json.JSONDecodeError:
            print(f"JSON 파싱 오류: AI 응답이 유효한 JSON이 아닙니다. 응답: {full_content}")
            return JSONResponse(
                content={'feedback': '피드백을 생성하는 중 오류가 발생했습니다.', 'score': 0, 'status': '실패'},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
        return JSONResponse(
            content={'message': '외부 API에서 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'},
            status_code=http_err.response.status_code if http_err.response is not None else 500
        )
    except requests.exceptions.ConnectionError as conn_err:
        print(f"연결 오류 발생: {conn_err}")
        return JSONResponse(
            content={'message': '네트워크 연결 상태를 확인해주세요.'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except requests.exceptions.Timeout as timeout_err:
        print(f"시간 초과 오류 발생: {timeout_err}")
        return JSONResponse(
            content={'message': '요청 시간이 초과되었습니다. 다시 시도해 주세요.'},
            status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except Exception as e:
        print("피드백 엔드포인트에서 예기치 않은 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={'message': f'서버 오류: {e}'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@app.post("/api/interview/chat")
async def get_general_chat_response(chat_request: ChatRequest):
    try:
        messages_to_send = [msg.dict() for msg in chat_request.chatHistory]
        system_prompt = {
            "role": "system",
            "content": "당신은 도움이 되는 AI 어시스턴트입니다. 사용자의 질문에 한국어로 친절하게 답변해주세요."
        }
        messages_to_send = [system_prompt] + messages_to_send

        response = requests.post(
            OPENAI_API_URL,
            json=messages_to_send,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        response.raise_for_status()
        api_response = response.json()
        
        if not api_response.get('choices'):
            raise HTTPException(status_code=500, detail='API 응답 형식이 올바르지 않습니다.')

        chat_response = api_response['choices'][0]['message']['content']
        return JSONResponse(
            content={'response': chat_response},
            status_code=status.HTTP_200_OK
        )
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 오류 발생: {http_err}")
        return JSONResponse(
            content={'message': '외부 API에서 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.'},
            status_code=http_err.response.status_code if http_err.response is not None else 500
        )
    except requests.exceptions.ConnectionError as conn_err:
        print(f"연결 오류 발생: {conn_err}")
        return JSONResponse(
            content={'message': '네트워크 연결 상태를 확인해주세요.'},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except requests.exceptions.Timeout as timeout_err:
        print(f"시간 초과 오류 발생: {timeout_err}")
        return JSONResponse(
            content={'message': '요청 시간이 초과되었습니다. 다시 시도해 주세요.'},
            status_code=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except Exception as e:
        print("채팅 엔드포인트에서 예기치 않은 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={'message': f'서버 오류: {e}'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.post("/api/interviews/save")
async def save_interview(request: SaveInterviewRequest):
    try:
        interview_data = request.dict()
        interview_data['id'] = str(uuid.uuid4())
        with open(DB_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(interview_data, ensure_ascii=False) + "\n")
        return JSONResponse(
            content={"message": "면접 기록이 성공적으로 저장되었습니다."},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print("면접 기록 저장 중 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={"message": "면접 기록 저장에 실패했습니다."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/api/interviews")
async def get_interviews(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    try:
        if not os.path.exists(DB_FILE):
            return JSONResponse(content={"interviews": [], "total_count": 0}, status_code=status.HTTP_200_OK)
        
        interviews = []
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for line in f:
                interviews.append(json.loads(line))
        
        interviews.reverse()

        total_count = len(interviews)
        
        start_index = (page - 1) * size
        end_index = start_index + size
        paginated_interviews = interviews[start_index:end_index]

        return JSONResponse(
            content={"interviews": paginated_interviews, "total_count": total_count},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print("면접 기록 불러오기 중 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={"message": "면접 기록 불러오기에 실패했습니다."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.get("/api/interviews/{interview_id}")
async def get_interview_detail(interview_id: str):
    try:
        if not os.path.exists(DB_FILE):
            return JSONResponse(content={"message": "기록이 없습니다."}, status_code=status.HTTP_404_NOT_FOUND)
        
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for line in f:
                interview = json.loads(line)
                if interview.get('id') == interview_id:
                    return JSONResponse(
                        content={"interview": interview},
                        status_code=status.HTTP_200_OK
                    )
        
        return JSONResponse(
            content={"message": "면접 기록을 찾을 수 없습니다."},
            status_code=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print("면접 기록 상세 불러오기 중 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={"message": "면접 기록 상세 불러오기에 실패했습니다."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@app.delete("/api/interviews/delete/{interview_id}")
async def delete_interview(interview_id: str):
    try:
        if not os.path.exists(DB_FILE):
            return JSONResponse(content={"message": "기록이 없습니다."}, status_code=status.HTTP_404_NOT_FOUND)
        
        interviews = []
        with open(DB_FILE, "r", encoding="utf-8") as f:
            for line in f:
                interviews.append(json.loads(line))
        
        new_interviews = [i for i in interviews if i.get('id') != interview_id]
        
        if len(new_interviews) == len(interviews):
            return JSONResponse(content={"message": "삭제할 기록을 찾을 수 없습니다."}, status_code=status.HTTP_404_NOT_FOUND)

        with open(DB_FILE, "w", encoding="utf-8") as f:
            for interview in new_interviews:
                f.write(json.dumps(interview, ensure_ascii=False) + "\n")
        
        return JSONResponse(
            content={"message": "면접 기록이 성공적으로 삭제되었습니다."},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        print("면접 기록 삭제 중 오류 발생:", e)
        traceback.print_exc()
        return JSONResponse(
            content={"message": "면접 기록 삭제에 실패했습니다."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        open(DB_FILE, "w").close()
    uvicorn.run(app, host="127.0.0.1", port=8000)