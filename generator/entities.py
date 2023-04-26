from __future__ import annotations

from numpy import sort
from numpy.random import default_rng


class EntityProperty:
    def __init__(self, alias: str, type: int, max_interval: int = 200, enumerate_count: int = 10) -> None:
        self.type = ''
        self.alias = alias
        self.value_period = []
        self.possible_values = []
        self.normal_value = None

        rng = default_rng()

        self.number_trend_periods = rng.choice(range(1, 6), size=1)[0]

        if enumerate_count < 10:
            raise ValueError(f'Enumerate count less than {enumerate_count}.')
        
        if type == 0:
            self.type = 'bool'
            self.possible_values = [True, False]
            self.normal_value = rng.choice(self.possible_values, size=1)[0]
        elif type == 1:
            self.type = 'enumerate'

            with open('data/possible_values_of_symptom.txt', 'r') as input:
                possible_val = input.read().split('\n')

            if len(possible_val) < enumerate_count:
                raise ValueError("Values count more then all possible values.")
            else:
                values_positions = rng.choice(len(possible_val), size=enumerate_count, replace=False)
            
            self.possible_values = [possible_val[i] for i in values_positions]
            self.normal_value = rng.choice(self.possible_values, size=1)[0]
        else:
            self.type = 'interval'
            self.possible_values = sort(rng.choice(max_interval, size=2, replace=False))
            self.normal_value = sort(rng.choice(range(self.possible_values[0], self.possible_values[1]), size=2))

    def __str__(self) -> str:
        return self.alias


class Entity:
    def __init__(self, alias: str, property_count: int = 3) -> None:
        self.entity_properties = []

        types_count = 3
        rng = default_rng()
        
        if property_count >= types_count:
            self.property_count = property_count
        else:
            raise ValueError(f'Property count less than {types_count}.')
        
        self.alias = alias

        with open('data/symptom_names.txt', 'r') as input:
            property_aliases = input.read().split('\n')

        if len(property_aliases) < self.property_count:
            raise ValueError("Properties count more then all possible properties.")
        else:
            aliases_positions = rng.choice(len(property_aliases), size=self.property_count, replace=False)

        for i in range(self.property_count):
            self.entity_properties.append(EntityProperty(property_aliases[aliases_positions[i]], i % types_count))

    def __str__(self) -> str:
        property_aliases = '\n'.join([str(i.number_trend_periods) for i in self.entity_properties])

        return f'''Болезнь: {self.alias}\n\nСимптомы:\n{property_aliases}'''