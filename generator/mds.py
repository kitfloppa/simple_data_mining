from __future__ import annotations

import secrets
import numpy as np

from decouple import config
from generator.mkb import MKB
from generator.entities import Entity
from generator.random_generator import RandomGenerator


CLASS_INSTANCES_COUNT = int(config('CLASS_INSTANCES_COUNT'))
COUNT_MOMENTS_OBSERVATION = int(config('COUNT_MOMENTS_OBSERVATION')) + 1


# Model data set
class MDS:
    def __init__(self, mkb: MKB) -> None:
        self.__mkb = mkb
        self.__class_instances = []

        for entity in self.__mkb.entity:
            for i in range(CLASS_INSTANCES_COUNT):
                self.__class_instances.append(ClassInstances(entity, i + 1))

    
    def __str__(self) -> str:
        string = '\n'.join([class_instance.alias + ' ' + str(class_instance.observation_moments) for class_instance in self.__class_instances])

        return string


    @property
    def class_instances(self) -> list:
        return self.__class_instances
        


class ClassInstances:
    def __init__(self, entity: Entity, number: int) -> None:
        self.__alias = 'Экземпляр ' + entity.alias + ' - ' + str(number)
        self.__main_entity = entity
        self.__duration_period = []
        self.__observation_moments = []
        self.__observation_moments_val = []
        self.__observation_moments_counts = []
        self.__observation_moments_numbers = []

        for i, property in enumerate(self.__main_entity.properties):
            rand_gen_om = RandomGenerator(1, COUNT_MOMENTS_OBSERVATION)
            sum_observation_moments = 1
            for border, val_period in zip(property.borders, property.value_period):
                if not isinstance(val_period, list):
                    val_period = [val_period]

                rand_gen_dp = RandomGenerator(border[0], border[1])
                tmp_duration_period = rand_gen_dp.randint()
                self.__duration_period.append(tmp_duration_period)
                
                observation_moment = rand_gen_om.randint()
                self.__observation_moments_numbers.append(observation_moment)

                rand_gen = RandomGenerator(sum_observation_moments, sum_observation_moments + tmp_duration_period + 1)
                sum_observation_moments += tmp_duration_period
                tmp_observation_moments = []
                tmp_observation_moments_val = []
                
                for _ in range(observation_moment):
                    rand_observation_moment = rand_gen.randint()

                    while rand_observation_moment in tmp_observation_moments:
                        rand_observation_moment = rand_gen.randint()
                    
                    tmp_observation_moments.append(rand_observation_moment)

                    if type(val_period[0]) is np.ndarray:
                        tmp_observation_moments_val.append(secrets.choice(range(val_period[0][0], val_period[0][1] + 1)))
                    else:
                        tmp_observation_moments_val.append(secrets.choice(val_period))

                self.__observation_moments += sorted(tmp_observation_moments)
                self.__observation_moments_counts.append(len(tmp_observation_moments))
                self.__observation_moments_val += tmp_observation_moments_val

                



    @property
    def alias(self) -> str:
        return self.__alias
    

    @property
    def duration_period(self) -> list:
        return self.__duration_period
    

    @property
    def observation_moments_numbers(self) -> list:
        return self.__observation_moments_numbers
    

    @property
    def observation_moments(self) -> list:
        return self.__observation_moments
    
    @property
    def observation_moments_val(self) -> list:
        return self.__observation_moments_val
    
    @property
    def observation_moments_counts(self) -> list:
        return self.__observation_moments_counts
    

    @property
    def properties(self) -> list:
        return self.__main_entity.properties