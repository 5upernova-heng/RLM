"""
This class implements the union-find set data structure.

Attribute:
    size: the number of elements in the set
"""


class UnionFindSet:
    def __init__(self, size):
        self.size = size
        self._flag_array = [i for i in range(size)]
        self._set_size = [1 for _ in range(size)]
        self._set_num = size

    def unite(self, x, y) -> None:
        x_flag = self.find(x)
        y_flag = self.find(y)
        if x_flag == y_flag:
            return
        if self._set_size[x_flag] < self._set_size[y_flag]:
            self._flag_array[x_flag] = y_flag
            self._set_size[y_flag] += self._set_size[x_flag]
        else:
            self._flag_array[y_flag] = x_flag
            self._set_size[x_flag] += self._set_size[y_flag]
        self._set_num -= 1

    def find(self, x):
        if x < 0 or x >= len(self._flag_array):
            raise ValueError(f"The index {x} is out of range {self.size}.")
        while x != self._flag_array[x]:
            x = self._flag_array[x]
        return x

    def isUnited(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

    def isAllUnited(self) -> bool:
        return self._set_num == 1


if __name__ == "__main__":
    """
    Test Examples
    """
    union_find_set = UnionFindSet(6)
    union_find_set.unite(1, 2)
    union_find_set.unite(3, 4)
    print(union_find_set.find(1))
    print(union_find_set.find(4))
    union_find_set.unite(1, 3)
    print(union_find_set.find(3))
    print(union_find_set.isUnited(1, 4))
    print(union_find_set.isUnited(1, 5))
    union_find_set.unite(0, 5)
    union_find_set.unite(5, 2)
    print(union_find_set.isAllUnited())
