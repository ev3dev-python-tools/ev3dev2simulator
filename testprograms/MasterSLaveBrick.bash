#!/bin/bash
python3 testprograms/MasterBrick.py & 
sleep 1
python3 testprograms/SlaveBrick.py
