#!/bin/bash
python3 testprograms/MainLarge.py & 
sleep 1
python3 testprograms/MainLarge_slave.py
