import numpy as np
from itertools import chain


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


if __name__ == '__main__':
    easy_task()
