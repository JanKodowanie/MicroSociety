#!/bin/bash

array=( AccountService BlogService )

for i in "${array[@]}"
do
	rm $i/db.sqlite
    rm $i/db.sqlite-shm
    rm $i/db.sqlite-wal
done