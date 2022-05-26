#!/usr/bin/env python3

import base64
import os
import tempfile
from sys import argv
from urllib.request import urlopen

import yaml
from fontTools.ttLib import TTFont
from jinja2 import Template

if len(argv) < 2:
    print("You have to specify a domain name")
    exit(1)

domain = argv[1]

# Download the DOS font
fontSrc = "http://laemeur.sdf.org/fonts/MorePerfectDOSVGA.ttf"
data = urlopen(fontSrc).read()
# Convert it to WOFF
woffdata = None
with tempfile.SpooledTemporaryFile() as i:
  with tempfile.SpooledTemporaryFile() as o:
    i.write(data)
    with TTFont(i) as ttFont:
      ttFont.flavor = "woff2"
      ttFont.save(o)
    o.seek(0)
    woffdata = o.read()
# To Base64
font = "".join(base64.encodebytes(woffdata).decode("UTF-8").split("\n"))

with open("errors.yml", "r") as f:
    errors = next(yaml.load_all(f, Loader=yaml.SafeLoader))

with open("base.html", "r") as f:
    tplhtml = f.read()

tpl = Template(tplhtml)

if not os.path.isdir("build"):
    os.mkdir("build")

for err in errors:
    err["domain"] = domain
    err["font"] = font
    html = tpl.render(err)
    with open("build/"+str(err["err"])+".html", "w") as f:
        f.write(html)
        f.flush()
