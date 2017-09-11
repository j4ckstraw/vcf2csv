#!/usr/bin/evn python3
#coding:utf-8
#function: convert name,phone-num .csv file to .vcf file.

import os
import sys
import argparse
import codecs
from card import Card
debug = False

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='input file, SHOULD BE .csv FORMAT')
    # TODO handle file which not .csv format
    parser.add_argument('-o', '--outfile', help='output to file',default='output.vcf')
    parser.add_argument('-d', '--delimiter', help='delimiter, default is semicolon',default=';')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_argument()
    infile = args.infile
    outfile = args.outfile
    # TODO use delimiter
    delimiter = args.delimiter if args.delimiter else ';'

    # TODO handle outfile.
    print(infile)
    print(outfile)
    try:
        inf = codecs.open(infile,'r',encoding='utf-8')
        outf = codecs.open(outfile, 'w', encoding='utf-8')
        # inf = open(infile,'r')
        line = inf.readline().strip('\r\n')
        record = None
        while line:
            head,dem,tail = line.partition(delimiter)
            # print(head,dem,tail)
            record = Card()
            record.fn = head
            record.family_name = head[0]
            record.given_name = head[1:]
            record.tels.append({'tel_type':'TYPE=CELL','tel':tail})
            if debug:
                print(record.to_vcf())
            outf.write(record.to_vcf())
            line = inf.readline().strip('\r\n')

    except Exception as e:
        print(e)
    finally:
        inf.close()
        outf.close()


