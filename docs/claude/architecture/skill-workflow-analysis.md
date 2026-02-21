# Skill & Workflow 구조 분석

코드 작업 요청 시 시스템이 어떤 구조로 동작하는지 분석하고, 장단점과 개선점을 정리한다.

## 전제

- 본 문서는 **Claude Code**(Anthropic CLI 에이전트)의 커스텀 skill/workflow 시스템을 대상으로 한다.
- Claude Code는 `.claude/` 디렉토리 하위에 사용자가 정의한 skill과 workflow를 배치하면, 에이전트가 이를 읽고 지시에 따라 동작한다.
- 본 프로젝트는 PDCA(Plan-Do-Check-Act) 사이클과 TDD(Test-Driven Development)를 결합한 코드 작업 프로세스를 workflow로 구성하여 사용하고 있다.
- 이 문서를 이해하려면 Claude Code의 skill/workflow 개념, PDCA 사이클, TDD에 대한 기본적인 이해가 필요하다.

## 1. 전체 동작 흐름

```
유저 요청
  │
  ▼
CLAUDE.md (강제 지시)
  │  "모든 요청에 router skill 먼저 사용"
  ▼
Router Skill (.claude/skills/router/SKILL.md)
  │  요청 의도 분석 → 워크플로우 선택
  │  터미널 출력: [Router] → code-work 워크플로우로 라우팅
  ▼
Code-Work Workflow (.claude/workflows/code-work/workflow.md)
  │
  ├─ Step 0. 요청 확인 ─── 유저와 이해 내용 합의
  ├─ Step 1. Plan ──────── 작업 범위, 접근 방식 정의 → plan.md
  ├─ Step 1.5. Plan Review ── 서브 에이전트가 plan.md 검증 (최대 3회)
  │     └─ plan-review workflow
  ├─ Step 2. Do ─────────── 실패하는 테스트 작성 (TDD Red) → do.md
  ├─ Step 3. Check ──────── 서브 에이전트가 테스트 실행 + 품질 점검
  │     └─ pdca-check workflow
  ├─ Step 4. Act ─────────── 본 구현 (TDD Green + Refactor) → act.md
  └─ Step 5. Code Review ── 서브 에이전트가 최종 리뷰 (최대 3회)
        └─ code-review workflow
```

### 산출물 구조

```
claude_task/<task_id>/
├── plan/
│   ├── plan.md           # 계획
│   └── plan_review.md    # 계획 검증 결과
├── do/
│   └── do.md             # 테스트 설계 기록
├── check/
│   └── check.md          # 품질 점검 결과
├── act/
│   └── act.md            # 구현 기록
└── review/
    └── review.md         # 코드 리뷰 결과
```

## 2. 각 구성요소의 역할

### CLAUDE.md
- 진입점. `router skill`을 반드시 먼저 호출하도록 강제한다.
- 이 한 줄의 지시가 전체 파이프라인의 시작점을 보장한다.

### Router Skill
- 유저 요청의 의도를 파악하여 적절한 워크플로우로 분기한다.
- 현재 라우팅 대상: `code-work`, `documentation`

### Code-Work Workflow (메인)
- PDCA 사이클과 TDD를 결합한 코드 작업 프로세스.
- 메인 에이전트가 Plan/Do/Act를 직접 수행하고, 검증 단계(Plan Review/Check/Code Review)는 서브 에이전트에 위임한다.

### 서브 워크플로우 (Plan Review / PDCA-Check / Code Review)
- 각각 독립된 `workflow.md`에 검증 절차와 체크리스트가 정의되어 있다.
- 서브 에이전트로 실행되어 메인 컨텍스트를 오염시키지 않는다.
- Plan Review와 Code Review는 **검증만** 수행하고 직접 수정하지 않는다.
- PDCA-Check는 문제 발견 시 **직접 수정**까지 수행한다.

## 3. 장점

### 구조적 강제력
- CLAUDE.md의 router 강제 지시 → 모든 요청이 반드시 정해진 프로세스를 거친다. 에이전트가 임의로 프로세스를 건너뛰는 것을 방지한다.

### 관심사 분리
- 메인 에이전트는 작업(Plan/Do/Act)에 집중하고, 검증은 서브 에이전트가 담당한다. 이로 인해:
  - 메인 컨텍스트 윈도우가 검증 로직으로 소모되지 않는다.
  - 검증 에이전트는 "작성자"가 아닌 "리뷰어" 관점에서 독립적으로 판단할 수 있다.

### 산출물 기반 추적성
- 모든 단계가 마크다운 파일로 기록된다. 작업이 끝난 후에도 왜 이렇게 구현했는지, 어떤 검증을 거쳤는지 추적할 수 있다.

### 실패 안전장치
- Plan Review와 Code Review에 최대 3회 반복 제한이 있다. 무한 루프에 빠지지 않으며, 해결 불가 시 유저에게 수동 개입을 요청한다.

### TDD 내장
- Do → Check → Act 흐름이 자연스럽게 Red-Green-Refactor 사이클을 강제한다. 테스트 없는 구현이 원천적으로 불가능하다.

## 4. 단점

### 컨텍스트 전달의 한계
- 서브 에이전트는 메인 에이전트의 대화 맥락을 공유하지 않는다. 산출물 파일(plan.md, do.md 등)을 통해서만 정보를 전달받는다. 파일에 기록되지 않은 암묵적 맥락(유저와의 구두 합의, 이전 대화에서 논의된 제약 사항 등)은 서브 에이전트에 전달되지 않는다.

### 오버헤드
- 단순한 코드 변경(한두 줄 수정, 오타 수정 등)에도 동일한 6단계 프로세스를 거쳐야 한다. Plan 작성 → Plan Review → 테스트 작성 → Check → 구현 → Code Review로 이어지는 전체 파이프라인은 소규모 작업에 비해 과도하다.

### 라우팅 경직성
- Router에 등록된 워크플로우가 `code-work`와 `documentation` 두 가지뿐이다. 이 두 가지에 해당하지 않는 요청(예: 단순 질문, 디버깅 조사, 환경 설정 등)이 들어왔을 때의 폴백 동작이 정의되어 있지 않다.

### 서브 에이전트 간 정보 단절
- Plan Review, PDCA-Check, Code Review 서브 에이전트는 각각 독립적으로 실행된다. 이전 리뷰 사이클에서 어떤 피드백이 있었는지 서브 에이전트가 알 수 있는 방법은 산출물 파일뿐인데, 이전 사이클의 리뷰 결과가 다음 사이클의 서브 에이전트에 명시적으로 전달되는 구조가 아니다 (같은 파일을 덮어쓰는 방식).

### 언어 제약
- 테스트 파일 형식이 `<filename>.py.test` (pytest)로 고정되어 있다. Python 이외의 언어로 작업할 경우 워크플로우를 그대로 적용하기 어렵다.

## 5. 개선점

### 작업 규모에 따른 경량 경로 도입
- Router 또는 code-work 워크플로우에 작업 규모 판단 단계를 추가하여, 소규모 작업(한두 줄 수정, 오타, 설정 변경 등)은 간소화된 경로로 처리할 수 있도록 한다.
- 예: "경량 모드"에서는 Plan Review를 생략하고 Do/Check/Act를 축약 실행.

### 폴백 라우팅 정의
- Router에 등록된 워크플로우와 매칭되지 않는 요청에 대한 기본 동작을 정의한다. "해당 없음" 시 워크플로우 없이 일반 응답을 하거나, 유저에게 어떤 워크플로우로 진행할지 확인하는 식의 폴백 경로가 필요하다.

### 리뷰 사이클 간 히스토리 누적
- 리뷰 산출물 파일(plan_review.md, review.md)에 이전 사이클의 피드백을 삭제하지 않고 누적 기록하면, 다음 사이클의 서브 에이전트가 "이전에 어떤 지적이 있었고 어떻게 수정되었는지"를 파악할 수 있다. 같은 피드백이 반복되는 것을 방지할 수 있다.

### 다국어/멀티 프레임워크 지원
- 테스트 형식을 프로젝트 설정(CLAUDE.md 또는 별도 설정 파일)에서 정의하도록 하면, Python 이외의 프로젝트에서도 동일한 워크플로우를 재사용할 수 있다.
- 예: `test_framework: jest`, `test_file_pattern: "*.test.ts"` 등.
