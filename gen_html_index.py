#!/usr/bin/env python

"""Search through tex files and pull out function names for html index."""

import os
import re
import sys

apih = re.compile(r'''^\\apih{(.*)}{(.*)}$''')

pre="""
<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
    <head>
        <title>PNNL: Global Arrays Toolkit %s API</title>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
        <meta  name="description" content="The Global Arrays (GA) toolkit
        provides an efficient and portable &quot;shared-memory&quot;
        programming interface for distributed-memory computers." />
        <meta name="keywords" content="PNNL, Global Arrays, EMSL" />
        <!--#include virtual="/docs/global/shared/globals.inc"-->
        <style type="text/css">
        dt {
        font-size:small;
        }
        </style>
    </head>
    <body>
    <dl>
"""

post="""
    </dl>
    </body>
</html>
"""

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        raise ValueError, "usage: ./gen_html_index.py input_dir language [output_filename]"
    path = sys.argv[1]
    lang = sys.argv[2]
    name = ""
    if len(sys.argv) == 4:
        name = sys.argv[3]
    else:
        name = "%s_op_index.html" % lang
    assert lang in ["c", "f", "py", "cxx"]
    if path[-1] != '/':
        path += '/'
    files = os.listdir(path)
    out = open(name,'w')
    out.write(pre)
    # sort filenames but ignore the .tex extension
    for file in sorted(files, key=lambda x: x[:-4]):
        if file[-4:] != '.tex':
            print "skipping file %s" % path+file
            continue
        if os.path.isdir(path+file):
            print "skipping dir %s" % path+file
            continue
        print "parsing %s" % path+file
        for line in open(path+file):
            if 'apih' in line:
                line = line.strip()
                match = apih.match(line)
                if not match:
                    raise ValueError, "apih error, line %s" % line
                name,desc = match.groups()
                link = name.replace(" ", "_")
                out.write('<dt><a target="api" href="%s_op_api.html#%s">%s</a></dt>\n' % (
                    lang, link, name))
    out.write(post)
    out.close()

if __name__ == '__main__':
    main()

