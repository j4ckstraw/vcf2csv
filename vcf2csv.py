#!/usr/bin/evn python3
#coding:utf-8

import os
import sys
import argparse
import codecs
from card import Card
debug = False

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='input file, SHOULD BE .vcf FORMAT VERSION3.0')
    parser.add_argument('-o', '--outfile', help='output to file',default='output.csv')
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
        outf = codecs.open(outfile,'w',encoding='utf-8')
        # inf = open(infile,'r')
        line = inf.readline().strip('\r\n')
        record = None
        while line:
            if Card.BEGIN == line:
                record = Card(delimiter=delimiter)
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
                # print(record.to_csv())
                outf.write(record.to_csv())
            line = inf.readline().strip('\r\n')

    except Exception as e:
        print(e)
    finally:
        inf.close()
        outf.close()
