# -*- coding: utf-8 -*-

from datetime import datetime

from invoke import task
from invoke.util import cd

CONFIG = {
    'commit_message': "'Publish site on {:%Y-%m-%d %H:%M}'".format(datetime.now()),
}


@task
def github(c):
    """Build production version of site"""
    c.run('git add --all')
    c.run('git commit -m {}'.format(CONFIG['commit_message']))
    c.run('git push')
