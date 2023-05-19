from __future__ import annotations

import numpy as np

from decouple import config
from collections import defaultdict
from generator.mds import ClassInstances


MIN_TREND_PERIOD = int(config('MIN_TREND_PERIOD'))
MAX_TREND_PERIOD = int(config('MAX_TREND_PERIOD'))


# Inductive knowledge base
class IKB:
    def __init__(self) -> None:
        raise NotImplementedError()
    



class Alternative:
    def __init__(self, class_instances: ClassInstances, propery_alias: str) -> None:
        self.__main_class_instances = class_instances
        self.__ntp_instances = defaultdict(list)

        property_data = PropertyData(class_instances, propery_alias)

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
    def __init__(self, property_data: PropertyData, ntp: int, sep: list) -> None:
        self.__sep = sep
        self.__data = []
        self.__border = []

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
                self.__data.append(np.unique(property_data.vals[:sep[0]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[0]:]).tolist())
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
                self.__data.append(np.unique(property_data.vals[:sep[0]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[0]:sep[1]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[1]:]).tolist())
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
                self.__data.append(np.unique(property_data.vals[:sep[0]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[0]:sep[1]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[1]:sep[2]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[2]:]).tolist())
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
                self.__data.append(np.unique(property_data.vals[:sep[0]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[0]:sep[1]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[1]:sep[2]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[2]:sep[3]]).tolist())
                self.__data.append(np.unique(property_data.vals[sep[3]:]).tolist())
                self.__border.append([(max(property_data.om[:sep[0]]) + min(property_data.om[:sep[0]])) // 2] * 2)
                self.__border.append([(max(property_data.om[sep[0]:sep[1]]) + min(property_data.om[sep[0]:sep[1]])) // 2] * 2)
                self.__border.append([(max(property_data.om[sep[1]:sep[2]]) + min(property_data.om[sep[1]:sep[2]])) // 2] * 2)
                self.__border.append([(max(property_data.om[sep[2]:sep[3]]) + min(property_data.om[sep[2]:sep[3]])) // 2] * 2)
                self.__border.append([(max(property_data.om[sep[3]:]) + min(property_data.om[sep[3]:])) // 2] * 2)   
            
            self.__sep = sep
                    


    def __str__(self) -> str:
        return str(self.__data) + '\n' + str(self.__border)


    @property
    def sep(self) -> list:
        return self.__sep
    

    class MergingAlternatives:
        def __init__(self, alternative_1: Alternative, alternative_2: Alternative, ntp: int) -> None:
            