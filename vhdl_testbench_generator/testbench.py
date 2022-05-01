from parser import VHDL_Parser

class VHDL_TB:
    def __init__(self, vhdl_string):
        self.parser = VHDL_Parser(vhdl_string).parse_vhdl()
        self.clock_period = "5 ns"

    def return_signals(self):
        self.signal_def_block, _ = self.build_block_from_table(
                self.parser.signals, "signals", "port", "signal"
                )
        return "\n".join(self.signal_def_block)

    def __call__(self):
        self.build_library_block()
        self.build_entity_block()
        self.build_architecture_block()

        compose_block = [
                self.library_block,
                self.entity_block,
                self.architecture_block
                ]

        tb_string = ""
        for block in compose_block:
            tb_string += "\n".join(block)

        return tb_string

    def build_library_block(self):
        self.library_block = [
                "library ieee;",
                "use ieee.std_logic_1164.all;",
                "\n"
                ]

    def build_entity_block(self):
        self.entity_block = [
                f"entity {self.parser.entity_name}_tb is",
                f"end {self.parser.entity_name}_tb;",
                "\n"
                ]

    def build_uut_block(self):

        compose_block = [
                f"\tuut: entity work.{self.parser.entity_name}({self.parser.architecture_name})",
                self.generic_uut_block,
                self.signal_uut_block,
                ""
                ]

        self.uut_block = []
        for block in compose_block:
            if isinstance(block, list):
                self.uut_block.extend(block)
            elif isinstance(block, str):
                self.uut_block.append(block)

    def build_architecture_block(self):
        self.generic_def_block, self.generic_uut_block = self.build_block_from_table(
                self.parser.generics, "component generics", "generic", "constant"
                )
        self.signal_def_block, self.signal_uut_block = self.build_block_from_table(
                self.parser.signals, "component ports", "port", "signal"
                )
        self.build_uut_block()
        self.build_clock_block()
        self.build_reset_block()
        self.build_stimulus_block()

        compose_block = [
                f"architecture testbench of {self.parser.entity_name}_tb is",
                self.generic_def_block,
                self.signal_def_block,
                self.clock_def_block,
                "",
                "begin",
                "",
                self.uut_block,
                self.clock_block,
                self.reset_block,
                self.stimulus_block,
                "end testbench"
                ]

        self.architecture_block = []
        for block in compose_block:
            if isinstance(block, list):
                self.architecture_block.extend(block)
            elif isinstance(block, str):
                self.architecture_block.append(block)

    def build_clock_block(self):
        self.clock_block = None
        clock_name = self.parser.clock_name
        if clock_name:
            self.clock_block = [
                    "\t-- clock generation",
                    f"\t{clock_name} <= not {clock_name} after {self.clock_period};",
                    ""
                    ]

            self.clock_def_block = [
                    "\n\t-- clock",
                    f"\tsignal {clock_name}: std_logic := '1';",
                    ]

    def build_reset_block(self):
        self.reset_block = None
        reset_name = self.parser.reset_name
        if reset_name:
            if (reset_name == "reset") or (reset_name == "rst"):
                self.reset_block = [
                        "\t-- reset generation",
                        f"\t{reset_name} <= '1', '0' after {self.clock_period};",
                        ""
                        ]
            else:
                self.reset_block = [
                        "\t-- reset generation",
                        f"\t{reset_name} <= '0', '1' after {self.clock_period};",
                        ""
                        ]

    def build_stimulus_block(self):
        self.stimulus_block = [
                "\t-- waveform generation",
                "\tWaveGen_Proc: process",
                "\tbegin",
                "\t-- insert signal assignments here"
                "\n",
                "\tend process;",
                ""
                ]

    def build_block_from_table(
            self, table, comment_block_title, map_block_title, obj_name
            ):
        arch_block = None
        uut_block = None
        if table:
            arch_block = [None] * (len(table) + 1)
            arch_block[0] = f"\n\t-- {comment_block_title}"

            uut_block = [None] * (len(table) + 2)
            uut_block[0] = f"\t{map_block_title} map ("
            uut_block[-1] = "\t)"

            for idx, (identifier_name, identifier_type) in enumerate(table.items()):
                arch_block[idx + 1] = f"\t{obj_name} {identifier_name}: {identifier_type};"
                uut_block[idx + 1] = f"\t\t{identifier_name} => {identifier_name},"

            # remove the comma in the last item of the map block
            uut_block[-2] = uut_block[-2][:-1]

            # add a semicolon to the uut signal block to close it
            if map_block_title == "port":
                uut_block[-1] = uut_block[-1] + ";"

        return arch_block, uut_block
