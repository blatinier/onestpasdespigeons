#!/usr/bin/env bash
wget -O mongodbdump-off.tar.gz http://world.openfoodfacts.org/data/openfoodfacts-mongodbdump.tar.gz
zcat mongodbdump-off.tar.gz | mongorestore --host localhost --username user --password pass -
