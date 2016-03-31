#!/usr/bin/env python
import sys,os,time
sys.path.insert(0,os.path.dirname(__file__))
from fabric.api import *
from toughradius import __version__

env.user = 'root'
env.hosts = ['121.201.63.77']

def build():
    releases = {'dev':'release-dev','stable':'release-stable'}
    release = releases.get(raw_input("release (dev|stable):"),'dev')
    linux_dist = 'centos'
    build_ver = "{0}-{1}-{2}".format(linux_dist,release, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    gitrepo = "git@bitbucket.org:talkincode/toughradius-enterprise.git"
    rundir = "/opt/toughee"
    dist = "toughee-{0}.tar.bz2".format(build_ver)
    run("test -d {0} || git clone {1} {2}".format(rundir,gitrepo,rundir))
    with cd(rundir):
        run("git pull -f origin {0}".format(release))
        run("sh venv.sh")
        run("\cp installs/{0}.mk Makefile".format(linux_dist))
    with cd("/opt"):
        excludes = ['.git','.gitignore','fabfile.py','']
        excludes = "--exclude .git --exclude fabfile.py --exclude pymodules"
        run("tar -jpcv -f /tmp/{0} toughee {1}".format(dist,excludes))
    local("scp  root@121.201.63.77:/tmp/{0} {1}".format(dist,dist))

def tag():
    local("git tag -a v%s -m 'version %s'"%(__version__,__version__))
    local("git push origin v%s:v%s"%(__version__,__version__))

def commit():
    try:
        local("ps aux | grep '/test.json' | awk '{print $2}' | xargs  kill")
    except:
        pass
    local("echo 'coverage report: version:%s   date:%s' > coverage.txt" % (__version__,time.ctime()))
    local("echo >> coverage.txt")
    local("coverage report >> coverage.txt")
    local("git status && git add .")
    local("git commit -m \"%s\"" % raw_input("type message:"))
    local("git push origin master")


def all():
    local("venv/bin/python radiusctl standalone -c ~/toughradius_test.json")


def initdb():
    local("venv/bin/python radiusctl initdb -c ~/toughradius_test.json")
    local("venv/bin/python radiusctl inittest -c ~/toughradius_test.json")

