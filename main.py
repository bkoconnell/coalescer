#!/usr/bin/env python3

import sys
import os
import csv
# local modules
import dataparser
import coalescence
import common
from common import ConstructionError as ctor


####################
##  Main Program  ##
####################

# ---------------------------------------------
## Class for writing the coalesced data to the output file
class FileWriter:
        
    def __init__(self, filepath: str, data: list):
        # check ctor arg types
        ctor.check_arg_type("Failed to construct FileWriter obj (arg1 must be type 'str')", filepath, str)
        ctor.check_arg_type("Failed to construct FileWriter obj (arg2 must be type 'list')", data, list)
        # check that a file name exists in the 'filepath' arg
        if filepath.endswith('/'):
            raise ctor(f"File name is missing from the output filepath arg: '{filepath}'")
        self.__outfile = filepath
        self.__output_data = data
        self.__check_dir()

    @property
    def outfile(self):
        return self.__outfile

    @property
    def output_data(self):
        return self.__output_data

    # check if output directory exists; create the directory if needed
    def __check_dir(self):
        if '/' not in self.outfile:
            print(f"...Output directory not specified.")
        else:
            dirpath_end_idx = self.outfile.rfind('/')
            dir_path = self.outfile[:dirpath_end_idx + 1 ]
            print(f"...Checking if '{dir_path}' directory exists.")
            common.make_dir_if_needed(dir_path)

    # write the output file
    def write_file(self):
        try:
            with open(self.outfile, 'w', newline='') as f:
                print(f"...Writing output file to '{self.outfile}'")
                filewriter = csv.writer(f)
                filewriter.writerows(self.output_data)
        except PermissionError:
            print("Permission Denied: Try running the script as root or sudo.")
            # TODO: try to change permissions


# ---------------------------------------------
############
##  Main  ##
############
class Main:

    def __init__(self, argv):
        self.__input_file = argv[0]
        self.__output_file = argv[1]

    @property
    def input_file(self):
        return self.__input_file

    @property
    def output_file(self):
        return self.__output_file

    def run(self):
        # Use the Parser to parse & store input data, and validate IPv4 format
        input_parser = dataparser.Parser(self.input_file)
        
        # Validate the parsed data, format it, and coalesce IP's if possible
        data_coalescer = coalescence.Coalescer(input_parser.parsed_data)

        # Write the coalesced data to the output file
        filewriter = FileWriter(self.output_file, data_coalescer.datatable)
        filewriter.write_file()
        print(f"...Coalesced data successfully written to output file.")


# ---------------------------------------------
##################
##  Entrypoint  ##
##################
if __name__ == "__main__":
    argv = sys.argv[1:]
    main = Main(argv)
    main.run()