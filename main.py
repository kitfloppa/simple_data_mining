from __future__ import annotations

from generator.mkb import MKB
from generator.mds import MDS
from generator.ikb import IKB
from xlsx_maker import GeneratorXLSX


def main() -> None:
    mkb = MKB()
    mds = MDS(mkb)
    ikb = IKB(mkb, mds)
    
    
    print(ikb)
    
    
    xlsx = GeneratorXLSX('test')
    xlsx.add_mkb_sheet(mkb)
    xlsx.add_mds_sheet(mds)
    xlsx.close()


if __name__ == '__main__':
    main()