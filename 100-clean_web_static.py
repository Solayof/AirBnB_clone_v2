#!/usr/bin/python3
""" These methods aid in deploying the web_static directory
to the remote servers
"""
from fabric.api import *
from os import path
from datetime import datetime

env.hosts = ['100.26.174.107', '52.86.116.134']


@runs_once
def do_pack():
    """This method will pack the web_static dir into a tar.gz
    """
    if not path.exists(path.dirname("./web_static")):
        return None

    if not path.exists(path.dirname("versions")):
        try:
            local("mkdir -p versions")
        except Exception as e:
            print(e)
            return None
    fname = "web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    local("tar cpfz {} ./web_static".format(fname))
    local("mv {file} versions/{file}".format(file=fname))
    return "versions/{}".format(fname)


def do_deploy(archive_path):
    """ this method will deploy compressed file
    then unpack and move the content to is proper destination

    Returns:
        Bool: True on sucess well Fale
    """
    try:
        open(archive_path)
    except IOError:
        return False
    split_path = archive_path.split('/')
    cln_name = split_path[1][0:split_path[1].rfind('.')]
    dest = '/data/web_static'
    put(archive_path, "/tmp/")
    with cd("/tmp/"):
        run('tar xpf {}'.format(split_path[1]))
        run('mv web_static {}/releases/{}'.format(dest, cln_name))
        run('rm -rf {}'.format(split_path[1]))

    with cd(dest):
        run('rm {}/current'.format(dest))
        run('ln -s {d}/releases/{t} {d}/current'
            .format(d=dest, t=cln_name))
    print('New version deployed!')
    return True


def deploy():
    """this method will pack and deploy
    """
    path = do_pack()
    print(path)
    if path:
        return do_deploy(path)
    return False


def do_clean(number=0):
    """method that deletes out-of-date archives from version directory and
    from the remote server(s).
    """
    tgz_files = local("ls versions/*.tgz", capture=True)
    tgz_list = tgz_files.split("\n")
    number = int(number)
    tgz_list.sort()
    if number > 1:
        rm_tgz = tgz_list[0:-number]
    else:
        rm_tgz = tgz_list[0:-1]
    for line in rm_tgz:
        local("rm {}".format(line))
    remote_dir = [rm.split("/")[-1].split(".")[0] for rm in rm_tgz]
    with cd("/data/web_static/releases/"):
        for rm_dir in remote_dir:
            run("rm -rf {}".format(rm_dir))
