#!/usr/bin/env python2.7
# encoding: utf-8

from subprocess import check_call, check_output
from tempfile import NamedTemporaryFile
from string import Template

git_desc = check_output(["git", "describe", "--tags"]).strip()
docker_compose_content = Template(open('docker-compose.yml').read()).substitute(IMG_TAG=git_desc)
tmpfp = NamedTemporaryFile()
tmpfp.write(docker_compose_content)
print(docker_compose_content)
tmpfp.flush()

target_dir = '/opt/b2w/'
cmd = ['fpm', '-s', 'dir', '-t', 'rpm', '-n', 'b2w-management',
       '-a', 'noarch', '-f',
       '{}={}docker-compose.yml'.format(tmpfp.name, target_dir)]

print(cmd)
check_call(cmd)
