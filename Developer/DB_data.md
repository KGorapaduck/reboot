# 고급 학습 기능 데이터 설계 (Table 추가 없음)

사용자의 요청에 따라 **새로운 테이블을 추가하지 않고**, 기존 테이블(`Lecture`, `Curriculum`, `CurriculumItem`)에 **JSON 필드**를 추가하여 모든 기능을 유연하게 구현하는 설계입니다.

이 방식은 스키마 변경을 최소화하면서도 NoSQL처럼 유연하게 데이터를 관리할 수 있는 장점이 있습니다.

## 1. `Lecture` 모델 확장
강의 콘텐츠 자체에 포함되어야 하는 정적 데이터(스크립트, 체크포인트, 보충자료)를 모두 `Lecture` 테이블에 통합합니다.

### 추가 필드
- **`script_segments` (JSONField)**
    - **역할**: 핀포인트 지식 검색을 위한 스크립트 분절 데이터.
    - **구조**:
      ```json
      [
        {
          "start": 0, "end": 60,
          "content": "리액트의 가상돔 개념 설명...",
          "keywords": ["Virtual DOM", "Rendering"]
        },
        ...
      ]
      ```

- **`checkpoints` (JSONField)**
    - **역할**: 강의 중간 점검을 위한 체크포인트 및 퀴즈.
    - **구조**:
      ```json
      [
        {
          "id": "cp_1",
          "time_point": 120,
          "question": "가상돔의 역할은?",
          "is_critical": true,
          "options": ["...", "..."],
          "answer": 1
        }
      ]
      ```

- **`supplemental_materials` (JSONField)**
    - **역할**: 학습 부진 시 제공할 맞춤형 보충 자료 및 성찰 과제 정보.
    - **구조**:
      ```json
      [
        {
          "id": "mat_1",
          "type": "REFLECTION",
          "trigger_condition": {"quiz_fail_count": 2},
          "content": "왜 이 개념이 헷갈리는지 3줄로 요약해보세요."
        }
      ]
      ```

## 2. `CurriculumItem` 모델 확장
사용자와 강의 간의 상호작용에서 발생하는 **동적인 상태 데이터**를 모두 이곳에 저장합니다.

### 추가 필드
- **`learning_status` (JSONField)**
    - **역할**: 마이크로 단위 시청 기록 및 체크포인트 달성 현황.
    - **구조**:
      ```json
      {
        "watched_segments": [[0, 60], [120, 150]], // 시청 구간
        "last_position": 145,
        "checkpoint_progress": {
          "cp_1": {"resolved": true, "timestamp": "2024-02-14..."}
        }
      }
      ```

- **`reflection_data` (JSONField)**
    - **역할**: 사용자가 제출한 성찰 과제 및 AI 피드백 저장.
    - **구조**:
      ```json
      {
        "mat_1": {
          "submission": "상태 관리가 어렵습니다.",
          "ai_feedback": "Flux 패턴을 다시 복습해보세요.",
          "is_passed": true
        }
      }
      ```

## 3. `Course` 및 `Curriculum` 모델 확장
통계 및 분석 데이터 저장소입니다.

### `Course` 추가 필드
- **`cohort_analytics` (JSONField)**
    - **역할**: 해당 과정 수강생들의 평균 데이터를 캐싱(Caching)하여 비교 지표로 활용.
    - **구조**:
      ```json
      {
        "avg_progress": 45.2,
        "avg_quiz_score": 78,
        "updated_at": "2024-02-14..."
      }
      ```

### `Curriculum` 추가 필드
- **`retention_metrics` (JSONField)**
    - **역할**: 개인별 이탈 위험도 및 학습 습관 분석 데이터.
    - **구조**:
      ```json
      {
        "prediction_score": 0.85, // 이탈 위험도
        "last_login_gap": 3,
        "quiz_fail_streak": 2,
        "alert_sent": false
      }
      ```

---
## 요약
- **정적 데이터** (콘텐츠) -> `Lecture` 테이블의 JSON 필드로 병합.
- **동적 데이터** (사용자 활동) -> `CurriculumItem` 테이블의 JSON 필드로 병합.
- **통계/분석 데이터** -> `Course` / `Curriculum` 테이블의 JSON 필드로 병합.
