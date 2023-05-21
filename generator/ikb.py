from __future__ import annotations

import numpy as np

from copy import deepcopy
from decouple import config
from generator.mkb import MKB
from generator.mds import MDS
from collections import defaultdict
from generator.mds import ClassInstances


MIN_TREND_PERIOD = int(config('MIN_TREND_PERIOD'))
MAX_TREND_PERIOD = int(config('MAX_TREND_PERIOD'))

CLASS_INSTANCES_COUNT = int(config('CLASS_INSTANCES_COUNT'))


# Inductive knowledge base
class IKB:
    def __init__(self, mkb: MKB, mds: MDS) -> None:
        entity_len = len(mkb.entity)
        properties_name = [i.alias for i in mkb.entity[0].properties]
        self.__alternative_class_instances = []
        self.__ikb_iterations = []
        merging_alternatives = {}
        
        for i in range(entity_len):
            for j in range(CLASS_INSTANCES_COUNT):
                self.__alternative_class_instances.append(AlternativeClassInstances(mds.class_instances[i * entity_len + j]))
                
        for i in range(entity_len):
            for j in range(CLASS_INSTANCES_COUNT):
                if mkb.entity[i].alias not in merging_alternatives.keys():
                    merging_alternatives[mkb.entity[i].alias] = self.__alternative_class_instances[i * entity_len + j]
                    self.__ikb_iterations.append(deepcopy(merging_alternatives))
                else:
                    merging_alternatives[mkb.entity[i].alias] = merging_alternatives[mkb.entity[i].alias] + self.__alternative_class_instances[i * entity_len + j]
                    self.__ikb_iterations.append(deepcopy(merging_alternatives))
    
    
    def __str__(self) -> str:
        for i in self.__ikb_iterations:
            for key in i.keys():
                for j in i[key].alternative_property.keys():
                    print(i[key].alternative_property[j])
            print('-------------------')
        
        return ''
    
    
    @property
    def alternative_class_instances(self) -> list:
        return self.__alternative_class_instances
    
    
    @property
    def iterations(self) -> list:
        return self.__ikb_iterations
    



class Alternative:
    def __init__(self, *args) -> None:
        if len(args) == 2:
            self.__main_class_instances = args[0]
            self.__ntp_instances = defaultdict(list)

            property_data = PropertyData(args[0], args[1])

            self.__ntp_instances[1].append(VDP(property_data, 1, [0]))
            
            sep = [0, 0]

            while sep[0] != len(property_data.vals):
                vdp = VDP(property_data, 2, sep)
                sep = vdp.sep

                if sep[0] == 0:
                    break
                else:
                    self.__ntp_instances[2].append(vdp)
                    
            sep = [0, 0]
            
            while sep[0] != len(property_data.vals):
                vdp = VDP(property_data, 3, sep)
                sep = vdp.sep
        
                if 0 in sep:
                    break
                else:
                    self.__ntp_instances[3].append(vdp)

            sep = [0, 0, 0]
            
            while sep[0] != len(property_data.vals):
                vdp = VDP(property_data, 4, sep)
                sep = vdp.sep
        
                if 0 in sep:
                    break
                else:
                    self.__ntp_instances[4].append(vdp)

            sep = [0, 0, 0, 0]
            
            while sep[0] != len(property_data.vals):
                vdp = VDP(property_data, 5, sep)
                sep = vdp.sep
        
                if 0 in sep:
                    break
                else:
                    self.__ntp_instances[5].append(vdp)
        else:
            self.__main_class_instances = None
            self.__ntp_instances = defaultdict(list)
                
    
    def __str__(self) -> str:
        res = ''
        
        for i in self.__ntp_instances[1]:
            print(i)
        print()
        for i in self.__ntp_instances[2]:
            print(i)
        print()
        for i in self.__ntp_instances[3]:
            print(i)
        print()
        for i in self.__ntp_instances[4]:
            print(i)
        print()
        for i in self.__ntp_instances[5]:
            print(i)
        
        return res
    
    
    def __add__(self, other: Alternative) -> Alternative:
        new_class = Alternative()
        new_class.__main_class_instances = self.__main_class_instances
        
        for i in range(1, 6):
            if i in self.__ntp_instances.keys() and i in other.__ntp_instances.keys():
                for j in self.__ntp_instances[i]:
                    for k in other.__ntp_instances[i]:
                        vdp = j + k
                        if not vdp.delet:
                            new_class.__ntp_instances[i].append(j + k)
        
        return new_class
    

    @property
    def ntp_instances(self) -> defaultdict:
        return self.__ntp_instances

        
class PropertyData:
    def __init__(self, class_instances: ClassInstances, propery_alias: str) -> None:
        self.__property_vals = []
        self.__observation_moments = []
        
        ntp_offset = 0
        om_offset = 0

        for property in class_instances.properties:
            if property.alias != propery_alias:
                om_offset += sum(class_instances.observation_moments_numbers[ntp_offset:ntp_offset + property.ntp])
                ntp_offset += property.ntp
            else:
                self.__property_vals.extend(class_instances.observation_moments_val[om_offset:om_offset +
                        sum(class_instances.observation_moments_numbers[ntp_offset:ntp_offset + property.ntp])])
                
                self.__observation_moments.extend(class_instances.observation_moments[om_offset:om_offset +
                        sum(class_instances.observation_moments_numbers[ntp_offset:ntp_offset + property.ntp])])

                break


    def __str__(self) -> str:
        return str(self.__property_vals) + '\n' + str(self.__observation_moments)
    

    @property
    def vals(self) -> list:
        return self.__property_vals
    

    @property
    def om(self) -> list:
        return self.__observation_moments
    

class VDP:
    def __init__(self, *args) -> None:
        if len(args) == 3:
            sep = args[2]
            ntp = args[1]
            property_data = args[0]
            
            self.__sep = sep
            self.__data = []
            self.__border = []
            self.__delet = False

            if ntp == 1:
                self.__data.append(np.unique(property_data.vals).tolist())
                self.__border.append([max(property_data.om)] * 2)
            elif ntp == 2:
                sep = [0]
                flag = False
                for i in range(self.__sep[0] + 1, len(property_data.vals)):
                    if len(list(set(property_data.vals[:i]) & set(property_data.vals[i:]))) == 0:
                        sep[0] = i
                        break

                if sep[0] != 0:
                    self.__data.append(list(set(property_data.vals[:sep[0]])))
                    self.__data.append(list(set(property_data.vals[sep[0]:])))
                    self.__border.append([(max(property_data.om[:sep[0]]) + min(property_data.om[:sep[0]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[0]:]) + min(property_data.om[sep[0]:])) // 2] * 2)

                self.__sep = sep
            elif ntp == 3:
                sep = [0, 0]
                flag = False
                
                if self.__sep[0] >= 1 and self.__sep[1] < len(property_data.vals):
                    self.__sep[0] -= 1

                for i in range(self.__sep[0] + 1, len(property_data.vals)):
                    for j in range(i + 1, len(property_data.vals)):
                        if j > self.__sep[1]:
                            if len(list(set(property_data.vals[:i]) & set(property_data.vals[i:j]))) + len(list(set(property_data.vals[i:j]) & set(property_data.vals[j:]))) == 0:
                                sep = [i, j]
                                flag = True
                                break
                    self.__sep[1] = 0
                    if flag:
                        break
                
                if 0 not in sep:
                    self.__data.append(list(set(property_data.vals[:sep[0]])))
                    self.__data.append(list(set(property_data.vals[sep[0]:sep[1]])))
                    self.__data.append(list(set(property_data.vals[sep[1]:])))
                    self.__border.append([(max(property_data.om[:sep[0]]) + min(property_data.om[:sep[0]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[0]:sep[1]]) + min(property_data.om[sep[0]:sep[1]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[1]:]) + min(property_data.om[sep[1]:])) // 2] * 2)


                self.__sep = sep
            elif ntp == 4:
                sep = [0, 0, 0]

                if self.__sep[0] >= 1 and self.__sep[1] < len(property_data.vals) and self.__sep[2] < len(property_data.vals):
                    self.__sep[0] -= 1

                flag = False
                for i in range(self.__sep[0] + 1, len(property_data.vals)):
                    for j in range(i + 1, len(property_data.vals)):
                        if j > self.__sep[1]:
                            for k in range(j + 1, len(property_data.vals)):
                                if k > self.__sep[2]:
                                    if len(list(set(property_data.vals[:i]) & set(property_data.vals[i:j]))) + len(list(set(property_data.vals[i:j]) & set(property_data.vals[j:k]))) + \
                                    len(list(set(property_data.vals[j:k]) & set(property_data.vals[k:]))) == 0:
                                        sep = [i, j, k]
                                        flag = True
                                        break
                            self.__sep[2] = 0
                            if flag:
                                break
                    self.__sep[1] = 0
                    if flag:
                        break

                if 0 not in sep:
                    self.__data.append(list(set(property_data.vals[:sep[0]])))
                    self.__data.append(list(set(property_data.vals[sep[0]:sep[1]])))
                    self.__data.append(list(set(property_data.vals[sep[1]:sep[2]])))
                    self.__data.append(list(set(property_data.vals[sep[2]:])))
                    self.__border.append([(max(property_data.om[:sep[0]]) + min(property_data.om[:sep[0]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[0]:sep[1]]) + min(property_data.om[sep[0]:sep[1]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[1]:sep[2]]) + min(property_data.om[sep[1]:])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[2]:]) + min(property_data.om[sep[1]:])) // 2] * 2)
                    
                self.__sep = sep
            elif ntp == 5:
                sep = [0, 0, 0, 0]

                if self.__sep[0] >= 1 and self.__sep[1] < len(property_data.vals) and self.__sep[2] < len(property_data.vals) and self.__sep[3] < len(property_data.vals):
                    self.__sep[0] -= 1

                flag = False
                for i in range(self.__sep[0] + 1, len(property_data.vals)):
                    for j in range(i + 1, len(property_data.vals)):
                        if j > self.__sep[1]:
                            for k in range(j + 1, len(property_data.vals)):
                                if k > self.__sep[2]:
                                    for h in range(k + 1, len(property_data.vals)):
                                        if h > self.__sep[3]:
                                            if len(list(set(property_data.vals[:i]) & set(property_data.vals[i:j]))) + len(list(set(property_data.vals[i:j]) & set(property_data.vals[j:k]))) + \
                                            len(list(set(property_data.vals[j:k]) & set(property_data.vals[k:h]))) + len(list(set(property_data.vals[k:h]) & set(property_data.vals[h:]))) == 0:
                                                sep = [i, j, k, h]
                                                flag = True
                                                break
                                    self.__sep[3] = 0
                                    if flag:
                                        break
                            self.__sep[2] = 0
                            if flag:
                                break
                    self.__sep[1] = 0
                    if flag:
                            break
                
                if 0 not in sep:
                    self.__data.append(list(set(property_data.vals[:sep[0]])))
                    self.__data.append(list(set(property_data.vals[sep[0]:sep[1]])))
                    self.__data.append(list(set(property_data.vals[sep[1]:sep[2]])))
                    self.__data.append(list(set(property_data.vals[sep[2]:sep[3]])))
                    self.__data.append(list(set(property_data.vals[sep[3]:])))
                    self.__border.append([(max(property_data.om[:sep[0]]) + min(property_data.om[:sep[0]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[0]:sep[1]]) + min(property_data.om[sep[0]:sep[1]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[1]:sep[2]]) + min(property_data.om[sep[1]:sep[2]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[2]:sep[3]]) + min(property_data.om[sep[2]:sep[3]])) // 2] * 2)
                    self.__border.append([(max(property_data.om[sep[3]:]) + min(property_data.om[sep[3]:])) // 2] * 2)   
                
                self.__sep = sep
                
        else:
            self.__sep = []
            self.__data = []
            self.__border = []
            self.__delet = False
                    

    def __add__(self, other: VDP) -> VDP:
        new_class = VDP()
        new_class.__sep = self.__sep
        new_class.__delet = False
        
        for i in range(len(self.__data)):
            print(set(self.__data[i] + other.__data[i]))
            new_class.__data.append(sorted(list(set(self.__data[i] + other.__data[i]))))
            new_class.__border.append([min(self.__border[i] + other.__border[i]), max(self.__border[i] + other.__border[i])])

        for i in range(len(self.__data) - 1):
            if len(list(set(new_class.__data[i]) & set(new_class.__data[i + 1]))) != 0:
                new_class.__delet = True

            if isinstance(new_class.__data[i][0], int) and sum(new_class.__data[i]) > 1:
                if len(list(set(range(min(new_class.__data[i]), max(new_class.__data[i]) + 1)) & \
                    set(range(min(new_class.__data[i + 1]), max(new_class.__data[i + 1]) + 1)))) != 0:
                    new_class.__delet = True

        return new_class
    

    def __str__(self) -> str:
        return str(self.__data) + '\n' + str(self.__border)


    @property
    def sep(self) -> list:
        return self.__sep
    

    @property
    def data(self) -> list:
        return self.__data
    

    @property
    def border(self) -> list:
        return self.__border
    

    @property
    def delet(self) -> bool:
        return self.__delet
    
    
class AlternativeClassInstances:
    def __init__(self, *args) -> None:
        self.__alternative_property = {}
        
        if len(args) == 1:
            for property in args[0].properties:
                self.__alternative_property[property.alias] = Alternative(args[0], property.alias)
            
            
    def __add__(self, other: AlternativeClassInstances) -> AlternativeClassInstances:
        new_class = {}
        for key in self.__alternative_property.keys():
            new_class[key] = self.__alternative_property[key] + other.__alternative_property[key]
            
        res =  AlternativeClassInstances()
        res.__alternative_property = new_class
        
        return res
            
    
    def __str__(self) -> str:
        for i in self.__alternative_property.keys():
            print(self.__alternative_property[i])
        
        return ''
    
            
    @property
    def alternative_property(self) -> dict:
        return self.__alternative_property
            

class MergingAlternatives:
    def __init__(self, alternative_class_properties: list) -> None:
        associations_alternatives = defaultdict(list)
        
        for alternative_property in alternative_class_properties:
            for j in range(1, 6):
                associations_alternatives[j].append(alternative_property[j])
            
    
    # def __str__(self) -> str:
    #     pass