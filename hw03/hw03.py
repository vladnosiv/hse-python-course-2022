import numpy as np
import numbers
from itertools import chain
from numpy.lib.mixins import NDArrayOperatorsMixin


# Easy Matrix
class MyMatrix:
    def __init__(self, matrix: list[list[any]]):
        self._matrix = matrix

    def __str__(self):
        s = ''
        for row in self._matrix:
            s += ' ['
            for el in row:
                s += ' ' + str(el)
            s += ']\n'
        return '[' + s[1:-1] + ']'

    def __iter__(self):
        return chain.from_iterable(self._matrix)

    def __getitem__(self, key):
        return self._matrix[key]

    def __len__(self) -> int:
        return len(self._matrix)

    def shape(self) -> tuple[int, int]:
        return len(self._matrix), len(self._matrix[0])

    def __op__(self, right_matrix, op):
        if self.shape() != right_matrix.shape():
            raise ValueError("Incorrect matrix dimensions.\n"
                             f"{self.shape()} not equal {right_matrix.shape()}.")
        result = []
        for row_left, row_right in zip(self._matrix, right_matrix._matrix):
            result.append([])
            for el_left, el_right in zip(row_left, row_right):
                result[-1].append(op(el_left, el_right))
        return MyMatrix(result)

    def __add__(self, right_matrix):
        return self.__op__(right_matrix, lambda a, b: a + b)

    def __sub__(self, right_matrix):
        return self.__op__(right_matrix, lambda a, b: a - b)

    def __mul__(self, right_matrix):
        return self.__op__(right_matrix, lambda a, b: a * b)

    def __matmul__(self, right_matrix):
        if self.shape()[1] != right_matrix.shape()[0]:
            raise ValueError("Incorrect matrix dimensions.\n"
                             f"{self.shape()[1]} not equal {right_matrix.shape()[0]}.")
        result = [[0 for _ in range(right_matrix.shape()[1])] for _ in range(self.shape()[0])]
        for i in range(self.shape()[0]):
            for k in range(self.shape()[1]):
                for j in range(right_matrix.shape()[1]):
                    result[i][j] += self._matrix[i][k] * right_matrix[k][j]
        return MyMatrix(result)


class StrMatrixMixin:
    def __str__(self):
        s = ''
        for row in self._matrix:
            s += ' ['
            for el in row:
                s += ' ' + str(el)
            s += ']\n'
        return '[' + s[1:-1] + ']'


class MatrixProperties:
    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, new_matrix):
        self._matrix = np.asarray(new_matrix)


# Medium Matrix
class MediumMatrix(NDArrayOperatorsMixin, StrMatrixMixin, MatrixProperties):
    def __init__(self, matrix):
        self._matrix = np.asarray(matrix)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x._matrix if isinstance(x, MediumMatrix) else x
                       for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        return type(self)(result)


# Hard Task Mixin
# Simply XOR all values in matrix
class HashXorMixin:
    def __hash__(self):
        result = 0
        for x in self:
            result ^= x
        return result


# Hard Task
class CachedMatrix(MyMatrix, HashXorMixin):
    _cached_matmul = dict()

    def __matmul__(self, other):
        _hash = hash((self, other))
        if _hash not in self._cached_matmul:
            self._cached_matmul[_hash] = CachedMatrix(super().__matmul__(other)._matrix)
        return self._cached_matmul[_hash]


def easy_task():
    np.random.seed(0)

    my_a = MyMatrix(np.random.randint(0, 10, (10, 10)))
    my_b = MyMatrix(np.random.randint(0, 10, (10, 10)))

    with open('artifacts/easy/matrix+.txt', 'w') as f:
        f.write(str(my_a + my_b))
    with open('artifacts/easy/matrix*.txt', 'w') as f:
        f.write(str(my_a * my_b))
    with open('artifacts/easy/matrix@.txt', 'w') as f:
        f.write(str(my_a @ my_b))


def medium_task():
    np.random.seed(0)

    my_a = MediumMatrix(np.random.randint(0, 10, (10, 10)))
    my_b = MediumMatrix(np.random.randint(0, 10, (10, 10)))

    with open('artifacts/medium/matrix+.txt', 'w') as f:
        f.write(str(my_a + my_b))
    with open('artifacts/medium/matrix*.txt', 'w') as f:
        f.write(str(my_a * my_b))
    with open('artifacts/medium/matrix@.txt', 'w') as f:
        f.write(str(my_a @ my_b))


def hard_task():
    A = MyMatrix([
        [0, 1],
        [1, 0]
    ])
    C = MyMatrix([
        [1, 1],
        [0, 0]
    ])
    B = D = MyMatrix([
        [1, 2],
        [1, 1]
    ])

    for matrix, name in [(A, 'A'), (B, 'B'), (C, 'C'), (D, 'D')]:
        with open(f"artifacts/hard/{name}.txt", 'w') as f:
            f.write(str(matrix))

    with open('artifacts/hard/AB.txt', 'w') as f:
        f.write(str(A @ B))
    with open('artifacts/hard/CD.txt', 'w') as f:
        f.write(str(C @ D))

    with open('artifacts/hard/hash.txt', 'w') as f:
        f.write(f"AB Hash: {hash(CachedMatrix((A @ B)._matrix))}\n"
                f"CD Hash: {hash(CachedMatrix((C @ D)._matrix))}\n")


if __name__ == '__main__':
    easy_task()
    medium_task()
    hard_task()
