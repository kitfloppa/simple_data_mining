from __future__ import annotations

from generator.mkb import MKB
from generator.mds import MDS
from generator.ikb import IKB
from xlsx_maker import GeneratorXLSX


def main() -> None:
    mkb = MKB()
    mds = MDS(mkb)
    ikb = IKB(mkb, mds)
    
    xlsx = GeneratorXLSX('test')
    xlsx.add_mkb_sheet(mkb)
    xlsx.add_mds_sheet(mds)
    xlsx.add_ikb_sheet(ikb)
    xlsx.add_comparison_sheet(mkb, ikb)
    xlsx.close()


if __name__ == '__main__':
    main()