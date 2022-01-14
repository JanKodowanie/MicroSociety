#!/bin/bash

array=( AccountService BlogWriteService EmailService)

for i in "${array[@]}"
do
    cd $i
	rm db.sqlite
    rm db.sqlite-shm
    rm db.sqlite-wal
    aerich upgrade
    cd ..
done