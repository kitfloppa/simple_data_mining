from __future__ import annotations

from generator.mkb import MKB
from generator.mds import MDS
from generator.ikb import IKB
from collections import defaultdict

import xlsxwriter as xw


class GeneratorXLSX:
    def __init__(self, file_name: str) -> None:
        self.__workbook = xw.Workbook(file_name + '.xlsx')


    def add_mkb_sheet(self, mkb: MKB) -> None:
        self.__mkb_sheet = self.__workbook.add_worksheet('МБЗ')

        column_format = self.__workbook.add_format({'bold': True, 'bg_color': '#9fdf9f', 'border': 1})
        cell_format = self.__workbook.add_format({'bg_color': '#9fdf9f', 'border': 1, 'text_wrap': True, 'valign': 'top'})

        self.__mkb_sheet.write('A1', 'Заболевания', column_format)
        self.__mkb_sheet.write('C1', 'Признаки', column_format)
        self.__mkb_sheet.merge_range('E1:F1', 'Возможные значения (ВЗ)', column_format) # type: ignore
        self.__mkb_sheet.merge_range('H1:I1', 'Нормальные значения (НЗ)', column_format) # type: ignore
        self.__mkb_sheet.merge_range('K1:L1', 'Клиническая картина (КК)', column_format) # type: ignore
        self.__mkb_sheet.merge_range('N1:P1', 'Число периодов динамики (ЧПД)', column_format) # type: ignore
        self.__mkb_sheet.merge_range('R1:U1', 'Значения для периода (ЗДП)', column_format) # type: ignore
        self.__mkb_sheet.merge_range('W1:AA1', 'Верхние и нижние границы (НГ и ВГ)', column_format) # type: ignore

        offset = 0

        for i, entity in enumerate(mkb.entity):
            self.__mkb_sheet.write(i + 1, 0, entity.alias, cell_format)

            for j, entity_property in enumerate(entity.properties):
                self.__mkb_sheet.write(i * len(entity.properties) + j + 1, 10, entity.alias, cell_format)
                self.__mkb_sheet.write(i * len(entity.properties) + j + 1, 11, entity_property.alias, cell_format)

            for j, entity_property in enumerate(entity.properties):
                self.__mkb_sheet.write(i * len(entity.properties) + j + 1, 13, entity.alias, cell_format)
                self.__mkb_sheet.write(i * len(entity.properties) + j + 1, 14, entity_property.alias, cell_format)
                self.__mkb_sheet.write(i * len(entity.properties) + j + 1, 15, entity_property.ntp, cell_format)

                for k in range(entity_property.ntp):
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 17, entity.alias, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 18, entity_property.alias, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 19, k + 1, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 20, str(entity_property.value_period[k]), cell_format)

                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 22, entity.alias, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 23, entity_property.alias, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 24, k + 1, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 25, entity_property.borders[k][0], cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 26, entity_property.borders[k][1], cell_format)
                offset += entity_property.ntp - 1
                
                    
        for i, entity_property in enumerate(mkb.entity[0].properties):
            self.__mkb_sheet.write(i + 1, 2, entity_property.alias, cell_format)
            
            self.__mkb_sheet.write(i + 1, 4, entity_property.alias, cell_format)
            self.__mkb_sheet.write(i + 1, 5, str(entity_property.possible_values), cell_format)

            self.__mkb_sheet.write(i + 1, 7, entity_property.alias, cell_format)
            self.__mkb_sheet.write(i + 1, 8, str(entity_property.normal_value), cell_format)

    
    def add_mds_sheet(self, mds: MDS) -> None:
        self.__mds_sheet = self.__workbook.add_worksheet('МВД')

        column_format = self.__workbook.add_format({'bold': True, 'bg_color': '#9fdf9f', 'border': 1})
        cell_format = self.__workbook.add_format({'bg_color': '#9fdf9f', 'border': 1, 'text_wrap': True, 'valign': 'top'})

        self.__mds_sheet.merge_range('A1:E1', '(ИБ, признак, номер ПД, длительность ПД, число МН в ПД)', column_format) # type: ignore
        self.__mds_sheet.merge_range('G1:J1', 'Выборка данных (ИБ, признак, МН, значение в МН)', column_format) # type: ignore

        offset = 0
        offset_om_out = 0

        for i, class_instance in enumerate(mds.class_instances):
            duration_offset = 0
            offset_om_int = 0
            for j, property in enumerate(class_instance.properties):
                for k, value_period in enumerate(property.value_period):
                    self.__mds_sheet.write(i * len(class_instance.properties) + j + offset + k + 1, 0, class_instance.alias, cell_format)
                    self.__mds_sheet.write(i * len(class_instance.properties) + j + offset + k + 1, 1, property.alias, cell_format)
                    self.__mds_sheet.write(i * len(class_instance.properties) + j + offset + k + 1, 2, str(k + 1), cell_format)
                    self.__mds_sheet.write(i * len(class_instance.properties) + j + offset + k + 1, 3, str(class_instance.duration_period[duration_offset + k]), cell_format)
                    self.__mds_sheet.write(i * len(class_instance.properties) + j + offset + k + 1, 4, str(class_instance.observation_moments_numbers[duration_offset + k]), cell_format)
                    
                    for l in range(class_instance.observation_moments_numbers[duration_offset + k]):
                        self.__mds_sheet.write(offset_om_out + l + 1, 6, class_instance.alias, cell_format)
                        self.__mds_sheet.write(offset_om_out + l + 1, 7, property.alias, cell_format)
                        self.__mds_sheet.write(offset_om_out + l + 1, 8, str(class_instance.observation_moments[offset_om_int + l]), cell_format)
                        self.__mds_sheet.write(offset_om_out + l + 1, 9, str(class_instance.observation_moments_val[offset_om_int + l]), cell_format)

                    offset_om_out += class_instance.observation_moments_numbers[duration_offset + k]
                    offset_om_int += class_instance.observation_moments_numbers[duration_offset + k]

                duration_offset += len(property.value_period)
                offset += property.ntp - 1


    def add_ikb_sheet(self, ikb: IKB) -> None:
        self.__ikb_sheet = self.__workbook.add_worksheet('ИФБЗ')

        column_format = self.__workbook.add_format({'bold': True, 'bg_color': '#9fdf9f', 'border': 1})
        cell_format = self.__workbook.add_format({'bg_color': '#9fdf9f', 'border': 1, 'text_wrap': True, 'valign': 'top'})
        
        self.__ikb_sheet.write('A1', 'Итерация ИФБЗ', column_format)
        self.__ikb_sheet.write('B1', 'Заболевания', column_format)
        self.__ikb_sheet.write('C1', 'Признаки', column_format)
        self.__ikb_sheet.write('D1', 'Альтернативы', column_format)
        self.__ikb_sheet.write('E1', 'ЧПД', column_format)
        self.__ikb_sheet.write('F1', 'Период', column_format)
        self.__ikb_sheet.write('G1', 'НГ-ВГ', column_format)
        self.__ikb_sheet.write('H1', 'ВЗ', column_format)
        
        offset = 0
        
        for i, iter in enumerate(ikb.iterations):
            for j, key in enumerate(iter.keys()):
                for k, prop in enumerate(iter[key].alternative_property.keys()):
                    alter = 1
                    for h in range(1, 6):
                        for vdp in iter[key].alternative_property[prop].ntp_instances[h]:
                            period = 0
                            for d, b in zip(vdp.data, vdp.border): # type: ignore
                                period += 1
                                self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 0, 'Итерация - ' + str(i + 1), cell_format)
                                self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 1, key, cell_format)
                                self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 2, prop, cell_format)
                                self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 3, alter, cell_format)
                                self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 4, h, cell_format)
                                self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 5, period, cell_format)
                                self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 6, str(b), cell_format)
                                if isinstance(d[0], int) and sum(d) > 1:
                                    self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 7, str([min(d), max(d)]), cell_format)
                                else:
                                    self.__ikb_sheet.write(i * len(ikb.iterations) + j * len(iter.keys()) + k + offset + 1, 7, str(d), cell_format)
                                offset += 1
                            alter += 1
                    offset -= 1
            offset += 1

        
    def add_comparison_sheet(self, mkb: MKB, ikb: IKB):
        self.__comparison_sheet = self.__workbook.add_worksheet('МБЗ vs. ИФБЗ')

        column_format = self.__workbook.add_format({'bold': True, 'bg_color': '#9fdf9f', 'border': 1})
        cell_format = self.__workbook.add_format({'bg_color': '#9fdf9f', 'border': 1, 'text_wrap': True, 'valign': 'top'})

        self.__comparison_sheet.merge_range('A1:C1', 'Число периодов динамики (МБЗ)', column_format) # type: ignore
        self.__comparison_sheet.merge_range('E1:G1', 'Число периодов динамики (ИФБЗ)', column_format) # type: ignore
        self.__comparison_sheet.merge_range('I1:L1', 'Значения для периода (МБЗ)', column_format) # type: ignore
        self.__comparison_sheet.merge_range('N1:Q1', 'Значения для периода (ИФБЗ)', column_format) # type: ignore
        
        offset = 0
        offset_2 = 0
        offset_3 = 0
        ntp_percent = {}
        property_ntp = defaultdict(list)
        
        for i, entity in enumerate(mkb.entity):
            ntp_percent[entity.alias] = [0, len(entity.properties)]
            for j, entity_property in enumerate(entity.properties):
                offset += 1
                property_ntp[entity.alias].append(entity_property.ntp)
                
                self.__comparison_sheet.write(i * len(entity.properties) + j + 1, 0, entity.alias, cell_format)
                self.__comparison_sheet.write(i * len(entity.properties) + j + 1, 1, entity_property.alias, cell_format)
                self.__comparison_sheet.write(i * len(entity.properties) + j + 1, 2, entity_property.ntp, cell_format)

                for k in range(entity_property.ntp):
                    self.__comparison_sheet.write(i * len(entity.properties) + j + offset_2 + k + 1, 8, entity.alias, cell_format)
                    self.__comparison_sheet.write(i * len(entity.properties) + j + offset_2 + k + 1, 9, entity_property.alias, cell_format)
                    self.__comparison_sheet.write(i * len(entity.properties) + j + offset_2 + k + 1, 10, k + 1, cell_format)
                    self.__comparison_sheet.write(i * len(entity.properties) + j + offset_2 + k + 1, 11, str(entity_property.value_period[k]), cell_format)
                offset_2 += entity_property.ntp - 1

        for i, key in enumerate(ikb.iterations[-1].keys()):
                for j, prop in enumerate(ikb.iterations[-1][key].alternative_property.keys()):
                    ntp = []

                    for h in range(1, 6):
                        if len(ikb.iterations[-1][key].alternative_property[prop].ntp_instances[h]) != 0:
                            ntp.append(h)

                    if property_ntp[key][j] in ntp:
                        ntp_percent[key][0] += 1

                    self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + 1, 4, key, cell_format)
                    self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + 1, 5, prop, cell_format)
                    self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + 1, 6, str(ntp), cell_format)

                    step = 1
                    if len(ikb.iterations[-1][key].alternative_property[prop].ntp_instances[property_ntp[key][j]]) != 0:
                        for vdp in [ikb.iterations[-1][key].alternative_property[prop].ntp_instances[property_ntp[key][j]][0]]:
                            for d, b in zip(vdp.data, vdp.border): # type: ignore
                                self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 13, key, cell_format)
                                self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 14, prop, cell_format)
                                self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 15, step, cell_format)
                                if isinstance(d[0], int) and sum(d) > 1:
                                    self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 16, str([min(d), max(d)]), cell_format)
                                else:
                                    self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 16, str(d), cell_format)
                                step += 1
                                offset_3 += 1
                    else:
                        for h in range(property_ntp[key][j]):
                            self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 13, key, cell_format)
                            self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 14, prop, cell_format)
                            self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 15, h + 1, cell_format)
                            self.__comparison_sheet.write(i * len(ikb.iterations[-1][key].alternative_property.keys()) + j + offset_3 + 1, 15, '', cell_format)
                            offset_3 += 1
                    offset_3 -= 1


        persent_sum = 0

        for i, key in enumerate(ntp_percent.keys()):
            persent_sum += (ntp_percent[key][0] / ntp_percent[key][1]) * 100

            self.__comparison_sheet.write(offset + 2 + i, 3, key, cell_format)
            self.__comparison_sheet.write(offset + 2 + i, 4, str('{:.2f}'.format((ntp_percent[key][0] / ntp_percent[key][1]) * 100)) + ' %', cell_format)

        
        self.__comparison_sheet.write(offset + 4 + len(ntp_percent.keys()), 3, 'Средний процент совпадения ЧПД', cell_format)
        self.__comparison_sheet.write(offset + 4 + len(ntp_percent.keys()), 4, str('{:.2f}'.format(persent_sum / len(ntp_percent.keys()))) + ' %', cell_format)


    def close(self) -> None:
        self.__workbook.close()