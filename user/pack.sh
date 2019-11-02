#!/usr/bin/env bash
rm -rf target
mkdir -p target
cp oppor-user.py target
cp requirements.txt target
cp setup.cfg target
cd target
pip3 install -r requirements.txt --target .
zip -r oppor-user.zip *