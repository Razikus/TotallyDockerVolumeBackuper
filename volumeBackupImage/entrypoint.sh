#!/bin/sh

export GZIP=-9
cd /
if [ -z "$1" ]; then
    tar -cOz volume
else
    tar -cvzf $1 volume
fi