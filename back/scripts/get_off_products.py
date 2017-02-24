#!/usr/bin/env python
import os
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

from mongoengine.context_managers import switch_collection

import config.main as conf
from models.product import Product


def import_OFF_db():
    print('[1/6] Create tmp working dir')
    tmp_dir = tempfile.mkdtemp()

    DUMP_FILE = "mongodbdump-off.tar.gz"
    DUMP_FILE_PATH = os.path.join(tmp_dir, DUMP_FILE)

    # Get file from remote OFF site
    print('[2/6] Download mongo OFF dump')
    urllib.request.urlretrieve(conf.OFF_DB_LINK, filename=DUMP_FILE_PATH)

    # Extract tar archive
    print('[3/6] Extract tar')
    tar_db = tarfile.open(DUMP_FILE_PATH, "r:gz")
    tar_db.extractall(path=tmp_dir)

    # Restore dump in tmp_collection (override it)
    print('[4/6] Restore dump in %s db on %s host' % (conf.MONGODB['db'],
                                                      conf.MONGODB['host']))
    subprocess.call(["mongorestore", "--drop",
                     "--host", conf.MONGODB['host'],
                     "--username", conf.MONGODB['user'],
                     "--password", conf.MONGODB['pwd'],
                     "--db", conf.MONGODB['db'],
                     "--collection", "products_tmp",
                     os.path.join(tmp_dir, "dump/off/products.bson")])

    # Clean up
    print('[5/6] Clean tmp dir')
    shutil.rmtree(tmp_dir)

    # Update prod collection with the diff
    print('[6/6] Compare new dump to existant db for updates')
    with switch_collection(Product, 'products_tmp') as ProductOFF:
        for product_off in ProductOFF.objects():
            if product_off.code is not None:
                try:
                    prod = Product.objects.get(code=product_off.code)
                    prod.update_with_OFF_product(product_off)
                except Product.DoesNotExist:
                    Product(**product_off.copy_dump()).save()
