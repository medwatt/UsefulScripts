import re

class VHDL_Parser:
    def __init__(self, vhdl_string):
        self.vhdl_string = vhdl_string

    def get_entity_block(self):
        regex = r"\bentity\s+\w+.*?end([\w\s]+)?;"
        entity_block = self.get_block(regex, self.vhdl_string)
        if entity_block is not None:
            self.entity_block = entity_block
            # get entity name
            regex = r"\bentity\s(\w+)\sis"
            match = re.search(regex, self.entity_block, re.I)
            self.entity_name = match.group(1)
        else:
            raise ValueError("ERROR: VHDL file does not have an entity")

    def get_port_block(self):
        regex = r"port\s?\(.*?end"
        port_block = self.get_block(regex, self.entity_block)
        if port_block is not None:
            self.port_block = self.get_content_inside_parenthesis(port_block)
        else:
            raise ValueError("ERROR: VHDL file does not have ports")

    def get_generic_block(self):
        regex = r"generic\s?\(.*?end"
        generic_block = self.get_block(regex, self.entity_block)
        self.generic_block = None
        if generic_block:
            self.generic_block = self.get_content_inside_parenthesis(generic_block)

    def get_signals(self):
        regex = r"([\w,\s]+)\s?:\s?(?:in|out|inout)\s(.*?)(?=;)"
        signals = self.get_parameters_from_block(regex, self.port_block)
        if signals:
            self.signals = signals
        else:
            raise ValueError("ERROR: Check definition of the ports")

    def get_generics(self):
        regex = r"(\w.*?\w?)\s?:\s?(\w+).*?;"
        self.generics = None
        if self.generic_block:
            self.generics = self.get_parameters_from_block(regex, self.generic_block)

    def get_entity_name(self):
        regex = r"entity\s+(\w+)\sis"
        self.entity_name = self.get_name_from_block(regex, self.entity_block, None)

    def get_architecture_name(self):
        regex = r"architecture\s+(\w+)\sof"
        self.architecture_name = self.get_name_from_block(
            regex, self.vhdl_string, "__architecture_name__"
        )

    def get_clock_name(self):
        regex = r"\b(clk|clock)[\s\w,]*:\s*in.*?;"
        self.clock_name = self.get_name_from_block(regex, self.port_block, None)

    def get_reset_name(self):
        regex = r"\b(reset|rst|rstn|nrst)[\s\w,]*:\s*in.*?;"
        self.reset_name = self.get_name_from_block(regex, self.port_block, None)

    def get_name_from_block(self, regex, block, default_name):
        match = re.search(regex, block, re.I)
        return match.group(1) if match is not None else default_name

    def get_block(self, pattern, string):
        block_match = re.search(pattern, string, re.DOTALL | re.I)
        if block_match is not None:
            block = block_match.group(0)
            block = re.sub("--\s*.*?\n", " ", block)  # remove comments
            block = re.sub("\s+", " ", block)  # remove spaces, tabs, newlines, etc
            return block
        else:
            return None

    def get_parameters_from_block(self, pattern, block):
        matches = re.findall(pattern, block, re.I)
        parameters = {}
        if matches is not None:
            for line in matches:
                identifier_names = line[0].split(",")
                identifier_type = line[1]
                for name in identifier_names:
                    parameters[name.strip()] = identifier_type.strip()
        return parameters

    def get_content_inside_parenthesis(
        self, block, opening_paren="(", closing_paren=")"
    ):
        start_idx = block.index(opening_paren)
        open_count = 1
        pos = start_idx + 1
        while pos < len(block):
            if block[pos] == opening_paren:
                open_count += 1
            elif block[pos] == closing_paren:
                open_count -= 1
            if open_count == 0:
                break
            pos += 1
        return block[start_idx + 1 : pos] + ";"

    def parse_vhdl(self):
        self.get_entity_block()
        self.get_port_block()
        self.get_generic_block()
        self.get_signals()
        self.get_generics()
        self.get_entity_name()
        self.get_architecture_name()
        self.get_clock_name()
        self.get_reset_name()
        return self
