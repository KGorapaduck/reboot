
# Re:Boot 서비스 구현 계획

이 계획서는 `final_presentation.md`에 명시된 Re:Boot 서비스의 Frontend, Backend, Database 구축을 위한 상세 구현 계획입니다. 사용자의 학습 경험을 극대화하고 중도 포기를 방지하는 "페이스메이커" 역할을 수행하는 시스템을 목표로 합니다.

## 사용자 리뷰 필요 (User Review Required)

> [!IMPORTANT]
> **AI 모델 및 API 키 설정**: Whisper(STT) 및 GPT-4o(RAG) 사용을 위해 OpenAI API Key 설정이 필요합니다. `.env` 파일에 안전하게 관리해야 합니다.

> [!NOTE]
> **디자인 시스템**: Glassmorphism 디자인을 적용하기 위해 CSS 변수 및 공통 컴포넌트 설계가 중요합니다.

## 제안된 변경 사항 (Proposed Changes)

### 1. Database Schema (PostgreSQL with pgvector)

학습 데이터와 AI 기능을 지원하기 위한 데이터베이스 스키마를 설계합니다.

#### [NEW] ERD 설계
- **User / UserProfile**: 사용자 계정 및 성향 정보
- **Course / Lecture**: 강좌 및 강의 (기존 Lesson -> Lecture 변경)
- **LectureNote**: AI 생성 강의 요약 및 키워드 (기존 Notes -> LectureNote 변경)
- **AIChatSession / AIChatMessage**: 강의 문맥 기반 질의응답 세션
- **Curriculum / ReroutingLog**: 다이내믹 리라우팅 및 커리큘럼 관리 (기존 LearningLogs 확장)
- **Quiz / QuizAttempt**: 퀴즈 및 응시 이력
- **SkillBlock / UserSkill**: 스킬 획득 및 자산화 관리
- **Portfolio / Project**: 이력서 및 창업 아이템 생성 (확장됨)
- **MockInterview / InterviewPersona**: 페르소나 기반 모의 면접 세션 및 피드백

### 2. Backend (Django REST Framework)

대규모 트래픽 처리와 AI 기능 연동을 위한 백엔드 구조를 구축합니다.

#### [NEW] Django 앱 구조
- `core`: 공통 유틸리티 및 설정
- `users`: 사용자 인증 및 프로필 관리
- `lectures`: 강의 관리 및 스트리밍 지원
- `ai_tutor`: OpenAI API 연동, RAG 로직, STT 처리
- `analytics`: 학습 데이터 분석 및 다이내믹 리라우팅 로직
- `assets`: 스키마 블록 및 포트폴리오(이력서/창업) 생성 관리
- `career`: 모의 면접 및 커리어 코칭 기능 추가

#### [NEW] API Endpoints
- `POST /api/ai/stt/`: 음성 데이터 수신 및 텍스트 변환
- `POST /api/ai/chat/`: RAG 기반 질의응답
- `GET /api/re-route/`: 학습 상태 기반 커리큘럼 재설계 제안
- `POST /api/portfolio/resume/`: 스킬 블록 기반 이력서 자동 생성
- `POST /api/portfolio/startup/`: 창업 아이템 기획서 자동 생성
- `POST /api/career/interview/start/`: 모의 면접 세션 시작 (페르소나 선택)
- `POST /api/career/interview/chat/`: 면접관 페르소나와 대화


### 3. Frontend (Vue.js 3)

몰입감을 주는 Glassmorphism 디자인과 반응형 UI를 구현합니다.

#### [NEW] 프로젝트 구조
- `src/components/common`: GlassCard, GlassButton 등 공통 디자인 컴포넌트
- `src/views/HomeView`: 랜딩 페이지 (로그인 전 메인)
- `src/views/Auth`: 로그인/회원가입 (Student/Instructor 분리)
- `src/views/Dashboard`: 학습 현황, 리라우팅 알림
- `src/views/Classroom`: 강의 시청, 실시간 AI 노트, 챗봇 인터페이스
- `src/views/MyPage`: 스킬 블록 시각화, 포트폴리오 다운로드
- `src/views/Instructor`: 강의 업로드, STT/임베딩 상태 관리, 통계 (신규)
- `src/stores`: Pinia를 이용한 상태 관리 (User, Learning, AI)

#### [NEW] 주요 기능 구현
- **Real-time STT View**: WebSocket 또는 Polling을 통해 실시간 자막/노트 표시
- **Interactive Chat**: 문맥 인식 튜터와의 채팅 UI
- **Dynamic Dashboard**: 학습 진행도에 따른 동적 UI 변경

## 검증 계획 (Verification Plan)

### 자동화 테스트 (Automated Tests)
- `python manage.py test`: Django 유닛 테스트 (모델, 뷰, 시리얼라이저)
- `npm run test:unit`: Vue 컴포넌트 유닛 테스트

### 수동 검증 (Manual Verification)
1.  **회원가입/로그인**: 정상 동작 확인
2.  **강의 수강 시뮬레이션**:
    - 가상 음성 파일 업로드 -> STT 변환 확인
    - AI 튜터에게 질문 -> RAG 기반 답변 정확도 확인
3.  **리라우팅 테스트**: 임의로 진도율을 낮게 조작 -> "압축 패스트 트랙" 제안 팝업 확인
4.  **포트폴리오 생성**: 스킬 블록 누적 후 "생성" 버튼 클릭 -> 결과물 확인
