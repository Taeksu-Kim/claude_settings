# CLAUDE.md 베스트 프랙티스 가이드라인

> **참고 출처**  
> - [Anthropic 공식 Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)  
> - [HumanLayer Blog - Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)  
> - [codewithmukesh - CLAUDE.md Complete Guide](https://codewithmukesh.com/blog/claude-md-mastery-dotnet/)  
> - [Claude Code Best Practices 종합 분석](https://rosmur.github.io/claudecode-best-practices/)

---

## 1. CLAUDE.md란 무엇인가?

`CLAUDE.md`는 Claude Code가 세션 시작 시 자동으로 읽는 마크다운 파일이다.  
매 세션마다 Claude의 시스템 프롬프트에 자동으로 삽입되므로, **자주 쓰는 프롬프트처럼 정제**해야 한다.

> Claude는 기본적으로 stateless하다. 세션이 시작될 때 코드베이스에 대해 아무것도 모른다.  
> `CLAUDE.md`는 Claude를 프로젝트에 온보딩시키는 유일한 기본 수단이다.

---

## 2. 메모리 계층 구조

우선순위 높은 순서대로:

| 위치 | 용도 | Git 커밋 여부 |
|------|------|--------------|
| `./CLAUDE.md` | 팀 전체 공유 프로젝트 규칙 | ✅ Yes |
| `./CLAUDE.local.md` | 개인 로컬 설정 (.gitignore에 추가) | ❌ No |
| `./.claude/rules/*.md` | 태스크/폴더별 세부 규칙 | ✅ Yes |
| `~/.claude/CLAUDE.md` | 모든 프로젝트에 적용되는 개인 글로벌 설정 | N/A |

> 모든 레벨은 **대체가 아닌 합산**으로 적용된다. 충돌 시 더 구체적인 규칙이 우선한다.

---

## 3. WHAT-WHY-HOW 프레임워크

Anthropic이 권장하는 3-Layer 구성:

### WHAT — 기술 스택과 프로젝트 구조
Claude에게 어떤 기술을 쓰고 프로젝트가 어떻게 구성되어 있는지 알려준다.
```markdown
## Tech Stack
- Runtime: Node.js 20 + TypeScript 5.x
- Framework: FastAPI 0.115 (Python 3.12)
- Database: PostgreSQL 16 + Prisma ORM
- Testing: pytest + Jest
```

### WHY — 아키텍처 결정과 그 이유
설계 철학을 설명하면 Claude가 코드베이스와 일관된 결정을 내린다.
```markdown
## Architecture Philosophy
- Clean Architecture: 의존성은 항상 안쪽(도메인)을 향한다
- CQRS 패턴 사용: 읽기/쓰기 모델 분리
- 모든 외부 API 호출은 Infrastructure Layer에서만
```

### HOW — 명령어와 워크플로우 규칙
빌드, 테스트, 실행 방법과 Claude가 따라야 할 절차를 명시한다.
```markdown
## Commands
- Build: `npm run build`
- Test: `npm run test` (변경 후 반드시 실행)
- Lint: `npm run lint` (Claude가 직접 실행하지 않음 — linter가 처리)

## Workflow
- 구현 전 반드시 관련 파일을 먼저 읽을 것
- 테스트 먼저 작성 → 실패 확인 → 구현
- 커밋은 Conventional Commits 형식 준수
```

---

## 4. ✅ 포함해야 할 내용

| 항목 | 설명 |
|------|------|
| **기술 스택 + 버전** | `"Entity Framework Core 10"` 처럼 구체적으로 명시 |
| **프로젝트 구조** | 주요 폴더와 그 역할 매핑 |
| **핵심 명령어** | 빌드, 테스트, 실행, 마이그레이션 등 |
| **코딩 컨벤션** | 네이밍 규칙, 파일 구조, 패턴 |
| **사용하는 패턴** | 어떤 패턴을 쓰는지 명시 |
| **사용하지 않는 패턴** | Claude가 제안하면 안 되는 패턴도 명시 |
| **도메인 용어** | 비즈니스 용어 → 코드 엔티티 매핑 |
| **테스트 방법** | 어떻게 테스트를 실행하고 검증하는지 |
| **Git 워크플로우** | 브랜치 네이밍, PR 프로세스 |
| **Claude가 자주 틀리는 것** | 경험 기반의 핵심 교정 사항 |

---

## 5. ❌ 포함하면 안 되는 내용

| 항목 | 이유 |
|------|------|
| **API 키, 비밀번호, 연결 문자열** | 절대 금지 — 보안 위협 |
| **Linter/Formatter가 처리하는 스타일 규칙** | Claude를 linter로 쓰지 말 것. ESLint/Prettier/dotnet format 사용 |
| **프레임워크의 기본 지식** | Claude는 ASP.NET Core, FastAPI 등을 이미 안다 |
| **과도한 문서** | 문서 내용을 복붙하지 말고 링크로 대체 |
| **프로젝트 역사/히스토리** | 현재 상태에 집중. 과거 컨텍스트는 불필요 |
| **특정 태스크에만 해당되는 지시사항** | 범용적이지 않은 지시는 Claude가 무시할 가능성 높음 |

---

## 6. 길이와 구조 가이드라인

### 권장 길이
- **루트 `CLAUDE.md`**: 300줄 이하, 이상적으로는 **50~100줄**
- HumanLayer 팀의 루트 CLAUDE.md: **60줄 미만**
- 2000 토큰 이하를 목표로 할 것

### 이유: Instruction Saturation 문제
```
- LLM은 약 150~200개의 instruction을 신뢰성 있게 따를 수 있다
- Claude Code 시스템 프롬프트에는 이미 ~50개의 instruction이 있다
- instruction 수가 많아질수록 모델은 모든 instruction을 균일하게 무시하기 시작한다
- "나중에 추가된 instruction"만 무시되는 것이 아니라 전체적으로 성능이 저하된다
```

### 파일 분리 전략 (Progressive Disclosure)
루트 CLAUDE.md에 모든 내용을 넣지 말고, **Claude가 필요할 때 읽을 파일을 안내**한다:

```markdown
## Documentation
상세 가이드는 아래 파일을 참고:
- `agent_docs/building_the_project.md` — 빌드 방법
- `agent_docs/running_tests.md` — 테스트 실행
- `agent_docs/code_conventions.md` — 코딩 컨벤션
- `agent_docs/service_architecture.md` — 서비스 아키텍처
```

> 파일 내용을 복붙하지 말고 **파일 경로 참조(pointer)**를 사용하라.  
> 코드 스니펫은 금방 outdated되므로 `file:line` 참조로 대체하라.

---

## 7. Import 문법

대규모 프로젝트에서 CLAUDE.md를 분리할 때:

```markdown
@.claude/rules/architecture.md
@.claude/rules/testing.md
@.claude/rules/git-workflow.md
```

- 최대 5단계까지 재귀적으로 import 가능
- 루트 파일을 간결하게 유지하면서 세부 내용을 분리

---

## 8. Anti-Patterns (흔한 실수)

```markdown
❌ @-file docs 직접 임베드 (매 세션마다 전체 파일을 컨텍스트에 로드)
✅ "복잡한 사용법은 path/to/docs.md 를 참고할 것"

❌ "절대 --foo-bar 플래그를 쓰지 말 것" (Claude가 stuck됨)
✅ "절대 --foo-bar 사용 금지; 대신 --baz 사용"

❌ 포괄적인 매뉴얼처럼 모든 것을 문서화
✅ Claude가 자주 틀리는 것만 문서화

❌ /init 또는 자동 생성된 내용을 그대로 사용
✅ 직접 작성하고 정제 — CLAUDE.md는 가장 레버리지가 높은 설정 포인트

❌ 스타일 규칙을 CLAUDE.md에 넣음
✅ .editorconfig, Prettier, ESLint 등 결정론적 도구 사용
```

---

## 9. 세션 중 업데이트

- **`#` 키** 입력: Claude Code 세션 중 즉시 instruction을 CLAUDE.md에 저장
- 세션에서 발견한 패턴, Claude가 틀린 점을 실시간으로 기록
- CLAUDE.md는 코드베이스와 함께 **살아있는 문서(living documentation)**로 관리

```bash
# 예시: 세션 중 발견한 패턴 즉시 기록
# Claude에게 말하는 대신:
"# 앞으로 Prisma 쿼리는 반드시 try-catch로 감싸고 Sentry에 에러를 보고할 것"
```

---

## 10. 실전 체크리스트

커밋 전 CLAUDE.md 점검:

- [ ] 기술 스택과 버전이 구체적으로 명시됨
- [ ] 프로젝트 구조와 주요 폴더 역할이 설명됨
- [ ] 빌드, 테스트, 실행 명령어가 포함됨
- [ ] 아키텍처 철학 (WHY)이 설명됨
- [ ] 사용하는 패턴과 **사용하지 않는 패턴** 모두 명시됨
- [ ] Git 워크플로우와 브랜치 네이밍 규칙 포함
- [ ] 도메인 용어 매핑 포함
- [ ] **비밀번호, API 키, 연결 문자열 없음** ✅
- [ ] 300줄 이하 (상세 내용은 import로 분리)
- [ ] 실제 프롬프트로 테스트해서 효과 검증됨

---

## 11. CLAUDE.md 기본 템플릿

아래 내용을 프로젝트에 맞게 수정하여 사용:

```markdown
# Project: [프로젝트명]

## Overview
[프로젝트의 목적과 핵심 기능을 2-3문장으로]

## Tech Stack
- Language: [언어 + 버전]
- Framework: [프레임워크 + 버전]
- Database: [DB + ORM]
- Testing: [테스트 프레임워크]
- Package Manager: [npm/yarn/pnpm/uv 등]

## Project Structure
```
src/
  domain/       # 비즈니스 로직, 엔티티
  application/  # Use case, 서비스
  infrastructure/ # DB, 외부 API
  api/          # 라우터, 컨트롤러
tests/
```

## Commands
- Build: `[빌드 명령어]`
- Test: `[테스트 명령어]`
- Dev server: `[개발 서버 명령어]`
- Lint: `[lint 명령어]` (Claude가 직접 실행 금지 — CI에서 처리)

## Architecture
- [사용하는 핵심 아키텍처 패턴]
- [의존성 방향 규칙]
- [레이어 간 통신 방식]

## Patterns We Use
- [패턴 1]
- [패턴 2]

## Patterns We Do NOT Use
- [피해야 할 패턴 1]
- [피해야 할 패턴 2]

## Code Conventions
- [네이밍 규칙]
- [파일 구조 규칙]

## Testing Rules
- 구현 전 테스트 먼저 작성
- 테스트 실패 확인 후 구현
- [테스트 파일 위치 규칙]

## Git Workflow
- 브랜치: `feat/`, `fix/`, `chore/` 접두사 사용
- 커밋: Conventional Commits 형식
- PR 전 모든 테스트 통과 확인

## Important Notes
- [Claude가 자주 틀리거나 주의해야 할 항목]
- [프로젝트 특수 사항]

## Additional Docs
- `agent_docs/architecture.md` — 상세 아키텍처 설명
- `agent_docs/testing_guide.md` — 테스트 가이드
```

---

## 12. NLP 엔지니어를 위한 추가 팁

NLP/ML 프로젝트의 경우 아래 항목도 추가:

```markdown
## ML/NLP Specific
- Model serving: [vLLM/TGI/Triton 등]
- Experiment tracking: [MLflow/W&B/Comet 등]
- Data pipeline: [Airflow/Prefect/dagster 등]
- Vector DB: [Pinecone/Weaviate/Chroma 등]

## Evaluation
- 모델 평가 스크립트 위치: `scripts/eval/`
- 기준 메트릭: [BLEU/ROUGE/F1 등]
- 평가 실행: `[평가 명령어]`

## Data Conventions
- Raw data: `data/raw/` (절대 수정 금지)
- Processed data: `data/processed/`
- 데이터 버전 관리: DVC 사용
```
