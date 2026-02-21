# Act - 20260218-001

## 작업 대상 파일
- `test/fibonacci.py` (신규 생성)
- `test/fibonacci.py.test` (테스트 파일)
- `conftest.py` (pytest 커스텀 컬렉터)
- `pytest.ini` (pytest 설정)

## 변경 내용 요약
- `fibonacci(n)`: n번째 피보나치 수를 반복문으로 계산하여 반환
- `fibonacci_sequence(n)`: 처음 n개의 피보나치 수열을 리스트로 반환
- 음수 입력 시 `ValueError` 발생
- `__main__` 블록으로 직접 실행 시 사용자 입력을 받아 수열 출력

## 최종 테스트 결과
- 9 passed in 0.08s
- 모든 테스트 통과 (Green)
