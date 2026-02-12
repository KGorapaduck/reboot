# Re:Boot 서비스 실행 가이드 (Execution Guide)

이 문서는 Re:Boot 서비스의 백엔드(Django) 및 프론트엔드(Vue.js) 서버를 로컬 환경에서 실행하고 테스트하는 방법을 안내합니다.

## 1. 자동 실행 (권장)

루트 디렉토리(`re_boot_NEW`)의 **`start.bat`** 파일을 더블 클릭하십시오.
- **Backend**: `http://127.0.0.1:8000/`에서 실행됩니다.
- **Frontend**: `http://localhost:5173/`에서 실행됩니다.

> [!IMPORTANT]
> 실행 전 `backend/.env` 파일에 `OPENAI_API_KEY`가 설정되어 있는지 확인하세요.

---

## 2. 수동 실행 방법

### 백엔드 (Backend)
```bash
cd backend
..\venv\Scripts\activate
python manage.py migrate
python manage.py runserver
```

### 프론트엔드 (Frontend)
```bash
cd frontend
npm install # 최초 1회
npm run dev
```

---

## 3. 주요 기능 테스트 접근 경로 (Frontend Routes)

웹 브라우저에서 `http://localhost:5173` 접속 후 다음 경로들을 테스트할 수 있습니다.
(현재 백엔드 연동 전이므로 Mock Data로 동작합니다.)

| 기능 | 경로 | 설명 |
|---|---|---|
| **대시보드** | `/dashboard` | 학습 진행 현황, 최근 강의 이어하기 |
| **강의실** | `/classroom` | 동영상 플레이어, AI 튜터 채팅, 강의 노트 |
| **포트폴리오** | `/portfolio` | [NEW] 스킬 기반 포트폴리오 목록 및 미리보기 |
| **모의 면접** | `/interview` | [NEW] 면접관 페르소나 선택 및 채팅 면접 |
| **마이페이지** | `/mypage` | [NEW] 프로필 정보 및 획득 스킬 배지 확인 |

## 4. 문제 해결 (Troubleshooting)

- **로그인 오류**: 현재는 데모 버전이므로 로그인 없이도 일부 페이지(`HomeView`) 접근 후 `Dashboard`로 이동 가능하도록 설정될 수 있습니다. (또는 수동으로 URL 입력)
- **모듈 없음 오류**: `frontend` 폴더에서 `npm install`을 실행했는지 확인하세요.
- **포트 충돌**: 8000번 또는 5173번 포트가 사용 중인지 확인하세요.
