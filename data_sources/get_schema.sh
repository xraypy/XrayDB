#!/bin/sh

db='xraydb.sqlite'
schema='xraydb.schema'
echo '.schema' > tmp.sql
echo '.exit'  >> tmp.sql

sqlite3 -version -init tmp.sql xraydb.sqlite > $schema
echo "wrote schema for $db to $schema"
rm -f tmp.sql
