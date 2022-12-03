#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
# to work in it as project use following the install dependencies of project
pip install  --editable .

## run simulator as module
# python -mev3dev2simulator

## create wheel
## see: https://realpython.com/python-wheels/
#pip install wheel
#python setup.py bdist_wheel

## inspect version installed
#pip install pipdeptree
#pipdeptree -p ev3dev2simulator |grep -v pyobjc
