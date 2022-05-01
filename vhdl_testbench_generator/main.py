import pathlib
import sys
from testbench import VHDL_TB

if __name__ == "__main__":
    vhdl_string = pathlib.Path(sys.argv[1]).read_text()

    tb = VHDL_TB(vhdl_string)()
    print(tb)
