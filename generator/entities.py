from __future__ import annotations

from numpy import sort
from decouple import config
from numpy.random import default_rng
from generator.random_generator import RandomGenerator


MAX_BORDER = int(config('MAX_BORDER'))
MAX_INTERVAL = int(config('MAX_INTERVAL'))
ENUMERATE_COUNT = int(config('ENUMERATE_COUNT'))


class EntityProperty:
    def __init__(self, alias: str, number_trend_periods: int, type: int) -> None:
        self.__rng = default_rng()
        
        self.__type = ''
        self.__alias = alias
        self.__borders = []
        self.__value_period = []
        self.__possible_values = []
        self.__normal_value = []
        self.number_trend_periods = number_trend_periods

        lower_bound_one = False

        for i in range(self.number_trend_periods):
            borders = sort(self.__rng.choice(range(1, MAX_BORDER), size=2, replace=False))
            
            while borders[1] - borders[0] < 4:
                borders = sort(self.__rng.choice(range(1, MAX_BORDER), size=2, replace=False))

            if lower_bound_one:
                while borders[0] == 1:
                    borders = sort(self.__rng.choice(range(1, MAX_BORDER), size=2, replace=False))
            else:
                if borders[0] == 1:
                    lower_bound_one = True

            self.__borders.append(borders)

        if ENUMERATE_COUNT < 10:
            raise ValueError(f'Enumerate count less than {ENUMERATE_COUNT}.')
        
        if type == 0:
            self.__type = 'bool'
            self.__possible_values = [True, False]
            self.__normal_value = [self.__rng.choice(self.__possible_values, size=1)[0]]

            for i in range(self.number_trend_periods):
                self.__value_period.append(self.__possible_values[i % len(self.__possible_values)])
        elif type == 1:
            self.__type = 'enumerate'

            with open('data/possible_values_of_symptom.txt', 'r', encoding='utf-8') as input:
                possible_val = input.read().split('\n')

            if len(possible_val) < ENUMERATE_COUNT:
                raise ValueError("Values count more then all possible values.")
            else:
                values_positions = self.__rng.choice(len(possible_val), size=ENUMERATE_COUNT, replace=False)
            
            self.__possible_values = [possible_val[i] for i in values_positions]

            self.__normal_value = list(self.__rng.choice(self.__possible_values, 
                                                  size=self.__rng.integers(low=1, high=len(self.__possible_values) - 1, size=1)[0]))

            values_positions = self.__rng.choice(ENUMERATE_COUNT,
                                                         size=self.__rng.integers(low=1, high=ENUMERATE_COUNT - 1, size=1)[0], replace=False)

            for i in range(self.number_trend_periods):
                if i % 2 == 0:
                    tmp_values_positions = self.__rng.choice(ENUMERATE_COUNT,
                                                         size=self.__rng.integers(low=1, high=ENUMERATE_COUNT - 1, size=1)[0], replace=False)

                    while len([j for j in tmp_values_positions if j in values_positions]) != 0:
                        tmp_values_positions = self.__rng.choice(ENUMERATE_COUNT,
                                                         size=self.__rng.integers(low=1, high=ENUMERATE_COUNT - 1, size=1)[0], replace=False)
                        
                    values_positions = tmp_values_positions
                else:
                    values_positions = [j for j in range(ENUMERATE_COUNT) if j not in values_positions]
                    values_positions = values_positions[:self.__rng.integers(low=1, high=len(values_positions), size=1)[0]]

                self.__value_period.append([self.__possible_values[j] for j in values_positions])
        elif type == 2:
            self.__type = 'interval'
            self.__possible_values = list(sort(self.__rng.choice(MAX_INTERVAL, size=2, replace=False)))

            while self.__possible_values[1] - self.__possible_values[0] < MAX_INTERVAL // 1.2:
                self.__possible_values = list(sort(self.__rng.choice(MAX_INTERVAL, size=2, replace=False)))

            self.__normal_value = list(sort(self.__rng.choice(range(self.__possible_values[0], self.__possible_values[1]), 
                                                            size=2)))
            
            min_cur_interval = (self.__possible_values[0] + self.__possible_values[1]) // 2
            max_cur_interval = min_cur_interval

            for i in range(self.number_trend_periods):
                cur_interval = sort(self.__rng.choice(range(self.__possible_values[0], self.__possible_values[1]), 
                                                            size=2))
                
                while ((cur_interval[0] >= min_cur_interval and cur_interval[0] <= max_cur_interval) or \
                        (cur_interval[1] >= min_cur_interval and cur_interval[1] <= max_cur_interval)) or \
                        (cur_interval[0] <= min_cur_interval and cur_interval[1] >= min_cur_interval):
                        cur_interval = sort(self.__rng.choice(range(self.__possible_values[0], self.__possible_values[1]), 
                                                                    size=2))

                min_cur_interval, max_cur_interval = cur_interval[0], cur_interval[1]

                self.__value_period.append(cur_interval)
        else:
            raise ValueError('A type is specified that does not exist.')
    

    @property
    def alias(self) -> str:
        return self.__alias
    

    @property
    def ntp(self) -> int:
        return self.number_trend_periods
    

    @property
    def type(self) -> str:
        return self.__type
    

    @property
    def value_period(self) -> list:
        return self.__value_period
    

    @property
    def borders(self) -> list:
        return self.__borders
    

    @property
    def possible_values(self) -> list:
        return self.__possible_values
    

    @property
    def normal_value(self) -> list:
        return self.__normal_value


class Entity:
    def __init__(self, alias: str, namesake_features: list, property_aliases: list, random_gen: RandomGenerator, types_count: int) -> None:
        self.__random_gen = RandomGenerator(random_gen.range[0], random_gen.range[1], random_gen.use_one)
        
        self.__alias = alias
        self.__entity_properties = namesake_features.copy()

        for i in range(len(property_aliases)):
            self.__entity_properties.append(EntityProperty(property_aliases[i], 
                                                           self.__random_gen.randint(), i % types_count))


    def __str__(self) -> str:
        property_aliases = '\n'.join([str(i.alias) for i in self.__entity_properties])

        return f'''Болезнь: {self.__alias}\n\nСимптомы:\n{property_aliases}'''
    

    @property
    def alias(self) -> str:
        return self.__alias
    

    @property
    def properties(self) -> list:
        return self.__entity_properties