# RE:BOOT 기능 명세서 (Updated)

## 1. 프로젝트 개요
**프로젝트명**: RE:BOOT (AI 기반 맞춤형 학습 플랫폼)
**목표**: AI 기반 콘텐츠 분석 및 대화형 피드백을 통해 개인의 커리어 목표와 학습 격차에 맞춘 개인화된 학습 경험을 제공합니다.

## 2. 시스템 아키텍처 및 데이터베이스 설계
본 프로젝트는 다음 기술 스택과 데이터베이스 모델을 기반으로 구현되었습니다.

### 2.1 기술 스택
- **Frontend**: Vue.js 3 (Composition API), Vite, Vue Router
- **Backend**: Django REST Framework (DRF)
- **Database**: PostgreSQL (pgvector 확장 사용)
- **AI/ML**: OpenAI GPT-4o, OpenAI `text-embedding-3-small` (임베딩)

### 2.2 데이터베이스 모델 (Backend Models)

#### 사용자 및 인증 (Users & Authentication)
- **User**: 기본 사용자 정보 (username, email, nickname).
  - 역할(Role): `STUDENT` (학생), `INSTRUCTOR` (강사), `ADMIN` (관리자).
- **UserProfile**: 사용자의 추가 정보 및 목표.
  - `career_goal`: `JOB_SEEKER` (취업 준비), `ENTREPRENEUR` (창업).
  - `preferences`: 학습 스타일 및 관심사 (JSON).
  - `portfolio_url`: 기존 포트폴리오 링크.

#### 학습 관리 (Learning Management) - `lectures`, `analytics` 앱
- **Course**: 강의/코스 정보 (예: "Web Development 101").
  - `category`: 프론트엔드, 백엔드 등.
- **Lecture**: 코스 내 개별 강의/세션.
  - `video_url`: 강의 영상 링크 (YouTube 등).
  - `original_script`: Whisper STT로 추출된 스크립트.
  - `embedding`: 벡터 검색을 위한 임베딩 데이터 (1536 차원).
  - `ai_status`: AI 처리 상태 (PENDING, PROCESSING, COMPLETED).
- **Curriculum**: 학생의 코스 등록 및 진행 상태 (Enrollment 역할).
  - `status`: ACTIVE, COMPLETED, DROPPED.
- **CurriculumItem**: 커리큘럼 내 개별 강의 진행도 추적.
  - `is_completed`: 강의 완료 여부.

#### AI 튜터 및 노트 (AI Tutor) - `ai_tutor` 앱
- **LectureNote**: 강의에 대한 AI 요약 및 노트.
  - `summary`: AI가 생성한 요약본.
  - `keywords`: 추출된 핵심 키워드.
- **AIChatSession**: 강의와 관련된 AI 튜터와의 채팅 세션.
- **AIChatMessage**: 채팅 메시지 (User/AI).

#### 평가 (Assessment) - `lectures` 앱
- **Quiz**: 강의별 자동 생성된 퀴즈.
  - `question`, `options`, `correct_answer`, `explanation`.
- **QuizAttempt**: 학생의 퀴즈 풀이 시도 및 결과.
  - `is_correct`: 정답 여부.

#### 커리어 및 포트폴리오 (Career & Assets) - `career`, `assets` 앱
- **Portfolio**: 사용자의 포트폴리오 문서.
  - `type`: RESUME (이력서), BUSINESS_PLAN (사업계획서).
  - `sections`: 섹션별 구조화된 데이터 (JSON).
  - `compiled_markdown`: 최종 생성된 마크다운 내용.
- **PortfolioProject**: 포트폴리오 내 프로젝트 항목.
- **SkillBlock**: 습득 가능한 스킬 단위.
- **UserSkill**: 사용자가 획득한 스킬 및 인증 출처.
- **InterviewPersona**: 모의 면접을 위한 AI 페르소나 (예: 기술 면접관, HR 담당자).
- **MockInterviewSession**: 모의 면접 세션.
  - `score`: 면접 점수.
  - `feedback_summary`: 종합 피드백.
- **MockInterviewMessage**: 면접 질의응답 내역.

---

## 3. 화면별 기능 명세 (Frontend Views)

### 3.1 대시보드 (`/dashboard`)
**목표**: 학습 진행 상황을 한눈에 파악하고 학습을 이어서 진행합니다.
- **주요 기능**:
  - **내 커리큘럼 (My Curriculums)**: 현재 진행 중인 `Curriculum` 목록 표시.
  - **진행률 (Progress)**: 각 코스 및 전체 학습 진행률 시각화.
  - **최근 활동**: 최근 수강한 `Lecture`로 바로 이동 ("이어하기").

### 3.2 강의실 (`/classroom/:id`)
**목표**: 동영상 강의 시청 및 AI 튜터링을 통한 딥러닝.
- **UI 구성**:
  - **비디오 플레이어**: `Lecture`의 `video_url` 재생.
  - **AI 튜터 채팅 (AIChat)**: 우측/플로팅 패널. 해당 강의(`Lecture`) 문맥에 기반한 Q&A (`AIChatSession`).
  - **스마트 노트 (LectureNote)**: 하단/탭. AI가 생성한 강의 요약(`summary`) 및 키워드 확인.
- **학습 완료**: 강의 시청 완료 시 `CurriculumItem` 상태 업데이트 -> 퀴즈로 이동.

### 3.3 퀴즈 (`/classroom/:id/quiz` - 모달 또는 섹션)
- **동작**: 강의 완료 후 `Quiz` 데이터 로드.
- **피드백**: 답안 제출(`QuizAttempt`) 즉시 정답/해설 표시.

### 3.4 포트폴리오 (`/portfolio`)
**목표**: 학습 이력을 바탕으로 취업/창업용 포트폴리오 생성.
- **기능**:
  - **포트폴리오 생성**: `Portfolio` 모델 생성 요청. (AI가 `UserSkill` 및 `PortfolioProject` 기반 작성).
  - **보기 및 편집**: 생성된 마크다운(`compiled_markdown`) 렌더링 및 수정.

### 3.5 모의 면접 (`/interview`)
**목표**: 생성된 포트폴리오를 기반으로 실전 면접 연습.
- **프로세스**:
  1.  **페르소나 선택**: `InterviewPersona` 목록에서 선택 (Tech Lead, HR 등).
  2.  **면접 진행 (`/interview/:session_id`)**: 채팅 인터페이스.
      - AI 질문 -> 사용자 답변 (텍스트/음성) -> `MockInterviewMessage` 저장.
  3.  **결과 피드백**: 면접 종료 후 `MockInterviewSession`의 점수(`score`) 및 피드백(`feedback_summary`) 확인.
