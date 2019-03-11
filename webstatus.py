#!/usr/bin/env python3.6

import subprocess
import jinja2
import asyncio
import aiohttp
import aiohttp_jinja2
from aiohttp import web

async def status(request):
    info = subprocess.check_output("uname -s -r -p -o", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    model = subprocess.check_output("dmidecode | grep 'Product Name' | head -n 1 | awk -F:  {'print $2'} | sed 's/ //'", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    size = subprocess.check_output("df -h | grep -e dev/ -e Filesystem | grep -v tmp", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    inodes = subprocess.check_output("df -i | grep -e dev/ -e Filesystem | grep -v tmp", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    cpustat = subprocess.check_output("iostat -c | tail -n3", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    ram = subprocess.check_output("free -m | tail -n3", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    iostat = subprocess.check_output("iostat -d | tail -n5", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    ifstat = subprocess.check_output("ifstat | grep -v kernel", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    usernum = subprocess.check_output("ss -a | grep 8080 | awk '{print $6}' | awk -F: '{print $4}' | grep -v \* | sort | uniq | wc -l", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    userlst = subprocess.check_output("ss -a | grep 8080 | awk '{print $6}' | awk -F: '{print $4}' | grep -v \* | sort | uniq", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    hostname = subprocess.check_output("hostname", shell=True).decode("utf-8").strip().replace(' ', '&nbsp;')
    context = { "hostname": hostname, "model": model, "info": info, "size": size, "inodes": inodes, "iostat": iostat, "cpustat": cpustat, "ram": ram, "ifstat": ifstat, "usernum": usernum, "userlst": userlst  }
    response = aiohttp_jinja2.render_template('index.html', request, context)
    return response

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('/opt/geostatus'))
app.router.add_get('/geostatus', status)
web.run_app(app, port=7070)

try:
    loop.run_forever()
finally:
    loop.run_forever()
    loop.close()
