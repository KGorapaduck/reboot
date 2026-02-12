# Re:Boot 구현 현황 (Implementation Status)

## 📅 현재 상태 (Current Status)
- **Frontend**: 주요 UI/UX 뷰(`Dashboard`, `Classroom`, `Portfolio`, `Interview`, `MyPage`) 구현 완료 (Mock Data 기반).
- **Backend**: Django 모델 설계 및 마이그레이션 완료 (`User`, `Course`, `Lecture`, `Portfolio`, `Interview` 등).
- **Intergration**: 프론트엔드와 백엔드 간의 API 연동은 아직 진행되지 않음.

## ✅ 구현 완료된 기능 (Completed Features)

### 1. Frontend (Vue.js)
| 컴포넌트 | 경로 | 기능 설명 | 상태 |
|---|---|---|---|
| **Dashboard** | `/dashboard` | 학습 진행률 시각화, 최근 강의 바로가기 | ✅ 구현 완료 (Mock) |
| **Classroom** | `/classroom/:id` | 동영상 플레이어, 커리큘럼 사이드바, 탭(채팅/노트) | ✅ 구현 완료 (Mock) |
| **Portfolio** | `/portfolio` | 포트폴리오 목록 조회, 상세 내용 미리보기 | ✅ 구현 완료 (Mock) |
| **Interview** | `/interview` | 면접관 페르소나 선택, 채팅 UI, 타이머 | ✅ 구현 완료 (Mock) |
| **MyPage** | `/mypage` | 프로필 정보, 스킬 배지 목록 | ✅ 구현 완료 (Mock) |

### 2. Backend (Django Models)
| 앱 (App) | 모델 (Models) | 설명 | 상태 |
|---|---|---|---|
| **users** | `User`, `UserProfile` | 사용자 계정 및 확장 프로필 | ✅ 정의 완료 |
| **lectures** | `Course`, `Lecture` | 강의 콘텐츠 및 메타데이터 | ✅ 정의 완료 |
| **ai_tutor** | `AIChatSession`, `LectureNote` | AI 튜터링 세션 및 노트 | ✅ 정의 완료 |
| **career** | `InterviewPersona`, `MockInterviewSession` | 모의 면접 관련 데이터 | ✅ 정의 완료 |
| **assets** | `Portfolio`, `UserSkill` | 포트폴리오 및 스킬 자산 | ✅ 정의 완료 |

## 🚀 향후 계획 (Next Steps)

### 1. Backend API 구현 (Priority: High)
- [ ] **Auth API**: 회원가입, 로그인, 토큰 발급 (JWT).
- [ ] **Content API**: 강의 목록, 상세 조회, 진도율 업데이트.
- [ ] **AI API**:
    - RAG 기반 `chat` 엔드포인트 구현 (OpenAI 연동).
    - STT 결과 저장 및 조회.
    - 면접 페르소나 프롬프트 로직 구현.

### 2. Frontend-Backend 연동 (Priority: Medium)
- [ ] **Axios 설정**: Mock Data 제거 및 실제 API 호출로 변경.
- [ ] **State Management**: Pinia 스토어를 이용한 전역 상태 관리 (유저 정보, 학습 상태).

### 3. AI 기능 고도화 (Priority: Low)
- [ ] **Vector Search**: PostgreSQL `pgvector`를 이용한 강의 내용 검색.
- [ ] **Real-time Feedback**: 면접 종료 후 AI 피드백 생성.
