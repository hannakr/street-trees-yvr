from app import db, models
#from models import *
import re
import os
import datetime

all_lines = 0
new_houses = 0
new_trees = 0

def import_data():
    print "running function"
    tree_path = os.path.join(os.getcwd(),'csv_street_trees')
    for fn in os.listdir(tree_path):
        if os.path.isfile(os.path.join(tree_path,fn)):
            print (fn)
            print datetime.datetime.now()
            with open(os.path.join(tree_path,fn), "r") as csv_file:
                csv_file.readline()     #skip the header line
                all_lines = 0
                new_houses = 0
                new_trees = 0
                for line in csv_file:
                    all_lines += 1
                    pieces = line.strip().split(',')
                    #print pieces
                    find_or_create_house(pieces, new_houses, new_trees)
                print "lines: " + str(all_lines)
                print "houses added: " + str(new_houses)
                print "trees added: " + str(new_trees)

def parse_address(street_string):
    string_pieces = street_string.upper().split()

    # parse_streets
    string_pieces = map(lambda s:s.replace('.',''), string_pieces)
    string_pieces = map(lambda s:s.replace('\'',''), string_pieces)


    # replace alternate street types
    string_pieces = map(lambda s:re.sub(r'\b(AVENUE|AVE)\b', 'AV', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(BLVD)\b', 'BOULEVARD', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(CIR)\b', 'CIRCLE', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(CRT)\b', 'COURT', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(CRES)\b', 'CRESCENT', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(DR)\b', 'DRIVE', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(LN)\b', 'LANE', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(PASS)\b', 'PASSAGE', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(PL)\b', 'PLACE', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(RD)\b', 'ROAD', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(SQ)\b', 'SQUARE', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(STREET)\b', 'ST', s), string_pieces)

    # replace directions
    string_pieces = map(lambda s:re.sub(r'\b(WEST)\b', 'W', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(EAST)\b', 'E', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(NORTH)\b', 'N', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(SOUTH)\b', 'S', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(SOUTHWEST)\b', 'SW', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(SOUTHEAST)\b', 'SE', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(NORTHWEST)\b', 'NW', s), string_pieces)
    string_pieces = map(lambda s:re.sub(r'\b(NORTHEAST)\b', 'NE', s), string_pieces)

    # replace random bits
    string_pieces = map(lambda s:re.sub(r'\b(SAINT)\b', 'ST', s), string_pieces)

    # have to figure out how to turn 'SW' into 'S', 'W' - otherwise South West Marine Drive will never work
    try:
        i = string_pieces.index('SW')
    except ValueError:
        pass
    else:
        string_pieces[i] = 'S'
        string_pieces.append('W')

    try:
        i = string_pieces.index('NW')
    except ValueError:
        pass
    else:
        string_pieces[i] = 'N'
        string_pieces.append('W')

    try:
        i = string_pieces.index('SE')
    except ValueError:
        pass
    else:
        string_pieces[i] = 'S'
        string_pieces.append('E')

    try:
        i = string_pieces.index('NE')
    except ValueError:
        pass
    else:
        string_pieces[i] = 'N'
        string_pieces.append('E')

    string_pieces.sort()
    sorted_string = " ".join(string_pieces)
    return sorted_string


def find_or_create_house(pieces, new_houses, new_trees):
    house = models.House.query.filter(models.House.stdStreet==pieces[2],
                                models.House.civicNumber==pieces[1]).first()
    #print house
    if house:
        #print "house found"
        find_or_create_tree(pieces, house, new_trees)
    else:
        #print "house not found"
        new_houses += 1
        h = models.House(civicNumber=pieces[1], stdStreet=pieces[2], stdStreetSorted=parse_address(pieces[2]), neighbourhoodName=pieces[3])
        db.session.add(h)
        db.session.commit()
        find_or_create_tree(pieces, h, new_trees)

def find_or_create_tree(pieces, house, new_trees):
    tree = models.Tree.query.filter(models.Tree.treeID==pieces[0]).first()
    #print tree
    if tree:
        #print "tree found"
        return
    else:
        new_trees += 1
        #print "tree not found"
        corner = False
        if (house.stdStreet != pieces[5]):
            corner = True
        t = models.Tree(treeID=pieces[0],
        cell=pieces[4],
        onStreet=pieces[5],
        onStreetBlock=pieces[6],
        streetSideName=pieces[7],
        assigned=pieces[8],
        heightRangeID=pieces[9],
        diameter=pieces[10],
        datePlanted=pieces[11],
        plantArea=pieces[12],
        rootBarrier=pieces[13],
        curb=pieces[14],
        cultivarName=pieces[15],
        genusName=pieces[16],
        speciesName=pieces[17],
        commonName=pieces[18],
        onCorner=corner,
        house=house.id)
        db.session.add(t)
        db.session.commit()

import_data()
