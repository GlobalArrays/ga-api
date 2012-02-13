#!/usr/bin/env python

"""Split ga_api.tex into separate tex files based on function groups."""

import os
import re
import sys

apih = re.compile(r'''^\\apih{(.*)}{(.*)}$''')

def normalize_whitespace(str):
    return re.sub(r'\s+', ' ', str.strip())

def get_filename(name, path):
    ret = name.lower().replace(" ","-")
    assert(" " not in ret)
    assert(len(path) != 0)
    if path[-1] != '/':
        path += '/'
    return path + ret + ".tex"

def main():
    if len(sys.argv) != 2:
        raise ValueError, "please supply directory argument"
    path = sys.argv[1]
    try:
        os.mkdir(path)
    except OSError:
        # directory already exists
        pass
    count = 0
    current_file = None
    buffer = ""
    for line in open("ga_api.tex"):
        #line = line[:-1] # remove trailing newline
        count += 1
        if 'apih' in line:
            if current_file is not None:
                f = open(current_file,'w')
                f.write(buffer.strip())
                f.close()
                #current_file.close()
            _line = line.strip()
            match = apih.match(_line)
            if not match:
                raise ValueError, "apih error, line %s: %s" % (count,_line)
            name,desc = match.groups()
            buffer = line
            current_file = get_filename(name, path)
        elif 'end{document}' in line:
            f = open(current_file,'w')
            f.write(buffer.strip())
            f.close()
        elif current_file is not None:
            buffer += line

if __name__ == '__main__':
    main()
