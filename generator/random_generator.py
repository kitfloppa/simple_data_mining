from __future__ import annotations

from numpy.random import default_rng


class RandomGenerator:
    def __init__(self, min_range: int, max_range: int, use_one: bool = False) -> None:
        self.__use_one = use_one
        self.__rng = default_rng()
        self.__min_range = min_range
        self.__max_range = max_range

    def randint(self) -> int:
        rand_value = int(self.__rng.integers(low=self.__min_range, high=self.__max_range, size=1))

        if self.__use_one:
            while rand_value == 1:
                rand_value = int(self.__rng.integers(low=self.__min_range, high=self.__max_range, size=1))
        else:
            if rand_value == 1:
                self.__use_one = True

        return rand_value
    

    @property
    def use_one(self) -> bool:
        return self.__use_one
    

    @property
    def range(self) -> tuple:
        return (self.__min_range, self.__max_range)