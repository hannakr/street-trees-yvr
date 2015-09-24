import re

def parse_address(street_string):
    # The system is looking for street addresses of the form
    # ONTARIO ST or W 18TH AV
    # Alternatives (ignoring case):
    # Ontario Street
    # West 18th Ave
    # West 18th Avenue
    # 18th Avenue West
    tmp_string = ''
    house_number = ''
    if street_string:
        string_pieces = street_string.upper().split()
        house_number, address_pieces = identify_number(string_pieces)
        #if house_number:
        #    address_pieces.insert(0,house_number)
        tmp_string = ' '.join(address_pieces)
    return house_number, tmp_string

def identify_number(address_pieces):
    pattern = '^\d+$'
    house_number = ''
    if re.search(pattern,  address_pieces[0]):
        house_number = address_pieces.pop(0)
    return house_number, address_pieces

def parse_streets(street_pieces):
    #remove apostrophes, periods
    street_pieces = map(lambda s:s.replace('.',''), street_pieces)
    street_pieces = map(lambda s:s.replace('\'',''), street_pieces)
    return street_pieces

def find_directions(street_pieces):
    direction = ''
    pattern = dict()
    pattern['west'] = '^W$|^WEST$'
    pattern['east'] = '^E$|^EAST$'
    pattern['south'] = '^S$'
    pattern['north'] = '^N$'
    pattern['ne'] = '^NE$'
    pattern['nw'] = '^NW$'
    pattern['se'] = '^SE$'
    pattern['sw'] = '^SW$'
    for key in pattern:
        if re.search(pattern[key], street_pieces[0]):
            direction = street_pieces.pop(0)
    return direction
