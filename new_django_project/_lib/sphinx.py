import sys, os


def index_rotate_all():
    SPHINX_INDEX_ROTATE_ALL_CMD = ''
    try:
        from django.conf import settings
        SPHINX_INDEX_ROTATE_ALL_CMD = settings.SPHINX_INDEX_ROTATE_ALL_CMD
    except:
        pass
    if not SPHINX_INDEX_ROTATE_ALL_CMD:
        symscnt = 80
        bordersym = '*'
        sys.stdout.write('\n\n\n%s\n%s%s%s' % (bordersym * symscnt, bordersym, ' ' * (symscnt - 2), bordersym))
        for msg in ('`SPHINX_INDEX_ROTATE_ALL_CMD` has no value!', 'Please, set it & try again, baby'):
            bats = (symscnt - msg.__len__()) / 2 - 1
            sys.stdout.write('%s%s%s%s%s' % (bordersym, ' ' * bats, msg, ' ' * bats, bordersym))
        sys.stdout.write('%s%s%s\n%s\n\n' % (bordersym, ' ' * (symscnt - 2), bordersym, bordersym * symscnt))
        return
    cmd = SPHINX_INDEX_ROTATE_ALL_CMD
    sys.stdout.write('\nExec `%s`\n' % cmd)
    os.system(cmd)


