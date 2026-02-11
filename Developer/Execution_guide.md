# Re:Boot 서비스 실행 가이드 (Execution Guide)

이 문서는 Re:Boot 서비스의 백엔드(Django) 및 프론트엔드(Vue.js) 서버를 로컬 환경에서 실행하는 방법을 안내합니다.

## 1. 터미널에서 수동 실행 방법

### 백엔드 (Django) 서버 실행
1. 새 터미널을 열고 `backend` 디렉토리로 이동합니다.
   ```bash
   cd backend
   ```
2. 가상환경(venv)을 활성화합니다.
   ```bash
   # Windows (PowerShell/CMD)
   ..\venv\Scripts\activate
   ```
3. (필요 시) 데이터베이스 마이그레이션을 수행합니다.
   ```bash
   python manage.py migrate
   ```
4. 서버를 실행합니다.
   ```bash
   python manage.py runserver
   ```
   - 서버 주소: `http://127.0.0.1:8000/`

### 프론트엔드 (Vue.js) 서버 실행
1. 새 터미널을 열고 `frontend` 디렉토리로 이동합니다.
   ```bash
   cd frontend
   ```
2. 개발 서버를 실행합니다.
   ```bash
   npm run dev
   ```
   - 서버 주소: `http://localhost:5173/` (Vite 기본값)

---

## 2. 배치 파일(start.bat)을 이용한 자동 실행

루트 디렉토리에 있는 `start.bat` 파일을 실행하면 백엔드와 프론트엔드 서버가 각각 새로운 터미널 창에서 자동으로 실행됩니다.

**사용 방법:**
1. 프로젝트 루트 (`re_boot_NEW`) 폴더에서 `start.bat` 파일을 더블 클릭합니다.
2. 백엔드 창(Django)과 프론트엔드 창(Vite)이 각각 열리는지 확인합니다.

> [!IMPORTANT]
> **OpenAI API Key 설정**: 실행 전 `backend/.env` 파일에 유효한 `OPENAI_API_KEY`가 설정되어 있는지 반드시 확인하십시오.


---

## 3. Git Clone 후 초기 설정 방법 (필수)

다른 컴퓨터에서 프로젝트를 `clone` 또는 `pull` 받은 경우, `.gitignore`에 의해 제외된 설정 파일과 패키지들을 수동으로 복원해야 합니다.

### 1단계: 환경 변수 설정
`backend` 폴더 내에 `.env` 파일을 생성하고 다음 내용을 입력하세요.
(OpenAI API Key는 필수입니다.)
```bash
# backend/.env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 2단계: 백엔드 패키지 설치 및 DB 초기화
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r ..\Developer\requirements.txt
python manage.py migrate
```

### 3단계: 프론트엔드 패키지 설치
```bash
cd frontend
npm install
```

### 4단계: 실행
이제 `start.bat`을 실행하거나 위 1번의 수동 실행 방법을 따르세요.
