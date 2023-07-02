#!/usr/bin/env python3

import pytest as pt
import os
# local modules
import main
import dataparser
import coalescence
import common


# Instantiate Main class
m = main.Main(["test_files/input_data.csv", "data/solution_output_test.csv"])


# ---------------------------------------------
##############################
##  Common Exception Tests  ##
##############################

# Function: check_path_exists
def test_check_path_exists():
    with pt.raises(FileNotFoundError):
        common.check_path_exists('directory/bad_filepath.txt')

# Function: check_arg_type
def test_check_arg_type():
    with pt.raises(TypeError):
        common.check_arg_type('string', list(), 'err msg')

# Class: ConstructionError(RuntimeError)
def test_ctor_error():
    msg = 'test'
    ctor_err = common.ConstructionError(msg)
    assert ctor_err.msg == msg

def test_ctor_check_arg_type_error():
    with pt.raises(common.ConstructionError):
        msg = 'test'
        arg1, arg2 = 'string', int
        common.ConstructionError.check_arg_type(msg, arg1, arg2)


# ---------------------------------------------
#############################
##  Common Function Tests  ##
#############################

# Function: make_dir_if_needed
def test_make_dir_if_needed_makedirs():
    dirpath1 = '000thisisatestdir999/'
    dirpath2 = 'andanother/'
    common.make_dir_if_needed(dirpath1 + dirpath2)
    assert os.path.exists(dirpath1 + dirpath2)
    os.rmdir(dirpath1 + dirpath2)
    os.rmdir(dirpath1)

# Function: set_bit
def test_set_bit():
    assert common.set_bit(0, 0) == 1

def test_set_bit2():
    assert common.set_bit(1, 3) == 9

# Function: get_bit_len
def test_get_bit_len():
    assert common.get_bit_len(3) == 2

def test_get_bit_len_offset():
    assert common.get_bit_len(4, -1) == 2

def test_get_bit_len_infiniteloop():
    with pt.raises(ValueError):
        common.get_bit_len(-1)

# Function: get_lowest_set_bit_pos
def test_get_lowest_set_bit_pos():
    assert common.get_lowest_set_bit_pos(0) == 0

def test_get_lowest_set_bit_pos2():
    assert common.get_lowest_set_bit_pos(20) == 2

# Function: is_valid_ipv4
def test_is_valid_ipv4_type_error():
    with pt.raises(TypeError):
        ipv4 = dict() # ipv4 should be type 'int'
        common.is_valid_ipv4(ipv4)

def test_is_valid_ipv4_goodval():
    ipv4 = '10.200.1.0'
    assert common.is_valid_ipv4(ipv4) is True

def test_is_valid_ipv4_minval():
    ipv4 = '0.0.0.0'
    assert common.is_valid_ipv4(ipv4) is True

def test_is_valid_ipv4_maxval():
    ipv4 = '255.255.255.255'
    assert common.is_valid_ipv4(ipv4) is True

def test_is_valid_ipv4_shortval():
    ipv4 = '1.2.3'
    assert common.is_valid_ipv4(ipv4) is False

def test_is_valid_ipv4_longval():
    ipv4 = '1.2.3.4.5'
    assert common.is_valid_ipv4(ipv4) is False

def test_is_valid_ipv4_alphaval():
    ipv4 = '1.a.3.4'
    assert common.is_valid_ipv4(ipv4) is False

def test_is_valid_ipv4_charval():
    ipv4 = '1.2.#.4'
    assert common.is_valid_ipv4(ipv4) is False

def test_is_valid_ipv4_lowval():
    ipv4 = '1.2.3.-7'
    assert common.is_valid_ipv4(ipv4) is False

def test_is_valid_ipv4_highval():
    ipv4 = '1.256.3.4'
    assert common.is_valid_ipv4(ipv4) is False

# Function: is_valid_mask_and_cidr
def test_is_valid_mask_and_cidr_type_error():
    with pt.raises(TypeError):
        mask = dict() # mask should be type 'int'
        common.is_valid_mask_and_cidr(mask)

def test_is_valid_mask_and_cidr_goodval():
    mask = 4294967040 # 255.255.255.0
    # should return a tuple w/ True (bool) and 24 (int... cidr#)
    assert common.is_valid_mask_and_cidr(mask) == (True, 24)

def test_is_valid_mask_and_cidr_zeroval():
    mask = 0 # 0.0.0.0
    # should return a tuple w/ True (bool) and 0 (int... cidr#)
    assert common.is_valid_mask_and_cidr(mask) == (True, 0)

def test_is_valid_mask_and_cidr_maxval():
    mask = 4294967295 # 255.255.255.255
    # should return a tuple w/ True (bool) and 32 (int... cidr#)
    assert common.is_valid_mask_and_cidr(mask) == (True, 32)

def test_is_valid_mask_and_cidr_invalid_octet():
    mask = 553648128 # 33.0.0.0
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')

def test_is_valid_mask_and_cidr_4thOct_256(): # less than 32bits
    mask = 256 # 0.0.0.256
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')

def test_is_valid_mask_and_cidr_3rdOct_256(): # less than 32bits
    mask = 65536 # 0.0.256.0
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')
    
def test_is_valid_mask_and_cidr_2ndOct_256(): # less than 32bits
    mask = 16777216 # 0.0.256.0
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')

def test_is_valid_mask_and_cidr_1stOct_256(): # more than 32 bits
    mask = 4294967296 # 0.0.256.0
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')

def test_is_valid_mask_and_cidr_4thOct_greaterthan_3rdOct():
    mask = 4294902015 # 255.255.0.255
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')

def test_is_valid_mask_and_cidr_3rdOct_greaterthan_2ndOct():
    mask = 4278255360 # 255.0.255.0
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')

def test_is_valid_mask_and_cidr_2ndOct_greaterthan_1stOct():
    mask = 16711680 # 0.255.0.0
    # should return a tuple w/ False (bool) and 'N/A' (str... cidr# not available)
    assert common.is_valid_mask_and_cidr(mask) == (False, 'N/A')

# Function: ipv4_to_int
def test_ipv4_to_int_minval():
    assert common.ipv4_to_int('0.0.0.0') == 0

def test_ipv4_to_int_maxval():
    assert common.ipv4_to_int('255.255.255.255') == 4294967295

def test_ipv4_to_int_badval():
    # passing an invalid ipv4 format will return the original arg value unchanged
    assert common.ipv4_to_int('256.255.255.255') == '256.255.255.255'

# Function: int_to_ipv4
def test_int_to_ipv4():
    assert common.int_to_ipv4(1) == '0.0.0.1'

def test_int_to_ipv4_minval():
    assert common.int_to_ipv4(0) == '0.0.0.0'

def test_int_to_ipv4_maxval():
    assert common.int_to_ipv4(4294967295) == '255.255.255.255'

def test_int_to_ipv4_negativenum():
    with pt.raises(ValueError):
        common.int_to_ipv4(-1)

def test_int_to_ipv4_over32bits():
    with pt.raises(ValueError):
        common.int_to_ipv4(4294967296)

# Function: convert_cidr_to_str
def test_convert_cidr_to_str32():
    assert common.convert_cidr_to_str(32) == ''

def test_convert_cidr_to_str31():
    assert common.convert_cidr_to_str(31) == '/31'

def test_convert_cidr_to_str0():
    assert common.convert_cidr_to_str(0) == '/0'


# ---------------------------------------------
# Note: m = main.Main()

#######################
##  Parser fixtures  ##
#######################
@pt.fixture
def input_data_numlines():
    with open(m.input_file, newline='') as f:
        numlines = len(f.readlines())
    return numlines

@pt.fixture
def parser_obj():
    return dataparser.Parser(m.input_file)

####################
##  Parser Tests  ##
####################
def test_parser_ctor_error():
    with pt.raises(common.ConstructionError):
        ctor = dataparser.Parser(4) # arg must be type 'str'

def test_file_not_found_error():
    with pt.raises(FileNotFoundError):
        bad_file_path = dataparser.Parser('input/bad_filepath.csv')

def test_setter_parsed_data(parser_obj):
    with pt.raises(TypeError):
        parser_obj.parsed_data = 'string' # parsed_data must be type 'list'

def test_data_length_equivalence(input_data_numlines, parser_obj):
    assert len(parser_obj.parsed_data) == input_data_numlines

def test_parsed_data_isnot_none(parser_obj):
    assert parser_obj.parsed_data is not None


# ---------------------------------------------
# Note: m = main.Main()

##########################
##  Coalescer fixtures  ##
##########################
@pt.fixture
def coalescer_obj(parser_obj):
    return coalescence.Coalescer(parser_obj.parsed_data)

#######################
##  Coalescer Tests  ##
#######################
def test_coalescer_ctor_error():
    with pt.raises(common.ConstructionError):
        ctor = coalescence.Coalescer('string') # arg must be type 'list'

def test_setter_datatable(coalescer_obj):
    with pt.raises(TypeError):
        coalescer_obj.datatable = 'string' # datatable must be type 'list'

def test_coalescer_format_invalid_mask():
    arg = [('1', [[common.ipv4_to_int('10.0.0.128'), common.ipv4_to_int('255.0.0.192')]])]
    obj = coalescence.Coalescer(arg)
    exp = [['1', '10.0.0.128/255.0.0.192']]
    act = obj.datatable
    assert exp == act

def test_coalescer_format_invalid_mask2():
    arg = [('1116', [
        [common.ipv4_to_int('10.0.0.1'), common.ipv4_to_int('255.0.0.255')],
        [common.ipv4_to_int('10.10.10.2'), common.ipv4_to_int('255.255.255.255')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['1116', '10.0.0.1/255.0.0.255;10.10.10.2']]
    act = obj.datatable
    assert exp == act

def test_coalescer_format_any():
    arg = [('0', [[0, 0]])]
    obj = coalescence.Coalescer(arg)
    exp = [['0', 'Any']]
    act = obj.datatable
    assert exp == act

def test_coalescer_format_0_255():
    arg = [('1409', [[0, common.ipv4_to_int('255.255.255.255')]])]
    obj = coalescence.Coalescer(arg)
    exp = [['1409', '0.0.0.0']]
    act = obj.datatable
    assert exp == act

def test_coalescer_format_single_ip():
    arg = [('3761', [[common.ipv4_to_int('10.101.72.10'), common.ipv4_to_int('255.255.255.254')]])]
    obj = coalescence.Coalescer(arg)
    exp = [['3761', '10.101.72.10/31']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_duplicate():
    arg = [('1556', [
        [common.ipv4_to_int('10.100.200.110'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.100.200.110'), common.ipv4_to_int('255.255.255.255')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['1556', '10.100.200.110']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_contiguous_samenetwork():
    arg = [('10', [
        [common.ipv4_to_int('10.100.200.110'), common.ipv4_to_int('255.255.255.254')],
        [common.ipv4_to_int('10.100.200.111'), common.ipv4_to_int('255.255.255.254')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['10', '10.100.200.110/31']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_contiguous_diffnetwork():
    arg = [('10', [
        [common.ipv4_to_int('10.100.200.109'), common.ipv4_to_int('255.255.255.254')],
        [common.ipv4_to_int('10.100.200.110'), common.ipv4_to_int('255.255.255.254')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['10', '10.100.200.109/30']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_supernet_contiguous():
    arg = [('7138', [
        [common.ipv4_to_int('10.21.21.100'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.21.21.101'), common.ipv4_to_int('255.255.255.255')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['7138', '10.21.21.100/31']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_supernet_range():
    arg = [('1384', [
        [common.ipv4_to_int('10.0.0.1'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.2'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.3'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.4'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.5'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.6'), common.ipv4_to_int('255.255.255.255')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['1384', '10.0.0.1-10.0.0.6']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_supernet_range():
    arg = [('1384', [
        [common.ipv4_to_int('10.0.0.1'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.2'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.3'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.4'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.5'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.0.0.6'), common.ipv4_to_int('255.255.255.255')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['1384', '10.0.0.1-10.0.0.6']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_supernet_mixed():
    arg = [('6372', [
        [common.ipv4_to_int('10.200.1.110'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.200.1.111'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('10.200.1.112'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('172.16.30.100'), common.ipv4_to_int('255.255.255.255')],
        [common.ipv4_to_int('172.16.30.101'), common.ipv4_to_int('255.255.255.255')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['6372', '10.200.1.110-10.200.1.112;172.16.30.100/31']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_supernet_network():
    arg = [('334', [
        [common.ipv4_to_int('192.168.1.0'), common.ipv4_to_int('255.255.255.0')],
        [common.ipv4_to_int('192.168.2.0'), common.ipv4_to_int('255.255.255.0')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['334', '192.168.1.0-192.168.2.255']]
    act = obj.datatable
    assert exp == act

def test_coalesce_ips_no_coalescence():
    arg = [('1186', [
        [common.ipv4_to_int('10.100.51.0'), common.ipv4_to_int('255.255.255.0')],
        [common.ipv4_to_int('10.100.53.0'), common.ipv4_to_int('255.255.255.0')],
        [common.ipv4_to_int('10.100.55.0'), common.ipv4_to_int('255.255.255.0')],
        [common.ipv4_to_int('10.100.57.0'), common.ipv4_to_int('255.255.255.0')],
        [common.ipv4_to_int('10.100.59.0'), common.ipv4_to_int('255.255.255.0')]
        ])]
    obj = coalescence.Coalescer(arg)
    exp = [['1186', '10.100.51.0/24;10.100.53.0/24;10.100.55.0/24;10.100.57.0/24;10.100.59.0/24']]
    act = obj.datatable
    assert exp == act


# ---------------------------------------------
# Note: m = main.Main()

###########################
##  FileWriter Fixtures  ##
###########################
@pt.fixture
def writefile_obj():
    outfile = 'thisisatestfiletobewrittenanddeleted'
    data = ['test']
    return main.FileWriter(outfile, data)

########################
##  FileWriter Tests  ##
########################
def test_writefile_ctor_error():
    with pt.raises(common.ConstructionError):
        # outfile should be type 'str'
        outfile = 1234
        ctor = main.FileWriter(outfile, list())

def test_writefile_ctor_error2():
    with pt.raises(common.ConstructionError):
        # outfile path should end with the file's name
        outfile = 'fake_directory/nofilename/'
        ctor = main.FileWriter(outfile, list())

def test_check_file(capfd):
    outfile, data = 'zztesttesttestzz.xyz', ['test']
    wf = main.FileWriter(outfile, data)
    out, err = capfd.readouterr()
    assert 'Output directory not specified' in out

def test_write_file(writefile_obj):
    writefile_obj.write_file()
    assert os.path.getsize(writefile_obj.outfile) > 0
    os.remove(writefile_obj.outfile)


# ---------------------------------------------
# Note: m = main.Main()

##################
##  Main Tests  ##
##################
def test_input_filepath():
    assert os.path.exists(m.input_file)


# ---------------------------------------------
##################
##  Entrypoint  ##
##################
if __name__ == "__main__":
   pt.main()