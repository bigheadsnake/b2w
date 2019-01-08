#!/usr/bin/env python
# encoding: utf-8

import os
from subprocess import call, check_output

tag = check_output(['git', 'describe', '--tags']).strip()
cmd = ['docker', 'build', '-v', '{}:/ssh-agent-sock'.format(os.environ['SSH_AUTH_SOCK']), '-t', 'xxx.xxx.xxx:80/b2w:{}'.format(tag), '.']
call(cmd)
