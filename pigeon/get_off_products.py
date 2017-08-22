# -*- coding: utf-8 -*-
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  Copyright (c) 2017 Benoît Latinier, Fabien Bourrel
#  This file is part of project: OnEstPasDesPigeons
#
#!/usr/bin/env python
import csv
import os
import shutil
import tempfile
import urllib.request
from collections import Counter
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pigeon.settings")
OFF_DB_LINK = "http://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv"
django.setup()
from weights.models import Product


def import_OFF_db():
    print('[1/4] Create tmp working dir')
    tmp_dir = tempfile.mkdtemp()
    DUMP_FILE_PATH = os.path.join(tmp_dir, "products.csv")

    # Get file from remote OFF site
    print('[2/4] Download CSV OFF dump')
    urllib.request.urlretrieve(OFF_DB_LINK, filename=DUMP_FILE_PATH)

    # Update prod collection with the diff
    print('[3/4] Compare CSV to existant db for updates')
    pigeon_to_off = {"url_OFF": "url"}
    counts = Counter()
    with open(DUMP_FILE_PATH) as csv_off:
        reader = csv.DictReader(csv_off, dialect="excel-tab")
        for line in reader:
            counts["total"] += 1
            if "code" not in line or not line["code"]:
                continue
            product_dict = {k: line[pigeon_to_off.get(k, k)]
                            for k in Product.sourced_OFF_fields + ["code"]}
            csv_product = Product(**product_dict)
            try:
                local_product = Product.objects.get(code=csv_product.code)
                local_product.update_with_OFF_product(csv_product)
            except Product.DoesNotExist:
                csv_product.save()
                counts["created"] += 1
    print('Parsed {total} products. Created {created}.'.format(**counts))

    # Clean up
    print('[4/4] Clean tmp dir')
    try:
        shutil.rmtree(tmp_dir)
    except Exception:
        pass


if __name__ == "__main__":
    import_OFF_db()
