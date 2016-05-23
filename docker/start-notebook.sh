#!/bin/bash
# Install mysql driver
exec git clone https://github.com/mysql/mysql-connector-python.git /tmp/mysql-connector-python
exec cd /tmp/mysql-connector-python
exec python ./setup.py build
exec sudo ./setup.py install

exec jupyter notebook &> /dev/null &

