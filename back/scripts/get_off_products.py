#!/usr/bin/env python
import config.main as conf
import os
import shutils
import subprocess
import tarfile
import urllib.request

from mongoengine.context_managers import switch_collection
from models.product import Product


os.mkdir(conf.TMP_FOLDER)
DUMP_FILE = "mongodbdump-off.tar.gz"
DUMP_FILE_PATH = os.path.join(conf.TMP_FOLDER, DUMP_FILE)

# Get file from remote OFF site
urllib.request.urlretrieve(conf.OFF_DB_LINK, filename=DUMP_FILE_PATH)

# Extract tar archive
tar_db = tarfile.open(DUMP_FILE_PATH, "r:gz")
tar_db.extractall(path=conf.TMP_FOLDER)

# Restore dump in tmp_collection (override it)
subprocess.call("mongorestore", "--drop",
                "--host", conf.MONGODB['host'],
                "--username", conf.MONGODB['user'],
                "--password", conf.MONGODB['pwd'],
                "--db", conf.MONGODB['db'],
                "--collection", "products_tmp",
                "dump/off/products.bson")

# Clean up
shutils.rmtree(conf.TMP_FOLDER)

# Update prod collection with the diff
with switch_collection(Product, 'products_tmp') as ProductOFF:
    for product_off in ProductOFF.objects():
        try:
            prod = Product.objects.get(code=product_off.code)
            prod.update_with_OFF_product(product_off)
        except Product.DoesNotExist:
            Product(**product_off.copy_dump()).save()
