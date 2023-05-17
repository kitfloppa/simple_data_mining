from __future__ import annotations

from generator.mkb import MKB
from generator.mds import MDS
from xlsx_maker import GeneratorXLSX


from generator.ikb import PropertyData, Alternative

def main() -> None:
    mkb = MKB()
    mds = MDS(mkb)

    Alternative(mds.class_instances[0], 'Кашель')
    
    #xlsx = GeneratorXLSX('test')
    #xlsx.add_mkb_sheet(mkb)
    #xlsx.add_mds_sheet(mds)
    #xlsx.close()



if __name__ == '__main__':
    main()