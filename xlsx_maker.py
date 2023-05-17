from __future__ import annotations

from generator.mkb import MKB
from generator.mds import MDS
from generator.ikb import IKB

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
        self.__mkb_sheet.merge_range('R1:T1', 'Значения для периода (ЗДП)', column_format) # type: ignore
        self.__mkb_sheet.merge_range('V1:Y1', 'Верхние и нижние границы (НГ и ВГ)', column_format) # type: ignore

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
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 19, str(entity_property.value_period[k]), cell_format)

                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 21, entity.alias, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 22, entity_property.alias, cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 23, entity_property.borders[k][0], cell_format)
                    self.__mkb_sheet.write(i * len(entity.properties) + j + offset + k + 1, 24, entity_property.borders[k][1], cell_format)
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
        raise NotImplementedError()


    def close(self) -> None:
        self.__workbook.close()