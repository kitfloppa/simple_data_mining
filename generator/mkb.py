from __future__ import annotations

from decouple import config
from numpy.random import default_rng
from generator.entities import Entity, EntityProperty
from generator.random_generator import RandomGenerator


MIN_TREND_PERIOD = int(config('MIN_TREND_PERIOD'))
MAX_TREND_PERIOD = int(config('MAX_TREND_PERIOD'))

TYPES_COUNT = int(config('TYPES_COUNT'))



# Model knowledge base.
class MKB:
    def __init__(self, entity_count: int = 2, property_count: int = 6, namesake_property_count: int = 3) -> None:
        self.__rng = default_rng()
        self.__random_gen = RandomGenerator(MIN_TREND_PERIOD, MAX_TREND_PERIOD)
        self.__entity = []
        self.__namesake_property = []

        with open('data/namesake_features.txt', 'r') as input:
            aliases = input.read().split('\n')

        aliases_positions = self.__rng.choice(len(aliases), size=namesake_property_count, replace=False)

        for i in range(namesake_property_count):
            self.__namesake_property.append(EntityProperty(aliases[aliases_positions[i]], 
                                                           self.__random_gen.randint(), i % TYPES_COUNT))

        with open('data/disease_names.txt', 'r') as input:
            aliases = input.read().split('\n')

        if len(aliases) < entity_count:
            raise ValueError("Entities count more then all possible entities.")
        else:
            aliases_positions = self.__rng.choice(len(aliases), size=entity_count, replace=False)

        for i in range(entity_count):
            self.__entity.append(Entity(aliases[aliases_positions[i]], self.__namesake_property, 
                                        self.__random_gen, TYPES_COUNT, property_count=property_count))
            
    
    def __str__(self) -> str:
        result = ''
        
        for entity in self.__entity:
            property_aliases = '\n'.join([str(i.alias) + ' ' + str(i.borders) for i in entity.properties])
            result += f'Болезнь: {entity.alias}\n\nСимптомы:\n{property_aliases}\n\n\n'

        return result