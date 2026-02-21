---
name: router
description: Routes to the appropriate workflow based on user intent
user-invocable: true
---

# Router

사용자의 요청을 분석하여 적절한 workflow로 라우팅한다.

## Workflows 개념

- Workflows는 `.claude/workflows/` 디렉토리에 위치한다.
- 각 workflow는 독립된 폴더이며, 내부에 `workflow.md` 파일이 작업 지침을 담고 있다.
- Router는 사용자의 의도를 파악하고, 해당하는 workflow.md를 읽어 그 지침에 따라 작업을 수행한다.

## 사용 가능한 Workflows

| Workflow | 경로 | 설명 |
|----------|------|------|
| code-work | `.claude/workflows/code-work/workflow.md` | 코드 파일을 생성, 수정, 리팩토링 등 코드 작업이 발생하는 모든 상황에서 반드시 호출 |
| documentation | `.claude/workflows/documentation/workflow.md` | README, API 문서, 아키텍처 문서, 가이드 등 문서 작성/갱신 요청 시 호출 |
| claude-md-review | `.claude/workflows/claude-md-review/workflow.md` | CLAUDE.md의 품질 검토 및 개선점 제시 요청 시 호출 |

## 라우팅 흐름

1. 사용자의 요청을 분석한다.
2. 요청에 맞는 workflow를 위 목록에서 찾는다.
3. 라우팅 결과를 초록색으로 터미널에 표시한다: `echo -e '\033[32m[Router] → <워크플로우명> 워크플로우로 라우팅\033[0m'`
4. 해당 workflow.md 파일을 읽는다.
5. workflow.md에 정의된 Steps를 순서대로 수행한다.
