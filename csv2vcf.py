#!/usr/bin/evn python3
#coding:utf-8

import os
import sys
import argparse
import codecs

debug = True
class Card(object):
    """
    Card class for a record.
    """
    DELIMITER = ';'

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
    fn = ''

    # A structured representation of the name of the person, place or thing associated with the vCard object.
    # N:Doe;John;;Dr;
    N = 'N:'
    family_name = ''
    given_name = ''
    middle_name = ''
    prefix = ''
    suffix = ''

    # The canonical number string for a telephone number for telephony communication with the vCard object.
    # TEL;TYPE=cell:(123) 555-5832
    TEL = 'TEL;'
    tels = []

    def __init__(self):
        self.tels = []

    def to_vcf(self):
        # return self.BEGIN"""
        if debug:
            print(Card.BEGIN + Card.FN + self.fn + Card.END)
        # TODO format it.
        return Card.BEGIN + Card.FN + self.fn  + Card.END


    def to_csv(self):
        if debug:
            print(self.DELIMITER.join([self.fn,self.tels[0]['tel']]))
        # TODO show all tels.
        return self.DELIMITER.join([self.fn,self.tels[0]['tel']])


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='input file')
    parser.add_argument('-o', '--outfile', help='output to file')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_argument()
    infile = args.infile
    outfile = args.outfile
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
                    tel = line.split(':')[1]
                    tel_type = line.split(':')[0].strip(Card.TEL)
                    record.tels.append({'tel_type':tel_type,'tel':tel})
                    if debug:
                        print(record.tels)
                except Exception as e:
                    print('TEL error')
                    raise(e)
            if Card.END == line.strip('\r\n'):
                print('#'*79)
                print(record.to_csv())
                del(record)
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



