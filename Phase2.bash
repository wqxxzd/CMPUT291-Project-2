#!/bin/bash
sort -u -o ads.txt ads.txt
sort -u -o terms.txt terms.txt
sort -u -o pdates.txt pdates.txt
sort -u -o prices.txt prices.txt
cat ads.txt | perl break.pl | db_load  -T -t hash ad.idx
cat terms.txt | perl break.pl | db_load  -c duplicates=1 -T -t btree te.idx
cat pdates.txt | perl break.pl | db_load  -c duplicates=1 -T -t btree da.idx
cat prices.txt | perl break.pl | db_load  -c duplicates=1 -T -t btree pr.idx
