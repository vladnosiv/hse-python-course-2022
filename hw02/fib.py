def fibonacci(n: int) -> list[int]:
    fib = [0, 1]
    for i in range(1, n - 1):
        fib.append(fib[i - 1] + fib[i])
    return fib[:n]  # Slice for n == 0 and n == 1 cases
