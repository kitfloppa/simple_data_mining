from __future__ import annotations

from generator.mkb import MKB

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
        self.__mkb_sheet.merge_range('V1:Y1', 'Верхние и нижние границы (ВГ и НГ)', column_format) # type: ignore

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


    def close(self) -> None:
        self.__workbook.close()