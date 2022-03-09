from time import time
from math import cos, pi
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from functools import partial


def integrate_(f, n_iter, rng):
    l, r = rng
    acc = 0
    step = (r - l) / n_iter
    for i in range(n_iter):
        acc += f(l + i * step) * step
    return acc


def integrate(f, a, b, n_jobs=1, n_iter=10**8):
    print(f"Start integrate from {a} to {b}, n_jobs = {n_jobs}, n_iter = {n_iter}")
    start_time = time()
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        result = sum(executor.map(
            partial(integrate_, f, n_iter // n_jobs),
            [(x, x + (b - a) / n_jobs) for x in np.arange(a, b, (b - a) / n_jobs)]
        ))
        end_time = time()
        print(f"End integrate. Result = {result}, time: {end_time - start_time}")
        return result


if __name__ == '__main__':
    cpu_num = 8

    n_jobs_to_time = {}
    for n_jobs in range(1, 2 * cpu_num + 1):
        start = time()
        integrate(cos, 0, pi / 2, n_jobs=n_jobs)
        result_time = time() - start
        n_jobs_to_time[n_jobs] = result_time

    with open('artifacts/medium_time.txt', 'w') as f:
        for n_jobs in range(1, 2 * cpu_num + 1):
            f.write(f"n_jobs: {n_jobs}, time: {n_jobs_to_time[n_jobs]}\n")
