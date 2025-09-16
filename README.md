# 🤖AI 면접 준비 도우미🤖
<img width="1903" height="940" alt="Image" src="https://github.com/user-attachments/assets/0b73bcb5-6bdd-4f9f-95c4-3549e4511a12" />


# 나의 프로젝트 설명
면접 준비 도우미는 일반 회사 , 대기업 ,중소기업 등 면접을 연습하고, 어느부분이 미숙하고 부족한지 피드백을 해주는 서비스입니다. 사용자들은 로그인 , 회원가입 후에 직무를 선택하고 곧 바로 면접 연습을 할 수 있습니다. 모든 면접 내용은 사용자의 별도로 저장이 되어 참고 할수 있도록 전에 면접 내용을 불러와서 다시 확인 할 수 있습니다.

## 🚀 주요 기능
-   **면접 질문**: 사용자가 설정한 직무에 맞는 맞춤형 면접 질문을 제공합니다.
-   **실시간 피드백**: 답변에 대한 명확성, 관련성, 깊이 등을 기준으로 상세한 피드백과 점수를 제공합니다.
-   **면접 기록**: 과거에 진행했던 모든 면접 기록을 저장하고 다시 불러와 복기할 수 있습니다.
-   **사용자 관리**: 회원가입 및 로그인을 통해 개인별 면접 기록을 관리할 수 있습니다.

## 🛠️ 기술 스택

### 백엔드 (Backend)
- **Python**: FastAPI
- **AI API**: OpenAI API
- **데이터베이스**: File-based (JSON)

### 프론트엔드 (Frontend)
- **JavaScript**: React.js
- **상태 관리**: React Hooks (useState, useEffect)
- **라우팅**: React Router DOM
- **스타일링**: CSS

# WBS (Work Breakdown Structure)
1일차(9/12금요일) -프로젝트 설계 및 환경 구축 오전(09:00-12:00) 1.1프로젝트 계획 수립 1.1.1핵심 기능 정의(MVP범위 설정) 1.1.2기술 스택 최종 결정 1.1.3간단한 와이어프레임 스케치 오후(13:00-18:00) 1.2개발 환경 구축 1.2.1프론트엔드 프로젝트 초기화(React/Vue선택) 1.2.2백엔드 프로젝트 초기화(Node.js/Express권장) 1.2.3데이터베이스 연결 설정(SQLite/MySQL) 1.2.4 Git저장소 설정 및 초기 커밋 1.3외부API연동 준비 1.3.1 ChatGPT API키 설정 및 테스트 1.3.2기본API호출 테스트 코드 작성 1일차 목표 산출물 [ ]개발 환경 완료 [ ] ChatGPT API연동 테스트 성공 [ ]기본 프로젝트 구조 완성  

2일차(9/13토요일) -백엔드 핵심 기능 구현 오전(09:00-12:00) 2.1데이터베이스 설계 및 구현 2.1.1사용자(Users)테이블 생성 2.1.2면접세션(Interviews)테이블 생성 2.1.3질문답변(QnA)테이블 생성 2.1.4기본 데이터 삽입 오후(13:00-18:00) 2.2인증 시스템 구현 2.2.1회원가입API 2.2.2로그인API 2.2.3 JWT토큰 인증(간단한 버전) 2.2.4미들웨어 설정 2.3기본 면접API구현 2.3.1면접 세션 생성API 2.3.2 ChatGPT질문 생성API 2.3.3답변 저장API 2.3.4기본 피드백 생성API 2일차 목표 산출물 [ ]데이터베이스 완성 [ ]로그인/회원가입 기능 완료 [ ] ChatGPT연동API완료  

3일차(9/14일요일) -프론트엔드 기본 구현 오전(09:00-12:00) 3.1기본 레이아웃 구성 3.1.1헤더/네비게이션 컴포넌트 3.1.2기본 페이지 라우팅 설정 3.1.3반응형 레이아웃 기본 구조 오후(13:00-18:00) 3.2인증 관련 페이지 3.2.1로그인 페이지 3.2.2회원가입 페이지 3.2.3인증 상태 관리(Context/Vuex) 3.3메인 대시보드 3.3.1메인 페이지UI 3.3.2면접 시작 버튼 및 설정 3.3.3기본적인 스타일링(CSS/Tailwind) 3일차 목표 산출물 [ ]로그인/회원가입 화면 완료 [ ]메인 대시보드UI완료 [ ]기본 라우팅 및 상태 관리 완료  

4일차(9/15월요일) -핵심 면접 기능 구현 오전(09:00-12:00) 4.1면접 진행 페이지 4.1.1면접 시작 페이지(직무 선택) 4.1.2질문 표시 컴포넌트 4.1.3답변 입력 폼(텍스트에리어) 오후(13:00-18:00) 4.2 API연동 및 실시간 기능 4.2.1프론트엔드-백엔드API연동 4.2.2질문 생성 요청 및 표시 4.2.3답변 제출 및 피드백 받기 4.2.4로딩 상태 처리 4.3결과 화면 구현 4.3.1피드백 결과 표시 페이지 4.3.2면접 완료 처리 4.3.3다시하기 기능 4일차 목표 산출물 [ ]면접 진행 플로우 완료 [ ] ChatGPT와의 실시간 질답 기능 완료 [ ]피드백 표시 기능 완료  

5일차(9/16화요일) -완성 및 배포 오전(09:00-12:00) 5.1히스토리 기능 구현 5.1.1면접 히스토리 조회API 5.1.2히스토리 목록 페이지 5.1.3이전 면접 결과 상세 보기 오후(13:00-16:00) 5.2최종 테스트 및 버그 수정 5.2.1전체 기능 테스트 5.2.2 UI/UX개선 5.2.3에러 처리 보완 5.2.4반응형 디자인 점검 마감 전(16:00-18:00) 5.3배포 및 문서화 5.3.1간단한 배포(Vercel + Railway/Heroku) 5.3.2 README작성 5.3.3프로젝트 데모 준비 5.3.4최종 점검 및 제출 준비 5일차 목표 산출물 [ ]히스토리 기능 완료 [ ]전체 시스템 테스트 완료 [ ]배포 완료 및 문서화


# 와이어 프레임
<img width="1911" height="1079" alt="Image" src="https://github.com/user-attachments/assets/3264c719-f4b3-4dd6-9a71-c8580d00ab10" />

<img width="1918" height="1072" alt="Image" src="https://github.com/user-attachments/assets/440e030a-7fc4-43e7-a13f-6ca72db47264" />

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/80c3f871-a538-4440-9da3-509d0137577d" />

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/b49d37dd-6d26-46cf-a375-9b4b4440e399" />

<img width="1919" height="1079" alt="Image" src="https://github.com/user-attachments/assets/02868097-6521-4c49-8376-3e6392f8d71f" />

# 프로젝트 폴더 구조
<img width="298" height="774" alt="Image" src="https://github.com/user-attachments/assets/2e0c0f61-5784-466f-bdfb-ca71cfdbc024" />


## 💻 설치 및 실행 방법
### 1. 프로젝트 클론하기
# 터미널을 열고 아래 명령어를 입력하여 프로젝트를 로컬 컴퓨터에 복제합니다.
```bash
git clone [https://github.com/Ganghwai02/modu_mini_project2.git]
cd modu_mini_project2

### 2. 백엔드 설정 (FastAPI)
# 프로젝트 폴더 내의 back 디렉터리로 이동하여 백엔드 환경을 설정합니다.
```bash
cd backend
pip install -r requirements.txt
python main.py
- pip install -r requirements.txt 명령은 프로젝트에 필요한 모든 파이썬 라이브러리(FastAPI, uvicorn, pydantic 등)를 자동으로 설치해줍니다.

- 서버는 http://127.0.0.1:8000에서 실행됩니다.

### 3. 프론트엔드 설정 (React)
# 백엔드와는 별개로, front 디렉터리에서 프론트엔드를 실행해야 합니다.
```bash
# 터미널에서 상위 폴더로 이동
cd ../front
npm install
npm start
- npm install 명령은 package.json 파일에 정의된 모든 자바스크립트 라이브러리(React, React Router DOM, axios 등)를 설치합니다.

- npm start 명령은 개발 서버를 시작하며, 웹 브라우저가 자동으로 열려 http://localhost:3000에서 애플리케이션을 볼 수 있습니다.