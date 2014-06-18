# coding: utf-8

import sys
import os


def flushall():
    REDIS_CLI_PATH = ''
    try:
        from django.conf import settings
        REDIS_CLI_PATH = settings.REDIS_CLI_PATH
    except:
        pass
    if not REDIS_CLI_PATH:
        symscnt = 80
        bordersym = '*'
        sys.stdout.write('\n\n\n%s\n%s%s%s' % (bordersym * symscnt, bordersym, ' ' * (symscnt - 2), bordersym))
        for msg in ('`REDIS_CLI_PATH` has no value!', 'Please, set it & try again, baby'):
            bats = (symscnt - msg.__len__()) / 2 - 1
            sys.stdout.write('%s%s%s%s%s' % (bordersym, ' ' * bats, msg, ' ' * bats, bordersym))
        sys.stdout.write('%s%s%s\n%s\n\n' % (bordersym, ' ' * (symscnt - 2), bordersym, bordersym * symscnt))
        return
    cmd = '%s -r 1 flushall' % REDIS_CLI_PATH
    sys.stdout.write('\nExec `%s`\n' % cmd)
    os.system(cmd)


