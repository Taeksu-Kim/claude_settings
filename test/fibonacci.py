# ## 20260218-001


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_sequence(n: int) -> list[int]:
    if n <= 0:
        return []
    result = [0]
    a, b = 0, 1
    for _ in range(1, n):
        result.append(b)
        a, b = b, a + b
    return result


if __name__ == "__main__":
    count = int(input("생성할 피보나치 수의 개수: "))
    print(fibonacci_sequence(count))
