from __future__ import annotations

from generator.mkb import MKB
from xlsx_maker import GeneratorXLSX

def main() -> None:
    mkb = MKB()
    
    xlsx = GeneratorXLSX('test')
    xlsx.add_mkb_sheet(mkb)
    xlsx.close()



if __name__ == '__main__':
    main()