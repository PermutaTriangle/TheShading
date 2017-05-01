#!/bin/bash
cat tasks.txt | parallel --eta --progress -j7 --joblog /tmp/tsalog.txt --colsep ' ' -- python2 process_task.py
