#!/bin/bash

array=( AccountService BlogWriteService )

for i in "${array[@]}"
do
	rm $i/db.sqlite
    rm $i/db.sqlite-shm
    rm $i/db.sqlite-wal
done