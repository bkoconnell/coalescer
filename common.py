import os


# ---------------------------------------------
#################################
##  Common Exception Handling  ##
#################################
            
# function to verify if a filepath exists
def check_path_exists(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"'{filepath}' could not be found.")

# function to verify a given arg's type vs. the expected type
def check_arg_type(arg, exp, msg):
    if not isinstance(arg, exp):
        raise TypeError(msg)

# Custom exception class that can be thrown during an object's construction (__init__).
# Distinguishes between a generic RuntimeError vs ConstructionError for exception handling.
class ConstructionError(RuntimeError):

    def __init__(self, msg):
        self.__msg = msg

    @property
    def msg(self):
        return self.__msg

    # function to evaluate an arg for its expected type.
    # Note: when calling ConstructionError.check_arg_type(), pass 3 args:
    #       1) error_msg_string; 2) arg_to_check; 3) expected_type
    #       The error_msg_string will pass to __init__() as the msg arg if the error is raised.
    def check_arg_type(self, arg, exp):
        if not isinstance(arg, exp):
            raise ConstructionError(self)


# ---------------------------------------------
########################
##  Common Functions  ##
########################

# function to check if a directory exists and create it if needed
def make_dir_if_needed(dir_path):
    # will not overwrite an existing directory
    if not os.path.exists(dir_path):
        err = None
        try:
            os.makedirs(dir_path, 0o666)
            print(f"...Created empty directory '{dir_path}'")
        except FileNotFoundError:
            print(f"...Unable to create directory '{dir_path}'")
    else:
        print(f"'{dir_path}' already exists.")
    if not os.path.isdir(dir_path):
        print(f"...File '{dir_path}' exists but is not a directory.")

# function to set a specific bit to '1'
def set_bit(num: int, pos: int) -> int:
    # check arg types
    check_arg_type(num, int, "set_bit() arg1 must be of type 'int'")
    check_arg_type(pos, int, "set_bit() arg2 must be of type 'int'")
    # return the union of the original num and a 1 shifted left to the position arg
    return num | (1 << pos)

# function to get bit length (or to locate the position of a specific bit)
def get_bit_len(num: int, bit_length=0) -> int:
    # check arg types
    check_arg_type(num, int, "get_bit_len() arg1 must be of type 'int'")
    check_arg_type(bit_length, int, "get_bit_len() arg2 must be of type 'int'")
    # negative num will cause infinite loop
    if not num >= 0:
        raise ValueError("get_bit_len() arg(1) must be a non-negative integer>")
    # https://wiki.python.org/moin/BitManipulation
    # right-shift one bit at a time, incrementing bit_length each time until num = 0
    while(num):
        num >>= 1
        bit_length += 1
    return bit_length
    
# https://wiki.python.org/moin/BitManipulation#lowestSet.28.29
# function to get the position of the lowest-set-bit (aka: the right-most 1 )
def get_lowest_set_bit_pos(num: int) -> int:
    # check arg types
    check_arg_type(num, int, "get_lowest_set_bit_pos() arg must be of type 'int'")
    if num == 0:
        # there are no set bits
        return 0
    # use twos-compliment format to identify the lowest set bit
    low_set_bit = num & -num    
    # we'll be counting 0's, but starting position is right-most-One, not left-most-Zero,
    # so inititialize an offset 'length' val at -1 to account for starting position
    bit_length_offset = -1
    # call get_bit_len() to find the position of the lowest set bit
    # (aka: count the number of consecutive right-most-Zeros)
    low_set_bit_pos = get_bit_len(low_set_bit, bit_length_offset)
    return low_set_bit_pos
    
# function to validate the address/mask is IPv4 format.
# (takes either a 'str' or a 'list' as its arg)
def is_valid_ipv4(ipv4) -> bool:
    # check arg type
    if isinstance(ipv4, str):
        octets = ipv4.split('.')
    elif isinstance(ipv4, list):
        octets = ipv4
    else:
        raise TypeError("is_valid_ipv4() arg must be of type 'str' or 'list'")
    # https://codereview.stackexchange.com/a/209250
    # validate format length, and each octet value
    length_bool = (len(octets) == 4)
    if not length_bool:
        return length_bool
    value_bool = all((byte_str.isdecimal() and (0 <= int(byte_str) <= 255)) for byte_str in octets)
    return value_bool

# function to validate mask value and check cidr #
#   returns tuple: (True & cidr int) or (False & 'N/A')
def is_valid_mask_and_cidr(mask: int):
    # check arg type
    check_arg_type(mask, int, "is_valid_mask_and_cidr() arg must be of type 'int'")
    cidr = 0    
    if mask == 0:
        # 0 bit mask is valid
        return (True, cidr)
    # verify the mask is 32bits
    mask_binstr = bin(mask)
    mask_binlength = len(mask_binstr[2:]) # remove '0b' prefix
    if not (mask_binlength == 32):
        return (False, 'N/A')
    # https://codereview.stackexchange.com/a/209250
    ## Verify octet vals (the bin str should have all 1's left-side and 0's right-side).
    # first, get the position of the lowest-set-bit and then get its 'int' val
    low_set_bit_pos = get_lowest_set_bit_pos(mask)
    low_set_bit_int = set_bit(0, low_set_bit_pos)
    # one number less than this val will flip the right-most 0's to 1's
    right_zeros_flipped_on = low_set_bit_int - 1
    # a union of the 32bit mask and the flipped zeros should now be all 1's (no 0's)
    if (mask | right_zeros_flipped_on) != 0xffffffff:
        # if it's not all 1's then it had invalid 0's on the left side (bad mask value)
        return (False, 'N/A')
    # calculate the CIDR # and verify that it is in range 0 -> 32
    cidr = mask_binlength - low_set_bit_pos
    if not (0 <= cidr <= 32):
        return (False, 'N/A')
    return (True, cidr)

# function to convert IPv4 string to an integer
def ipv4_to_int(ipv4: str) -> int:
    # check arg type
    check_arg_type(ipv4, str, "ipv4_to_int() arg must be of type 'str'")
    octets = ipv4.split('.')
    # invalid ipv4 fmt --> return the arg unchanged (as original ipv4 string)
    if not is_valid_ipv4(octets):
        return ipv4
    # convert each octet/byte string to 'int', then left-shift each for 32bit union
    a, b, c, d = (int(byte_str) for byte_str in octets)
    int_form = a << 24 | b << 16 | c << 8 | d
    return int_form

# function to convert an integer to IPv4 string
def int_to_ipv4(num: int) -> str:
    # check arg
    check_arg_type(num, int, "int_to_ipv4() arg must be of type 'int'")
    num_binstr = bin(num)
    num_binstr = num_binstr[2:]
    # IPv4 format must be non-negative and between 0 -> 32 bits
    if not (num >= 0) or not (len(num_binstr) <= 32):
        raise ValueError(f"{num} is invalid for IPv4 conversion. Must be non-negative and 32bits or less.")
    # make four 8bit-chunks, bitmasked then shifted right enough to isolate them, stringify each, then join with '.'
    a = str((num & 0xFF000000) >> 24) # left-most chunk (bit pos 24-31)
    b = str((num & 0xFF0000) >> 16) # inner-left chunk (bit pos 16-23)
    c = str((num & 0xFF00) >> 8) # inner-right chunk (bit pos 8-15)
    d = str(num & 0xFF) # right-most chunk (bit pos 0-7)
    ipv4 = '.'.join([a,b,c,d])
    # assertion for sanity check because an error here means bad code (not user error)
    assert is_valid_ipv4(ipv4)
    return ipv4

# function to convert cidr# to a str
def convert_cidr_to_str(cidr: int) -> str:
    # check arg
    check_arg_type(cidr, int, "convert_cidr_to_str() arg must be of type 'int'")
    if cidr == 32:
        cidr = ''
    else:
        cidr = '/' + str(cidr)
    return cidr


# ---------------------------------------------