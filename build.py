#!/usr/bin/env python3

import yaml
import os
from sys import argv
from jinja2 import Template

if len(argv) < 2:
    print("You have to specify a domain name")
    exit(1)

domain = argv[1]

with open("errors.yml", "r") as f:
    errors = next(yaml.load_all(f, Loader=yaml.SafeLoader))

with open("base.html", "r") as f:
    tplhtml = f.read()

tpl = Template(tplhtml)

if not os.path.isdir("build"):
    os.mkdir("build")

for err in errors:
    err["domain"] = domain
    html = tpl.render(err)
    with open("build/"+str(err["err"])+".html", "w") as f:
        f.write(html)
        f.flush()