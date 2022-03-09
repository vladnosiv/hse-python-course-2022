from time import time
from threading import Thread
from multiprocessing import Process

def fibonacci(n: int) -> list[int]:
    fib = [0, 1]
    for i in range(1, n - 1):
        fib.append(fib[i - 1] + fib[i])
    return fib[:n]


if __name__ == '__main__':
    N = 10 ** 5

    start = time()
    for _ in range(10):
        fibonacci(N)
    time_simple = time() - start

    start = time()
    threads = []
    for _ in range(10):
        threads.append(
            Thread(target=fibonacci, args=(N,))
        )
        threads[-1].start()
    list(map(lambda t: t.join(), threads))
    time_threads = time() - start

    start = time()
    processes = []
    for _ in range(10):
        processes.append(
            Process(target=fibonacci, args=(N,))
        )
        processes[-1].start()
    list(map(lambda p: p.join, processes))
    time_processes = time() - start

    with open('artifacts/easy.txt', 'w') as f:
        f.write(f"Simple time: {time_simple}\n")
        f.write(f"Threads time: {time_threads}\n")
        f.write(f"Processes time: {time_processes}\n")
