#!/usr/bin/evn python3
#coding:utf-8

import os
import sys
import argparse
import codecs

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
        return result


    def to_csv(self):
        a = [self.fn]
        a.extend([tel['tel'] for tel in self.tels])
        if debug:
            print(self.delimiter.join(a))
        return self.delimiter.join(a)


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='input file')
    parser.add_argument('-o', '--outfile', help='output to file')
    parser.add_argument('-d', '--delimiter', help='delimiter, default is semicolon',default=';')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_argument()
    infile = args.infile
    outfile = args.outfile
    delimiter = args.delimiter if args.delimiter else ';'

    # TODO handle outfile.
    print(infile)
    try:
        inf = codecs.open(infile,'r',encoding='utf-8')
        # inf = open(infile,'r')
        line = inf.readline().strip('\r\n')
        record = None
        while line:
            if Card.BEGIN == line:
                pass
                record = Card()
            if Card.VERSION == line:
                pass
            if line.startswith(Card.N):
                v = line.strip(Card.N).split(';')
                if debug:
                    print(v)
                record.family_name = v[0]
                record.given_name = v[1]
                record.middle_name = v[2]
                record.prefix = v[3]
                record.suffix = v[4]
            if Card.FN in line:
                record.fn = line.strip(Card.FN)
                if debug:
                    print(record.fn)
            if line.startswith(Card.TEL):
                try:
                    # TODO strip has sth wrongs
                    tel_type,_,tel = line.partition(':')
                    _,_,tel_type = tel_type.partition(';')
                    # tel_type = line.split(':')[0]
                    record.tels.append({'tel_type':tel_type,'tel':tel})
                    if debug:
                        print(record.tels)
                except Exception as e:
                    print('TEL error')
                    raise(e)
            if Card.END == line.strip('\r\n'):
                if debug:
                    print('#'*79)
                    # print(record.to_vcf())
                    print(record.to_csv())
                # del(record)
                print(record.to_csv())
            # print(record.to_vcf())
            line = inf.readline().strip('\r\n')

    except Exception as e:
        print(e)

    finally:
        inf.close()

    # if outfile and os.path.exists(outfile):
    #     print(outfile,'has exists!')
    #     os.exit(1)
    # if outfile and not os.path.exists(outfile):
    #     with open(os.path.basename(outfile),'w') as f:



