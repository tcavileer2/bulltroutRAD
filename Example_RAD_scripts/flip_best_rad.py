#!/usr/bin/env python
"""
    Flip reads around so that the cut site and barcode are all
    on the forward read.
    flip_best_rad.py --output <output directory> --distance <barcode distance>
        <barcodes file> <input directory>
    
    The barcode distance is the tolerance for mismatched barcodes.
    This is basically the same as Paul's script, except that it produces
    gzipped output if the input is gzipped and it can handle mismatched
    barcodes.
"""

#==============================================================================#

import argparse
import gzip
import os
import os.path as osp
import re
import itertools
import difflib

from Bio import SeqIO

#==============================================================================#

parser = argparse.ArgumentParser(usage=__doc__)
parser.add_argument('--output')
parser.add_argument('--distance', type=int, default=0)
parser.add_argument('--prefix', default=None)
parser.add_argument('barcodes')
parser.add_argument('indir')
args = parser.parse_args()

barcodes = set()
with open(args.barcodes, 'r') as bhandle:
    for line in bhandle:
        barcodes.add(line.strip())

infiles = [f for f in os.listdir(args.indir) if 'fastq' in f and '_R1_' in f]
if args.prefix is not None:
    infiles = [f for f in infiles if f.startswith(args.prefix)]
for infile in infiles:
    prefix = re.sub('_R[12].+', '', infile)
    f1 = osp.join(args.indir, infile)
    f2 = osp.join(args.indir, re.sub('R1', 'R2', infile))
    of1 = osp.join(args.output, infile)
    of2 = osp.join(args.output, re.sub('R1', 'R2', infile))

    print 'Reading from %s and %s; writing to %s and %s' % (f1, f2, of1, of2)
    if f1.endswith('.gz'):
        open_function = gzip.open
    else:
        open_function = open
    i1, i2 = open_function(f1, 'rb'), open_function(f2, 'rb')
    o1, o2 = open_function(of1, 'w'), open_function(of2, 'w')

    for r1, r2 in itertools.izip(SeqIO.parse(i1, 'fastq'), SeqIO.parse(i2, 'fastq')):
        s1, s2 = str(r1.seq), str(r2.seq)
        if s1[10:15] == 'TGCAG' and s2[10:15] != 'TGCAG':
            # Cut site in forward read; write forward read to o1
            which = 1
        elif s1[10:15] != 'TGCAG' and s2[10:15] == 'TGCAG':
            # Cut site in reverse read; write reverse read to o1
            which = 2
        elif s1[10:15] == 'TGCAG' and s2[10:15] == 'TGCAG':
            # Cut site in both reads, look for barcode
            b1, b2 = s1[:10], s2[:10]
            which = 0
            if b1 in barcodes:
                # Perfect barcode match in first read
                which = 1
            elif b2 in barcodes:
                # Perfect barcode match in second read
                which = 2
            elif args.distance > 0:
                # Partial matching; weakness here is that we don't
                # check for the best match in either read; the forward
                # read is checked first and then the reverse read. It will
                # probably do the right thing in the vast majority of cases.
                if difflib.get_close_matches(b1, barcodes, args.distance):
                    # partial match in first read
                    which = 1
                elif difflib.get_close_matches(b2, barcodes, args.distance):
                    # partial match in second read
                    which = 2
                else:
                    # No matches, skip the read
                    which = 0
        else:
            # No cut site (or sequencing error), do not write read
            which = 0

        if which == 1:
            SeqIO.write(r1, o1, 'fastq')
            SeqIO.write(r2, o2, 'fastq')
        elif which == 2:
            SeqIO.write(r1, o2, 'fastq')
            SeqIO.write(r2, o1, 'fastq')

    i1.close(); i2.close(); o1.close(); o2.close()
    print '\tfinished ' + prefix