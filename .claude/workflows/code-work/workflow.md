# Code Work Workflow

코드 작업 시 PDCA + TDD 방법론에 따라 진행한다.

## 산출물 구조

```
claude_task/<task_id>/
├── plan/
│   ├── plan.md
│   └── plan_review.md
├── do/
│   └── do.md
├── check/
│   └── check.md
├── act/
│   └── act.md
└── review/
    └── review.md
```

task_id는 `YYYYMMDD-순번` 형식으로 부여한다. (예: 20260218-001)

## 터미널 출력 규칙

각 스텝 진입 시 현재 단계를 터미널에 출력한다:
```
echo -e "\033[36m[STEP 0] 요청 확인 - task_id: <task_id>\033[0m"
```

승인이 필요한 단계(Plan Review, Code Review)에서 승인되면 초록색으로 출력한다:
```
echo -e "\033[32m[APPROVED] Plan Review 승인 완료 - task_id: <task_id>\033[0m"
echo -e "\033[32m[APPROVED] Code Review 승인 완료 (커밋 가능) - task_id: <task_id>\033[0m"
```

스텝 출력 형식:
| 스텝 | 출력 |
|------|------|
| 0. 요청 확인 | `\033[36m[STEP 0] 요청 확인\033[0m` |
| 1. Plan | `\033[36m[STEP 1] Plan\033[0m` |
| 1.5 Plan Review | `\033[36m[STEP 1.5] Plan Review (N/3)\033[0m` |
| 2. Do | `\033[36m[STEP 2] Do\033[0m` |
| 3. Check | `\033[36m[STEP 3] Check\033[0m` |
| 4. Act | `\033[36m[STEP 4] Act\033[0m` |
| 5. Code Review | `\033[36m[STEP 5] Code Review (N/3)\033[0m` |

## PDCA Steps

### 0. 요청 확인
- Plan에 들어가기 전, 유저의 요청을 정리하여 본인이 이해한 내용을 유저에게 보여주고 확인을 받는다.
- 정리 항목: 작업 목표, 예상 범위, 제약 사항(있는 경우)
- 유저가 확인해야 다음 단계로 진행한다.

### 1. Plan
- 사용자 요청을 분석하고 작업 범위를 정의한다.
- `plan.md`에 기록: 요청 요약, 영향 범위, 접근 방식

### 1.5. Plan Review (최대 3회 반복)
- Plan 작성 후, `plan-review` 워크플로우를 서브 에이전트로 실행하여 plan.md를 검증한다. 메인 컨텍스트에서 직접 실행하지 않는다.
  - 예시: `Task(subagent_type="general-purpose", prompt="claude_task/<task_id>/plan/plan.md를 읽고, .claude/workflows/plan-review/workflow.md의 절차에 따라 계획을 검증하고 결과를 claude_task/<task_id>/plan/plan_review.md에 기록해줘. 현재 리뷰 사이클: N/3회차")`
- 세부 검증 관점 및 절차는 `.claude/workflows/plan-review/workflow.md` 참조
- **승인** → 즉시 Do 단계로 진행한다.
- **리플랜 필요** → plan_review.md의 피드백(수정 필요 부분, 문제점, 개선방안)을 유저에게 보여주고 확인을 받은 뒤 plan.md를 수정하고 다시 검증한다.
- **최대 반복 횟수는 3회**이다. 3회 후에도 승인되지 않으면 터미널에 빨간색(\033[31m)으로 실패를 알리고 유저에게 수동 개입을 요청한다.
  - 예시: `echo -e "\033[31m[PLAN FAILED] task_id: <task_id> - 3회 플랜 리뷰 반복 후에도 승인되지 않았습니다. 수동 개입이 필요합니다.\033[0m"`

### 2. Do
- TDD: 먼저 실패하는 테스트를 작성한다.
- 테스트 파일: `<filename>.py.test` (pytest)
- `do.md`에 기록: 작성한 테스트 목록, 각 테스트의 검증 의도

### 3. Check
- `pdca-check` 워크플로우를 서브 에이전트로 실행한다. 메인 컨텍스트에서 직접 실행하지 않는다.
  - 예시: `Task(subagent_type="Bash", prompt="claude_task/<task_id>/ 경로의 plan/plan.md, do/do.md를 읽고, Do 단계에서 작성한 테스트 파일을 pytest로 실행한 뒤, .claude/workflows/pdca-check/workflow.md의 절차에 따라 코드 품질 점검 및 수정을 수행하고 결과를 check/check.md에 기록해줘")`
- 세부 점검 항목 및 절차는 `.claude/workflows/pdca-check/workflow.md` 참조

### 4. Act
- Check 단계에서 수정이 완료된 코드를 기반으로 본 구현에 들어간다.
- 코드 파일 최상단에 `# ## <task_id>` 주석을 추가(또는 갱신)한다.
- `act.md`에 기록: 작업 대상 파일, 변경 내용 요약, 최종 테스트 결과

### 5. Code Review (최대 3회 반복)
- Act 완료 후, `code-review` 워크플로우를 서브 에이전트로 실행한다. 메인 컨텍스트에서 직접 실행하지 않는다.
  - 예시: `Task(subagent_type="general-purpose", prompt="claude_task/<task_id>/ 경로의 plan/plan.md, do/do.md, check/check.md, act/act.md를 읽고, 변경된 코드 파일을 확인한 뒤, .claude/workflows/code-review/workflow.md의 절차에 따라 코드 리뷰를 수행하고 결과를 claude_task/<task_id>/review/review.md에 기록해줘. 현재 리뷰 사이클: N/3회차")`
- 세부 리뷰 관점 및 절차는 `.claude/workflows/code-review/workflow.md` 참조
- 서브 에이전트는 커밋 가능 여부를 판단한다. 종합 판정: **승인(커밋 가능)** / **수정 필요**
- 리뷰 결과가 **수정 필요**인 경우, 수정 후 다시 Check(3단계)부터 재수행한다.
- **최대 반복 횟수는 3회**이다. 3회 리뷰 후에도 승인되지 않으면 워크플로우 내에서 해결 불가로 판단하고, 터미널에 빨간색(\033[31m)으로 실패 사유를 출력하여 유저에게 알린다.
  - 예시: `echo -e "\033[31m[WORKFLOW FAILED] task_id: <task_id> - 3회 코드 리뷰 반복 후에도 승인되지 않았습니다. 수동 개입이 필요합니다.\033[0m"`

## TDD 원칙

1. **Red**: 실패하는 테스트를 먼저 작성
2. **Green**: 테스트를 통과하는 최소한의 코드 작성
3. **Refactor**: 통과 후 코드 정리 (테스트는 계속 통과해야 함)
