#!/usr/bin/python3
"""script that generates a .tgz archive from the contents of the web_static
"""
from datetime import datetime
from fabric.api import local
from os import path


def do_pack():
    """This method will pack web_static dir into tar.gz
    for airbnb deployment
    """
    if not path.exists(path.dirname("./web_static")):
        return None
    if not path.exists(path.dirname("versions")):
        try:
            local("mkdir -p versions")
        except Exception as err:
            print(err)
            return None
    fname = "web_static_{}.tgz".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    local("echo {}".format(fname))
    local("tar cpfz {} ./web_static".format(fname))
    local("mv {file} versions/{file}".format(file=fname))
    return "versions/{}".format(fname)
