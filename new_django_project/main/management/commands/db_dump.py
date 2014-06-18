# coding: utf-8

from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--router', dest='router', action='store', default='default'),
    )

    def handle(self, *args, **options):
        dbs = settings.DATABASES[options.get('router')]
        cmd = '''export PGPASSWORD={3}; {0} -h {4} -p {5} -U {2} -d {1} -F p --clean'''.format(
            dbs.get('PGDUMP', 'pg_dump'),
            dbs.get('NAME'),
            dbs.get('USER'),
            dbs.get('PASSWORD'),
            dbs.get('HOST'),
            dbs.get('PORT'),
        )
        proc = subprocess.Popen(cmd, shell=True)
        proc.wait()