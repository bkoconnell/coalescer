import common
from common import ConstructionError as ctor


#################
##  Coalescer  ##
#################

# ---------------------------------------------
## Class for additional data validation, data formatting, and coalescing of IP's (if possible)
class Coalescer:

    def __init__(self, data: list):
        # check ctor arg type
        ctor.check_arg_type("Failed to initialize Coalescer obj (arg must be type 'list')", data, list)
        self.__parsed_data = data
        self.__candidates_list = list()
        self.__data_table = None
        self.__format_datatable()

    @property
    def parsed_data(self):
        return self.__parsed_data
    
    @property
    def datatable(self):
        return self.__data_table
    @datatable.setter
    def datatable(self, content):
        common.check_arg_type(content, list, "datatable.setter -> arg must be of type 'list'")
        self.__data_table = content

    # a valid sub will be type 'int' because the parser converted valid IPv4's to integers
    def __is_valid_sub(self, sub) -> bool:
        if isinstance(sub, int):
            return True
        return False

    # ------------------------
    # Combine IP's if possible
    def __coalesce_ips(self, subs_list: list, init_idx=0, prior_submap=None):
        common.check_arg_type(subs_list, list, "Coalescer.__coalesce_ips() arg1 must be of type 'list'")
        common.check_arg_type(init_idx, int, "Coalescer.__coalesce_ips() arg2 must be of type 'int'")

        # Define some local methods for subnet coalescence
        def __track_coalesced(self):
            sub_datamap['coalesced'] = True
            self.__num_coalesced += 1

        def __is_contiguous(sub1: int, sub2: int) -> bool:
            # diff between sub1 and sub2 must equal 1 to be contiguous
            return max(sub1, sub2) - min(sub1, sub2) == 1

        def __get_network_int(subnet, mask) -> int:
            common.check_arg_type(subnet, int, "get_network_int() arg1 must be of type 'int'")
            common.check_arg_type(mask, int, "get_network_int() arg2 must be of type 'int'")
            # bitwise AND of subnet & mask will return the network address (as an integer)
            return subnet & mask

        def __calculate_supernet() -> int:
            # use "2 to the N" to calculate supernet mask, where 'N' is the diff of (32 - cidr #)
            mask = sub_datamap['mask_int'] - (2 ** (32 - sub_datamap['cidr']))
            network = __get_network_int(sub_datamap['sub_int'], mask)
            return network
        
        def __supernet():
            # update subnet datamap values with supernet vals
            sub_datamap['network'] = __calculate_supernet()
            sub_datamap['mask_int'] = sub_datamap['mask_int'] - (2 ** (32 - sub_datamap['cidr']))
            sub_datamap['cidr'] -= 1
            sub_datamap['cidr_str'] = common.convert_cidr_to_str(sub_datamap['cidr'])
            # update prior sub's datamap to reflect supernet vals
            prior_submap['mask_int'] = sub_datamap['mask_int']
            prior_submap['cidr'] = sub_datamap['cidr']
            prior_submap['cidr_str'] = sub_datamap['cidr_str']

        # Map pertinent data values for current subnet
        valid_mask, cidr = common.is_valid_mask_and_cidr(subs_list[0][1])
        sub_datamap = {
            'sub_idx' : init_idx,
            'sub_int' : subs_list[0][0],
            'sub_str' : common.int_to_ipv4(subs_list[0][0]),
            'mask_int' : subs_list[0][1],
            'cidr' : cidr,
            'cidr_str' : common.convert_cidr_to_str(cidr),
            'network' : __get_network_int(subs_list[0][0], subs_list[0][1]),
            'network_ips' : 2 ** (32 - cidr),
            'contiguous' : False,
            'range' : False,
            'coalesced': False,
            'contiguous_network': False
        }
        # set the broadcast ip (int & str)
        sub_datamap['broadcast_ip'] = sub_datamap['network'] + sub_datamap['network_ips'] - 1
        sub_datamap['broadcast_str'] = common.int_to_ipv4(sub_datamap['broadcast_ip'])
        # append subnet to candidates list; initialize boolean for tracking recursion criteria
        self.__candidates_list.append(sub_datamap)
        recursion_bool = True
        subnets = ''

        ## Check specific conditions to determine the type of coalescence, if any.
        # Need at least 2 candidates to compare subnet data.
        if len(self.__candidates_list) >= 2:
            # a) Check for duplicate
            if prior_submap['sub_int'] == sub_datamap['sub_int']:
                __track_coalesced(self)
            # b) Check if the subs are contiguous
            elif __is_contiguous(prior_submap['sub_int'], sub_datamap['sub_int']):
                sub_datamap['contiguous'] = True
                # check if contiguous subs are in the same network
                if prior_submap['network'] == sub_datamap['network']:
                    __track_coalesced(self)
                # check if the prior subnet is contiguous (which would make this part of a range)
                elif prior_submap['contiguous']:
                    sub_datamap['range'] = True
                    # check if the next sub is contiguous
                    if len(subs_list) >= 2:
                        if __is_contiguous(sub_datamap['sub_int'], subs_list[1][0]):
                            __track_coalesced(self)
                # check if supernetting will put the contiguous subs in the same network
                elif prior_submap['network'] == __calculate_supernet():
                    __supernet()
                    __track_coalesced(self)
                    # check if the next sub is contiguous
                    if len(subs_list) >= 2:
                        if __is_contiguous(sub_datamap['sub_int'], subs_list[1][0]):
                            # these contiguous subs are a multi-network range
                            sub_datamap['range'] = True
                            prior_submap['range'] = True
                else:
                    # these contiguous subs are a multi-network range
                    sub_datamap['range'] = True
                    prior_submap['range'] = True
                    # check if the next sub is contiguous
                    if len(subs_list) >= 2:
                        if __is_contiguous(sub_datamap['sub_int'], subs_list[1][0]):
                            __track_coalesced(self)
                        else:
                            # next sub is not contiguous, no need for recursive call
                            recursion_bool = False
            # c) Check if supernetting will put the non-contiguous subs in the same network
            elif prior_submap['network'] == __calculate_supernet():
                __supernet()
                __track_coalesced(self)
            # d) Check to see if the networks are contiguous
            elif __is_contiguous(prior_submap['broadcast_ip'], sub_datamap['network']):
                prior_submap['range'] = True
                sub_datamap['contiguous_network'] = True
            # e) Based on the above criteria, there is no need for a recursive call
            else:
                recursion_bool = False

        # Criteria has been met that warrants a recursive call...
        if recursion_bool:
            # but only if there is a subnet (or more) to be checked
            if len(subs_list) >= 2:
                subnets = self.__coalesce_ips(subs_list[1:], (init_idx + 1), sub_datamap)
        # recursive call not needed; sub not contiguous with prior sub; not a candidate for coalescence
        elif not sub_datamap['contiguous']:
            self.__candidates_list.pop()

        # The subnet has been coalesced and can be removed from the candidates list
        if sub_datamap['coalesced'] is True:
            del self.__candidates_list[init_idx]
        # coalesced & non-candidate subnets do not need to be formatted, so return subnet string as-is
        if sub_datamap not in self.__candidates_list:
            return subnets

        ## At this point, we have our full list of candidates and coalesced subs, so format the data.
        # Check to see if 'subnets' string is empty; if it is, we're at the far-right candidate on the list
        if not subnets:
            # check to see if this is a contiguous network range
            if sub_datamap['contiguous_network']:
                subnets = sub_datamap['broadcast_str']
                return subnets
            else:
                subnets = sub_datamap['sub_str'] + sub_datamap['cidr_str']
                return subnets
        # check to see if this is part of a contiguous sub range
        elif sub_datamap['range']:
            # concatenate the current substring to the front of whatever exists & return the full subnets string
            subnets = sub_datamap['sub_str'] + '-' + subnets
            return subnets
        else:
            # concatenate the current substring to the front of whatever exists & return the full subnets string
            subnets = sub_datamap['sub_str'] + sub_datamap['cidr_str'] + ';' + subnets
            return subnets

    # --------------------------------------------
    # Format the parsed data & build the datatable
    def __format_datatable(self) -> list:
        self.datatable = list()
        print("...Formatting parsed data; Coalescing IP's...")
        # yield 1 row of parsed id data at a time; initialize the entry
        data_gen = (row for row in self.parsed_data)
        for row in data_gen:
            id = row[0]
            formatted_entry = []
            # 2 elements per row -> [id, nested subs list]
            for element in row:
                if element == id:
                    continue
                # initialize index tracker, then iterate the sub/mask pairs and validate
                next_idx = 0
                for idx, pair in enumerate(element):
                    if idx < next_idx:
                        continue
                    self.__num_coalesced = 0
                    subnet, mask = pair[0], pair[1]
                    valid_sub = self.__is_valid_sub(subnet)
                    valid_mask, cidr = common.is_valid_mask_and_cidr(mask)
                    # Now determine how to format the entry based on conditions.
                    # a) Invalid: subnet IPv4 format
                    if not valid_sub:
                        # check if entry is empty
                        if not formatted_entry:
                            formatted_entry.append(id)
                            # no ipv4 conversion needed b/c invalid subs were left in 'str' format
                            formatted_entry.append(subnet + '/' + mask)
                        else:
                            formatted_entry.extend(';' + subnet + '/' + mask)
                    # b) Invalid: mask value
                    if not valid_mask:
                        subnet = common.int_to_ipv4(subnet)
                        mask = common.int_to_ipv4(mask)
                        # check if entry is empty
                        if not formatted_entry:
                            formatted_entry.append(id)
                            formatted_entry.append(subnet + '/' + mask)
                        else:
                            formatted_entry[1] += ';' + subnet + '/' + mask
                    # c) Valid: subnet string value is '0.0.0.0'
                    elif subnet == 0:
                        # 'Any'
                        if mask == 0:
                            formatted_entry.append(id)
                            formatted_entry.append('Any')
                        else:
                            subnet = common.int_to_ipv4(subnet)
                            formatted_entry.append(id)
                            formatted_entry.append(subnet)
                    # d) Valid: last pair in sub/mask list for this id
                    elif len(element[idx:]) == 1:
                        subnet = common.int_to_ipv4(subnet)
                        cidr = common.convert_cidr_to_str(cidr)
                        # check if entry is empty
                        if not formatted_entry:
                            formatted_entry.append(id)
                            formatted_entry.append(subnet + cidr)
                        else:
                            formatted_entry[1] += ';' + subnet + cidr
                    # e) Valid: potential candidate for coalescence
                    else:
                        subnets = self.__coalesce_ips(element[idx:])
                        # set the next index to be checked; clear the candidates list
                        next_idx = idx + len(self.__candidates_list) + self.__num_coalesced
                        self.__candidates_list.clear()
                        # check if entry is empty
                        if not formatted_entry:
                            formatted_entry.append(id)
                            formatted_entry.append(subnets)
                        else:
                            formatted_entry[1] += ';' + subnets
            # add the formatted entry to the data table
            self.datatable.append(formatted_entry)