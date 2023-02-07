import common
from common import ConstructionError as ctor


###################
##  Data Parser  ##
###################

# ---------------------------------------------
## Class for reading the input file, parsing each line, and storing the parsed data
class Parser:

    def __init__(self, filepath: str):        
        # check ctor arg type
        ctor.check_arg_type("Failed to initialize Parser obj (arg must be type 'str')", filepath, str)
        # verify the file exists
        common.check_path_exists(filepath)
        self.__file = filepath
        self.__parsed_data = None
        self.__parse_input_file()

    @property
    def file(self):
        return self.__file

    @property
    def parsed_data(self):
        return self.__parsed_data
    @parsed_data.setter
    def parsed_data(self, content):
        common.check_arg_type(content, list, "parsed_data.setter -> must be of type 'list'")
        self.__parsed_data = content

    # Generator to read the input file line by line
    def __file_reader(self, file: str):
        with open(file, newline='') as f:
            print(f"...Opening input file and parsing data...")
            for row in f.readlines():
                yield row.rstrip()

    # Parser method
    def __parse_input_file(self):
        # read in one line at a time from the input file for parsing
        self.parsed_data = list()        
        for line in self.__file_reader(self.file):
            # split the i.d. from its subnets/masks
            line_split = line.split(':')
            id, subnets = line_split[0], line_split[1].split(',')
            parsed_subnets = list()
            # split sub address & mask, convert valid ipv4 to 'int', store sub & mask as a pair
            for subnet in subnets:
                if '/' not in subnet:
                    continue
                addr, mask = subnet.split('/')
                addr = common.ipv4_to_int(addr)
                mask = common.ipv4_to_int(mask)
                parsed_subnets.append([addr, mask])  
            # sort sub/mask pairs for the current id line; append the parsed line to the datatable
            parsed_subnets.sort()
            self.__parsed_data.append([id, parsed_subnets])
        # finally, sort the completed parsed data table by id #
        self.__parsed_data.sort()
        print("...Data successfully parsed.")