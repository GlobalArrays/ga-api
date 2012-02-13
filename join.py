#!/usr/bin/env python

"""Join separate tex files based on function groups into complete.tex."""

import os
import re
import sys

def main():
    if len(sys.argv) != 3:
        raise ValueError, "usage: ./join.py input_dir output_filename"
    path = sys.argv[1]
    name = sys.argv[2]
    if path[-1] != '/':
        path += '/'
    files = os.listdir(path)
    out = open(name,'w')
    # sort filenames but ignore the .tex extension
    for file in sorted(files, key=lambda x: x[:-4]):
        if file[-4:] != '.tex':
            print "skipping file %s" % file
        f = open(path+file)
        out.write(f.read()+"\n\n")
        f.close()
    out.close()

if __name__ == '__main__':
    main()
