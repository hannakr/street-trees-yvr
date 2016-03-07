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
        address_sorted = parse_streets(address_pieces)
        #if house_number:
        #    address_pieces.insert(0,house_number)
        tmp_string = ' '.join(address_sorted)
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

    # replace alternate street types
    street_pieces = map(lambda s:re.sub(r'\b(AVENUE|AVE)\b', 'AV', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(BLVD)\b', 'BOULEVARD', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(CIR)\b', 'CIRCLE', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(CRT)\b', 'COURT', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(CRES)\b', 'CRESCENT', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(DR)\b', 'DRIVE', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(LN)\b', 'LANE', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(PASS)\b', 'PASSAGE', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(PL)\b', 'PLACE', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(RD)\b', 'ROAD', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(SQ)\b', 'SQUARE', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(STREET)\b', 'ST', s), street_pieces)

    # replace directions
    street_pieces = map(lambda s:re.sub(r'\b(WEST)\b', 'W', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(EAST)\b', 'E', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(NORTH)\b', 'N', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(SOUTH)\b', 'S', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(SOUTHWEST)\b', 'SW', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(SOUTHEAST)\b', 'SE', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(NORTHWEST)\b', 'NW', s), street_pieces)
    street_pieces = map(lambda s:re.sub(r'\b(NORTHEAST)\b', 'NE', s), street_pieces)

    # replace random bits
    street_pieces = map(lambda s:re.sub(r'\b(SAINT)\b', 'ST', s), street_pieces)

    # have to figure out how to turn 'SW' into 'S', 'W' - otherwise South West Marine Drive will never work
    try:
        i = street_pieces.index('SW')
    except ValueError:
        pass
    else:
        street_pieces[i] = 'S'
        street_pieces.append('W')

    try:
        i = street_pieces.index('NW')
    except ValueError:
        pass
    else:
        street_pieces[i] = 'N'
        street_pieces.append('W')

    try:
        i = street_pieces.index('SE')
    except ValueError:
        pass
    else:
        street_pieces[i] = 'S'
        street_pieces.append('E')

    try:
        i = street_pieces.index('NE')
    except ValueError:
        pass
    else:
        street_pieces[i] = 'N'
        street_pieces.append('E')

    street_pieces.sort()

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
