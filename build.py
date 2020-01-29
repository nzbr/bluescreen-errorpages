#!/usr/bin/python3

import yaml
import os
from jinja2 import Template

with open("errors.yml", "r") as f:
    errors = next(yaml.load_all(f, Loader=yaml.SafeLoader))

with open("base.html", "r") as f:
    tplhtml = f.read()

tpl = Template(tplhtml)

if not os.path.isdir("build"):
    os.mkdir("build")

for err in errors:
    html = tpl.render(err)
    with open("build/"+str(err["err"])+".html", "w") as f:
        f.write(html)
        f.flush()