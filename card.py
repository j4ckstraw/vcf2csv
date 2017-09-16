#!/usr/bin/env python3
#coding:utf-8

import os

debug = False

class Card(object):
    """
    Card class for a record.
    """
    # The version of the vCard specification. In versions 3.0 and 4.0, this must come right after the BEGIN property.
    # VERSION:3.0
    # now ONLY SUPPORT vcf version 3.0
    VERSION = 'VERSION:3.0'

    # All vCards must start with this property.
    # BEGIN:VCARD
    BEGIN = 'BEGIN:VCARD'

    # All vCards must end with this property.
    # END:VCARD
    END = 'END:VCARD'

    # The formatted name string associated with the vCard object
    # FN:Dr. John Doe
    FN = 'FN:'

    # A structured representation of the name of the person, place or thing associated with the vCard object.
    # N:Doe;John;;Dr;
    N = 'N:'

    # The canonical number string for a telephone number for telephony communication with the vCard object.
    # TEL;TYPE=cell:(123) 555-5832
    TEL = 'TEL;'

    def __init__(self, delimiter=';'):
        self.delimiter = delimiter
        self.fn = ''
        self.family_name = ''
        self.given_name = ''
        self.middle_name = ''
        self.prefix = ''
        self.suffix = ''
        self.tels = []

    def to_vcf(self):
        if debug:
            # print(Card.BEGIN + Card.FN + self.fn + Card.END)
            print(Card.BEGIN)
            print(Card.VERSION)
            print(Card.N,end="")
            print(self.family_name,self.given_name,self.middle_name,self.prefix,self.suffix,sep=';')
            print(Card.FN,end="")
            print(self.fn)
            for tel in self.tels:
                print(Card.TEL,end="")
                # print('TYPE',tel.tel_type,sep='=')
                print(tel['tel_type'],end=":")
                print(tel['tel'])
            print(Card.END)
        # TODO format it.
        result = ''
        result += Card.BEGIN
        result += os.linesep
        result += Card.VERSION
        result += os.linesep
        result += Card.N
        result += self.family_name
        result += ';'
        result += self.given_name
        result += ';'
        result += self.middle_name
        result += ';'
        result += self.prefix
        result += ';'
        result += self.suffix
        result += os.linesep
        result += Card.FN
        result += self.fn
        result += os.linesep
        for tel in self.tels:
            result += Card.TEL
            result += tel['tel_type']
            result += ':'
            result += tel['tel']
            result += os.linesep
        result += Card.END
        result += os.linesep
        return result


    def to_csv(self):
        a = [self.fn]
        a.extend([tel['tel'] for tel in self.tels])
        if debug:
            print(self.delimiter.join(a))
        return self.delimiter.join(a) + os.linesep

