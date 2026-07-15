#!/bin/bash
pkill -f python
rm -f saf_data/saf_log.txt
nohup python3 saf_minimal.py > saf_data/kernel.log 2>&1 &
python3 auto_bifurcation.py
pkill -f python
