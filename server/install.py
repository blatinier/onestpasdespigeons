#!/usr/bin/env python
import click

import bootstrap
from scripts.get_off_products import import_OFF_db

SCRIPTS = {"import_db": import_OFF_db}


@click.command()
@click.argument("script")
def launch_script(script):
    SCRIPTS[script]()


if __name__ == "__main__":
    launch_script()
