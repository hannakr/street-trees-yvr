from app import db, models
#from models import *

def import_data():
    print "running function"
    f = open('StreetTrees_Strathcona.csv', 'r')
    f.readline()
    for line in f:
        pieces = line.strip().split(',')
        print pieces
        find_or_create_house(pieces)

def find_or_create_house(pieces):
    house = models.House.query.filter(models.House.stdStreet==pieces[2],
                                models.House.civicNumber==pieces[1]).first()
    print house
    if house:
        print "house found"
        find_or_create_tree(pieces, house)
    else:
        print "house not found"
        h = models.House(civicNumber=pieces[1], stdStreet=pieces[2], neighbourhoodName=pieces[3])
        db.session.add(h)
        db.session.commit()
        find_or_create_tree(pieces, h)

def find_or_create_tree(pieces, house):
    tree = models.Tree.query.filter(models.Tree.treeID==pieces[0]).first()
    print tree
    if tree:
        print "tree found"
        return
    else:
        print "tree not found"
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
