#!/usr/bin/env python

"""Search through tex files and pull out function names for html index."""

import os
import re
import sys

have_pygments = True
try:
    from pygments import highlight
    from pygments.lexers import CLexer
    from pygments.lexers import FortranLexer
    from pygments.lexers import PythonLexer
    from pygments.lexers import CppLexer
    from pygments.formatters import HtmlFormatter
    lang_to_lexer = {
            "c": CLexer(stripall=True),
            "f": FortranLexer(stripall=True),
            "py": PythonLexer(stripall=True),
            "cxx": CppLexer(stripall=True),
            }
    formatter = HtmlFormatter()
    extra_header = '<style type="text/css">\n'
    extra_header += formatter.get_style_defs('.highlight')
    extra_header += '</style>\n'
except ImportError,e:
    have_pygments = False
    extra_header = ""
    raise

apih = re.compile(r'''^\\apih{(.*)}{(.*)}$''')
inarg = re.compile(r'''^\\inarg{(.*)}{(.*)}{(.*)}$''')
outarg = re.compile(r'''^\\outarg{(.*)}{(.*)}{(.*)}$''')
inoutarg = re.compile(r'''^\\inoutarg{(.*)}{(.*)}{(.*)}$''')

lang_to_pretty = {
        "c": "C",
        "f": "Fortran",
        "py": "Python",
        "cxx": "C++",
        }

pre="""
<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
    <head>
        <title>PNNL: Global Arrays Toolkit %%s API</title>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
        <meta  name="description" content="The Global Arrays (GA) toolkit
        provides an efficient and portable &quot;shared-memory&quot;
        programming interface for distributed-memory computers." />
        <meta name="keywords" content="PNNL, Global Arrays, EMSL" />
        <!--#include virtual="/docs/global/shared/globals.inc"-->
        %s
    </head>
    <body>
""" % extra_header

post="""
    </body>
</html>
"""

def normalize_whitespace(str):
    return re.sub(r'\s+', ' ', str.strip())

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        raise ValueError, "usage: ./gen_html_api.py input_dir language [output_filename]"
    path = sys.argv[1]
    lang = sys.argv[2]
    name = ""
    if len(sys.argv) == 4:
        name = sys.argv[3]
    else:
        name = "%s_op_api.html" % lang
    assert(lang in ["c", "f", "py", "cxx"])
    if path[-1] != '/':
        path += '/'
    files = os.listdir(path)
    out = open(name,'w')
    out.write(pre % lang_to_pretty[lang])
    need_rule = False
    in_code = False
    code = ""
    in_funcargs = False
    in_api = False
    in_desc = False
    in_verb = False
    # sort filenames but ignore the .tex extension
    for file in sorted(files, key=lambda x: x[:-4]):
        if file[-4:] != '.tex' or file[0] == '.':
            print "skipping file %s" % path+file
        for line in open(path+file):
            if 'apih' in line:
                line = line.strip()
                # skip writing the first horizontal rule
                if need_rule:
                    out.write("<hr/>\n")
                else:
                    need_rule = True
                match = apih.match(line)
                if not match:
                    raise ValueError, "apih error, line %s" % line
                name,desc = match.groups()
                link = name.replace(" ", "_")
                out.write('<h3 id="%s">%s</h3>\n' % (link, name))
            elif ((lang == "c" and "begin{capi}" in line)
                    or (lang == "f" and "begin{fapi}" in line)
                    or (lang == "py" and "begin{pyapi}" in line)
                    or (lang == "cxx" and "begin{cxxapi}" in line)):
                in_api = True
            elif ((lang == "c" and "end{capi}" in line)
                    or (lang == "f" and "end{fapi}" in line)
                    or (lang == "py" and "end{pyapi}" in line)
                    or (lang == "cxx" and "end{cxxapi}" in line)):
                in_api = False
            elif in_api and "begin" in line and "code" in line:
                in_code = True
                code = ""
            elif in_api and "end" in line and "code" in line:
                in_code = False
                if have_pygments:
                    lexer = lang_to_lexer[lang]
                    out.write(highlight(code, lexer, formatter))
                else:
                    out.write('<pre><span style="color: rgb(255, 0, 0);">\n')
                    out.write(code)
                    out.write('</span></pre>\n')
            elif in_code:
                code += line
            elif in_api and "begin{funcargs}" in line:
                in_funcargs = True
                out.write("<small><table>\n")
            elif in_api and "end{funcargs}" in line:
                in_funcargs = False
                out.write("</table></small>\n")
            elif in_funcargs:
                if 'inoutarg' in line:
                    match = inoutarg.match(line.strip())
                    if not match:
                        print "in %s\nline: %s" % (path+file,line)
                        assert(False)
                    type,name,desc = match.groups()
                    out.write("<tr><td>%s</td><td>%s</td><td>%s</td>\n" % (type,name,desc))
                elif 'inarg' in line:
                    match = inarg.match(line.strip())
                    if not match:
                        print "in %s\nline: %s" % (path+file,line)
                        assert(False)
                    type,name,desc = match.groups()
                    out.write("<tr><td>%s</td><td>%s</td><td>%s</td>\n" % (type,name,desc))
                elif 'outarg' in line:
                    match = outarg.match(line.strip())
                    if not match:
                        print "in %s\nline: %s" % (path+file,line)
                        assert(False)
                    type,name,desc = match.groups()
                    out.write("<tr><td>%s</td><td>%s</td><td>%s</td>\n" % (type,name,desc))
                else:
                    print "in %s\nline: %s" % (path+file,line)
                    assert(False)
            elif "\\wcoll" in line:
                out.write("<p>Collective on the world processor group.</p>\n")
            elif "\\dcoll" in line:
                out.write("<p>Collective on the default processor group.</p>\n")
            elif "\\gcoll" in line:
                out.write("<p>Collective on the processor group inferred from the arguments.</p>\n")
            elif "\\ncoll" in line:
                out.write("<p>One-sided (non-collective).</p>\n")
            elif "\\local" in line:
                out.write("<p>Local operation.</p>\n")
            elif ((lang == "c" and "begin{cdesc}" in line)
                    or (lang == "f" and "begin{fdesc}" in line)
                    or (lang == "py" and "begin{pydesc}" in line)
                    or (lang == "cxx" and "begin{cxxdesc}" in line)
                    or ("begin{desc}" in line)):
                in_desc = True
                out.write("<p>\n")
            elif ((lang == "c" and "end{cdesc}" in line)
                    or (lang == "f" and "end{fdesc}" in line)
                    or (lang == "py" and "end{pydesc}" in line)
                    or (lang == "cxx" and "end{cxxdesc}" in line)
                    or ("end{desc}" in line)):
                in_desc = False
                out.write("</p>\n")
            elif in_desc:
                if "begin{verbatim}" in line:
                    in_verb = True
                    out.write("</p>\n<pre>\n")
                elif "end{verbatim}" in line:
                    in_verb = False
                    out.write("</pre>\n<p>\n")
                elif in_verb:
                    out.write(line)
                else:
                    line = line.strip()
                    if not line: # empty line, begin new paragraph
                        out.write("</p>\n<p>\n")
                    out.write(line)

                
    out.write(post)
    out.close()

if __name__ == '__main__':
    main()

